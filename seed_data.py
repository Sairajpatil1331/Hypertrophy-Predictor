import os
import django
import random
from datetime import timedelta, date

# 1. Boot up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_core.settings')
django.setup()

from django.contrib.auth.models import User
from analytics.models import Exercise, WorkoutLog, PerformanceSet

def generate_mock_data():
    # Grab the superuser you already created
    user = User.objects.first()
    if not user:
        print("No user found. Please run createsuperuser first.")
        return

    # Ensure we have a couple of exercises to work with
    bench, _ = Exercise.objects.get_or_create(name='Bench Press', defaults={'target_muscle_group': 'Chest'})
    squat, _ = Exercise.objects.get_or_create(name='Barbell Squat', defaults={'target_muscle_group': 'Legs'})

    splits = ['PUSH', 'LEGS', 'ARNOLD_CHEST_BACK', 'ARNOLD_LEGS']
    
    print("Generating 30 days of mock workouts...")
    
    # Generate 15 workouts (roughly every other day)
    for i in range(15):
        workout_date = date.today() - timedelta(days=i * 2)
        split = random.choice(splits)
        
        # 1. Create the Workout Log
        workout = WorkoutLog.objects.create(
            user=user,
            date=workout_date,
            split_name=split,
            duration_minutes=random.randint(45, 90),
            session_rpe=random.randint(6, 9)
        )

        # 2. Add 3 sets to each workout
        current_exercise = bench if 'PUSH' in split or 'CHEST' in split else squat
        
        # Base weight fluctuates slightly to mimic real life
        base_weight = random.randint(50, 85) 
        
        for set_num in range(1, 4):
            PerformanceSet.objects.create(
                workout=workout,
                exercise=current_exercise,
                set_number=set_num,
                weight=base_weight,
                reps=random.randint(5, 12),
                rpe=random.randint(7, 10)
            )
            
    print("Successfully injected 45 Performance Sets into MySQL!")

if __name__ == "__main__":
    generate_mock_data()