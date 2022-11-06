from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

# Create your models here.
class Chain(models.Model):
    TYPES_CHOISE_FIELD = (
        ('0', 'Factory'),
        ('1', 'Distributor'),
        ('2', 'Dealership'),
        ('3', 'Large retail chain'),
        ('4', 'Individual entrepreneur'),
    )

    name = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    debt = models.DecimalField(max_digits=50, decimal_places=2)
    date = models.DateField(verbose_name = 'creation date', auto_now_add=True)
    supplier = models.ForeignKey('Chain', on_delete = models.RESTRICT, blank=True, null=True)

    type = models.CharField(max_length=1, choices = TYPES_CHOISE_FIELD)
    level = models.SmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.clean()
        if self.supplier is not None:
            supplie_obj = Chain.objects.get(pk = self.supplier_id)
            self.level = supplie_obj.level + 1

        if self.level > 4:
            raise ValidationError(' validation error: level is too hight to this network ')
        else:
            return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Contact(models.Model):
    email = models.EmailField(blank=False)
    country = models.CharField(max_length=20, blank=False)
    city = models.CharField(max_length=30, blank=False)
    street = models.CharField(max_length=50, blank=False)
    house = models.CharField(max_length=10, blank=False)
    chain_fk = models.ForeignKey(Chain, on_delete=models.CASCADE, )

    def __str__(self):
        return str(self.email)


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False)
    model = models.CharField(max_length=60, blank=False)
    chain = models.ForeignKey(Chain, on_delete = models.CASCADE)
    date = models.DateField(verbose_name = 'relise date', auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.name)
