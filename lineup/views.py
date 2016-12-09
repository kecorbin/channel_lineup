from django.views.generic.list import ListView, View
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from models import Channel, Lineup, Key
from forms import NewLineupForm


class ChannelListView(ListView):
    template_name = 'channels.html'
    context_object_name = 'channels'
    model = Channel

    def get(self, request, *args, **kwargs):

        # this is generally a request from a browser or API call if this is set
        if 'HTTP_ACCEPT' in request.META:
            print args
            print request.META['HTTP_ACCEPT']

        # control systems don't send any headers - assume that's whats requesting
        else:
            print 'NO HTTP ACCEPT HEADERS'
            print args

        return super(ChannelListView, self).get(request, *args, **kwargs)

    def get_queryset(self):

        # Here we will determine the channel lineup based on parameters from the request
        # e.g ?provider=dish&zipcode=64101&key=00:60:9F:93:82:0B

        # A key is a customized, or system specific lineup based on the mac address
        requested_key = self.request.GET['key']
        try:
            key = Key.objects.get(mac=requested_key)
            print "we have a key for {}".format(key)
        except ObjectDoesNotExist:
            print "nothing special"

        requested_provider = self.request.GET['provider']
        requested_zip = self.request.GET['zipcode']

        print "Getting Lineup for provider {} zipcode {}".format(requested_provider,
                                                                 requested_zip)
        try:
            lineup = Lineup.objects.get(zipcode=requested_zip, provider=requested_provider)
        except ObjectDoesNotExist:
            raise Http404("Lineup does not exist")

        qs = lineup.channel_set.get_queryset()
        return qs

class NewLineupView(View):
    template_name = 'new.html'

    def get(self, request):
        form = NewLineupForm
        return render(request, 'new.html', {'form': form})

    def post(self, request):
        csvdata = request.POST['csvdata']
        zipcode = request.POST['zipcode']
        provider = request.POST['provider']

        lineup = Lineup.objects.create(zipcode=zipcode, provider=provider)
        lineup.save()
        print csvdata
        lines = csvdata.split('\r\n')

        for line in lines:
            line = line.split(',')
            name, number, icon = line[0], line[1], line[2]
            print "Creating Channel for {},{},{}".format(name, number, icon)
            channel = Channel.objects.create(name=name, number=number, icon=icon, lineup=lineup)
        return redirect('new-lineup')