from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DailyMetric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(unique=True)),
                ("revenue", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("orders", models.PositiveIntegerField(default=0)),
                ("customers", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["date"]},
        ),
    ]
