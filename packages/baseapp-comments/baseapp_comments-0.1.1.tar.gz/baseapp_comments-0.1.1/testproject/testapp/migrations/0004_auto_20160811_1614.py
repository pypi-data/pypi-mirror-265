# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("testapp", "0003_auto_20160725_2001")]

    operations = [
        migrations.RemoveField(model_name="user", name="is_new_email_verified"),
        migrations.AddField(
            model_name="user",
            name="is_new_email_confirmed",
            field=models.BooleanField(
                default=False,
                help_text="Has the user confirmed they want an email change?",
            ),
        ),
    ]
