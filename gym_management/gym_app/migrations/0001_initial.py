# Generated by Django 5.0.7 on 2024-07-30 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Gym",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("address_city", models.CharField(max_length=255)),
                ("address_street", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="HallType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("SAUNA", "Sauna"),
                            ("TRAINING", "Training"),
                            ("YOGA", "Yoga"),
                            ("SWIMMING", "Swimming"),
                        ],
                        default="Training",
                        max_length=100,
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        choices=[
                            ("SAUNA", "Sauna"),
                            ("TRAINING", "Training"),
                            ("YOGA", "Yoga"),
                            ("SWIMMING", "Swimming"),
                        ],
                        default="TRAINING",
                        max_length=20,
                        unique=True,
                    ),
                ),
                (
                    "type_description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Machine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("serial_number", models.CharField(max_length=100)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("walking", "Walking"),
                            ("running", "Running"),
                            ("cycling", "Cycling"),
                            ("elliptical", "Elliptical"),
                            ("rowing", "Rowing"),
                            ("stair_climber", "Stair Climber"),
                        ],
                        max_length=100,
                    ),
                ),
                ("model", models.CharField(blank=True, max_length=100, null=True)),
                ("brand", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("operational", "Operational"), ("broken", "Broken")],
                        max_length=20,
                    ),
                ),
                ("maintenance_date", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("address_city", models.CharField(max_length=255)),
                ("address_street", models.CharField(max_length=255)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("positions", models.TextField(blank=True, default="")),
                (
                    "manager_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subordinates",
                        to="gym_app.employee",
                    ),
                ),
                (
                    "gym_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employees",
                        to="gym_app.gym",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Admin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("address_city", models.CharField(max_length=255)),
                ("address_street", models.CharField(max_length=255)),
                (
                    "gym_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="admins",
                        to="gym_app.gym",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Hall",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("users_capacity", models.PositiveIntegerField(default=10)),
                (
                    "gym_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="halls",
                        to="gym_app.gym",
                    ),
                ),
                (
                    "hall_type_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="halls",
                        to="gym_app.halltype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("birth_date", models.DateField()),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "gym_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="members",
                        to="gym_app.gym",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HallMachine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("uid", models.CharField(max_length=100, unique=True)),
                (
                    "hall_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hall_machines",
                        to="gym_app.hall",
                    ),
                ),
                (
                    "machine_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hall_machines",
                        to="gym_app.machine",
                    ),
                ),
            ],
            options={
                "unique_together": {("hall_id", "machine_id")},
            },
        ),
    ]
