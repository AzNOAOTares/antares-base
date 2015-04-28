# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('AlertID', models.IntegerField(primary_key=True, serialize=False)),
                ('Decision', models.CharField(max_length=50, choices=[('NA', 'Not Applicable'), ('T', 'Throttled Alert'), ('D', 'Diverted'), ('L1', 'Level-I Alert'), ('L2', 'Level-II Alert'), ('R', 'Rarest of the rare Alert')], default='NA')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlertReplica',
            fields=[
                ('ReplicaID', models.IntegerField(primary_key=True, serialize=False)),
                ('ReplicaNumber', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('ChannelID', models.IntegerField()),
                ('ChannelProbability', models.FloatField()),
                ('AlertID', models.ForeignKey(to='LADB.Alert')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AstroObject',
            fields=[
                ('AstroObjectID', models.IntegerField(primary_key=True, serialize=False)),
                ('Catalog', models.CharField(max_length=500)),
                ('IDinCatalog', models.IntegerField()),
                ('IsPointSource', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('AttrName', models.CharField(primary_key=True, max_length=100, serialize=False)),
                ('IsScaled', models.BooleanField(default=False)),
                ('DataType', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('ContainerID', models.IntegerField()),
                ('ContainerType', models.CharField(max_length=1, choices=[('A', 'AstroObject Table'), ('C', 'Combo Table'), ('I', 'Image Table'), ('E', 'Alert Table'), ('L', 'LocusAggregatedAlert Table'), ('M', 'ImageSection Table'), ('R', 'AlertReplica Table'), ('S', 'Source Table')])),
                ('ComputedAt', models.DateTimeField(verbose_name='Time the value was computed')),
                ('Value', models.FloatField()),
                ('Annotation', models.CharField(max_length=500)),
                ('Confidence', models.FloatField()),
                ('AttrName', models.ForeignKey(to='LADB.Attribute')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Locus',
            fields=[
                ('LocusID', models.IntegerField(primary_key=True, serialize=False)),
                ('RA', models.FloatField()),
                ('Decl', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='attributevalue',
            unique_together=set([('AttrName', 'ContainerID', 'ContainerType', 'ComputedAt')]),
        ),
        migrations.AddField(
            model_name='astroobject',
            name='LocusID',
            field=models.ForeignKey(to='LADB.Locus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertreplica',
            name='AstroObjectID',
            field=models.ForeignKey(to='LADB.AstroObject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertreplica',
            name='LocusID',
            field=models.ForeignKey(to='LADB.Locus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='LocusID',
            field=models.ForeignKey(to='LADB.Locus'),
            preserve_default=True,
        ),
    ]
