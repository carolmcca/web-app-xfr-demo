# Generated by Django 5.0.4 on 2024-04-25 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_image_is_feature_example_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='is_feature_example',
        ),
        migrations.RemoveField(
            model_name='image',
            name='is_identification_example',
        ),
        migrations.RemoveField(
            model_name='image',
            name='is_verification_example',
        ),
        migrations.AddField(
            model_name='image',
            name='is_example',
            field=models.BooleanField(default=False),
        ),
    ]
