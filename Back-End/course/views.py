from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, generics
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .models import Submission, Topic, Video, Task
from .serializers import SubmissionSerializer, TaskSerializer, TopicSerializer, TopicWithTasksSerializer, TopicWithVideosSerializer, VideoSerializer

class TopicAdminViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAdminUser]  

class TopicWithVideosView(generics.RetrieveAPIView):
    queryset = Topic.objects.prefetch_related("videos").all()
    serializer_class = TopicWithVideosSerializer
    permission_classes = [IsAuthenticated] 

class TopicWithTasksView(generics.RetrieveAPIView):
    queryset = Topic.objects.prefetch_related("tasks").all()
    serializer_class = TopicWithTasksSerializer
    permission_classes = [IsAuthenticated]

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAdminOrReadOnly]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)  

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
