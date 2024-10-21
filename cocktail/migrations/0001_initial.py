# Generated by Django 5.1.1 on 2024-10-16 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cocktail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('base_liquor', models.CharField(max_length=100)),
                ('ingredients', models.JSONField()),
                ('garnish', models.CharField(blank=True, max_length=100)),
                ('alcohol_strength', models.CharField(max_length=50)),
                ('glass', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('technique', models.CharField(max_length=100)),
                ('recipe_tip', models.TextField(blank=True)),
            ],
        ),
    ]
