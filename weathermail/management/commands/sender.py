from collections import namedtuple

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.template import loader, Context
import json
import requests
from weathermail.models import Recipient, City


class Command( BaseCommand):
    help = 'sends weather notice emails to the entire email list'

    def add_arguments( self, parser):
        # no arguments accepted
        pass

    def pull_cities( self ):
        # first pull out all the referenced cities (as fks).
        # i.e. ignore any cities where no one has signed up, and dedup ones where many people signed up.
        referenced_fks = Recipient.objects.all().values_list('location', flat=True).distinct()
        # then pull the id, and api_name columns for those referenced fks
        location_records = City.objects.filter( pk__in=set(referenced_fks)).values_list('id','api_name');

        city_locations = {};
        for r in location_records:
            cur_entry = {'api_name': r[1]}
            city_locations[ r[0]] = cur_entry
        return city_locations;

    def pull_recipients( self):
        recipRecords = Recipient.objects.all();
        return recipRecords;

    def gather_weather( self, locations):
        # start API calls
        url_prefix='http://api.wunderground.com/api/'
        api_key = settings.WUNDERGROUND_API_KEY
        url_features = '/conditions/almanac/'

        for (key, location) in locations.items():
            get_url = url_prefix+str(api_key)+str(url_features)+'q/'+str(location['api_name'])+'.json';
            self.stdout.write("## for: "+location['api_name'])

            # for debugging
            res = requests.get( get_url)

            if 200 == res.status_code:
                # self.stdout.write("data<text>: "+str( res.text ))
                body = res.json()
                if "current_observation" in body:
                    self.stdout.write("    >> found current observations.")
                    # just replace the whole thing
                    locations[key] = body['current_observation'];

                if "almanac" in body:
                    historical_weather = body['almanac'];
                    self.stdout.write("    >> found historical observations:")
                    # self.stdout.write("       "+str(json.dumps(historical_weather, indent=4, sort_keys=True)))
                    # self.stdout.write("============================================================")

                    locations[key]['historical_high_f'] = float(historical_weather['temp_high']['normal']['F']);
                    locations[key]['historical_low_f'] = float(historical_weather['temp_low']['normal']['F']);

            else:
                self.stdout.write("    ?! api call: status= "+str(res.status_code))

        return locations

    def send_emails( self, recipients, locations ):

        for recipient in recipients:

            to_addr = recipient.email
            for_location = locations[ recipient.location.id ]
            weather_description= for_location['weather']
            precip_metric = for_location['precip_today_metric']
            try:
                precip_metric = float(precip_metric)
            except:
                precip_metric = 0
            cur_temp_f = float(for_location['temp_f'])

            context = {
                "weather_description": weather_description,
                "location_description": recipient.location.display_name,
                "current_temperature_fahrenheit": cur_temp_f,
                "precip_metric": precip_metric,
                "temperature_string": for_location['temperature_string'],
                "icon_url": for_location['icon_url'],
            }

            historical_high_f = float(for_location['historical_high_f'])
            historical_low_f = float(for_location['historical_low_f'])
            hist_avg = float((historical_high_f + historical_low_f)/2.0);

            cheerful_subject = "It's nice out! Enjoy a discount on us."
            sympthathetic_subject = "Not so nice out? That's okay, enjoy a discount on us."
            neutral_subject = 'Enjoy a discount on us.'

            # for more detail, see: https://www.wunderground.com/weather/api/d/docs?d=resources/phrase-glossary&MR=1'
            if 'clear' in weather_description or ( cur_temp_f > ( hist_avg + 5.0)):
                context['subject'] = cheerful_subject
            elif ( cur_temp_f < ( hist_avg - 5.0)) or ( precip_metric > 0.0):
                context['subject'] = sympthathetic_subject
            else:
                context['subject'] = neutral_subject

            message_text = context['temperature_string']+" and "+context['weather_description'];
            message_html = loader.get_template('weather_notice.html').render( Context(context));

            self.stdout.write("## recip: "+str(to_addr)+"  subj:"+str(context['subject'])+"  body: "+str(message_text));
            # self.stdout.write("html: \n"+str(message_html));

            msg = EmailMultiAlternatives(
                subject=context['subject'],
                body=message_text,
                from_email="Daniel Williams <equipoise@gmail.com>",
                to=[to_addr],
            )
            msg.attach_alternative( message_html, "text/html")
            cnt = msg.send()
            self.stdout.write("message sent:? "+str(cnt));
        return;


    def handle( self, *args, **options ):
        recipients = self.pull_recipients()
        locations = self.pull_cities()
        # done with db.

        self.stdout.write("## found "+str(len(recipients))+" recipients in "+str(len(locations))+" Cities")

        # wundeground API calls:
        locations = self.gather_weather( locations )

        self.send_emails( recipients, locations)
