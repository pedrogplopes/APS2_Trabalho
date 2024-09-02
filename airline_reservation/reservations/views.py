from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight, Reservation
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def home(request):
    if request.user.is_authenticated:
        return redirect('search_flights')

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"Você está logado como {username}.")
                    return redirect('search_flights')
                else:
                    messages.error(request, "Nome de usuário ou senha inválidos.")
            else:
                messages.error(request, "Nome de usuário ou senha inválidos.")
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "Registro bem-sucedido.")
                return redirect('search_flights')
            else:
                messages.error(request, "Falha no registro. Verifique os dados informados.")
    else:
        login_form = AuthenticationForm()
        register_form = UserCreationForm()

    return render(request, 'home.html', {'login_form': login_form, 'register_form': register_form})

def search_flights(request):
    query = request.GET.get('query', '')
    if query:
        flights = Flight.objects.filter(
            destination__icontains=query
        )
    else:
        flights = Flight.objects.all()

    return render(request, 'reservations/search_flights.html', {'flights': flights})

def make_reservation(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        seats_requested = int(request.POST.get('seats_requested', 1))
        if seats_requested <= flight.available_seats:
            request.session['flight_id'] = flight.id
            request.session['seats_requested'] = seats_requested
            return redirect('payment')  # Redireciona para a página de pagamento
        else:
            messages.error(request, "Não há assentos suficientes disponíveis.")
    return render(request, 'reservations/make_reservation.html', {'flight': flight})

def payment(request):
    flight_id = request.session.get('flight_id')
    seats_requested = request.session.get('seats_requested')

    if not flight_id or not seats_requested:
        return redirect('home')

    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        Reservation.objects.create(
            user=request.user,
            flight=flight,
            seats_reserved=seats_requested
        )
        flight.available_seats -= seats_requested
        flight.save()
        messages.success(request, "Reserva feita com sucesso!")
        return redirect('search_flights')

    return render(request, 'reservations/payment.html', {
        'flight': flight,
        'seats_requested': seats_requested,
        'total_price': flight.price * seats_requested
    })

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

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        flight = reservation.flight
        flight.available_seats += reservation.seats_reserved
        flight.save()
        reservation.delete()
        messages.success(request, "Reserva cancelada com sucesso!")
        return redirect('my_reservations')
    return render(request, 'reservations/confirm_cancel.html', {'reservation': reservation})