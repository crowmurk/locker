from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.validators import validate_slug

# Create your models here.

class Client(models.Model):
    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name=_('Name'),
    )
    slug = models.SlugField(
        max_length=120,
        editable=False,
        validators=[
            validate_slug,
        ],
        help_text=_('A label for URL config.'),
    )
    details = models.TextField(
        blank=False,
        verbose_name=_('Details'),
        help_text=_('Details regarding the client'),
    )

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['name', ]

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

    def _get_number_of_orders(self):
        return len(self.order_set.filter(client__id=self.id))

    number_of_orders = property(_get_number_of_orders)

    def get_absolute_url(self):
        return reverse(
            'client:detail',
            kwargs={'slug': self.slug},
        )

    def get_update_url(self):
        return reverse(
            'client:update',
            kwargs={'slug': self.slug},
        )

    def get_delete_url(self):
        return reverse(
            'client:delete',
            kwargs={'slug': self.slug},
        )
