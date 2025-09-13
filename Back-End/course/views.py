from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import viewsets, generics
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminForSubmission
from .models import Submission, Topic, Video, Task
from .serializers import SubmissionSerializer, TaskSerializer, TopicSerializer, TopicWithTasksSerializer, TopicWithVideosSerializer, VideoSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        
        return [permission() for permission in permission_classes]   

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
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminForSubmission]

    def get_queryset(self):
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Submission.objects.none()
        
        user = self.request.user
        if user.is_staff:  
            return Submission.objects.all()
        return Submission.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)