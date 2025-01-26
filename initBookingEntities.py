from booking.models import Hotel,Reservation,Service

#questo script inizializza il sistema di booking con delle entita' di supporto per 
#impostare un ambiente di Demo basilare. Viene eseguito una sola volta nel primo run
#dopo la docker compose



#Creo la gerarchia iniziando dalle foglie ovviamente. Prima una manciata di servizi
listaServizi = ["TV Satellitare", "Aria Condizionata", "Vasca Idromassaggio", "Servizio Navetta", "SPA", "Guida turistica"]

for servizio in listaServizi:
    newService = Service (service_name = servizio)
    newService.save()


#Aggiungo qualche Hotel, ne creo una manciata per praticita'

#Hotel numero 1, tutti i servizi
newHotel = Hotel ()
newHotel.hotel_name = "Gran Signore"
newHotel.hotel_description ="L'hotel gran signore, come suggerisce il nome, offre il massimo che il lusso e lo sfarzo possano offrire negli states."
newHotel.hotel_email = "gransignore@pegasohotels.it"
newHotel.hotel_phone = "+36 263 4728 42"
newHotel.hotel_address = "Via Gran Signore 123, 00121, Nonsaprei"
newHotel.hotel_rooms_number = 200
newHotel.hotel_rooms_basic_price = 3000
newHotel.hotel_front_picture_url = "img/hotel4.jpg"
newHotel.save()

for servizio in Service.objects.all():
    newHotel.hotel_services.add(servizio)    
newHotel.save()


#Hotel numero 2
newHotel = Hotel ()
newHotel.hotel_name = "Alabarda"
newHotel.hotel_description ="L'hotel Alabarda e' il giusto equilibrio tra relax, tranquillità e piacere della vita. Si trova in un posto meraviglioso vicino al mare"
newHotel.hotel_email = "alabarda@pegasohotels.it"
newHotel.hotel_address = "Via dei Navigatori 23, 00021, Bologna"
newHotel.hotel_phone = "+39 363 1128 42"
newHotel.hotel_rooms_number = 100
newHotel.hotel_rooms_basic_price = 300
newHotel.hotel_front_picture_url = "img/hotel1.jpg"
newHotel.save()

servizio = Service.objects.get(service_name = listaServizi[1])
newHotel.hotel_services.add(servizio)    
servizio = Service.objects.get(service_name = listaServizi[3])
newHotel.hotel_services.add(servizio)    
servizio = Service.objects.get(service_name = listaServizi[2])
newHotel.hotel_services.add(servizio)    
servizio = Service.objects.get(service_name = listaServizi[5])
newHotel.hotel_services.add(servizio)    
newHotel.save()


#Hotel numero 3
newHotel = Hotel ()
newHotel.hotel_name = "Afrodite"
newHotel.hotel_description ="Un Hotel per veri intenditori dove grazia, lusso e piacere si uniscono in una esperienza magica, unica e sublime."
newHotel.hotel_email = "afrodite@pegasohotels.it"
newHotel.hotel_phone = "+36 263 4728 42"
newHotel.hotel_description = "Via degli astronauti 42, 27763"
newHotel.hotel_rooms_number = 200
newHotel.hotel_rooms_basic_price = 3000
newHotel.hotel_front_picture_url = "img/hotel2.jpg"
newHotel.save()

servizio = Service.objects.get(service_name = listaServizi[1])
newHotel.hotel_services.add(servizio)    
servizio = Service.objects.get(service_name = listaServizi[2])
newHotel.hotel_services.add(servizio)    
servizio = Service.objects.get(service_name = listaServizi[3])
newHotel.hotel_services.add(servizio)    
newHotel.save()

#Hotel numero 4
newHotel = Hotel ()
newHotel.hotel_name = "Stazione"
newHotel.hotel_description ="Un Hotel per viaggiatori. La soluzione piu comoda vicino "
newHotel.hotel_email = "afrodite@pegasohotels.it"
newHotel.hotel_phone = "+36 263 4728 42"
newHotel.hotel_rooms_number = 200
newHotel.hotel_rooms_basic_price = 3000
newHotel.hotel_front_picture_url = "img/hotel5.jpg"
newHotel.save()

servizio = Service.objects.get(service_name = listaServizi[1])
newHotel.hotel_services.add(servizio)    
servizio = Service.objects.get(service_name = listaServizi[2])
newHotel.hotel_services.add(servizio)    
servizio = Service.objects.get(service_name = listaServizi[3])
newHotel.hotel_services.add(servizio)    
newHotel.save()









