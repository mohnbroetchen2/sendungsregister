# Generated by Django 3.2.12 on 2022-02-25 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnp', '0005_alter_dataset_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='prospective_date_of_disposal',
            field=models.DateField(blank=True, null=True),
        ),
    ]