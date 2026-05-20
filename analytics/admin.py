from django.contrib import admin
from .models import UserMetrics, DailyLog, Exercise, WorkoutLog, PerformanceSet


admin.site.register(UserMetrics)
admin.site.register(DailyLog)
admin.site.register(Exercise)
admin.site.register(WorkoutLog)
admin.site.register(PerformanceSet)