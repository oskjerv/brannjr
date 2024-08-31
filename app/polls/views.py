from django.db.models import F

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404

from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count, Sum, Avg, Max, Min


from .models import Squad, Match, Player


def index(request):
    latest_match_list = Match.objects.order_by("-date")[:5]
    context = {"latest_match_list": latest_match_list}
    return render(request, "polls/index.html", context)

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
    try:
        selected_choice = match.player_set.get(pk=request.POST["choice"])
        
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