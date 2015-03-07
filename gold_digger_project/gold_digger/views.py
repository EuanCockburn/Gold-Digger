from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forms import UserProfileForm, UserForm
from models import UserProfile, UserAchievements, Achievements
from django.core.urlresolvers import reverse
import utility
import json

 

locations = ['California', 'Yukon', 'Brazil', 'South Africa', 'Scotland', 'Victoria']

def home(request):
    try:
        return utility.loginhome(request)
    except:
        return utility.basichome(request)


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
    if request.method == 'POST':

        return utility.postlogin(request)

    else:

        return utility.otherlogin(request)


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/gold_digger/')


@login_required
def user_profile(request):
    return utility.userprofile(request)


@login_required
def move(request):
    return utility.move(request)


@login_required
def back_to_main(request):
    return utility.back2main(request)


@login_required
def game_over(request):
    return utility.gameover(request)


def leaderboards(request):
    return utility.leaderboards(request)


@login_required
def game_choice2(request):
    return utility.gamechoice(request)


@login_required
def game2(request):
    return utility.game(request)


@login_required
def ajaxview(request):
    return utility.ajaxview(request)


@login_required
def store(request):
    return utility.store(request)


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
    return utility.update_cost(request)


@login_required
def ajax_exit():
    return HttpResponse(status=200)


@login_required
def game_over2(request):
    return utility.gameover2(request)


@login_required
def achievements(request):
    user = UserProfile.objects.get(user=request.user)

    myResponse = {}

    if user.gold < 50:
        myResponse['unlocked'] = True

    if user.gold > 50:
        myResponse = utility.achievement(user, 1)

    if user.gold > 500:
        myResponse = utility.achievement(user, 2)

    if user.gold > 1000:
        myResponse = utility.achievement(user, 3)

    if user.gold > 5000:
        myResponse = utility.achievement(user, 4)

    if user.gold > 10000:
        myResponse = utility.achievement(user, 5)

    if user.gold > 20000:
        myResponse = utility.achievement(user, 6)

    if user.games_played > 5:
        myResponse = utility.achievement(user, 7)

    if user.games_played > 10:
        myResponse = utility.achievement(user, 8)

    if user.games_played > 15:
        myResponse = utility.achievement(user, 9)

    if user.games_played > 20:
        myResponse = utility.achievement(user, 10)

    if user.games_played > 50:
        myResponse = utility.achievement(user, 11)

    if user.mines > 50:
        myResponse = utility.achievement(user, 12)

    if user.mines > 100:
        myResponse = utility.achievement(user, 13)

    if user.mines > 300:
        myResponse = utility.achievement(user, 14)

    return HttpResponse(json.dumps(myResponse), content_type="application/json")


def display_achievements(request):
    ach = Achievements.objects.all()
    context = RequestContext(request)

    return render_to_response('gold_digger/achievements.html', {'achievements': ach}, context)


def egg(request):
    user = UserProfile.objects.get(user=request.user)
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
	
#post score to Facebook walll
def share(request):
    return utility.post_to_wall(request)
