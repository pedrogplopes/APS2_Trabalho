from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight, Reservation
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .facade import ReservationFacade
from .strategies import StandardPricingStrategy, DiscountPricingStrategy

facade = ReservationFacade()

def home(request):
    return redirect('search_flights')

def search_flights(request):
    query = request.GET.get('query', '')
    flights = facade.search_flights(query)
    return render(request, 'reservations/search_flights.html', {'flights': flights})

@login_required
def make_reservation(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        seats_requested = int(request.POST.get('seats_requested', 1))
        if seats_requested <= flight.available_seats:
            request.session['flight_id'] = flight.id
            request.session['seats_requested'] = seats_requested
            return redirect('payment')
        else:
            messages.error(request, "Não há assentos suficientes disponíveis.")
    return render(request, 'reservations/make_reservation.html', {'flight': flight})

@login_required
def payment(request):
    flight_id = request.session.get('flight_id')
    seats_requested = request.session.get('seats_requested')

    if not flight_id or not seats_requested:
        return redirect('home')

    flight = get_object_or_404(Flight, id=flight_id)
    strategy = StandardPricingStrategy()  # Ou use DiscountPricingStrategy para descontos

    if request.method == 'POST':
        success = facade.reserve_flight(request.user, flight_id, seats_requested)
        if success:
            messages.success(request, "Reserva feita com sucesso!")
            return redirect('search_flights')
        else:
            messages.error(request, "Não há assentos suficientes disponíveis.")
    return render(request, 'reservations/payment.html', {
        'flight': flight,
        'seats_requested': seats_requested,
        'total_price': facade.calculate_price(flight, seats_requested, strategy)
    })

@login_required
def cancel_reservation(request, reservation_id):
    if request.method == 'POST':
        facade.cancel_reservation(reservation_id)
        messages.success(request, "Reserva cancelada com sucesso!")
        return redirect('my_reservations')
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'reservations/confirm_cancel.html', {'reservation': reservation})


@login_required
def cancel_reservation(request, reservation_id):
    if request.method == 'POST':
        facade.cancel_reservation(reservation_id)
        messages.success(request, "Reserva cancelada com sucesso!")
        return redirect('my_reservations')
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'reservations/confirm_cancel.html', {'reservation': reservation})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro feito com sucesso.")
            return redirect('search_flights')
        else:
            messages.error(request, "Informações de cadastro inválidas.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Você logou como: {username}.")
                return redirect('search_flights')
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logout feito.")
    return redirect('home')

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})
