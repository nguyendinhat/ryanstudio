# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-01 14:13
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giohang', '0002_auto_20180429_0913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giohang',
            old_name='cvv',
            new_name='ccv',
        ),
        migrations.AlterField(
            model_name='giohang',
            name='sdt',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Số điện thoại không hợp lệ', regex='^\\d{10,11}$')]),
        ),
    ]