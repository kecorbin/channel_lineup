import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channel_lineup.settings")

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from lineup.models import Lineup, Channel


def lineup_from_file(zip, provider, file):
    """

    :param zip: zipcode for lineup
    :param provider: str name of provider
    :param file: file handler
    :return:
    """
    lineup = Lineup.objects.create(zipcode=zip, provider=provider)

    lineup.save()
    for l in file:
         # ABC,9,abc.png
        name, number, file = l.rstrip().split(',')
        channel = Channel.objects.create(lineup=lineup, name=name, number=number, icon=file)
        channel.save()


fh = open('66085.txt')
lineup_from_file('66085','twcable',fh)