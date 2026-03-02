from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse

from .models import Booking, Room
from .forms import RoomForm

User = get_user_model()


# -------------------------
# Helper Function
# -------------------------
def is_admin(user):
    return user.is_superuser or user.role == "admin"


# -------------------------
# Home Page
# -------------------------
def home(request):
    return redirect("login")


# -------------------------
# Register View
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
            password=password,
            role="student"
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

        if user is not None:
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
    booked_today = Booking.objects.filter(date=today).count()
    available_today = total_rooms - booked_today

    recent_bookings = Booking.objects.order_by("-created_at")[:5]

    return render(request, "dashboard.html", {
        "total_rooms": total_rooms,
        "booked_today": booked_today,
        "available_today": available_today,
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

    # Filter dropdown data
    blocks = (
        Room.objects
        .values_list("block__block_name", flat=True)
        .order_by("block__block_name")
        .distinct()
    )

    floors = Room.FLOOR_CHOICES

    room_types = (
        Room.objects
        .values_list("room_type", flat=True)
        .order_by("room_type")
        .distinct()
    )

    # IMPORTANT: Get all rooms for dropdown
    rooms = Room.objects.all()

    if request.method == "POST":
        room_id = request.POST.get("room")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        purpose = request.POST.get("purpose")

        # If using room_id as primary key
        room = get_object_or_404(Room, room_id=room_id)
        Booking.objects.create(
            user=request.user,
            room=room,
            date=date,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose,
            booking_type="regular",
            status="pending"
        )

        messages.success(request, "Booking created successfully")
        return redirect("dashboard")

    return render(request, "create_booking.html", {
        "blocks": blocks,
        "floors": floors,
        "room_types": room_types,
        "rooms": rooms,
    })


# -------------------------
# Approve Booking (Admin Only)
# -------------------------
@login_required
@user_passes_test(is_admin)
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    booking.status = "approved"
    booking.approved_by = request.user
    booking.save()
    return redirect("dashboard")


# -------------------------
# Reject Booking (Admin Only)
# -------------------------
@login_required
@user_passes_test(is_admin)
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    booking.status = "rejected"
    booking.approved_by = request.user
    booking.save()
    return redirect("dashboard")


# -------------------------
# Room List
# -------------------------
@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, "rooms.html", {"rooms": rooms})

from django.http import JsonResponse

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
            "id": room.room_id,
            "name": room.room_name
        }
        for room in rooms
    ]

    return JsonResponse(room_data, safe=False)