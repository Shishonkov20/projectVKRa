from django.urls import path
from .views import *


urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('detail/<int:pk>', ProjectDetailView.as_view(), name='detail_project'),
    path('works_by_project/<int:pk>', works_by_project, name='works_by_project'),
    path('register/', RegistrationFormView.as_view(), name='register'),
    path('login/', MainLoginView.as_view(), name='login'),
    path('logout/', MainLogoutView.as_view(), name='logout'),
]
