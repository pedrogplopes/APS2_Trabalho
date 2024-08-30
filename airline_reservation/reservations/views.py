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
        passenger_name = request.POST.get('passenger_name')
        Reservation.objects.create(flight=flight, passenger_name=passenger_name)
    return render(request, 'reservations/make_reservation.html', {'flight': flight})
