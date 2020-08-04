import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

def index(request):
    url = url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=7f90854c2588cbb6a159d57ac96b3a88'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == "POST":
        form = CityForm(request.POST)
         
        if form.is_valid():
            new_city = form.cleaned_data['name']
            
            x = City.objects.filter(name=new_city).count()

            if x == 0:
                r = requests.get(url.format(new_city)).json()
                #if weather api cod for a city = 404, the city is invalid
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City Doesn't Exist!"
            else:
                err_msg = 'City already exists!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = "City added successfully"
            message_class = 'is-success'
    
    form = CityForm()

    cities = City.objects.all()

    weather_data=[]

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
        'city' : city.name,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message' : message,
        'message_class' : message_class
    }

    return render(request, 'weather/weather.html', context)

#Delete the city
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')
    
