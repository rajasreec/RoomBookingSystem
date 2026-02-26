

# Create your views here.
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Room
from django.contrib.auth import get_user_model
from datetime import datetime


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Check if user is admin
def is_admin(user):
    return user.is_superuser

@login_required
@login_required
def view_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'view_rooms.html', {'rooms': rooms})
@user_passes_test(lambda u: u.is_superuser)
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RoomForm()

    return render(request, 'add_room.html', {'form': form})
User = get_user_model()


# -------------------------
# Home Page
# -------------------------


def home(request):
    return redirect('login')


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

        user = User.objects.create_user(
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



# -------------------------
# Logout View
# -------------------------



# -------------------------
# Dashboard
# -------------------------
@login_required
def dashboard(request):
    today = timezone.now().date()

    total_rooms = Room.objects.count()

    booked_rooms_today = Booking.objects.filter(
        date=today,
        status="approved"
    ).count()

    available_rooms = total_rooms - booked_rooms_today

    recent_bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    context = {
        "total_rooms": total_rooms,
        "booked_rooms_today": booked_rooms_today,
        "available_rooms": available_rooms,
        "recent_bookings": recent_bookings,
    }

    return render(request, "dashboard.html", context)


# -------------------------
# Create Booking
# -------------------------
@login_required
def create_booking(request):

    blocks = Room.objects.values_list('block_name', flat=True).distinct()
    floors = Room.FLOOR_CHOICES
    room_types = Room.objects.values_list('room_type', flat=True).distinct()

    if request.method == "POST":

        room_id = request.POST.get("room")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        purpose = request.POST.get("purpose")

        room = Room.objects.get(room_id=room_id)

        Booking.objects.create(
            user=request.user,
            room=room,
            date=date,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose,
            booking_type="regular",
        )

        messages.success(request, "Booking created successfully")
        return redirect("dashboard")

    return render(request, "create_booking.html", {
        "blocks": blocks,
        "floors": floors,
        "room_types": room_types,
    })

# -------------------------
# View All Rooms
# -------------------------
@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, "rooms.html", {"rooms": rooms})

from django.http import JsonResponse

@login_required
def load_rooms(request):
    block = request.GET.get('block')
    floor = request.GET.get('floor')
    room_type = request.GET.get('room_type')

    rooms = Room.objects.filter(
        block_name=block,
        floor=floor,
        room_type=room_type
    )

    room_list = []
    for room in rooms:
        room_list.append({
            'id': room.room_id,
            'name': room.room_name
        })

    return JsonResponse(room_list, safe=False)