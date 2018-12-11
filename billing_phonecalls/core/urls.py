""" urls to core """

from django.urls import path

from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('call', views.RegisterCallEventApi.as_view(), name="register-call"),
    path('billing/<slug:telephone>/', views.TelephoneBillApi.as_view(), name="telephone-bill")
]
