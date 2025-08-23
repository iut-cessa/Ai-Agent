from django.db import models
from account.models import User

class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    topic = models.ForeignKey(Topic, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    topic = models.ForeignKey(Topic, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    attachment = models.FileField(upload_to='tasks/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='created_tasks', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Submission(models.Model):
    task = models.ForeignKey(Task, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(blank=True, null=True)  

    def __str__(self):
        return f"{self.user.username} - {self.task.title}"