from django.db import models


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

    serial_number = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    model = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    maintenance_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.type} - {self.serial_number}"


class HallType(models.Model):
    TYPE_CHOICES = [
        ("sauna", "Sauna"),
        ("training", "Training"),
        ("yoga", "Yoga"),
        ("swimming", "Swimming"),
    ]

    type_description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    def __str__(self):
        return self.type


class Hall(models.Model):
    name = models.CharField(max_length=255)
    users_capacity = models.IntegerField()
    type = models.ForeignKey(HallType, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Admin(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
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
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
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
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class HallMachine(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    uid = models.CharField(max_length=100, unique=True)

    class Meta:
        unique_together = ("hall", "machine")

    def __str__(self):
        return f"{self.machine} in {self.hall}"

    def save(self, *args, **kwargs):
        # Generate the name based on hall and machine
        if not self.name:
            self.name = f"{self.hall.name} - {self.machine.type}"

        # Generate the UID based on machine type and count
        if not self.uid:
            count = HallMachine.objects.filter(
                hall=self.hall,
                machine=self.machine
            ).count() + 1
            self.uid = f"{self.machine.type}_{count}"

        super().save(*args, **kwargs)