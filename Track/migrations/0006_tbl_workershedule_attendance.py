from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Track', '0005_tbl_vacancy_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_workershedule',
            name='attendance',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
