# Generated by Django 5.0.4 on 2024-05-02 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_rename_id_image_img_id_image_user_id_image_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='img_hash',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
