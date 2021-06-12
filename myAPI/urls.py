from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='index'),
    path('predictImage', views.predictImage, name='predictImage'),
    path('symptoms', views.symptoms, name='symptoms'),
    path('prevention', views.prevention, name='prevention'),
    path('contact', views.contact, name='contact'),
    path('testNow', views.testnow, name='testNow'),
    path('registration', views.register, name='registration'),
    path('otp_verify', views.otp, name='otp'),
    path('login', views.login, name='login'),
    path('result_pdf/<mobile>', views.render_pdf_view, name='render_pdf_view'),
    path('cases', views.cases, name='cases'),
]




