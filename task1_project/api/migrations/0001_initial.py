# Generated by Django 4.1.3 on 2022-11-04 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('debt', models.DecimalField(decimal_places=2, max_digits=50)),
                ('date', models.DateField(auto_now_add=True, verbose_name='creation date')),
                ('type', models.CharField(choices=[('0', 'Factory'), ('1', 'Distributor'), ('2', 'Dealership'), ('3', 'Large retail chain'), ('4', 'Individual entrepreneur')], max_length=1)),
                ('level', models.SmallIntegerField(default=0)),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='api.chain')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=60)),
                ('date', models.DateField(auto_now=True, verbose_name='relise date')),
                ('chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chain')),
            ],
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('contry', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=30)),
                ('street', models.CharField(max_length=50)),
                ('house', models.CharField(max_length=10)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chain')),
            ],
        ),
    ]
