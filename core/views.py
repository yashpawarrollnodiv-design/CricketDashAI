from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from .models import Player, Team, Tournament


def dashboard(request):
    players = Player.objects.all()
    context = {'player_count':players.count(),'team_count':Team.objects.count(),'tournament_count':Tournament.objects.count(),
      'run_leader':players.order_by('-runs').first(),'wicket_leader':players.order_by('-wickets').first(),
      'top_players':players.order_by('-runs')[:5], 'teams':Team.objects.all()}
    return render(request,'core/dashboard.html',context)

def players(request):
    q=request.GET.get('q','').strip(); role=request.GET.get('role','')
    data=Player.objects.select_related('team').order_by('name')
    if q: data=data.filter(name__icontains=q)
    if role: data=data.filter(role=role)
    return render(request,'core/players.html',{'players':data,'q':q,'role':role,'teams':Team.objects.all()})

PLAYER_FIELDS=['name','age','jersey_number','team_id','role','batting_style','bowling_style','matches','runs','batting_average','strike_rate','wickets','economy','fitness','recent_form','catches']
def player_form_save(request, player=None):
    if request.method=='POST':
        try:
            player = player or Player()
            player.name=request.POST.get('name','').strip()
            if not player.name: raise ValueError('Player name is required.')
            for field in ['age','jersey_number','matches','runs','wickets','fitness','recent_form','catches']:
                setattr(player,field,int(request.POST.get(field,0) or 0))
            for field in ['batting_average','strike_rate','economy']:
                setattr(player,field,float(request.POST.get(field,0) or 0))
            player.role=request.POST.get('role','Batter')
            player.batting_style=request.POST.get('batting_style','')
            player.bowling_style=request.POST.get('bowling_style','')
            team_id=request.POST.get('team')
            player.team=Team.objects.filter(pk=team_id).first() if team_id else None
            player.save(); messages.success(request,'Player saved successfully.'); return redirect('players')
        except (ValueError,TypeError) as e: messages.error(request,f'Please check entered values: {e}')
    return render(request,'core/player_form.html',{'player':player,'teams':Team.objects.all()})
def player_add(request): return player_form_save(request)
def player_edit(request,pk): return player_form_save(request,get_object_or_404(Player,pk=pk))
def player_delete(request,pk):
    if request.method=='POST': get_object_or_404(Player,pk=pk).delete(); messages.success(request,'Player deleted.')
    return redirect('players')

def teams(request): return render(request,'core/teams.html',{'teams':Team.objects.all()})
def team_add(request):
    if request.method=='POST':
        name=request.POST.get('name','').strip()
        if name:
            Team.objects.get_or_create(name=name,defaults={'coach':request.POST.get('coach',''),'captain':request.POST.get('captain',''),'city':request.POST.get('city','')})
            messages.success(request,'Team added (or already existed).'); return redirect('teams')
        messages.error(request,'Team name is required.')
    return render(request,'core/team_form.html')
def team_delete(request,pk):
    if request.method=='POST': get_object_or_404(Team,pk=pk).delete(); messages.success(request,'Team deleted.')
    return redirect('teams')

def tournaments(request): return render(request,'core/tournaments.html',{'tournaments':Tournament.objects.all().order_by('-start_date')})
from django.utils.dateparse import parse_date

def tournament_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        venue = request.POST.get('venue', '').strip()

        # Clean date values (remove accidental quotation marks)
        start_date_raw = request.POST.get('start_date', '').strip().strip("\"'“”")
        end_date_raw = request.POST.get('end_date', '').strip().strip("\"'“”")

        start_date = parse_date(start_date_raw) if start_date_raw else None
        end_date = parse_date(end_date_raw) if end_date_raw else None

        if not name:
            messages.error(request, 'Tournament name is required.')
            return render(request, 'core/tournament_form.html')

        if start_date_raw and not start_date:
            messages.error(request, 'Invalid start date. Please select a valid date.')
            return render(request, 'core/tournament_form.html')

        if end_date_raw and not end_date:
            messages.error(request, 'Invalid end date. Please select a valid date.')
            return render(request, 'core/tournament_form.html')

        Tournament.objects.create(
            name=name,
            venue=venue,
            start_date=start_date,
            end_date=end_date
        )

        messages.success(request, 'Tournament created successfully!')
        return redirect('tournaments')

    return render(request, 'core/tournament_form.html')
def tournament_delete(request,pk):
    if request.method=='POST': get_object_or_404(Tournament,pk=pk).delete(); messages.success(request,'Tournament deleted.')
    return redirect('tournaments')

def compare(request):
    p1=get_object_or_404(Player,pk=request.GET.get('p1')) if request.GET.get('p1','').isdigit() else None
    p2=get_object_or_404(Player,pk=request.GET.get('p2')) if request.GET.get('p2','').isdigit() else None
    metrics=[('Matches','matches'),('Runs','runs'),('Batting average','batting_average'),('Strike rate','strike_rate'),('Wickets','wickets'),('Economy','economy'),('Fitness','fitness'),('Recent form','recent_form')]
    return render(request,'core/compare.html',{'players':Player.objects.all(),'p1':p1,'p2':p2,'metrics':metrics})

def score(player):
    # Simple normalized 0-100 score: batting and bowling are blended according to role.
    bat=min(player.batting_average/60*100,100)*.30 + min(player.strike_rate/180*100,100)*.25 + player.recent_form*.20 + player.fitness*.15
    bowl=min(player.wickets/25*100,100)*.25 + (max(0,100-player.economy*10) if player.economy else 0)*.20 + player.fitness*.15
    if player.role=='Bowler': return min(100,bowl + min(player.recent_form,100)*.20 + min(player.batting_average/50*100,100)*.20)
    if player.role=='All-rounder': return min(100,bat*.55+bowl*.45)
    if player.role=='Wicketkeeper': return min(100,bat+player.fitness*.10)
    return min(100,bat+player.fitness*.10)
def playing_xi(request):
    pool=list(Player.objects.all())
    wicketkeepers=sorted([p for p in pool if p.role=='Wicketkeeper'],key=score,reverse=True)
    batters=sorted([p for p in pool if p.role=='Batter'],key=score,reverse=True)
    allrounders=sorted([p for p in pool if p.role=='All-rounder'],key=score,reverse=True)
    bowlers=sorted([p for p in pool if p.role=='Bowler'],key=score,reverse=True)
    selected=[]
    def add_from(items,limit):
        for p in items:
            if p not in selected and len(selected)<11 and limit>0: selected.append(p); limit-=1
    add_from(wicketkeepers,1); add_from(batters,4); add_from(allrounders,2); add_from(bowlers,3)
    remaining=sorted([p for p in pool if p not in selected],key=score,reverse=True)
    add_from(remaining,11-len(selected))
    selected=sorted(selected,key=score,reverse=True)
    return render(request,'core/playing_xi.html',{'selected':selected,'team_score':round(sum(score(p) for p in selected)/len(selected),1) if selected else 0,'roles':{'Wicketkeepers':sum(p.role=='Wicketkeeper' for p in selected),'Batters':sum(p.role=='Batter' for p in selected),'All-rounders':sum(p.role=='All-rounder' for p in selected),'Bowlers':sum(p.role=='Bowler' for p in selected)}})
