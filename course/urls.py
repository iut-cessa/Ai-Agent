from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubmissionViewSet, TaskViewSet, TopicAdminViewSet, TopicWithTasksView, TopicWithVideosView, VideoViewSet

router = DefaultRouter()
router.register('videos', VideoViewSet)
router.register('tasks', TaskViewSet)
router.register('submit', SubmissionViewSet)
router.register('topics', TopicAdminViewSet, basename='topics')

urlpatterns = [
    path('', include(router.urls)),

    path('topics/<int:pk>/videos/', TopicWithVideosView.as_view(), name='topic-videos'),
    path('topics/<int:pk>/tasks/', TopicWithTasksView.as_view(), name='topic-tasks'),
]