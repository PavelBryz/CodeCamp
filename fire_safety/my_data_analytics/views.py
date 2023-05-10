from django.contrib.auth.decorators import permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .classes.data_processors import DataProcessor
from .classes.data_readers import BitesIOReader, DatabaseReader
from .classes.data_process_scenarios import PrintThreeYScenario, PrintSumYScenario, PrintDataScenario
from .classes.data_printers import WebPagePrinter, WebFormattedPrinter
from RTIMonitor.models import Incident


@permission_required('RTIMonitor.can_view_analytics')
def data(request: WSGIRequest):
    sum_y = three_y = format_y = ""
    lt = None

    if request.method == "POST":
        if request.POST['option'] == 'CSV':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                csv_reader = BitesIOReader(request.FILES["file"].file)
                data_processor = DataProcessor(csv_reader)
                data_processor.read_data()
                format_y = data_processor.data_processing(PrintDataScenario(WebFormattedPrinter()))
                sum_y = data_processor.data_processing(PrintSumYScenario(WebPagePrinter()))
                three_y = data_processor.data_processing(PrintThreeYScenario(WebPagePrinter()))
        elif request.POST['option'] == 'DB':
            form = UploadFileForm()
            query_res = Incident.objects.values('date', 'id_cfsdistrict').annotate(total=Count('id'))
            db_reader = DatabaseReader(query_res)
            data_processor = DataProcessor(db_reader)
            data_processor.read_data()
            # format_y = data_processor.data_processing(PrintDataScenario(WebFormattedPrinter()))
            sum_y = data_processor.data_processing(PrintSumYScenario(WebPagePrinter()))
            three_y = data_processor.data_processing(PrintThreeYScenario(WebPagePrinter()))
        elif request.POST['option'] == 'GD':
            form = UploadFileForm()
            lt = Incident.objects.all()[:10]
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()

    context = {"form": form, 'sum_y': sum_y, 'three_y': three_y, 'format_y': format_y, 'lt': lt}
    return render(request, 'my_data_analytics/data.html', context=context)