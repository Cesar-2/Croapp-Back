from django.db import models


class LandingPage(models.Model):
    name = models.CharField("Name", max_length=255)
    last_name = models.CharField("Last Name", max_length=255)
    email = models.EmailField("email", max_length=255)
    content = models.CharField("Content", max_length=1000)

    class Meta:
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'

    def __str__(self):
        return self.email
