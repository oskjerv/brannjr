from django.db.models import F
import hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404

from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count, Sum, Avg, Max, Min

from django.core.paginator import Paginator
from django.views.generic import ListView


from .models import Squad, Match, Player, VoteLog


def index(request):
    match_list = Match.objects.order_by("-date")  # get all match objects ordered by date
    paginator = Paginator(match_list, 5)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "polls/index.html", {"page_obj": page_obj})
    #return render(request, "list.html", {"page_obj": page_obj})

    
    #context = {"latest_match_list": latest_match_list}
    #return render(request, "polls/index.html", context)

def detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    return render(request, "polls/detail.html", {"match":  match})


def results(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    
    
    
    #for player in match.player_set.all():
    #    print(player.mom_votes) 
        
    votes = match.player_set.all().aggregate(
        sum = Sum('mom_votes')
    )
    
    return render(request, "polls/results.html", {"match": match, 'votes': votes})


def vote(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    user_ip = get_client_ip(request)
    hashed_ip = hash_ip(user_ip)
    
    print(user_ip)
    
    if has_voted(hashed_ip, match):
        return render(
            request,
            "polls/detail.html",
            {
                "match": match,
                "error_message": "Du har allerede stemt.",
            },
        )
    
    try:
        selected_choice = match.player_set.get(pk=request.POST["choice"])
        VoteLog.objects.create(hashed_ip=hashed_ip, match=match)
        
    except (KeyError, Player.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "match": match,
                "error_message": "Du må velge en spiller.",
            },
        )
    else:
        selected_choice.mom_votes = F("mom_votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(match.id,)))
    
def has_voted(hashed_ip, match):
    return VoteLog.objects.filter(hashed_ip=hashed_ip, match=match).exists()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hash_ip(ip_address):
    return hashlib.sha256(ip_address.encode()).hexdigest()