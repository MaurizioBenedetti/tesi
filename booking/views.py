from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader

from .models import Hotel,Reservation,Service


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