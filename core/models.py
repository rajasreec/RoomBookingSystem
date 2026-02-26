from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# -------------------------
# Department Model
# -------------------------
class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=200)
    head_of_department = models.CharField(max_length=200)
    email_id = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.department_name


# -------------------------
# Custom User Model
# -------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


# -------------------------
# Room Model
# -------------------------
class Room(models.Model):
    
    FLOOR_CHOICES = [
        ('Ground', 'Ground'),
        ('First', 'First'),
        ('Second', 'Second'),
        ('Third', 'Third'),
    ]

    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=100)
    room_capacity = models.IntegerField()
    block_name = models.CharField(max_length=100)
    floor = models.CharField(max_length=20, choices=FLOOR_CHOICES)
    room_type = models.CharField(max_length=100)
    no_of_regular_classrooms = models.IntegerField(default=0)

    def __str__(self):
        return self.room_name


# -------------------------
# Hall Model
# -------------------------
class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True)
    hall_name = models.CharField(max_length=100)
    hall_capacity = models.IntegerField()
    location = models.CharField(max_length=200)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.hall_name


# -------------------------
# Room-Department Mapping
# -------------------------
class RoomDepartment(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    class_dept = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.room} - {self.department}"


# -------------------------
# Booking Model
# -------------------------
class Booking(models.Model):
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='pending'
    )
    booking_type = models.CharField(max_length=100)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_bookings'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_id}"


# -------------------------
# Reports Model
# -------------------------
class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    issue_description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Report {self.report_id}"


# -------------------------
# Email Notifications Model
# -------------------------
class EmailNotification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.notification_id}"