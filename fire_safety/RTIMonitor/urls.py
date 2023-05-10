from django.urls import path
from django.contrib.auth import views as login_views
from . import views as RTIMonitor


urlpatterns = [
    path("", RTIMonitor.index, name='dashboard'),
    path('report_incident/', RTIMonitor.IncidentCreateView.as_view(), name="report_incident"),
    path('tips/', RTIMonitor.tips, name="tips"),

]
