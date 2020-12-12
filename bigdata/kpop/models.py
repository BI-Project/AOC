from django.db import models

class News(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Article(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Result(models.Model):
    pass
