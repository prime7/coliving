from django.core.management.base import BaseCommand
from requests import get
from bs4 import BeautifulSoup
import datetime
from rentals.models import House,ImageLinks
from accounts.models import User


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        
        title = html_soup.find(id='titletextonly').text
        description = html_soup.find(id='postingbody').text
        duration = 12
        
        current = datetime.date.today()
        earliest_move_in = str(current.year)+'-'+str(current.month+1)+'-'+str(1)
        latest_move_out = str(current.year+1)+'-'+str(current.month)+'-'+str(1)
        
        price = float(html_soup.find('span',class_='price').text.split('$')[1])
        external_source = True
        external_link = url
        
        user = User.objects.get(email='admin@meetquoteshack.com')
        house = House.objects.create(user=user,title=title,address="",description=description,duration=duration,earliest_move_in=earliest_move_in,latest_move_out=latest_move_out,monthly_rent=price,city=1,external_source=True,external_link=external_link)

        image_links = []
        images = html_soup.find_all('a',class_='thumb')
        for image in images:
            image_links.append(image['href'])
            ImageLinks.objects.create(house=house,url=image['href']) 