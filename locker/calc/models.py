from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from core.validators import validate_positive

from client.models import Client, Branch

# Create your models here.

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
    rating = models.PositiveIntegerField(
        blank=False,
        null=False,
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
        verbose_name=_('Total'),
    )

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['equipment', 'work']
        unique_together = (('equipment', 'work'),)

    def __str__(self):
        return _("{equipment} Work: {work} Price: {price}").format(
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
        equipment_price = models.F('options__service__equipment_price')
        work_price = models.F('options__service__work_price')
        factor = models.F('options__order__factor')
        quantity = models.F('options__quantity')

        price = models.ExpressionWrapper(
            (equipment_price + work_price * factor) * quantity,
            output_field=models.DecimalField(
                max_digits=9,
                decimal_places=2,
            ),
        )
        return super().get_queryset().select_related(
            'author', 'client', 'branch',
        ).prefetch_related(
            'options',
        ).annotate(price=models.Sum(price))


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
    branch = models.ForeignKey(
        Branch,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Branch'),
    )
    services = models.ManyToManyField(
        Service,
        related_name='orders',
        through='OrderOption',
        through_fields=('order', 'service'),
        verbose_name=_('Services'),
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
        return _("Order {id}: {client} ({branch}: {address})").format(
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
        equipment_price = models.F('service__equipment_price')
        work_price = models.F('service__work_price')
        factor = models.F('order__factor')
        quantity = models.F('quantity')

        price = models.ExpressionWrapper(
            (equipment_price + work_price * factor) * quantity,
            output_field=models.DecimalField(
                max_digits=9,
                decimal_places=2,
            ),
        )
        return super().get_queryset().select_related(
            'order', 'service',
        ).annotate(price=price)


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
        default=1,
        verbose_name=_('Quantity'),
    )

    objects = OrderOptionManager()

    class Meta:
        verbose_name = _('Order option')
        verbose_name_plural = _('Orders options')
        unique_together = (('order', 'service'),)

    def __str__(self):
        return _("Order: {order} Option: {service}"
                 " Quantity: {quantity} Sum: {price}").format(
                     order=self.order.pk,
                     service=self.service.equipment,
                     quantity=self.quantity,
                     price=self.price,
        )

    @property
    def price(self):
        factor = Decimal(self.order.factor)
        result = (self.service.equipment_price + self.service.work_price * factor) * self.quantity
        return result.quantize(Decimal('0.01'))

    @price.setter
    def price(self, value):
        pass

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
