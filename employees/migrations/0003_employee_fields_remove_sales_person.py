from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0002_rename_student_employee"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="sales_person",
        ),
        migrations.AlterField(
            model_name="employee",
            name="age",
            field=models.PositiveIntegerField(),
        ),
        migrations.AddField(
            model_name="employee",
            name="salary",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=12,
                validators=[MinValueValidator(0)],
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="experience",
            field=models.DecimalField(
                decimal_places=1,
                default=0,
                max_digits=5,
                validators=[MinValueValidator(0)],
            ),
        ),
    ]
