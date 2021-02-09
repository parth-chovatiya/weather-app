from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# from django.contrib.gis.utils import GeoIP


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=API'


#   find location of user
    t = requests.get('https://get.geojs.io/')
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    ipAdd = ip_request.json()['ip']
    # print(ipAdd)
    ip_url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
    geo_request = requests.get(ip_url)
    geo_data = geo_request.json()

    city = geo_data['city']

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            r = requests.get(url.format(new_city)).json()
            if r['cod'] == 200:
                form.save(commit=False)
                city = form.cleaned_data['name']
            else:
                err_msg = 'City does not exist in the world !! '

            if err_msg:
                message = err_msg
                message_class = 'is-danger'

    form = CityForm()

    r = requests.get(url.format(city)).json()
    # print(r)
    temperature_f = r['main']['temp'];
    temperature_c = round((temperature_f-32)*5/9,2);

    min_temperature_f = r['main']['temp_min']
    min_temperature_c = round((min_temperature_f-32)*5/9,2)

    max_temperature_f = r['main']['temp_max']
    max_temperature_c = round((max_temperature_f-32)*5/9,2)

    speed = round(r['wind']['speed'] * 3.6, 3)

    city_weather = {
        'city': city,
        'temperature_f': temperature_f,
        'temperature_c': temperature_c,
        'min_temperature_f': min_temperature_f,
        'min_temperature_c': min_temperature_c,
        'max_temperature_f': max_temperature_f,
        'max_temperature_c': max_temperature_c,
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
        'pressure': r['main']['pressure'],
        'speed': speed,
        'humidity': r['main']['humidity'],
        'ip': geo_data['ip'],
        'user_city': geo_data['city'],
        'region': geo_data['region'],
        'country': geo_data['country'],
        'timezone': geo_data['timezone'],
        'country_code': geo_data['country_code'],
    }

    context = {
        'city_weather': city_weather,
        'form': form,
        'message': message,
        'message_class': message_class,
    }

    return render(request, 'weather/weather.html', context)
