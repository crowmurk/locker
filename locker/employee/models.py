from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    middle_name = models.CharField(
        max_length=100,
        verbose_name=_('Middle name'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return "{name}".format(
            name=self.user.get_full_name(),
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
