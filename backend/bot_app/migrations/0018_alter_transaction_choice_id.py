# Generated by Django 4.1.6 on 2023-02-25 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0017_transaction_changer_proof_transaction_customer_proof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='choice_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='bot_app.customerchoice'),
        ),
    ]
