from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#89b4fa')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} — {self.name}'

class HabitLog(models.Model):
       habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
       date = models.DateField()
       completed = models.BooleanField(default = True)

       class Meta:
            unique_together = ('habit', 'date')

       def __str__(self):
           return f'{self.habit.name} on {self.date}'     

    