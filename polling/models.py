from django.db import models

# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    ending_date = models.DateTimeField('date ending', null=True, blank=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
