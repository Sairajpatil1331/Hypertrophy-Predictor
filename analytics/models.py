from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class UserMetrics(models.Model):
    """Tracks baseline physical metrics and macro targets."""
    GOAL_CHOICES = [
        ('BULK', 'Caloric Surplus / Hypertrophy'),
        ('CUT', 'Caloric Deficit / Fat Loss'),
        ('MAINTAIN', 'Maintenance'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='metrics')
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    fitness_goal = models.CharField(max_length=10, choices=GOAL_CHOICES, default='BULK')
    
    target_protein = models.PositiveIntegerField(help_text="grams")
    target_carbs = models.PositiveIntegerField(help_text="grams")
    target_fats = models.PositiveIntegerField(help_text="grams")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.fitness_goal}"

class DailyLog(models.Model):
    """Unified timeline logging daily intake and recovery metrics."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField()
    
    protein_consumed = models.PositiveIntegerField(default=0)
    carbs_consumed = models.PositiveIntegerField(default=0)
    fats_consumed = models.PositiveIntegerField(default=0)
    calories_consumed = models.PositiveIntegerField(default=0)
    
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0.0)])
    soreness_level = models.PositiveSmallIntegerField(
        help_text="Scale 1-5: 1 being fresh, 5 being severely fatigued",
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} | {self.date}"

class Exercise(models.Model):
    """Global index of exercises to standardize training data analysis."""
    name = models.CharField(max_length=100, unique=True)
    target_muscle_group = models.CharField(max_length=50, help_text="e.g., Chest, Back, Quads")

    def __str__(self):
        return self.name

class WorkoutLog(models.Model):
    """Logs the overall context of a single training session."""
    SPLIT_CHOICES = [
        ('PUSH', 'Push'),
        ('PULL', 'Pull'),
        ('LEGS', 'Legs'),
        ('ARNOLD_CHEST_BACK', 'Arnold Split - Chest & Back'),
        ('ARNOLD_ARM_SHOULDER', 'Arnold Split - Arms & Shoulders'),
        ('ARNOLD_LEGS', 'Arnold Split - Legs'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField()
    split_name = models.CharField(max_length=25, choices=SPLIT_CHOICES)
    duration_minutes = models.PositiveIntegerField(default=0)
    session_rpe = models.PositiveSmallIntegerField(
        help_text="Rate of Perceived Exertion (1-10) for the whole session",
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.date} | {self.split_name}"

class PerformanceSet(models.Model):
    """Granular data point for every single set performed."""
    workout = models.ForeignKey(WorkoutLog, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    set_number = models.PositiveSmallIntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight lifted in kg")
    reps = models.PositiveSmallIntegerField()
    rpe = models.PositiveSmallIntegerField(
        help_text="RPE (1-10) for this specific set",
        blank=True, null=True
    )

    class Meta:
        ordering = ['workout', 'exercise', 'set_number']

    @property
    def volume_load(self):
        return float(self.weight) * self.reps