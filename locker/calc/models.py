from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.db.models.expressions import Subquery, OuterRef
from django.db.models.functions import Coalesce

from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from core.validators import validate_positive

from client.models import Client, Branch

# Create your models here.

class Service(models.Model):
    equipment = models.CharField(
        null=False,
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
        null=False,
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
    rating = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name=_('Rating'),
    )
    price = models.DecimalField(
        null=False,
        blank=False,
        max_digits=9,
        decimal_places=2,
        editable=False,
        default=0,
        verbose_name=_('Total price'),
    )

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['equipment', 'work']
        unique_together = (('equipment', 'work'),)

    def __str__(self):
        return _("{equipment} ({work}): Price: {price}").format(
            equipment=self.equipment,
            work=self.work,
            price=self.price,
        )

    def save(self, *args, **kwargs):
        self.price = self.equipment_price + self.work_price
        super().save(*args, **kwargs)

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


class OrderManager(models.Manager):
    def get_queryset(self):
        price = Subquery(
            OrderOption.objects.filter(
                order=OuterRef('pk'),
            ).values('order').order_by('order').annotate(
                sum=Coalesce(Sum('price'), 0)
            ).values('sum'),
        )

        return super().get_queryset().select_related(
            'author', 'client', 'branch',
        ).prefetch_related(
            'options',
        ).annotate(price=Coalesce(price, 0))


class Order(models.Model):
    author = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Author'),
    )
    client = models.ForeignKey(
        Client,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Client'),
    )
    branch = models.ForeignKey(
        Branch,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Branch'),
    )
    services = models.ManyToManyField(
        Service,
        related_name='orders',
        through='OrderOption',
        through_fields=('order', 'service'),
        verbose_name=_('Options'),
    )
    created = models.DateField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )
    modified = models.DateField(
        auto_now=True,
        verbose_name=_('Modified'),
    )
    factor = models.FloatField(
        null=False,
        blank=False,
        default=1,
        validators=[
            validate_positive,
        ],
        verbose_name=_('Factor'),
    )

    objects = OrderManager()

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['author', 'client']

    def __str__(self):
        return _("{id}: {client} ({branch}, {address}) [{price}]").format(
            id=self.pk,
            client=self.client.name,
            branch=self.branch.name,
            address=self.branch.address,
            price=self.price,
        )

    @property
    def price(self):
        return sum([item.price for item in self.get_options()])

    @price.setter
    def price(self, value):
        pass

    def get_options(self):
        return self.options.all()

    def get_absolute_url(self):
        return reverse(
            'calc:order:detail',
            kwargs={'pk': self.pk},
        )

    def get_pdf_url(self):
        return reverse(
            'calc:order:detail_pdf',
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


class OrderOptionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'order', 'service',
        )


class OrderOption(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='options',
        verbose_name=_('Order'),
    )
    service = models.ForeignKey(
        Service,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='options',
        verbose_name=_('Option'),
    )
    service_price = models.DecimalField(
        null=False,
        blank=False,
        max_digits=9,
        decimal_places=2,
        editable=False,
        default=0,
        verbose_name=_('Option price'),
    )
    quantity = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=1,
        verbose_name=_('Quantity'),
    )
    price = models.DecimalField(
        null=False,
        blank=False,
        max_digits=9,
        decimal_places=2,
        editable=False,
        default=0,
        verbose_name=_('Total price'),
    )

    objects = OrderOptionManager()

    class Meta:
        verbose_name = _('Order option')
        verbose_name_plural = _('Orders options')
        unique_together = (('order', 'service'),)

    def __str__(self):
        return _("Order: {order} Option: {service}"
                 " Quantity: {quantity} Total price: {price}").format(
                     order=self.order.pk,
                     service=self.service.equipment,
                     quantity=self.quantity,
                     price=self.price,
        )

    def save(self, *args, **kwargs):
        self.service_price = self.service.equipment_price + self.service.work_price * Decimal(self.order.factor)
        self.price = self.service_price * self.quantity
        self.price.quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

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
