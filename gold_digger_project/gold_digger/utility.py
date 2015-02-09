from game import yieldgenerator, cuegenerator, game
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from models import UserProfile, ScanningEquipment, DiggingEquipment, Vehicle, UserAchievements, Achievements
import pickle
from django.core.urlresolvers import reverse
import json
from logger import event_logger

#added for open auth:
from social.pipeline.partial import partial
from django.contrib.auth.models import User
from gold_digger.models import UserProfile, ScanningEquipment, Vehicle, DiggingEquipment
from django.template import RequestContext
from requests import request
from gold_digger import views

# This function creates a dictionary of the various user values
# While forcing any function looking for user values to find all of them it stops repeated code
# May split each call into a separate function to limit calls needed to be made
# ONLY GOOD FOR RETRIEVING VALUES NEEDS TO BE REWORKED
def userstats(request):
    current_user = UserProfile.objects.get(user=request.user)

    userstat = {'current_user': current_user,
                'scan': current_user.equipment.image.url,
                'tool': current_user.tool.image.url,
                'vehicle': current_user.vehicle.image.url,
                'mod_scan': int(current_user.equipment.modifier) * 100,
                'mod_scan_l': int(current_user.equipment.modifier) * 10,
                'mod_tool': int(current_user.tool.modifier) * 100,
                'modt_tool': current_user.tool.time_modifier,
                'mod_vehicle': current_user.vehicle.modifier,
                'gold': current_user.gold,
                'mines': current_user.mines,
                'games_played': current_user.games_played}

    return userstat


# Function to retrieve the context, every time the context is needed to function will call here
# It stops the context request being repeated throughout the system
def contextget(request):
    context = RequestContext(request)

    return context


def startgame(request):
    user = userstats(request)
    _time_remaining = request.session['time_remaining']  # the player starts with 300 units of time
    _no_mines = 10  # the game will consist of ten individual mines
    _depth = 10  # each mine will be 10 blocks deep
    _max_yield = 100  # the player has the chance to mine a maximum of 100 gold

    _yield = yieldgenerator.RandomYield(_depth, _max_yield)
    _cue = cuegenerator.RandomCue(_max_yield, user['current_user'].equipment.modifier)
    _game = game.Game(_time_remaining,
                      _no_mines,
                      _max_yield,
                      _depth,
                      user['current_user'].equipment.modifier,
                      user['modt_tool'],
                      user['mod_vehicle'],
                      _yield, _cue)

    _game.start()

    if mine_type == 'California':
        # print "California"
        request.session['mine_type'] = 'California'

    elif mine_type == 'Yukon':
        # print "Yukon"
        request.session['mine_type'] = "Yukon"

    elif mine_type == 'Brazil':
        # print "Brazil"
        request.session['mine_type'] = 'Brazil'

    elif mine_type == 'South Africa':
        # print "South Africa"
        request.session['mine_type'] = 'South Africa'

    elif mine_type == 'Scotland':
        # print "Scotland"
        request.session['mine_type'] = 'Scotland'

    elif mine_type == 'Victoria':
        # print "Victoria"
        request.session['mine_type'] = 'Victoria'
    else:
        print "Invalid mine in session variable"

    return _game


def loginhome(request):
    print "Login Home"

    context = contextget(request)

    userstat = userstats(request)

    request.session['days'] = userstat['current_user'].games_played

    return render_to_response('gold_digger/home.html', {'current_user': userstat['current_user'],
                                                        'scan': userstat['scan'],
                                                        'tool': userstat['tool'],
                                                        'vehicle': userstat['vehicle'],
                                                        'gold': userstat['gold'],
                                                        'mod_scan': userstat['mod_scan'],
                                                        'mod_tool': userstat['mod_tool'],
                                                        'modt_tool': userstat['modt_tool'],
                                                        'mod_vehicle': userstat['mod_vehicle']}, context)


def basichome(request):
    print "Simple Home"

    context = contextget(request)

    request.session['time_remaining'] = 100
    request.session['gold'] = 0
    user_form = UserForm()
    profile_form = UserProfileForm()
    return render_to_response('gold_digger/home.html', {'user_form': user_form, 'profile_form': profile_form},
                              context)


