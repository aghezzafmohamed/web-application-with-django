# Generated by Django 3.1.3 on 2020-12-04 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20201204_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='picture',
            field=models.ImageField(default='store/media/upload/unknown.jpg', upload_to='upload'),
        ),
    ]
