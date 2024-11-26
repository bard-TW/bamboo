# Generated by Django 5.1.1 on 2024-11-26 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basiccompanyinformation',
            name='establishment_date',
            field=models.CharField(default=0, max_length=8, verbose_name='成立日期'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basiccompanyinformation',
            name='listing_Date',
            field=models.CharField(default=0, max_length=8, verbose_name='上市日期'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basiccompanyinformation',
            name='stk_ab',
            field=models.CharField(default='無', max_length=50, verbose_name='簡稱'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basiccompanyinformation',
            name='stk_cs',
            field=models.IntegerField(default=0, verbose_name='普通股數'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basiccompanyinformation',
            name='stk_ps',
            field=models.IntegerField(default=0, verbose_name='特別股數'),
            preserve_default=False,
        ),
    ]
