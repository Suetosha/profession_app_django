from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to='images/', null=False)

    objects = models.Manager()

    def __repr__(self):
        return f'Image({self.title}, {self.image})'

    def __str__(self):
        return self.title


class JSON(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    data = models.TextField(blank=False, null=False)

    objects = models.Manager()

    def __repr__(self):
        return f'JSON({self.title})'

    def __str__(self):
        return self.title
