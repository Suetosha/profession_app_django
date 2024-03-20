from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('demand', views.demand, name='demand'),
    path('geography', views.geography, name='geography'),
    path('skills', views.skills, name='skills'),
    path('last_vacancies', views.last_vacancies, name='last_vacancies'),
    path('registration', views.registration, name='registration'),
    path('login', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout', views.logout, name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
