from rest_framework import generics, permissions

from .permissions import IsOwner
from .models import Task
from .serializers import TaskCreateSerializer, TaskUpdateSerializer, TaskDetailSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskDetailSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaskUpdateSerializer
        return TaskDetailSerializer
        
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

