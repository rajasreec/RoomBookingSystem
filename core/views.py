from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from datetime import date

from .models import Booking, Room, Block
from .forms import RoomForm

User = get_user_model()


# -------------------------
# Helper Functions
# -------------------------

def is_admin(user):
    return user.is_staff or user.is_superuser


# -------------------------
# Home Page
# -------------------------

def home(request):
    return redirect("login")


# -------------------------
# Register View (FIXED)
# -------------------------

def register_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "register.html")


# -------------------------
# Login View
# -------------------------

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")


# -------------------------
# Logout View
# -------------------------

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------
# Dashboard
# -------------------------

@login_required
def dashboard(request):

    today = timezone.now().date()

    total_rooms = Room.objects.count()

    booked_rooms_today = Booking.objects.filter(date=today) \
                                         .values("room") \
                                         .distinct() \
                                         .count()

    available_rooms_today = total_rooms - booked_rooms_today

    recent_bookings = Booking.objects.order_by("-date")[:5]

    return render(request, "dashboard.html", {
        "total_rooms": total_rooms,
        "booked_today": booked_rooms_today,
        "available_rooms_today": available_rooms_today,
        "recent_bookings": recent_bookings,
    })


# -------------------------
# View Rooms
# -------------------------

@login_required
def view_rooms(request):
    rooms = Room.objects.all()
    return render(request, "view_rooms.html", {"rooms": rooms})


# -------------------------
# Add Room (Admin Only)
# -------------------------

@login_required
@user_passes_test(is_admin)
def add_room(request):

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Room added successfully")
            return redirect("dashboard")
    else:
        form = RoomForm()

    return render(request, "add_room.html", {"form": form})


# -------------------------
# Create Booking
# -------------------------

@login_required
def create_booking(request):

    rooms = Room.objects.filter(is_available=True)
    blocks = Block.objects.all()
    floors = Room.FLOOR_CHOICES
    room_types = Room.ROOM_TYPE_CHOICES

    if request.method == 'POST':
        room_id = request.POST.get('room')
        booking_date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        purpose = request.POST.get('purpose')

        conflict = Booking.objects.filter(
            room_id=room_id,
            date=booking_date
        ).filter(
            Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
        ).exists()

        if conflict:
            messages.error(request, "Room already booked for selected time.")
            return redirect('create_booking')

        Booking.objects.create(
            user=request.user,
            room_id=room_id,
            date=booking_date,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose,
            status="Pending"
        )

        messages.success(request, "Booking request submitted successfully!")
        return redirect('dashboard')

    return render(request, 'create_booking.html', {
        'rooms': rooms,
        'blocks': blocks,
        'floors': floors,
        'room_types': room_types,
    })

# -------------------------
# Manage Bookings (Admin)
# -------------------------

@login_required
@user_passes_test(is_admin)
def manage_bookings(request):
    bookings = Booking.objects.all().order_by('-date')
    return render(request, "manage_booking.html", {"bookings": bookings})
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "booking_detail.html", {"booking": booking})

# -------------------------
# Approve Booking
# -------------------------

@login_required
@user_passes_test(is_admin)
def approve_booking(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = "Approved"
    booking.save()
    return redirect("dashboard")

    messages.success(request, "Booking Approved Successfully.")
    return redirect("manage_bookings")
def approve_bookings(request):
    bookings = Booking.objects.filter(status="Pending")
    return render(request, "approve_bookings.html", {"bookings": bookings})

# -------------------------
# Reject Booking
# -------------------------

@login_required
@user_passes_test(is_admin)
def reject_booking(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = "Rejected"
    booking.save()

    messages.error(request, "Booking Rejected.")
    return redirect("manage_bookings")


# -------------------------
# Available Rooms Today
# -------------------------

@login_required
def available_rooms_today(request):

    today = timezone.now().date()

    booked_rooms = Booking.objects.filter(date=today) \
                                   .values_list('room_id', flat=True)

    available_rooms = Room.objects.exclude(id__in=booked_rooms)

    return render(request, 'available_rooms_today.html', {
        'rooms': available_rooms
    })


# -------------------------
# AJAX Load Rooms
# -------------------------

@login_required
def load_rooms(request):

    block = request.GET.get("block")
    floor = request.GET.get("floor")
    room_type = request.GET.get("room_type")

    rooms = Room.objects.filter(
        block__block_name=block,
        floor=floor,
        room_type=room_type
    )

    room_data = [
        {
            "id": room.id,
            "name": room.room_name
        }
        for room in rooms
    ]

    return JsonResponse(room_data, safe=False)