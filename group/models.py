from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Lessons(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    date = models.DateField()
    date_changed = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.group} - {self.date}"