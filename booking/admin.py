from django.contrib import admin

# Register your models here.

from .models import Hotel,Reservation,Service


#Abilito la gestione dei vari modelli delle diverse entita' di progetto per
#essere gestite attaverso la admin interface.
admin.site.register(Hotel)
admin.site.register(Reservation)
admin.site.register(Service)