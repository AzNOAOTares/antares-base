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
                ('AlertID', models.IntegerField(serialize=False, primary_key=True)),
                ('Decision', models.CharField(choices=[('NA', 'Not Applicable'), ('T', 'Throttled Alert'), ('D', 'Diverted'), ('L1', 'Level-I Alert'), ('L2', 'Level-II Alert'), ('R', 'Rarest of the rare Alert')], max_length=50, default='NA')),
            ],
            options={
                'db_table': 'Alert',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlertReplica',
            fields=[
                ('ReplicaID', models.IntegerField(serialize=False, primary_key=True)),
                ('ReplicaNumber', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('ChannelID', models.IntegerField()),
                ('ChannelProbability', models.FloatField()),
                ('AlertID', models.ForeignKey(db_column='AlertID', to='LADB.Alert')),
            ],
            options={
                'db_table': 'AlertReplica',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AstroObject',
            fields=[
                ('AstroObjectID', models.IntegerField(serialize=False, primary_key=True)),
                ('Catalog', models.CharField(max_length=500)),
                ('IDinCatalog', models.IntegerField()),
                ('IsPointSource', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'AstroObject',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('AttrName', models.CharField(serialize=False, max_length=100, primary_key=True)),
                ('IsScaled', models.BooleanField(default=False)),
                ('DataType', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'Attribute',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('ContainerID', models.IntegerField()),
                ('ContainerType', models.CharField(choices=[('A', 'AstroObject Table'), ('C', 'Combo Table'), ('I', 'Image Table'), ('E', 'Alert Table'), ('L', 'LocusAggregatedAlert Table'), ('M', 'ImageSection Table'), ('R', 'AlertReplica Table'), ('S', 'Source Table')], max_length=1)),
                ('ComputedAt', models.DateTimeField(verbose_name='Time the value was computed')),
                ('Value', models.FloatField()),
                ('Annotation', models.CharField(max_length=500)),
                ('Confidence', models.FloatField()),
                ('AttrName', models.ForeignKey(db_column='AttrName', to='LADB.Attribute')),
            ],
            options={
                'db_table': 'AttributeValue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Locus',
            fields=[
                ('LocusID', models.IntegerField(serialize=False, primary_key=True)),
                ('RA', models.FloatField()),
                ('Decl', models.FloatField()),
            ],
            options={
                'db_table': 'Locus',
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
            field=models.ForeignKey(db_column='LocusID', to='LADB.Locus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertreplica',
            name='AstroObjectID',
            field=models.ForeignKey(db_column='AstroObjectID', to='LADB.AstroObject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertreplica',
            name='LocusID',
            field=models.ForeignKey(db_column='LocusID', to='LADB.Locus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='LocusID',
            field=models.ForeignKey(db_column='LocusID', to='LADB.Locus'),
            preserve_default=True,
        ),
    ]