def postregister_valid(request, user_form, profile_form):

        user = user_form.save()

        user.set_password(user.password)

        user.save()

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
        print user_form.errors, profile_form.errors
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

            event_logger.info('USER ' + username + ' LOGIN')

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


def otherlogin(context, request):

    context = contextget(request)

    userstat = userstats(request)

    return render_to_response('gold_digger/home.html', {'current_user': userstat['current_user'],
                                                        'scan': userstat['scan'],
                                                        'tool': userstat['tool'],
                                                        'vehicle': userstat['vehicle'],
                                                        'gold': userstat['gold'],
                                                        'mod_scan': userstat['mod_scan'],
                                                        'mod_tool': userstat['mod_tool'],
                                                        'modt_tool': userstat['modt_tool'],
                                                        'mod_vehicle': userstat['mod_vehicle']}, context)


def userprofile(request):

    userstat = userstats(request)
    achieve = UserAchievements.objects.filter(user=userstats['current_user'])
    context = contextget(request)


    return render_to_response('gold_digger/profile.html', {'user': userstat['current_user'],
                                                           'mod_scan': userstat['mod_scan'],
                                                           'mod_tool': userstat['mod_tool'],
                                                           'modt_tool': userstat['modt_tool'],
                                                           'mod_scan_l': userstat['mod_scan_l'],
                                                           'achievements': achieve}, context)


def move(context, request):
    userstat = userstats(request)
    context = contextget(request)

    request.session['time_remaining'] -= userstat['mod_vehicle']
    request.session['pointer'] = 0
    userstat['current_user'].mines += 1
    userstat['current_user'].save()

    _game_pickled = request.session['game_pickled']
    _game = pickle.loads(_game_pickled)
    _game.player_move()
    _game_pickled = pickle.dumps(_game)
    request.session['game_pickled'] = _game_pickled

    return HttpResponseRedirect(reverse('game2'), context)


def back2main(request):
    user = UserProfile.objects.get(user=request.user)
    context = contextget(request)

    request.session['has_mine'] = False
    request.session['time_remaining'] = 0
    user.gold -= request.session['gold']
    user.save()

    return HttpResponseRedirect(reverse('home'), context)


def gameover(request):

    userstat = userstats(request)
    context = contextget(request)

    if userstat['gold'] > userstat['current_user'].all_time_max_gold:
        userstat['current_user'].all_time_max_gold = userstat['gold']

    # Updating user values
    userstat['current_user'].gold += request.session['gold']
    userstat['current_user'].mines += 1
    userstat['current_user'].games_played += 1
    request.session['days'] += 1
    userstat['current_user'].all_time_gold += request.session['gold']
    userstat['current_user'].average = userstat['current_user'].all_time_gold / userstat['mines']
    userstat['curent_user'].save()

    request.session['game_started'] = False
    request.session['mine_type'] = ''
    request.session['time_remaining'] = 100
    mine_no = (request.session['mine_no']) - 1
    request.session['mine_no'] = 0
    day_gold = request.session['gold']
    total_gold = userstat['gold']
    request.session['gold'] = 0
    cost = determine_cost(request.session['location'])

    if userstat['gold'] < 40:
        return HttpResponseRedirect(reverse('game_over2'), context)

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
    achiev = UserAchievements.objects.all()

    return render_to_response('gold_digger/leaderboards.html', {'users_avg': users_avg,
                                                                'users_gold': users_gold,
                                                                'users_games': users_games,
                                                                'users_all_time_gold': users_all_time_gold,
                                                                'users_achievements': users_achievements,
                                                                'achiev': achiev}, context)


