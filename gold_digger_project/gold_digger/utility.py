from game.game import *
from game.game import *
from game.yieldgenerator import *
from game.cuegenerator import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from models import UserProfile, ScanningEquipment, DiggingEquipment, Vehicle, UserAchievements, Achievements
import pickle
from django.core.urlresolvers import reverse
import json

# added for open auth:
from social.pipeline.partial import partial
from django.contrib.auth.models import User
from models import UserProfile, ScanningEquipment, Vehicle, DiggingEquipment
from requests import request
from views import *
import random
from django.core.cache import cache


def getuser(request):
    current_user = UserProfile.objects.get(user=request.user)
    return current_user


def getscan(user):
    return user.equipment.image.url


def gettool(user):
    return user.tool.image.url


def getvehicle(user):
    return user.vehicle.image.url


def getmod_scan(user):
    return int(user.equipment.modifier * 100)


def getmod_scan_l(user):
    return int(user.equipment.modifier * 10)


def getmodt_tool(user):
    return user.tool.time_modifier


def getmod_vehicle(user):
    return user.vehicle.modifier


def getgold(user):
    return user.gold


def getmines(user):
    return user.mines


def getgames_played(user):
    return user.games_played


def getaccuracy(user):
    return user.equipment.modifier


def getalltimegold(user):
    return user.all_time_max_gold


def usersave(user):
    user.save


def getequipid(user):
    return user.equipment.id


def gettoolid(user):
    return user.tool.id


def getvehicleid(user):
    return user.vehicle.id


def getequipment(user):
    return user.equipment


def gettl(user):
    return user.tool


def getvhcle(user):
    return user.vehicle


# Function to retrieve the context, every time the context is needed to function will call here
# It stops the context request being repeated throughout the system
def contextget(request):
    context = RequestContext(request)
    return context


def startgame(request, mine_type):
    user = getuser(request)
    time_remaining = 100  # the player starts with 300 units of time
    no_mines = 20  # the game will consist of ten individual mines
    depth = 10  # each mine will be 10 blocks deep
    id = mine_type + '_new' # Define cache id

    # Check if the object already exists in the cache
    if incache(id):
        # Return the cached game if it exists
        return get_game_incache(id)
    else:
        if mine_type == 'California':
            # print "California"
            request.session['mine_type'] = 'California'
            yield_array = RandUniformAdjustYield(depth, 25, 1, -2, 2)
            max_yield = 25

        elif mine_type == 'Yukon':
            # print "Yukon"
            request.session['mine_type'] = "Yukon"
            list = [15, 20, 25, 35, 45, 50, 55]
            yield_array = RandMaxYield(depth, 55, 1, 0, list)
            max_yield = 55

        elif mine_type == 'Brazil':
            # print "Brazil"
            request.session['mine_type'] = 'Brazil'
            span = [10, 12, 15, 20]
            yield_array = RandMaxYield(depth, 20, -1.5, 5, span)
            max_yield = 20

        elif mine_type == 'South Africa':
            # print "South Africa"
            request.session['mine_type'] = 'South Africa'
            span = [0.2, 0.1, 0.3, 6, 8]
            list = [47, 48, 49, 50, 51, 52, 53]
            yield_array = RandMaxYield(depth, 53, random.choice(span), 0, list)
            max_yield = 53

        elif mine_type == 'Scotland':
            # print "Scotland"
            request.session['mine_type'] = 'Scotland'
            list = [80, 83, 85, 87, 90, 92, 95]
            yield_array = RandMaxYield(depth, 95, 0.7, random.randint(-8, -2), list)
            max_yield = 95

        elif mine_type == 'Victoria':
            # print "Victoria"
            request.session['mine_type'] = 'Victoria'
            list = [40, 50, 60, 70, 80, 90, 100, 110]
            yield_array = RandMaxYield(depth, 110, 1, 3, list)
            max_yield = 110
        else:
            print "Invalid mine in session variable"

    accuracy = getaccuracy(user)

    cue = AccurateCue(max_yield, accuracy)

    game = Game(time_remaining,
                no_mines,
                max_yield,
                depth,
                accuracy,
                getmodt_tool(user),
                getmod_vehicle(user),
                yield_array,
                cue)

    # Store the generated game in the cache
    store_game_incache(id, game)

    game.start()

    return game


def loginhome(request):
    context = contextget(request)

    user = getuser(request)

    request.session['days'] = getgames_played(user)

    return render_to_response('gold_digger/home.html', {'current_user': user,
                                                        'scan': getscan(user),
                                                        'tool': gettool(user),
                                                        'vehicle': getvehicle(user),
                                                        'gold': getgold(user),
                                                        'mod_scan': getmod_scan(user),
                                                        'modt_tool': getmodt_tool(user),
                                                        'mod_vehicle': getmod_vehicle(user)}, context)


