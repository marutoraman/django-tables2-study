# Generated by Django 3.1.6 on 2021-04-09 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0023_blacklistwordmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistSellerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=32, verbose_name='アカウントID')),
                ('seller_name', models.TextField(max_length=16, verbose_name='除外セラー')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'db_table': 't_blacklist_seller',
            },
        ),
    ]