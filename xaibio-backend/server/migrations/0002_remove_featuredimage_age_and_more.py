# Generated by Django 5.0.4 on 2024-04-05 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featuredimage',
            name='age',
        ),
        migrations.RemoveField(
            model_name='featuredimage',
            name='ethnicity',
        ),
        migrations.RemoveField(
            model_name='featuredimage',
            name='nose',
        ),
        migrations.RemoveField(
            model_name='featuredimage',
            name='skin_tone',
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='african',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='asian',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='big_lips',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='big_nose',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='black_hair',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='blonde_hair',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='caucasian',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='curly_hair',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='middle_aged',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='young',
            field=models.IntegerField(null=True),
        ),
    ]
