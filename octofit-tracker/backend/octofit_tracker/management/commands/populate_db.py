from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data (delete individually to avoid unhashable error)
        for model in [Leaderboard, Activity, Workout, User, Team]:
            for obj in model.objects.all():
                if getattr(obj, 'id', None):
                    obj.delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Team')
        dc = Team.objects.create(name='DC', description='DC Team')

        # Create Users
        ironman = User.objects.create(email='ironman@marvel.com', username='Iron Man', team=marvel)
        spiderman = User.objects.create(email='spiderman@marvel.com', username='Spider-Man', team=marvel)
        batman = User.objects.create(email='batman@dc.com', username='Batman', team=dc)
        superman = User.objects.create(email='superman@dc.com', username='Superman', team=dc)

        # Create Activities
        Activity.objects.create(user=ironman, type='run', duration=30, date=timezone.now().date())
        Activity.objects.create(user=spiderman, type='cycle', duration=45, date=timezone.now().date())
        Activity.objects.create(user=batman, type='swim', duration=25, date=timezone.now().date())
        Activity.objects.create(user=superman, type='run', duration=60, date=timezone.now().date())

        # Create Workouts
        w1 = Workout.objects.create(name='Pushups', description='Upper body')
        w2 = Workout.objects.create(name='Squats', description='Lower body')
        w1.suggested_for.set([ironman, batman])
        w2.suggested_for.set([spiderman, superman])

        # Create Leaderboard
        Leaderboard.objects.create(user=ironman, score=100, rank=1)
        Leaderboard.objects.create(user=spiderman, score=90, rank=2)
        Leaderboard.objects.create(user=batman, score=80, rank=3)
        Leaderboard.objects.create(user=superman, score=70, rank=4)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
