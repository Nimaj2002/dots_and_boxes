# Generated by Django 5.1.2 on 2024-10-21 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('PVP', 'Player vs Player'), ('PVA', 'Player vs Agent'), ('AVA', 'Agent vs Agent')], max_length=3)),
                ('player1', models.CharField(max_length=100)),
                ('player2', models.CharField(max_length=100)),
                ('player1_score', models.IntegerField(default=0)),
                ('player2_score', models.IntegerField(default=0)),
                ('player1_is_agent', models.BooleanField(default=False)),
                ('player2_is_agent', models.BooleanField(default=False)),
                ('player1_moves', models.TextField(default='[]')),
                ('player2_moves', models.TextField(default='[]')),
                ('agent_file', models.FileField(blank=True, null=True, upload_to='agent_files/')),
                ('agent1_file', models.FileField(blank=True, null=True, upload_to='agent_files/')),
                ('agent2_file', models.FileField(blank=True, null=True, upload_to='agent_files/')),
                ('current_player', models.CharField(max_length=100)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('winner', models.CharField(blank=True, max_length=100, null=True)),
                ('board', models.TextField(default='')),
            ],
        ),
    ]