def gamechoice(request):
    context = contextget(request)
    user = userstats(request)

    if user['gold'] < 40:
        return HttpResponseRedirect(reverse('game_over2'), request)

    mine_types = ['California', 'Yukon', 'Brazil', 'South Africa', 'Scotland', 'Victoria']

    request.session['game_started'] = False
    request.session['mine_type'] = ''
    request.session['purchase'] = False
    request.session['time_remaining'] = 100
    request.session['gold'] = 0

    return render_to_response('gold_digger/game_choice2.html', {'mine_types': mine_types,
                                                                'scan': user['scan'],
                                                                'tool': user['tool'],
                                                                'vehicle': user['vehicle'],
                                                                'gold': user['gold'],
                                                                'mod_scan': user['mod_scan'],
                                                                'mod_tool': user['mod_tool'],
                                                                'modt_tool': user['modt_tool'],
                                                                'mod_vehicle': user['mod_vehicle']}, context)


def game(request):
    context = contextget(request)

    user = userstats(request)

    if request.session['mine_type'] == '':
        mine_type = request.session['location']
        user['current_user'].gold -= determine_cost(mine_type)
        user['current_user'].save()
    else:
        mine_type = request.session['mine_type']

    if not request.session['game_started']:
        _game = startgame(request)  # call on the start game method

        _game_pickled = pickle.dumps(_game)
        request.session['game_pickled'] = _game_pickled
        request.session['pointer'] = 0
        request.session['game_started'] = True

    else:
        # Unpickling
        _game_pickled = request.session['game_pickled']
        _game = pickle.loads(_game_pickled)
        _time_remaining = request.session['time_remaining']

    _location = request.sesstion['location']
    _pointer = request.session['pointer']

    return render_to_response('gold_digger/game2.html', {'blocks': _game.get_current_blocks(),
                                                         'user': user['current_user'],
                                                         'time_remaining': _time_remaining,
                                                         'move_cost': user['mod_vehicle'],
                                                         'dig_cost': user['modt_tool'],
                                                         'location': _location,
                                                         'pointer': _pointer,
                                                         'mine_no': _game.mine_position + 1,
                                                         'visibility': user['mod_scan_l'],
                                                         'mod_scan': user['mod_scan'],
                                                         'mod_tool': user['mod_tool'],
                                                         'modt_tool': user['modt_tool'],
                                                         'mod_vehicle': user['mod_vehicle']}, context)


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
    user = userstats(request)

    # Unpickling the blocks
    _game_pickled = request.session['game_pickled']
    _game = pickle.loads(_game_pickled)

    # POSTED objects['pointer']
    gold_collected = _game.player_dig()

    request.session['pointer'] += 1
    request.session['time_remaining'] -= user['modt_tool']
    request.session['gold'] += gold_collected

    # Pickling
    _game_pickled = pickle.dumps(_game)
    request.session['game_pickled'] = _game_pickled

    myResponse = {}

    if gold_collected == -1:
        move(request)

    if _game.check_end():
        return HttpResponse(status=204)

    myResponse['totalgold'] = user['gold']
    myResponse['timeremaining'] = request.session['time_remaining']
    myResponse['currentgold'] = request.session['gold']
    myResponse['goldextracted'] = gold_collected

    return HttpResponse(json.dumps(myResponse), content_type="application/json")


def store(request):
    context = contextget(request)
    user = userstats(request)

    equipment = ScanningEquipment.objects.all()
    vehicles = Vehicle.objects.all()
    tools = DiggingEquipment.objects.all()
    new_id_s = user['current_user'].equipment.id
    new_id_t = user['current_user'].tool.id
    new_id_v = user['current_user'].vehicle.id
    new_item_s = user['current_user'].equipment
    new_item_t = user['current_user'].tool
    new_item_v = user['current_user'].vehicle

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
                                                         'gold': user['gold'],
                                                         'scan': user['scan'],
                                                         'dig': user['tool'],
                                                         'move': user['vehicle'],
                                                         'new_item_s': new_item_s,
                                                         'new_item_t': new_item_t,
                                                         'new_item_v': new_item_v}, context)


def scanupgrade(request):
    user = userstats(request)

    item_id = user['current_user'].equipment.id
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
        user['current_user'].gold -= new_item.price
        user['current_user'].equipment = new_item
        user['current_user'].save()

        myResponse['image'] = new_item.image.url
        myResponse['gold'] = user['current_user'].gold

        return HttpResponse(json.dumps(myResponse), content_type="application/json")

