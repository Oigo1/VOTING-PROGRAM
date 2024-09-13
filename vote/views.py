from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Contestant, Vote
from .forms import VoteForm
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Set voting end time (adjust the time as needed, you can make it 2 minutes, etc.)
VOTING_END_TIME = timezone.now() + timedelta(days=1)

def home(request):
    categories = Category.objects.all()
    vote_form = VoteForm()
    remaining_time = VOTING_END_TIME - timezone.now()

    if remaining_time.total_seconds() > 0:
        # Pass the remaining time to the template for countdown
        return render(request, 'vote/home.html', {'categories': categories, 'vote_form': vote_form, 'remaining_time': remaining_time})
    else:
        # Directly display results when time is up
        return redirect('results')
    

def vote(request, contestant_id):
    contestant = get_object_or_404(Contestant, pk=contestant_id)
    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            voter_id = form.cleaned_data['voter_id']
            # Check if the voter has already voted
            if not Vote.objects.filter(voter_id=voter_id).exists():
                Vote.objects.create(voter_id=voter_id, contestant=contestant)
                contestant.votes += 1
                contestant.save()
                return redirect('home')
    return redirect('home')


@csrf_exempt
def submit_vote(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        voter_id = data.get('voter_id')
        contestant_id = data.get('contestant_id')

        # Check if the voter has already voted
        if Vote.objects.filter(voter_id=voter_id).exists():
            return JsonResponse({'error': 'You have already voted!'}, status=400)

        # Record the vote
        try:
            contestant = Contestant.objects.get(id=contestant_id)
            Vote.objects.create(voter_id=voter_id, contestant=contestant)
            contestant.votes += 1
            contestant.save()
            return JsonResponse({'success': 'Vote has been recorded successfully!'}, status=200)
        except Contestant.DoesNotExist:
            return JsonResponse({'error': 'Contestant not found!'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def results(request):
    results_data = []  # List to hold all contestants and their votes per category
    categories = ['CAPTAIN', 'DEPUTY', 'PREFECTS']

    for category in categories:
        category_contestants = Contestant.objects.filter(seat__name=category).annotate(vote_count=Count('vote')).order_by('-vote_count')
        if category_contestants.exists():
            # Find the contestant with the most votes in the category
            winner = category_contestants.first()
            contestant_data = []
            for contestant in category_contestants:
                contestant_data.append({
                    'name': contestant.name,
                    'votes': contestant.vote_count,
                    'image': contestant.image,  # Assuming 'image' is a field in Contestant model
                    'is_winner': contestant == winner  # Mark the winner
                })
            results_data.append({
                'category': category,
                'contestants': contestant_data
            })

    return render(request, 'vote/results.html', {'results_data': results_data})

