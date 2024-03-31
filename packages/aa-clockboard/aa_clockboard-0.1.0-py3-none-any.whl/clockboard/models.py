from django.db import models
from django.utils import timezone
from django.conf import settings


class General(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('can_see_clocks', "Can see clocks"),
            ('can_add_clocks', "Can add clocks"),
        )


class Clock(models.Model):
    name = models.CharField(max_length=255, unique=True)
    last_reset = models.DateTimeField(default=timezone.now)
    last_reset_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='+')
    is_active = models.BooleanField(default=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name


class ClockLog(models.Model):
    clock = models.ForeignKey(Clock, on_delete=models.CASCADE, related_name='history')
    reset_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='+')
    timestamp = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)
    num_involved = models.IntegerField()

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f"{self.clock} - {self.timestamp}"