def toolupgrade(request):
    user = userstats(request)

    item_id = user['current_user'].tool.id
    myResponse = {}
    myResponse['maxed_up'] = False
    myResponse['funds'] = False

    if item_id == 5:
        myResponse['maxed_up'] = True
        return HttpResponse(json.dumps(myResponse), content_type="application/json")

    else:
        item_id += 1
        new_item = DiggingEquipment.objects.get(id=item_id)

    if new_item.price > user['gold']:
        return HttpResponse(status=204)

    if (user['gold'] - new_item.price) < 40:
        return HttpResponse(status=202)


    else:
        user['current_user'].gold -= new_item.price
        user['current_user'].tool = new_item
        user['current_user'].save()

        myResponse['image'] = new_item.image.url
        myResponse['gold'] = user['current_user'].gold

        return HttpResponse(json.dumps(myResponse), content_type="application/json")


def vehicleupgrade(request):
    user = userstats(request)

    item_id = user['current_user'].vehicle.id
    myResponse = {}
    myResponse['maxed_up'] = False

    if item_id == 5:
        myResponse['maxed_up'] = True
        return HttpResponse(json.dumps(myResponse), content_type="application/json")

    else:
        item_id += 1
        new_item = Vehicle.objects.get(id=item_id)

    if new_item.price > user['gold']:
        return HttpResponse(status=204)

    if (user['gold'] - new_item.price) < 40:
        return HttpResponse(status=202)

    else:
        user['current_user'].gold -= new_item.price
        user['current_user'].vehicle = new_item
        user['current_user'].save()

        myResponse['image'] = new_item.image.url
        myResponse['gold'] = user['current_user'].gold

        return HttpResponse(json.dumps(myResponse), content_type="application/json")


def update_cost(request):
    user = userstats(request)
    user['current_user'].gold -= int(request.POST['cost'])
    if user['current_user'].gold < 20:
        return HttpResponse(status=204)

    user['current_user'].save()

    myResponse = user['current_user'].gold

    return HttpResponse(json.dumps(myResponse), content_type="application/json")

def gameover2(request):
    context = contextget(request)
    user = userstats(request)

    user['current_user'].gold = 0
    user['current_user'].equipment = ScanningEquipment.objects.get(id=1)
    user['current_user'].tool = DiggingEquipment.objects.get(id=1)
    user['current_user'].vehicle = Vehicle.objects.get(id=1)
    request.session['gold'] = 0
    mines = request.session['mine_no']
    request.session['mine_no'] = 0
    days = (request.session['days']) - 1
    request.session['days'] = 1
    user['current_user'].games_played += 1
    user['current_user'].game_overs += 1
    user['current_user'].gold = 100
    user['current_user'].save()

    return render_to_response('gold_digger/game_over2.html', {'mines': mines,
                                                              'days': days}, context)


def achievement(user, id):

    achieved = Achievements.objects.get(id=id)
    return add_achievement(user, achieved)


def add_achievement(user, achievement):
    myResponse = {}
    if not UserAchievements.objects.filter(user=user, achievement=achievement).exists():
        achieve = UserAchievements()
        achieve.user = user
        achieve.achievement = achievement
        achieve.save()
        print "Achievement UNLOCKED"

        myResponse['achievement_name'] = achievement.name
        myResponse['achievement_condition'] = achievement.condition
        myResponse['achievement_image'] = achievement.image.url
        myResponse['achievement_desc'] = achievement.description

        return myResponse
    else:
        myResponse['unlocked'] = True
        return myResponse
		
		
#method for open auth to create new profile
def add_new_profile( user, response, *args, **kwargs):
	try:
		profile = UserProfile.objects.get(user=user)
	except UserProfile.DoesNotExist:
		profile = UserProfile(user=user)

	profile.equipment = ScanningEquipment.objects.get(pk=1)
        profile.vehicle = Vehicle.objects.get(pk=1)
        profile.tool = DiggingEquipment.objects.get(pk=1)

	#probably need to add logger event for the new log???
        profile.save()
