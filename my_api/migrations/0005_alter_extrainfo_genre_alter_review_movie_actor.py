# Generated by Django 4.2.2 on 2023-07-01 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_api', '0004_alter_extrainfo_genre_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainfo',
            name='genre',
            field=models.IntegerField(choices=[(2, 'Sci-Fi'), (1, 'Horror'), (4, 'Comedy'), (0, 'Unknown'), (3, 'Drama')], default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='my_api.movie'),
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=32)),
                ('movies', models.ManyToManyField(to='my_api.movie')),
            ],
        ),
    ]
