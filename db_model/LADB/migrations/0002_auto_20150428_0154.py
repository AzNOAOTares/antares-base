# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LADB', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='alert',
            table='Alert',
        ),
        migrations.AlterModelTable(
            name='alertreplica',
            table='AlertReplica',
        ),
        migrations.AlterModelTable(
            name='astroobject',
            table='AstroObject',
        ),
        migrations.AlterModelTable(
            name='attribute',
            table='Attribute',
        ),
        migrations.AlterModelTable(
            name='attributevalue',
            table='AttributeValue',
        ),
        migrations.AlterModelTable(
            name='locus',
            table='Locus',
        ),
    ]
