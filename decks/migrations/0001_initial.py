# Generated by Django 2.2 on 2019-04-21 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CardInDeck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('in_sideboard', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('card_in_deck', models.ManyToManyField(through='decks.CardInDeck', to='cards.Edition')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cardindeck',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decks.Deck'),
        ),
        migrations.AddField(
            model_name='cardindeck',
            name='edition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cards.Edition'),
        ),
    ]
