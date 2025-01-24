from django.db import models


from django.conf import settings
from datetime import date
from django.contrib.auth.models import User



class Service(models.Model):
    service_name = models.CharField(max_length=50)    
    def __str__(self):
        return self.service_name

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=150)
    hotel_description = models.CharField(max_length=150)
    hotel_email = models.CharField(max_length=100)
    hotel_phone = models.CharField(max_length=100)    
    hotel_address = models.CharField(max_length=150)
    hotel_rooms_number = models.IntegerField(default=0)
    hotel_rooms_basic_price = models.IntegerField(default=100)
    hotel_front_picture_url = models.CharField(max_length=150)
    hotel_services = models.ManyToManyField(Service)
    def __str__(self):
        return self.hotel_name
    
    #definisco una utlity property per gestire centralmente la trim della strnga di descrizione.
    #uniformare il contenuto nella pagine degli hotels lascia una sensazione di polish migliore
    #ho preferito farlo qua per praticita', trovo molto piu naturale farlo in python che nella parte frontend 
    #dei templates
    @property
    def get_hotel_description(self):
        if self.hotel_description:
            if(len(self.hotel_description) > 120):
                return self.hotel_description[:120] + "..."
            else:
                return self.hotel_description


        



#Questo modello e' usato per rappresentare una reservation, una prenotazione.
#al momento in cui l'utente salva la prenotazione, il sistema salva le informazioni necessarie per
#potere onorare la prenozione. In particular il range temporale, l'utente e l'albergo
class Reservation(models.Model):
    start_date = models.DateTimeField("date start")
    end_date = models.DateTimeField("date end")
    comments = models.CharField(max_length=500)
    
    #salvo il valore della reservation in quanto potrebbe variare il prezzo della stanza nel tempo
    #ed e' giusto mantenere il prezzo concordato al momento della reservation. Avrei potuto anche calcolarlo in real time
    #inoltre, il sistema potrebbe essere evoluto per gestire special seasons events (per esempio black friday)
    #oppure coupons che si possono utilizzare per avere dei sconti
    value = models.IntegerField()
    user_id = models.IntegerField()
    Hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    #TODO: Per una corretta evoluzione del progetto, una relazione diretta con lo user object di
    # django.contrib.auth.models e' da evitarsi. Per praticita' di progetto ho proceduto in questo modo
    #conscio del trade-off intrapreso
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def start_date_string(self):
        if self.stat_date:
            return "%s..." % self.stat_date.strftime("%m/%d/%Y")