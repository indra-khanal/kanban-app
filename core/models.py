from django.db import models
from django.conf import settings


class KanBanBoard(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="board_user")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-id"]
        
    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=50)
    board = models.ForeignKey(KanBanBoard, on_delete=models.CASCADE, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name


class Lane(models.Model):
    name = models.CharField(max_length=50)
    board = models.ForeignKey(KanBanBoard, on_delete=models.CASCADE, related_name="lane_board")
    display_order  = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ["display_order"]
        
    def __str__(self):
        return f"{self.board.name}-->{self.name}"


class Card(models.Model):
    title = models.CharField(max_length=50)
    description  = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    card_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE, related_name="card_lane")
    display_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.lane.board.name} --> {self.title}"
    
    
class Comment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="card_comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="card_comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]