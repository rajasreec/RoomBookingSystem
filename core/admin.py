from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Room,RoomType

admin.site.register(Room)
from .models import (
    Department,
    User,
    Block,
    Room,
    Hall,
    Booking,
    Report,
)

# Register Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'head_of_department', 'email_id', 'contact_number')


# Register Custom User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'department', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'department')}),
    )


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('block_name',)


# Register Hall
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('hall_name', 'hall_capacity', 'location', 'department')


# Register RoomDepartment
#@admin.register(RoomDepartment)
#class RoomDepartmentAdmin(admin.ModelAdmin):
 #   list_display = ('room', 'department', 'class_dept')


# Register Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',          
        'room',
        'user',
        'date',
        'start_time',
        'end_time',
        'status'       
    )

    list_filter = ('status', 'date')
    search_fields = ('user__username', 'room')


# Register Report
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'booking', 'status', 'reported_at')


# Register EmailNotification
#@admin.register(EmailNotification)
#class EmailNotificationAdmin(admin.ModelAdmin):
#    list_display = ('notification_id', 'booking', 'sent_time')


admin.site.register(RoomType)