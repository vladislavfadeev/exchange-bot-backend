# Generated by Django 4.1.6 on 2023-02-09 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Changer',
            fields=[
                ('tg_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyPair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('tg_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_bank_account', models.IntegerField()),
                ('changer_bank_account', models.IntegerField()),
                ('amount', models.FloatField()),
                ('agreed_rate', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('changer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.changer')),
                ('currency_pair', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.currencypair')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_bank', models.CharField(max_length=50)),
                ('changer_bank', models.CharField(max_length=50)),
                ('sell_rate', models.FloatField(blank=True)),
                ('amount', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('currency_pair', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.currencypair')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_bank', models.CharField(max_length=50)),
                ('changer_bank', models.CharField(max_length=50)),
                ('customer_rate', models.FloatField(blank=True)),
                ('buy_rate', models.FloatField()),
                ('amount', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('changer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.changer')),
                ('currency_pair', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.currencypair')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.customer')),
                ('request_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.request')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_bank', models.CharField(max_length=50)),
                ('changer_bank', models.CharField(max_length=50)),
                ('customer_accept', models.BooleanField(default=False)),
                ('changer_accept', models.BooleanField(default=False)),
                ('customer_send_money_date', models.DateTimeField(blank=True)),
                ('customer_accept_date', models.DateTimeField(blank=True)),
                ('changer_accept_date', models.DateTimeField(blank=True)),
                ('changer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.changer')),
                ('choise_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.customerchoice')),
                ('currency_pair', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.currencypair')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.customer')),
                ('request_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.request')),
                ('response_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.response')),
            ],
        ),
        migrations.AddField(
            model_name='customerchoice',
            name='response_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.response'),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_account', models.IntegerField(unique=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.bank')),
                ('bank_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot_app.changer')),
            ],
        ),
    ]
