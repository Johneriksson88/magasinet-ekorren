# Generated by Django 3.2.16 on 2023-01-26 02:13

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
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
                ('person_or_org_nr', models.CharField(max_length=100)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='StorageUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Small 1st floor', 'Small 1st floor'), ('Medium 1st floor', 'Medium 1st floor'), ('Large 1st floor', 'Large 1st floor'), ('Small 2nd floor', 'Small 2nd floor'), ('Medium 2nd floor', 'Medium 2nd floor'), ('Large 2nd floor', 'Large 2nd floor'), ('X-Large 2nd floor', 'X-Large 2nd floor')], max_length=100)),
                ('size', models.CharField(choices=[('5 m2', '5 m2'), ('6 m2', '6 m2'), ('10 m2', '10 m2'), ('12 m2', '12 m2')], max_length=100)),
                ('floor', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=100)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_now=True)),
                ('start_date', models.DateField()),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
                ('storage_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.storageunit')),
            ],
            options={
                'ordering': ['-order_date'],
            },
        ),
    ]