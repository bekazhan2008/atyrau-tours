from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_alter_pasttournament_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='game',
            field=models.CharField(choices=[('standoff2', 'Standoff2'), ('pubg', 'Pubg'), ('csgo', 'Csgo'), ('dota2', 'Dota2'), ('valorant', 'Valorant'), ('brawlstars', 'Brawlstars'), ('clashroyale', 'Clashroyale')], max_length=50, verbose_name='Игра'),
        ),
    ]
