# Generated by Django 2.1.7 on 2019-02-26 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('part1', '0014_auto_20190227_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='relationss',
            field=models.ManyToManyField(related_name='relator', to='part1.Product'),
        ),
    ]