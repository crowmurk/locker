from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from client.models import Client

# Create your models here.

class Order(models.Model):
    author = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Author'),
    )
    client = models.ForeignKey(
        Client,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Client'),
    )
    created = models.DateField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )
    modified = models.DateField(
        auto_now=True,
        verbose_name=_('Modified'),
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['author', 'client']

    def __str__(self):
        return _("Order {id}: Author: {author}"
                 " Client: {client} Price: {price}").format(
            id=self.pk,
            author=self.author.get_full_name(),
            client=self.client,
            price=self.price
        )

    def _get_price(self):
        return sum([item.price for item in self.get_options()])

    price = property(_get_price)

    def get_options(self):
        return self.options.all()

    def get_absolute_url(self):
        return reverse(
            'calc:order:detail',
            kwargs={'pk': self.pk},
        )

    def get_pdf_url(self):
        return reverse(
            'calc:order:pdf',
            kwargs={'pk': self.pk},
        )

    def get_update_url(self):
        return reverse(
            'calc:order:update',
            kwargs={'pk': self.pk},
        )

    def get_delete_url(self):
        return reverse(
            'calc:order:delete',
            kwargs={'pk': self.pk},
        )


class Service(models.Model):
    equipment = models.CharField(
        blank=False,
        max_length=250,
        verbose_name=_('Equipment'),
    )
    equipment_price = models.DecimalField(
        null=False,
        blank=False,
        max_digits=9,
        decimal_places=2,
        verbose_name=_('Equipment price'),
    )
    work = models.CharField(
        blank=False,
        max_length=250,
        verbose_name=_('Work'),
    )
    work_price = models.DecimalField(
        null=False,
        blank=False,
        max_digits=9,
        decimal_places=2,
        verbose_name=_('Work price'),
    )

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['equipment', 'work']
        unique_together = (('equipment', 'work'),)

    def __str__(self):
        return _("Equipment: {equipment} Price: {price}").format(
            equipment=self.equipment,
            price=self.price,
        )

    def _get_price(self):
        return self.equipment_price + self.work_price

    price = property(_get_price)

    def get_absolute_url(self):
        return reverse(
            'calc:service:detail',
            kwargs={'pk': self.pk},
        )

    def get_update_url(self):
        return reverse(
            'calc:service:update',
            kwargs={'pk': self.pk},
        )

    def get_delete_url(self):
        return reverse(
            'calc:service:delete',
            kwargs={'pk': self.pk},
        )


class OrderOption(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_('Order'),
    )
    service = models.ForeignKey(
        Service,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_('Service'),
    )
    quantity = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name=_('Quantity'),
    )

    class Meta:
        verbose_name = _('Order option')
        verbose_name_plural = _('Orders options')
        unique_together = (('order', 'service'),)

    def __str__(self):
        return _("Order {order} option: {option} Quantity: {quantity} Total: {total}").format(
            order=self.order.pk,
            option=self.service,
            quantity=self.quantity,
            total=self.price,
        )

    def _get_price(self):
        return self.service.price * self.quantity

    price = property(_get_price)

    def get_absolute_url(self):
        return reverse(
            'calc:orderoption:detail',
            kwargs={'pk': self.pk},
        )

    def get_update_url(self):
        return reverse(
            'calc:orderoption:update',
            kwargs={'pk': self.pk},
        )

    def get_delete_url(self):
        return reverse(
            'calc:orderoption:delete',
            kwargs={'pk': self.pk},
        )
