# Generated by Django 4.2.7 on 2023-11-26 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0008_productwaitlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='productwaitlist',
            name='quantity_need',
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
    ]
