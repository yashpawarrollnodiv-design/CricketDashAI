from django.core.management.base import BaseCommand
from core.models import Team, Player, Tournament
class Command(BaseCommand):
    help='Add sample demo cricket teams, players and a tournament.'
    def handle(self,*args,**options):
        sample_teams=[('Mumbai Meteors','A. Coach','R. Captain','Mumbai'),('Delhi Falcons','B. Coach','S. Captain','Delhi'),('Chennai Kingsmen','C. Coach','V. Captain','Chennai')]
        teams={}
        for name,coach,captain,city in sample_teams:
            teams[name],_=Team.objects.get_or_create(name=name,defaults={'coach':coach,'captain':captain,'city':city})
        Tournament.objects.get_or_create(name='Demo T20 Cup',defaults={'venue':'City Cricket Ground','status':'Ongoing'})
        sample=[
         ('Arjun Mehta','Batter',teams['Mumbai Meteors'],28,745,54.2,151.4,0,0,92,88),('Kabir Shah','Wicketkeeper',teams['Mumbai Meteors'],25,420,35.0,138.5,0,0,90,80),('Dev Patel','All-rounder',teams['Mumbai Meteors'],26,330,29.1,132.0,15,7.8,87,84),('Rohan Iyer','Bowler',teams['Mumbai Meteors'],24,45,12.0,95.0,23,7.1,93,89),('Aman Gill','Batter',teams['Delhi Falcons'],27,610,46.9,144.0,1,8.5,84,86),('Vikram Rao','Bowler',teams['Delhi Falcons'],29,72,18.0,102.0,19,6.9,88,82),('Neel Joshi','All-rounder',teams['Delhi Falcons'],23,255,25.5,126.0,12,8.0,90,91),('Sameer Khan','Wicketkeeper',teams['Chennai Kingsmen'],30,390,30.0,136.0,0,0,85,83),('Jay Nair','Batter',teams['Chennai Kingsmen'],22,530,44.1,149.0,0,0,89,90),('Harsh Singh','Bowler',teams['Chennai Kingsmen'],25,28,9.0,85.0,26,7.2,86,88),('Pranav Das','All-rounder',teams['Chennai Kingsmen'],27,290,27.0,130.0,14,7.6,91,85),('Zaid Ahmed','Bowler',teams['Mumbai Meteors'],26,90,15.0,108.0,18,7.4,83,79),('Yash Verma','Batter',teams['Delhi Falcons'],24,480,40.0,142.0,0,0,91,82)]
        for name,role,team,matches,runs,avg,sr,wickets,econ,fitness,form in sample:
            Player.objects.get_or_create(name=name,defaults={'role':role,'team':team,'age':24,'matches':matches,'runs':runs,'batting_average':avg,'strike_rate':sr,'wickets':wickets,'economy':econ,'fitness':fitness,'recent_form':form})
        self.stdout.write(self.style.SUCCESS('Demo records added.'))
