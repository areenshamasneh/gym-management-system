from django.db import models, transaction, IntegrityError


class Gym(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address_city = models.CharField(max_length=255)
    address_street = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Machine(models.Model):
    STATUS_CHOICES = [
        ("operational", "Operational"),
        ("broken", "Broken"),
    ]

    TYPE_CHOICES = [
        ("walking", "Walking"),
        ("running", "Running"),
        ("cycling", "Cycling"),
        ("elliptical", "Elliptical"),
        ("rowing", "Rowing"),
        ("stair_climber", "Stair Climber"),
    ]

    serial_number = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    model = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    maintenance_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.type} - {self.serial_number}"


class HallType(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    type_description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)


class Hall(models.Model):
    name = models.CharField(max_length=255)
    users_capacity = models.PositiveIntegerField(default=10)
    hall_type_id = models.ForeignKey(
        HallType, on_delete=models.CASCADE, related_name="halls"
    )
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="halls")

    def __str__(self):
        return self.name


class Admin(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="admins")
    address_city = models.CharField(max_length=255)
    address_street = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(models.Model):
    POSITION_CHOICES = [
        ("cleaner", "Cleaner"),
        ("trainer", "Trainer"),
        ("system_worker", "System Worker"),
    ]

    name = models.CharField(max_length=255)
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="employees")
    manager_id = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
    )
    address_city = models.CharField(max_length=255)
    address_street = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    positions = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    def get_positions(self):
        return [pos.strip() for pos in self.positions.split(",") if pos.strip()]

    def set_positions(self, position_list):
        self.positions = ", ".join(position_list)


class Member(models.Model):
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class HallMachine(models.Model):
    hall_id = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name="hall_machines"
    )
    machine_id = models.ForeignKey(
        Machine, on_delete=models.CASCADE, related_name="hall_machines"
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    uid = models.CharField(max_length=100, unique=True)

    class Meta:
        unique_together = ("hall_id", "machine_id")

    def __str__(self):
        return f"{self.machine_id} in {self.hall_id}"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.hall_id.name} - {self.machine_id.type}"

        if not self.uid:
            if HallMachine.objects.filter(hall_id=self.hall_id, machine_id=self.machine_id).exists():
                return

            with transaction.atomic():
                count = (
                        HallMachine.objects.filter(
                            hall_id=self.hall_id, machine_id=self.machine_id
                        ).count() + 1
                )
                self.uid = f"{self.machine_id.type}_{count}"

                while HallMachine.objects.filter(uid=self.uid).exists():
                    count += 1
                    self.uid = f"{self.machine_id.type}_{count}"

        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            print(f"Error saving HallMachine: {e}")
            raise
