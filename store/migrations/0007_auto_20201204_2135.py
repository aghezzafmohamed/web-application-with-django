# Generated by Django 3.1.3 on 2020-12-04 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20201202_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='picture',
            field=models.ImageField(default='unknown.jpg', upload_to='upload'),
        ),
    ]