def basichome(request):
    context = contextget(request)

    request.session['time_remaining'] = 100
    request.session['gold'] = 0
    user_form = UserForm()
    profile_form = UserProfileForm()
    return render_to_response('gold_digger/home.html', {'user_form': user_form, 'profile_form': profile_form},
                              context)


def incache(id):
    return cache.has_key(id)


def store_game_incache(id, game):
    cache.set(id, pickle.dumps(game), 500)


def get_game_incache(id):
    game = pickle.loads(cache.get(id))
    return game


def postregister_valid(request, user_form, profile_form):
    user = user_form.save()

    user.set_password(user.password)

    usersave(user)

    profile = profile_form.save(commit=False)
    profile.user = user

    if 'picture' in request.FILES:
        profile.picture = request.FILES['picture']

    profile.equipment = ScanningEquipment.objects.get(pk=1)
    profile.vehicle = Vehicle.objects.get(pk=1)
    profile.tool = DiggingEquipment.objects.get(pk=1)
    profile.save()

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            print "User logged in"
            login(request, user)


def postregister_invalid(context, user_form, profile_form):
    return render_to_response('gold_digger/home.html', {'user_form': user_form, 'profile_form': profile_form,
                                                        'registered': registered}, context)


def postlogin(request):
    context = contextget(request)

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
        return render_to_response('gold_digger/home.html', {'user_form': user_form, 'profile_form': profile_form,
                                                            'bad_details': bad_details}, context)


def otherlogin(request):
    context = contextget(request)

    user = getuser(request)

    return render_to_response('gold_digger/home.html', {'current_user': user,
                                                        'scan': getscan(user),
                                                        'tool': gettool(user),
                                                        'vehicle': getvehicle(user),
                                                        'gold': getgold(user),
                                                        'mod_scan': getmod_scan(user),
                                                        'modt_tool': getmodt_tool(user),
                                                        'mod_vehicle': getmod_vehicle(user)}, context)


def userprofile(request):
    user = getuser(request)
    achieve = UserAchievements.objects.filter(user=user)
    context = contextget(request)

    return render_to_response('gold_digger/profile.html', {'user': user,
                                                           'mod_scan': getmod_scan(user),
                                                           'modt_tool': getmodt_tool(user),
                                                           'achievements': achieve}, context)


def move(request):
    user = getuser(request)
    context = contextget(request)

    request.session['time_remaining'] -= getmod_vehicle(user)
    request.session['pointer'] = 0
    request.session['mine_no'] += 1
    user.mines += 1
    usersave(user)

    if request.session['time_remaining'] <= 0:
        return HttpResponseRedirect(reverse('game_over'), context)

    game_pickled = request.session['game_pickled']
    game = pickle.loads(game_pickled)
    game.player_move()
    game_pickled = pickle.dumps(game)
    request.session['game_pickled'] = game_pickled

    return HttpResponseRedirect(reverse('game2'), context)


def back2main(request):
    user = getuser(request)
    context = contextget(request)

    request.session['has_mine'] = False
    request.session['time_remaining'] = 0
    user.gold -= request.session['gold']
    usersave(user)

    return HttpResponseRedirect(reverse('home'), context)


def gameover(request, is_facebook_user):
    user = getuser(request)
    context = contextget(request)
    currentgold = getgold(user)

    if currentgold > getalltimegold(user):
        user.all_time_max_gold = currentgold

    # Updating user values
    user.gold += request.session['gold']
    user.mines += 1
    user.games_played += 1
    request.session['days'] += 1
    user.all_time_gold += request.session['gold']
    user.average = user.all_time_gold / getmines(user)
    usersave(user)

    request.session['game_started'] = False
    request.session['mine_type'] = ''
    request.session['time_remaining'] = 100
    mine_no = request.session['mine_no']
    request.session['mine_no'] = 0
    day_gold = request.session['gold']
    total_gold = getgold(user)
    request.session['gold'] = 0
    cost = determine_cost(request.session['location'])

    if currentgold < 40:
        return HttpResponseRedirect(reverse('game_over2'), context)
		
	try:
        is_facebook_user=request.user.social_auth.filter( provider='facebook',)[0]
		is_facebook_user=1
	except:
		is_facebook_user=0
    return render_to_response('gold_digger/game_over.html', {'day_gold': day_gold,
                                                             'total_gold': total_gold,
                                                             'mine_no': mine_no,
                                                             'cost': cost}, context)


def leaderboards(request):
    context = contextget(request)

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


