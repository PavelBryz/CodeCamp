from django.shortcuts import render
import requests
from django.views.generic import CreateView
from rss_parser import Parser

from .feed import FeedDetailed
from .forms import IncidentForm
from .models import Incident


def index(request):
    rss = requests.get('https://data.eso.sa.gov.au/prod/cfs/criimson/cfs_current_incidents.xml')

    # Limit feed output to 5 items
    # To disable limit simply do not provide the argument or use None
    parser = Parser(xml=rss.content.decode(), limit=5)
    feed = parser.parse()

    detailed_feeds = []
    for f in feed.feed:
        fd = FeedDetailed()
        fd.parse_title(f.title)
        fd.parse_desc(f.description)
        detailed_feeds.append(fd)

    context = {'rss': detailed_feeds}

    return render(request, 'RTIMonitor/index.html', context=context)


class IncidentCreateView(CreateView):
    model = Incident
    template_name = 'RTIMonitor/report_incident.html'
    context_object_name = 'form'
    form_class = IncidentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn_text'] = "Report"
        context['header_text'] = 'Report incident'
        if 'pk' in self.kwargs:
            context["id"] = self.kwargs['pk']
        return context


def tips(request):
    return render(request, 'RTIMonitor/tips.html')
