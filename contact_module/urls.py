from django.urls import path

from contact_module import views
from contact_module.views import ContactUsView

urlpatterns = [
    path('' , ContactUsView.as_view() , name='contact_us_page')
    # path('' , views.contact_page , name='contact_us_page')
]