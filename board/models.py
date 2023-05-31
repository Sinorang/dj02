from django.db import models
from acc.models import User
from django.utils import timezone

# Create your models here.
class Board(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    content = models.TextField()
    pubdate = models.DateTimeField(default=timezone.now) # timezone.now : 현재 시간을 알려주는 함수 # DateTimeField() : 시간을 저장할 수 있는 필드
    likey = models.ManyToManyField(User, blank=True, related_name="likey") # N:N 관계, 나중에 다룰 예정

    def __str__(self):
        return self.subject

class Reply(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    replyer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.board}_{self.replyer} 님의 댓글"