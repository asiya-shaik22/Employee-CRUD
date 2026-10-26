from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Student",
            new_name="Employee",
        ),
    ]
