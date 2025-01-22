from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader
from django.shortcuts import redirect

from .models import Hotel,Reservation,Service
from django.contrib.auth import authenticate, login, logout



import logging
import datetime
from django.http import Http404

logger = logging.getLogger(__name__)




#Vista di gestione della pagina iniziale, carica la lista degli hotels per supportare un carosello
#nel corpo principale della pagina. La pagina e' un elemento base che non implementa nulla di speciale
#nello specifico, utilizza la base e la estende 
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

    #controllo se l'utente e' registrato, se non lo e', ovviamente lo forzo verso la login
    if request.user.is_authenticated:
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

            reservationOBJ = Reservation(comments = comments,value=hotel_obj.hotel_rooms_basic_price * diff, user_id=1, Hotel=hotel_obj, start_date=startDate,end_date=endDate, User =request.user)
            reservationOBJ.save()
            #context = {
            #    "hotel_list": hotel_list,
            #}
            #return HttpResponse(template.render(context, request))
            return redirect(bookings)
    else:
        return redirect(signin)        




def booking_edit(request,booking_id):
    logger.error(booking_id)

    if request.method =='GET':
        try:
            reservation = Reservation.objects.get(pk=booking_id)    
        except Reservation.DoesNotExist:
            raise Http404("La prenotazione non esiste")

        hotel_list = Hotel.objects.all()
        template = loader.get_template("booking/booking.html")
        context = {
            "hotel_list": hotel_list,
            "reservation": reservation,
        }
        return HttpResponse(template.render(context, request))
    if request.method =='POST':

        #la condizione in cui la prenotazione non esiste, in un utilizzo normale dovrebbe essere piuttosto difficile
        #nell'happy path mi aspetto il frontend di impacchettare i campi della post correttamente. Ovvio che una POST
        #frallocca posso impacchettarla in 5 secondi con una CURL a caso, meglio controllare ed intercettare 
        #la condizione        
        try:
            reservation = Reservation.objects.get(pk=booking_id)    
        except Reservation.DoesNotExist:
            raise Http404("La prenotazione non esiste")
        
        comments = request.POST["commenti"]
        startDate = datetime.datetime.strptime(request.POST["datecheckin"], "%Y-%m-%d").date()
        endDate = datetime.datetime.strptime(request.POST["datecheckout"], "%Y-%m-%d").date()

        #aggiorno i campi della richeista che ho trovato con l'id specificato, easy peasy
        reservation.comments = comments
        reservation.start_date = startDate
        reservation.end_date = endDate
        
        reservation.save()

        return redirect(bookings)
        

def bookings(request):
     if request.user.is_authenticated:
        #carico ovviamente solo le prenotazioni per l'utente autenticato
        reservation_list = Reservation.objects.filter(User=request.user)
        template = loader.get_template("booking/bookings.html")
        context = {
            "reservation_list": reservation_list,
        }
        return HttpResponse(template.render(context, request))
     else:
        return redirect(signin)    


def booking_delete(request, booking_id):
    reservation = Reservation.objects.get(pk=booking_id)
    reservation.delete()
    return redirect(bookings)


def signin(request):
    logger.error("Funzione Signin")
    if request.method =='GET':
        template = loader.get_template("booking/signin.html")        
        return HttpResponse(template.render(None, request))
    elif request.method == "POST":      
        #TODO: metti un try and catch

        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            logger.error("Authenticated user %s", username)
            login(request, user)
            return redirect(homepage)
        else:
            logger.error("Authenticated failed for user %s", username)
            template = loader.get_template("booking/signin.html")        
            return HttpResponse(template.render(None, request))
            
        
#metodo di servizio, implementa una semplice operazione di logout e redirezione alla
#homepage del site. 
def signout(request):
    logout(request)    
    return redirect(homepage)