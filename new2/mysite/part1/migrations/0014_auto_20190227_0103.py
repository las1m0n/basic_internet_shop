# Generated by Django 2.1.7 on 2019-02-26 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('part1', '0013_auto_20190226_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='shared',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='shared',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='shared_with_me',
        ),
        migrations.DeleteModel(
            name='Shared',
        ),
        migrations.AddField(
            model_name='relation',
            name='product',
            field=models.ForeignKey(on_delete=True, to='part1.Product'),
        ),
        migrations.AddField(
            model_name='relation',
            name='relationss',
            field=models.ManyToManyField(blank=True, related_name='relator', to='part1.Product'),
        ),
    ]
