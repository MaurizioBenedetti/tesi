from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader
from django.shortcuts import redirect

from .models import Hotel,Reservation,Service

import logging
import datetime

logger = logging.getLogger(__name__)

def homepage(request):
    hotel_list = Hotel.objects.all()
    template = loader.get_template("booking/index.html")
    context = {
        "hotel_list": hotel_list,
    }
    return HttpResponse(template.render(context, request))

def hotels(request):
    hotel_list = Hotel.objects.all()
    template = loader.get_template("booking/hotels.html")
    context = {
        "hotel_list": hotel_list,
    }
    return HttpResponse(template.render(context, request))



def booking_new(request):
     #il metodo GET consiste nel renderizzare la pagina di una nuova prenotazione.
     if request.method =='GET':
        hotel_list = Hotel.objects.all()
        template = loader.get_template("booking/booking.html")
        context = {
            "hotel_list": hotel_list,
        }
        return HttpResponse(template.render(context, request))
     if request.method =='POST':
        comments = request.POST["commenti"]
        startDate = datetime.datetime.strptime(request.POST["datecheckin"], "%Y-%m-%d").date()
        endDate = datetime.datetime.strptime(request.POST["datecheckout"], "%Y-%m-%d").date()
        idHotel=request.POST["hotel_selezionato"]
        #hotelSelected = request.POST["hotel_selezionato"]
        #commenti = "FINO"
        logger.error(comments)
        hotel_list = Hotel.objects.all()
        template = loader.get_template("booking/booking.html")

        hotel_obj =  Hotel.objects.get(pk=idHotel)

        diff = abs((endDate-startDate).days)

        reservationOBJ = Reservation(comments = comments,value=hotel_obj.hotel_rooms_basic_price * diff, user_id=1, Hotel=hotel_obj, start_date=startDate,end_date=endDate)
        reservationOBJ.save()
        #context = {
        #    "hotel_list": hotel_list,
        #}
        #return HttpResponse(template.render(context, request))
        return redirect(bookings)


def booking_edit(request,booking_id):
    logger.error(booking_id)

    if request.method =='GET':
        reservation = Reservation.objects.get(pk=booking_id)    

        hotel_list = Hotel.objects.all()
        template = loader.get_template("booking/booking.html")
        context = {
            "hotel_list": hotel_list,
            "reservation": reservation,
        }
        return HttpResponse(template.render(context, request))
    if request.method =='POST':


        logger.error("DAJE DE POST")
        reservation = Reservation.objects.get(pk=booking_id)    
        
        comments = request.POST["commenti"]
        startDate = datetime.datetime.strptime(request.POST["datecheckin"], "%Y-%m-%d").date()
        endDate = datetime.datetime.strptime(request.POST["datecheckout"], "%Y-%m-%d").date()

        reservation.comments = comments
        reservation.start_date = startDate
        reservation.end_date = endDate
        reservation.save()
        return redirect(bookings)
        

def bookings(request):
    reservation_list = Reservation.objects.all()
    template = loader.get_template("booking/prenotazioni.html")
    context = {
        "reservation_list": reservation_list,
    }
    return HttpResponse(template.render(context, request))


def booking_delete(request, booking_id):
    reservation = Reservation.objects.get(pk=booking_id)
    reservation.delete()
    return redirect(bookings)
    