def gamechoice(request):
    context = contextget(request)
    user = getuser(request)
    gold = getgold(user)

    if gold < 40:
        return HttpResponseRedirect(reverse('game_over2'), request)

    mine_types = ['California', 'Yukon', 'Brazil', 'South Africa', 'Scotland', 'Victoria']

    request.session['game_started'] = False
    request.session['mine_type'] = ''
    request.session['purchase'] = False
    request.session['time_remaining'] = 100
    request.session['gold'] = 0

    return render_to_response('gold_digger/game_choice2.html', {'mine_types': mine_types,
                                                                'scan': getscan(user),
                                                                'tool': gettool(user),
                                                                'vehicle': getvehicle(user),
                                                                'gold': gold,
                                                                'mod_scan': getmod_scan(user),
                                                                'modt_tool': getmodt_tool(user),
                                                                'mod_vehicle': getmod_vehicle(user)}, context)


def game(request):
    context = contextget(request)

    user = getuser()

    if request.session['mine_type'] == '':
        mine_type = request.session['location']
        user.gold -= determine_cost(mine_type)
        usersave(user)
    else:
        mine_type = request.session['mine_type']

    if not request.session['game_started']:
        _game = startgame(request, mine_type)  # call on the start game method

        _game_pickled = pickle.dumps(_game)
        request.session['game_pickled'] = _game_pickled
        request.session['pointer'] = 0
        request.session['mine_no'] = 1
        request.session['time_remaining'] = 100
        _time_remaining = 100
        request.session['game_started'] = True

    else:
        # Unpickling
        _game_pickled = request.session['game_pickled']
        _game = pickle.loads(_game_pickled)
        _time_remaining = request.session['time_remaining']

        if _time_remaining <= 0:
            return HttpResponseRedirect(reverse('game_over'), context)

    _location = request.session['location']
    _pointer = request.session['pointer']

    return render_to_response('gold_digger/game2.html', {'blocks': _game.get_current_blocks(),
                                                         'user': user,
                                                         'time_remaining': _time_remaining,
                                                         'move_cost': getmod_vehicle(user),
                                                         'dig_cost': getmodt_tool(user),
                                                         'location': _location,
                                                         'pointer': _pointer,
                                                         'mine_no': _game.mine_position + 1,
                                                         'visibility': getmod_scan_l(user),
                                                         'mod_scan': getmod_scan(user),
                                                         'modt_tool': getmodt_tool(user),
                                                         'mod_vehicle': getmod_vehicle(user)}, context)


def determine_cost(mine_type):
    cost = 0
    if mine_type == 'California':
        cost = 40
    elif mine_type == 'Yukon':
        cost = 100
    elif mine_type == 'Brazil':
        cost = 200
    elif mine_type == 'South Africa':
        cost = 300
    elif mine_type == 'Scotland':
        cost = 400
    elif mine_type == 'Victoria':
        cost = 500

    return cost


def ajaxview(request):
    user = getuser(request)

    # Unpickling the blocks
    _game_pickled = request.session['game_pickled']
    _game = pickle.loads(_game_pickled)

    # POSTED objects['pointer']
    gold_collected = _game.player_dig()
    max_yield = _game.get_max_yield()

    request.session['pointer'] += 1
    request.session['time_remaining'] -= getmodt_tool(user)
    request.session['gold'] += gold_collected

    # Pickling
    _game_pickled = pickle.dumps(_game)
    request.session['game_pickled'] = _game_pickled

    myResponse = {}

    if request.session['pointer'] == 10:
        myResponse['nextmine'] = True

    if _game.check_end():
        return HttpResponse(status=204)

    if gold_collected == 0:
        myResponse['nuggets'] = 0
    else:
        myResponse['nuggets'] = ((6 * gold_collected) / max_yield) + 1

    myResponse['totalgold'] = getgold(user)
    myResponse['timeremaining'] = request.session['time_remaining']
    myResponse['currentgold'] = request.session['gold']
    myResponse['goldextracted'] = gold_collected

    return HttpResponse(json.dumps(myResponse), content_type="application/json")


def store(request):
    context = contextget(request)
    user = getuser(request)

    equipment = ScanningEquipment.objects.all()
    vehicles = Vehicle.objects.all()
    tools = DiggingEquipment.objects.all()
    new_id_s = getequipid(user)
    new_id_t = gettoolid(user)
    new_id_v = getvehicleid(user)
    new_item_s = getequipment(user)
    new_item_t = gettl(user)
    new_item_v = getvhcle(user)

    if new_id_s != 5:
        new_id_s += 1
        new_item_s = ScanningEquipment.objects.get(id=new_id_s)

    if new_id_t != 5:
        new_id_t += 1
        new_item_t = DiggingEquipment.objects.get(id=new_id_t)

    if new_id_v != 5:
        new_id_v += 1
        new_item_v = Vehicle.objects.get(id=new_id_v)

    return render_to_response('gold_digger/store.html', {'equipment': equipment,
                                                         'vehicles': vehicles,
                                                         'tools': tools,
                                                         'gold': getgold(user),
                                                         'scan': getscan(user),
                                                         'dig': gettool(user),
                                                         'move': getvehicle(user),
                                                         'new_item_s': new_item_s,
                                                         'new_item_t': new_item_t,
                                                         'new_item_v': new_item_v}, context)


