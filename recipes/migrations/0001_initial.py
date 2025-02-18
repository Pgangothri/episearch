# Generated by Django 5.1.1 on 2024-10-01 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('ingredients', models.TextField()),
                ('directions', models.TextField()),
                ('rating', models.FloatField(blank=True, null=True)),
                ('calories', models.IntegerField(blank=True, null=True)),
                ('protein', models.FloatField(blank=True, null=True)),
                ('fat', models.FloatField(blank=True, null=True)),
                ('sodium', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
