# Generated by Django 5.0.3 on 2024-03-27 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_bocor_ds', '0002_remove_portfolio_image3_remove_portfolio_image4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='redirect_link',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='리다이렉트 링크'),
        ),
    ]
