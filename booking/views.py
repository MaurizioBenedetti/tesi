from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader
from django.shortcuts import redirect

from .models import Hotel,Reservation,Service
from django.contrib.auth import authenticate, login, logout


import logging, datetime
from django.http import Http404,HttpResponseBadRequest

from django.contrib.auth.models import User

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



#Vista con il "catalogo" degli hotels offerti dal portale. La vista e' al momento identica a quella della homepage
#da un punto di vista di backend django, cambia la visualizzazione in frontend, ho deciso cmq di differenziare
#le due funzioni per via dell'alta possibilita' che potrebbero divergere alla prima evoluzione della soluzione
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

            #controllo se si arriva alla prenotazione dal pulsante sul catalogo alberghi
            #uso questa tecnica per passare il valore nella querystring al template di django per
            #potere modificare la bootstrap select list e selezionare diterramente l'albergo selezionato
            #con il senno di poi, propabilmente una overkill, avrei potuto gestirlo in javascript frontend
            #questo e' un possibile improvement
            if request.GET.get('hotel_selected') != None:                
                context = {
                    "hotel_list": hotel_list,
                    #questo passaggio diretto senza una validita' dell'input e' un po kamikaze ma direi GEMO, Good Enough, Move On
                    "hotel_initially_selected": int(request.GET.get('hotel_selected'))
                }
            else:
                context = {
                    "hotel_list": hotel_list,
                }

            return HttpResponse(template.render(context, request))
        
        #Controllo se mi trovo in una situazione di POST. in questo caso, sto salvando una nuova prenotazione e procedo nella
        #verifica dei valori
        if request.method =='POST':
            comments = request.POST["commenti"]


            #provo a convertire i campi in data. Ovviamente in caso di flow lineare, il frontend mi ha
            #assicurato un input well formed. Non posso fidarmi nel backend, controllarlo e' sempre sensato
            try:
                startDate = datetime.datetime.strptime(request.POST["datecheckin"], "%Y-%m-%d").date()
                endDate = datetime.datetime.strptime(request.POST["datecheckout"], "%Y-%m-%d").date()
            except ValueError:
                return HttpResponseBadRequest("Le date fornite sono malformate.")
            
            idHotel=request.POST["hotel_selezionato"]            
            logger.error(comments)
            hotel_list = Hotel.objects.all()
            template = loader.get_template("booking/booking.html")

            hotel_obj =  Hotel.objects.get(pk=idHotel)

            daysDifference = abs((endDate-startDate).days)

            #controllo anche qui una condizione che non dovrebbe verificarsi, ma se ricevo una POST forged
            #potrebbero passarmi due date non compatibili
            if (daysDifference <= 0):
                return HttpResponseBadRequest("Le date non sono compatibili.")

            reservationOBJ = Reservation()
            reservationOBJ.comments = comments
            reservationOBJ.value = hotel_obj.hotel_rooms_basic_price * daysDifference

            #TODO remove this
            reservationOBJ.user_id = 1
            reservationOBJ.start_date = startDate
            reservationOBJ.end_date = endDate
            reservationOBJ.User = request.user      
            reservationOBJ.Hotel=hotel_obj

            reservationOBJ.save()           
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
            reservationOBJ = Reservation.objects.get(pk=booking_id)    
        except Reservation.DoesNotExist:
            raise Http404("La prenotazione non esiste")
        
        comments = request.POST["commenti"]
        #provo a convertire i campi in data. Ovviamente in caso di flow lineare, il frontend mi ha
        #assicurato un input well formed. Non posso fidarmi nel backend, controllarlo e' sempre sensato
        try:
            startDate = datetime.datetime.strptime(request.POST["datecheckin"], "%Y-%m-%d").date()
            endDate = datetime.datetime.strptime(request.POST["datecheckout"], "%Y-%m-%d").date()
        except ValueError:
            return HttpResponseBadRequest("Le date fornite sono malformate.")
    
        daysDifference = abs((endDate-startDate).days)
        #controllo anche qui una condizione che non dovrebbe verificarsi, ma se ricevo una POST forged
        #potrebbero passarmi due date non compatibili
        if (daysDifference <= 0):
            return HttpResponseBadRequest("Le date non sono compatibili.")

        #aggiorno i campi della richeista che ho trovato con l'id specificato, easy peasy
        reservationOBJ.comments = comments
        reservationOBJ.start_date = startDate
        reservationOBJ.end_date = endDate
        reservationOBJ.value = reservation.Hotel.hotel_rooms_basic_price * daysDifference
        
        reservationOBJ.save()

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

    if request.user.is_authenticated:    
        reservation = Reservation.objects.get(pk=booking_id)

        if(reservation.User == request.user):            
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




#Metodo che gestisce la registrazione di un nuovo utente. Ovviamente è un placeholder di qualcosa di molto
#più complesso che normalmente viene implementato per un portale di produzione degno di questo nome.
#nella funzione di gestione del POST, collezziona i campi e crea un utente usando il metodo standard 
#create_user, che assicura anche la creazione dell'utente come utente attivo
def signup(request):    
    if request.method =='GET':
        template = loader.get_template("booking/signup.html")        
        return HttpResponse(template.render(None, request))
    elif request.method == "POST":      
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            nome = request.POST["nome"]
            cognome = request.POST["cognome"]
            email = request.POST["email"]
        except:
            #in caso di errore in questa fase, semplicement faccio schiantare l'utente sulla pagina
            #standard di bad request.
            return HttpResponseBadRequest("Gli input forniti non sono validi.")
        
        newUser = User.objects.create_user(username, email, password)                
        newUser.first_name = nome
        newUser.last_name = cognome        
        newUser.save ()
        
        return redirect(signin)
        
        
#metodo di servizio, implementa una semplice operazione di logout e redirezione alla
#homepage del sito. 
def signout(request):
    logout(request)    
    return redirect(homepage)