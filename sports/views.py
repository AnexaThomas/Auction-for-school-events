from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import csv
from django.http import JsonResponse
import json
from .models import Group  # Add this with your other imports
from .models import Player  # Changed from lowercase 'player' to 'Player' for better convention
import pandas as pd

from django.http import HttpResponse
from .models import Player
from django.db.models import Sum
from django.contrib.humanize.templatetags.humanize import intcomma

def index(request):
    # Get all player spending by team in one query
    spending = Player.objects.values('team').annotate(total=Sum('final_price'))
    
    # Convert to dictionary for easy lookup
    spending_dict = {item['team']: item['total'] for item in spending}
    
    team_funds = {
        'Cutie Pie': 15000000 - spending_dict.get('Cutie Pie', 0),
        'Black Pink': 15000000 - spending_dict.get('Black Pink', 0),
        'Pink Pandas': 15000000 - spending_dict.get('Pink Pandas', 0),
        'Boss Babes': 15000000 - spending_dict.get('Boss Babes', 0)
    }
    
    # Create formatted versions with commas
    formatted_funds = {
        team: intcomma(amount)
        for team, amount in team_funds.items()
    }
    
    return render(request, 'index.html', {
        'players': Player.objects.all(),
        'team_funds': team_funds,  # Original numeric values
        'formatted_funds': formatted_funds  # Formatted strings with commas
    })
def control(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        
        new_player = Player(
            name=name,
            price=price,
            image=image
        )
        new_player.save()
        
        messages.success(request, 'Player added successfully!')
        return redirect('control')
    
    return render(request, 'control.html')

@csrf_exempt
def update_player(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            player_id = data.get('player_id')
            team = data.get('team')
            final_price = data.get('final_price')
            
            # Get the player and update
            player = Player.objects.get(id=player_id)
            player.team = team
            player.final_price = final_price
            player.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
        
# In your Django view
def get_team_players(request):
    if request.method == 'POST':
        team = request.POST.get('team')
        players = Player.objects.filter(team=team).values('id', 'name', 'image', 'final_price')
        return JsonResponse({'success': True, 'players': list(players)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
def RC(request):
    RC = Player.objects.filter(team__iexact='Boss Babes')
    print("Fetched players:", RC)
    return render(request, "RC.html", {'RC': RC})
def SK(request):
    SK = Player.objects.filter(team__iexact='Cutie Pie')
    print("Fetched players:", SK)
    return render(request, "SK.html", {'SK': SK})
def KR(request):
    KR = Player.objects.filter(team__iexact='Black Pink')
    print("Fetched players:", KR)
    return render(request, "KR.html", {'KR': KR})
def DD(request):
    DD = Player.objects.filter(team__iexact='Pink Pandas')
    print("Fetched players:", DD)
    return render(request, "DD.html", {'DD': DD})



def get_team_funds(request):
    teams = {
        'Cutie Pie': 15000000,
        'Black Pink': 15000000,
        'Pink Pandas': 15000000,
        'Boss Babes': 15000000
    }
    
    # Calculate remaining funds by summing player purchases
    for team in teams:
        total_spent = Player.objects.filter(team=team).aggregate(Sum('final_price'))['final_price__sum'] or 0
        teams[team] -= total_spent
    
    return JsonResponse(teams)
