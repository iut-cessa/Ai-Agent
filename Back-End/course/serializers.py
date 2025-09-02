from rest_framework import serializers
from .models import Submission, Topic, Video, Task

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['creator', 'created_at']

class TopicSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'videos', 'tasks']

class TopicWithVideosSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'videos']


class TopicWithTasksSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'tasks']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['user', 'submitted_at']

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        request = self.context.get('request')

        if request:
            if request.method == "POST":
                extra_kwargs['grade'] = {'read_only': True}
            elif request.method in ["PUT", "PATCH"]:
                if not request.user.is_staff:
                    extra_kwargs['grade'] = {'read_only': True}

        return extra_kwargs