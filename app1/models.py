from django.db import models
from django.contrib.auth.models import User

class ChessBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=10)
    piece_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.piece_type} at {self.position}"
