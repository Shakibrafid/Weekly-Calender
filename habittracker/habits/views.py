from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer
from .permissions import IsOwner
from rest_framework.decorators import action
from rest_framework.response import Response
from .utils import calculate_streaks


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'], url_path='streaks')
    def streaks(self, request, pk=None):
        habit = self.get_object()

        dates = list(
            habit.logs.filter(completed=True).values_list('date', flat=True)
        )

        return Response(calculate_streaks(dates))

class HabitLogViewSet(viewsets.ModelViewSet):
    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitLog.objects.filter(habit__user=self.request.user)
        
