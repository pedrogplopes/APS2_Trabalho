from django.shortcuts import render, get_object_or_404
from .models import Flight, Reservation

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
        # modelo Reservation atualmente não tem passenger_name, e requer user_id e seats_reserved
        # passenger_name = request.POST.get('passenger_name')
        # adicionado campo pra seats_reserved
        seats_reserved = request.POST.get('seats_reserved')
        # user_id deveria ser obtido por POST.get, forçando user_id 1 no código por enquanto
        Reservation.objects.create(user_id=1, flight=flight, seats_reserved=seats_reserved)
    return render(request, 'reservations/make_reservation.html', {'flight': flight})
