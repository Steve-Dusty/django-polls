from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True)
    choice_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
