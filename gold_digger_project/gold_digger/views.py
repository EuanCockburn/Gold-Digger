from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from forms import UserProfileForm, UserForm
from models import UserProfile, UserAchievements, Achievements
from django.core.urlresolvers import reverse
import utility
import json
import facebook
 

locations = ['California', 'Yukon', 'Brazil', 'South Africa', 'Scotland', 'Victoria']


def home(request):

    context = utility.contextget(request)

    user = request.user.id

    try:
        request.session['days'] = utility.getgames_played(user)

        return render_to_response('gold_digger/home.html', {'current_user': user,
                                                            'scan': utility.getscan(user),
                                                            'tool': utility.gettool(user),
                                                            'vehicle': utility.getvehicle(user),
                                                            'gold': utility.getgold(user),
                                                            'mod_scan': utility.getmod_scan(user),
                                                            'modt_tool': utility.getmodt_tool(user),
                                                            'mod_vehicle': utility.getmod_vehicle(user)}, context)

    except:
        request.session['time_remaining'] = 100
        request.session['gold'] = 0
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render_to_response('gold_digger/home.html', {'user_form': user_form,
                                                            'profile_form': profile_form}, context)


def about(request):
    context = utility.contextget(request)
    return render_to_response('gold_digger/about.html', context)


def tour(request):
    context = utility.contextget(request)
    return render_to_response('gold_digger/tour.html', context)


def register(request):
    context = utility.contextget(request)
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    if user_form.is_valid() and profile_form.is_valid():

        utility.postregister_valid(request, user_form, profile_form)

    else:

        return utility.postregister_invalid(context, user_form, profile_form)

    request.session['days'] = 1
    request.session['mine_no'] = 0
    return HttpResponseRedirect(reverse('game_choice2'), context)


