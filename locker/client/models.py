from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_unicode_slug

from core.validators import validate_slug
from core.utils import get_unique_slug

# Create your models here.

class ClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'branches', 'orders',
        ).annotate(
            number_of_orders=models.Count('orders', distinct=True),
        ).annotate(
            number_of_branches=models.Count('branches', distinct=True)
        )


class Client(models.Model):
    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name=_('Name'),
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        editable=False,
        allow_unicode=True,
        validators=[
            validate_unicode_slug,
            validate_slug,
        ],
        help_text=_('A label for URL config.'),
    )
    details = models.TextField(
        null=False,
        blank=False,
        verbose_name=_('Details'),
        help_text=_('Details regarding the client'),
    )

    objects = ClientManager()

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['name', ]

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, 'slug', 'name', unique=True)
        super(Client, self).save(*args, **kwargs)

    @property
    def number_of_branches(self):
        return self.branches.count()

    @number_of_branches.setter
    def number_of_branches(self, value):
        pass

    @property
    def number_of_orders(self):
        return self.orders.count()

    @number_of_orders.setter
    def number_of_orders(self, value):
        pass

    def get_orders(self):
        return self.orders.all()

    def get_branches(self):
        return self.branches.all()

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


class BranchManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'client',
        ).prefetch_related(
            'orders',
        ).annotate(
            number_of_orders=models.Count('orders'),
        )


class Branch(models.Model):
    client = models.ForeignKey(
        Client,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='branches',
        verbose_name=_('Client'),
    )
    name = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        verbose_name=_('Name'),
    )
    address = models.TextField(
        null=False,
        blank=False,
        verbose_name=_('Address'),
    )

    objects = BranchManager()

    class Meta:
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')
        ordering = ['client', 'name']
        unique_together = (('client', 'name', 'address'),)

    def __str__(self):
        return "{name}: {address} ({client})".format(
            name=self.name,
            address=self.address,
            client=self.client.name,
        )

    @property
    def number_of_orders(self):
        return self.orders.count()

    @number_of_orders.setter
    def number_of_orders(self, value):
        pass

    def get_orders(self):
        return self.orders.all()

    def get_absolute_url(self):
        return reverse(
            'client:branch:detail',
            kwargs={
                'pk': self.pk,
                'client_slug': self.client.slug,
            },
        )

    def get_update_url(self):
        return reverse(
            'client:branch:update',
            kwargs={
                'pk': self.pk,
                'client_slug': self.client.slug,
            },
        )

    def get_delete_url(self):
        return reverse(
            'client:branch:delete',
            kwargs={
                'pk': self.pk,
                'client_slug': self.client.slug,
            },
        )
