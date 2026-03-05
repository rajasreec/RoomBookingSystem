from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# -------------------------
# Department Model
# -------------------------
class Department(models.Model):
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

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    def __str__(self):
        return self.username


# -------------------------
# Block Model
# -------------------------
class Block(models.Model):
    block_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.block_name


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

    ROOM_TYPE_CHOICES = [
        ('Lab', 'Lab'),
        ('Classroom', 'Classroom'),
        ('Seminar Hall', 'Seminar Hall'),
    ]

    room_name = models.CharField(max_length=100)
    room_capacity = models.IntegerField()

    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    floor = models.CharField(max_length=20, choices=FLOOR_CHOICES)
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['room_name']

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
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.TextField(null=True,blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    #created_at = models.DateTimeField(auto_now_add=True)

    #class Meta:
    #    ordering = ['-created_at']

    #def clean(self):
    #    if self.start_time >= self.end_time:
     #       raise ValidationError("End time must be after start time.")

    def __str__(self):
       return f"Booking {self.id} - {self.status}"


# -------------------------
# Report Model
# -------------------------
class Report(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('resolved', 'Resolved'),
    )

    report_id = models.AutoField(primary_key=True)

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE
    )

    issue_description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    def __str__(self):
        return f"Report {self.id}"


# -------------------------
# Email Notifications Model
# -------------------------
class EmailNotification(models.Model):

    notification_id = models.AutoField(primary_key=True)

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE
    )

    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.id}"