def scanupgrade(request):
    user = getuser(request)

    item_id = getequipid(user)
    myResponse = {}
    myResponse['maxed_up'] = False
    myResponse['funds'] = False

    if item_id == 5:
        myResponse['maxed_up'] = True
        return HttpResponse(json.dumps(myResponse), content_type="application/json")
    else:
        item_id += 1
        new_item = ScanningEquipment.objects.get(id=item_id)

    if new_item.price > user['gold']:
        return HttpResponse(status=204)

    if (user['gold'] - new_item.price) < 40:
        return HttpResponse(status=202)

    else:
        user.gold -= new_item.price
        user.equipment = new_item
        usersave(user)

        myResponse['image'] = new_item.image.url
        myResponse['gold'] = getgold(user)

        return HttpResponse(json.dumps(myResponse), content_type="application/json")


def toolupgrade(request):
    user = getuser(request)

    item_id = gettoolid(user)
    myResponse = {}
    myResponse['maxed_up'] = False
    myResponse['funds'] = False

    if item_id == 5:
        myResponse['maxed_up'] = True
        return HttpResponse(json.dumps(myResponse), content_type="application/json")

    else:
        item_id += 1
        new_item = DiggingEquipment.objects.get(id=item_id)

    if new_item.price > getgold(user):
        return HttpResponse(status=204)

    if (user.gold - new_item.price) < 40:
        return HttpResponse(status=202)

    else:
        user.gold -= new_item.price
        user.tool = new_item
        usersave(user)

        myResponse['image'] = new_item.image.url
        myResponse['gold'] = getgold(user)

        return HttpResponse(json.dumps(myResponse), content_type="application/json")


def vehicleupgrade(request):
    user = getuser(request)
    gold = getgold(user)

    item_id = getvehicleid(user)
    myResponse = {}
    myResponse['maxed_up'] = False

    if item_id == 5:
        myResponse['maxed_up'] = True
        return HttpResponse(json.dumps(myResponse), content_type="application/json")

    else:
        item_id += 1
        new_item = Vehicle.objects.get(id=item_id)

    if new_item.price > gold:
        return HttpResponse(status=204)

    if (gold - new_item.price) < 40:
        return HttpResponse(status=202)

    else:
        user.gold -= new_item.price
        user.vehicle = new_item
        usersave(user)

        myResponse['image'] = new_item.image.url
        myResponse['gold'] = getgold(user)

        return HttpResponse(json.dumps(myResponse), content_type="application/json")


def update_cost(request):
    user = getuser(request)
    user.gold -= int(request.POST['cost'])

    gold = getgold(user)

    if gold < 20:
        return HttpResponse(status=204)

    usersave(user)

    myResponse = gold

    return HttpResponse(json.dumps(myResponse), content_type="application/json")


def gameover2(request):
    context = contextget(request)
    user = getuser(request)

    user.gold = 0
    user.equipment = ScanningEquipment.objects.get(id=1)
    user.tool = DiggingEquipment.objects.get(id=1)
    user.vehicle = Vehicle.objects.get(id=1)
    request.session['gold'] = 0
    mines = request.session['mine_no']
    request.session['mine_no'] = 0
    days = (request.session['days']) - 1
    request.session['days'] = 1
    user.games_played += 1
    user.game_overs += 1
    user.gold = 100
    usersave(user)

    return render_to_response('gold_digger/game_over2.html', {'mines': mines,
                                                              'days': days}, context)


def achievement(user, id):
    achieved = Achievements.objects.get(id=id)
    return add_achievement(user, achieved)


def add_achievement(user, achieved):
    myResponse = {}

    if not UserAchievements.objects.filter(user=user, achievement=achievement).exists():
        achieve = UserAchievements()
        achieve.user = user
        achieve.achievement = achievement
        achieve.save()
        print "Achievement UNLOCKED"

        myResponse['achievement_name'] = achieved.name
        myResponse['achievement_condition'] = achieved.condition
        myResponse['achievement_image'] = achieved.image.url
        myResponse['achievement_desc'] = achieved.description

        return myResponse

    else:
        myResponse['unlocked'] = True
        return myResponse


# method for open auth to create new profile
def add_new_profile(user, response, *args, **kwargs):
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)

    profile.equipment = ScanningEquipment.objects.get(pk=1)
    profile.vehicle = Vehicle.objects.get(pk=1)
    profile.tool = DiggingEquipment.objects.get(pk=1)
    profile.save()