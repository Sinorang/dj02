from django.db import models
from acc.models import User
from django.utils import timezone

# Create your models here.
class Center(models.Model):
    subject = models.CharField(max_length=100)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    content = models.TextField()
    pubdate = models.DateTimeField(default=timezone.now) # timezone.now : 현재 시간을 알려주는 함수 # DateTimeField() : 시간을 저장할 수 있는 필드

    def __str__(self):
        return self.subject

class Response(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    counselor = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.center}_{self.counselor} 님의 댓글"