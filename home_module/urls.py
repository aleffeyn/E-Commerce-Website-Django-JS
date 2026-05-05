from django.urls import path
from . import views
from .views import AboutUsView

urlpatterns = [
    # path('' , views.index_page , name='home_page')
    path('' , views.HomeView.as_view() , name='home_page'),
    path('about/' , AboutUsView.as_view() , name='about_page')
]