def user_login(request):

    context = utility.contextget(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                login(request, user)
                request.session['time_remaining'] = 100
                request.session['gold'] = 0
                request.session['mine_no'] = 0
                request.session['days'] = 1

                return HttpResponseRedirect(reverse('game_choice2'), context)
            else:
                return HttpResponse("Your Gold Digger account is disabled.")
        else:

            print "Invalid login details: {0}, {1}".format(username, password)
            bad_details = {'bad_details': " -=: Invalid login details supplied. :=-"}
            user_form = UserForm()
            profile_form = UserProfileForm()
            return render_to_response('gold_digger/home.html', {'user_form': user_form,
                                                                'profile_form': profile_form,
                                                                'bad_details': bad_details}, context)

    else:
        user = utility.getuser(request)

        return render_to_response('gold_digger/home.html', {'current_user': user,
                                                            'scan': utility.getscan(user),
                                                            'tool': utility.gettool(user),
                                                            'vehicle': utility.getvehicle(user),
                                                            'gold': utility.getgold(user),
                                                            'mod_scan': utility.getmod_scan(user),
                                                            'modt_tool': utility.getmodt_tool(user),
                                                            'mod_vehicle': utility.getmod_vehicle(user)}, context)


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/gold_digger/')


@login_required
def user_profile(request):
    user = utility.getuser(request)
    achieve = UserAchievements.objects.filter(user=user)
    context = utility.contextget(request)

    return render_to_response('gold_digger/profile.html', {'user': user,
                                                           'mod_scan': utility.getmod_scan(user),
                                                           'modt_tool': utility.getmodt_tool(user),
                                                           'achievements': achieve}, context)


@login_required
def move(request):
    user = utility.getuser(request)
    context = utility.contextget(request)

    request.session['time_remaining'] -= utility.getmod_vehicle(user)
    request.session['pointer'] = 0
    request.session['mine_no'] += 1
    user.mines += 1
    utility.usersave(user)
    sess_id = request.session._session_key

    game = utility.getgame(sess_id, request)

    # Conduct move and store changes in the cache
    game.player_move()
    utility.store_game_incache(sess_id, game)

    if request.session['time_remaining'] <= 0:
        return HttpResponseRedirect(reverse('game_over'), context)

    return HttpResponseRedirect(reverse('game2'), context)


@login_required
def back_to_main(request):
    user = utility.getuser(request)
    context = utility.contextget(request)

    request.session['has_mine'] = False
    request.session['time_remaining'] = 0
    user.gold -= request.session['gold']
    utility.usersave(user)

    return HttpResponseRedirect(reverse('home'), context)


@login_required
def game_over(request):
    user = utility.getuser(request)
    context = utility.contextget(request)
    currentgold = utility.getgold(user)
    sess_id = request.session._session_key

    if currentgold > utility.getalltimegold(user):
        user.all_time_max_gold = currentgold

    # Updating user values
    user.gold += request.session['gold']
    user.mines += 1
    user.games_played += 1
    request.session['days'] += 1
    user.all_time_gold += request.session['gold']
    user.average = user.all_time_gold / utility.getmines(user)
    utility.usersave(user)

    request.session['game_started'] = False
    request.session['mine_type'] = ''
    request.session['time_remaining'] = 100
    mine_no = request.session['mine_no']
    request.session['mine_no'] = 0
    day_gold = request.session['gold']
    total_gold = utility.getgold(user)
    request.session['gold'] = 0
    cost = utility.determine_cost(request.session['location'])
    cache.set(sess_id, None, 0)

    min_cost = utility.get_min_mine_cost()
    if currentgold < min_cost:
        return HttpResponseRedirect(reverse('game_over2'), context)
    try:
        is_facebook_user = request.user.social_auth.filter(provider='facebook', )[0]
        is_facebook_user = 1
    except:
        is_facebook_user = 0

    return render_to_response('gold_digger/game_over.html', {'day_gold': day_gold,
                                                             'total_gold': total_gold,
                                                             'mine_no': mine_no,
                                                             'cost': cost,
                                                             'is_facebook_user': is_facebook_user}, context)


def leaderboards(request):
    context = utility.contextget(request)

    users_avg = UserProfile.objects.order_by('-average')
    users_gold = UserProfile.objects.order_by('-all_time_max_gold')
    users_games = UserProfile.objects.order_by('-games_played')
    users_all_time_gold = UserProfile.objects.order_by('-all_time_gold')
    users_achievements = UserProfile.objects.all()
    achieve = UserAchievements.objects.all()

    return render_to_response('gold_digger/leaderboards.html', {'users_avg': users_avg,
                                                                'users_gold': users_gold,
                                                                'users_games': users_games,
                                                                'users_all_time_gold': users_all_time_gold,
                                                                'users_achievements': users_achievements,
                                                                'achiev': achieve}, context)


@login_required
def game_choice2(request):
    context = utility.contextget(request)
    user = utility.getuser(request)
    gold = utility.getgold(user)

    min_cost = utility.get_min_mine_cost()
    if gold < min_cost:
        return HttpResponseRedirect(reverse('game_over2'), request)

    mine_types = ['California', 'Yukon', 'Brazil', 'South Africa', 'Scotland', 'Victoria']

    request.session['game_started'] = False
    request.session['mine_type'] = ''
    request.session['purchase'] = False
    request.session['time_remaining'] = 100
    request.session['gold'] = 0

    return render_to_response('gold_digger/game_choice2.html', {'mine_types': mine_types,
                                                                'scan': utility.getscan(user),
                                                                'tool': utility.gettool(user),
                                                                'vehicle': utility.getvehicle(user),
                                                                'gold': gold,
                                                                'mod_scan': utility.getmod_scan(user),
                                                                'modt_tool': utility.getmodt_tool(user),
                                                                'mod_vehicle': utility.getmod_vehicle(user)}, context)


@login_required
def game2(request):
    context = utility.contextget(request)

    user = utility.getuser(request)

    if request.session['mine_type'] == '':
        mine_type = request.session['location']
        user.gold -= utility.determine_cost(mine_type)
        utility.usersave(user)
    else:
        mine_type = request.session['mine_type']

    sess_id = request.session._session_key

    # If the game is not in cache create a new game
    if not utility.incache(sess_id):
        _game = utility.startgame(request, mine_type)  # call on the start game method

        request.session['pointer'] = 0
        request.session['mine_no'] = 1
        request.session['time_remaining'] = 100
        _time_remaining = 100
        request.session['game_started'] = True

    # Otherwise load it from the cache
    else:
        _game = utility.get_game_incache(sess_id)
        _time_remaining = request.session['time_remaining']

    if request.session['time_remaining'] <= 0:
        return HttpResponseRedirect(reverse('game_over'), context)

    _location = request.session['location']
    _pointer = request.session['pointer']

    return render_to_response('gold_digger/game2.html', {'blocks': _game.get_current_blocks(),
                                                         'user': user,
                                                         'time_remaining': _time_remaining,
                                                         'move_cost': utility.getmod_vehicle(user),
                                                         'dig_cost': utility.getmodt_tool(user),
                                                         'location': _location,
                                                         'pointer': _pointer,
                                                         'mine_no': _game.mine_position + 1,
                                                         'visibility': utility.getmod_scan_l(user),
                                                         'mod_scan': utility.getmod_scan(user),
                                                         'modt_tool': utility.getmodt_tool(user),
                                                         'mod_vehicle': utility.getmod_vehicle(user)}, context)


@login_required
def ajaxview(request):
    user = utility.getuser(request)
    sess_id = request.session._session_key

    # Retrieve game from cache if it exists
    _game = utility.getgame(sess_id, request)

    # POSTED objects['pointer']
    gold_collected = _game.player_dig()
    max_yield = _game.get_max_yield()

    request.session['pointer'] += 1
    request.session['time_remaining'] -= utility.getmodt_tool(user)
    request.session['gold'] += gold_collected

    # Store game session into cache
    utility.store_game_incache(sess_id, _game)

    myResponse = {}

    if request.session['pointer'] == 10:
        myResponse['nextmine'] = True

    if request.session['time_remaining'] <= 0:
        return HttpResponse(status=204)

    if gold_collected == 0:
        myResponse['nuggets'] = 0
    else:
        myResponse['nuggets'] = ((6 * gold_collected) / max_yield) + 1

    myResponse['totalgold'] = utility.getgold(user)
    myResponse['timeremaining'] = request.session['time_remaining']
    myResponse['currentgold'] = request.session['gold']
    myResponse['goldextracted'] = gold_collected

    return HttpResponse(json.dumps(myResponse), content_type="application/json")


@login_required
def store(request):
    context = utility.contextget(request)
    user = utility.getuser(request)

    equipment = utility.ScanningEquipment.objects.all()
    vehicles = utility.Vehicle.objects.all()
    tools = utility.DiggingEquipment.objects.all()
    new_id_s = utility.getequipid(user)
    new_id_t = utility.gettoolid(user)
    new_id_v = utility.getvehicleid(user)
    new_item_s = utility.getequipment(user)
    new_item_t = utility.gettl(user)
    new_item_v = utility.getvhcle(user)

    if new_id_s != 5:
        new_id_s += 1
        new_item_s = utility.ScanningEquipment.objects.get(id=new_id_s)

    if new_id_t != 5:
        new_id_t += 1
        new_item_t = utility.DiggingEquipment.objects.get(id=new_id_t)

    if new_id_v != 5:
        new_id_v += 1
        new_item_v = utility.Vehicle.objects.get(id=new_id_v)

    return render_to_response('gold_digger/store.html', {'equipment': equipment,
                                                         'vehicles': vehicles,
                                                         'tools': tools,
                                                         'gold': utility.getgold(user),
                                                         'scan': utility.getscan(user),
                                                         'dig': utility.gettool(user),
                                                         'move': utility.getvehicle(user),
                                                         'new_item_s': new_item_s,
                                                         'new_item_t': new_item_t,
                                                         'new_item_v': new_item_v}, context)

def ajax_upgrade(request):
    item_type = request.POST['up']

    if item_type == 'scan':
        return utility.scanupgrade(request)

    if item_type == 'tool':
        return utility.toolupgrade(request)

    if item_type == 'vehicle':
        return utility.vehicleupgrade(request)


@login_required
def update_location(request):
    request.session['location'] = request.POST['loc']
    request.session['mine_type'] = ''
    print request.session['location']
    return HttpResponse(status=200)


@login_required
def update_cost(request):
    user = utility.getuser(request)
    user.gold -= int(request.POST['cost'])

    gold = utility.getgold(user)

    if gold < 20:
        return HttpResponse(status=204)

    utility.usersave(user)

    myResponse = gold

    return HttpResponse(json.dumps(myResponse), content_type="application/json")


@login_required
def ajax_exit():
    return HttpResponse(status=200)


@login_required
def game_over2(request):
    context = utility.contextget(request)
    user = utility.getuser(request)

    user.gold = 0
    user.equipment = utility.ScanningEquipment.objects.get(id=1)
    user.tool = utility.DiggingEquipment.objects.get(id=1)
    user.vehicle = utility.Vehicle.objects.get(id=1)
    request.session['gold'] = 0
    mines = request.session['mine_no']
    request.session['mine_no'] = 0
    days = (request.session['days']) - 1
    request.session['days'] = 1
    user.games_played += 1
    user.game_overs += 1
    user.gold = 100
    utility.usersave(user)

    return render_to_response('gold_digger/game_over2.html', {'mines': mines,
                                                              'days': days}, context)


@login_required
def achievements(request):
    user = UserProfile.objects.get(user=request.user)

    myResponse = {}

    gold = [50, 500, 1000, 5000, 10000, 20000]
    played = [5, 10, 15, 20, 50]
    mine = [50, 100, 300]

    i = 0
    if user.gold < 50:
        myResponse['unlocked'] = True

    while user.gold > gold[i]:
        i += 1

    if i > 0:
        myResponse = utility.add_achievement(user, i)

    j = 0
    while user.games_played > played[j]:
        j += 1

    j += 6
    if j > 6:
        myResponse = utility.add_achievement(user, j)

    k = 0
    while user.mines > mine[k]:
        k += 1

    k += 11
    if k > 11:
        myResponse = utility.add_achievement(user, k)

    return HttpResponse(json.dumps(myResponse), content_type="application/json")


def display_achievements(request):
    ach = Achievements.objects.all()
    context = RequestContext(request)

    return render_to_response('gold_digger/achievements.html', {'achievements': ach}, context)


def egg(request):
    user = utility.getuser(request)
    achievementegg = Achievements.objects.get(id=15)

    if not UserAchievements.objects.filter(user=user, achievement=achievementegg).exists():
        achieve = UserAchievements()
        achieve.user = user
        achieve.achievement = achievementegg
        achieve.save()

        return HttpResponse(status=200)

    else:
        return HttpResponse(status=204)


def should_stop(real_array, digcost, movecost):
    ycmax = 0.00
    cum_array = []
    yieldovercost = []
    cum_total = 0
    stop_here = 0

    for r in real_array:
        cum_total += r
        cum_array.append(cum_total)

    for i in range(0, len(cum_array)):
        yc = round(cum_array[i] / (movecost + ((i + 1) * digcost)), 2)
        yieldovercost.append(yc)

    for i in range(0, len(yieldovercost)):
        if yieldovercost[i] >= ycmax:
            ycmax = yieldovercost[i]
            stop_here = i

    return stop_here


# change the profile picture and return to the user profile page
def change_profile_image(request):
    user = utility.getuser(request)

    if 'image' in request.FILES:
        user.picture = request.FILES['image']
        utility.usersave(user)
    return user_profile(request)


# post score to Facebook wall
def share(request):
    social_user = request.user.social_auth.filter(provider='facebook', )[0]
    day_gold = request.session['gold']
    attachment = {'name': "Gold Digger game ", 'link': "http://goldrush.pythonanywhere.com/gold_digger/"}
    msg = "Lucky day! Just dug " + str(day_gold) + " gold nuggets today! Check it out here: "
    graph = facebook.GraphAPI(social_user.extra_data['access_token'])
    graph.put_object("me", "feed", message=msg, **attachment)
    return game_over(request)
