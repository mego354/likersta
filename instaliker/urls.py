from django.conf import settings

from django.urls import path
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from . import views

app_name = "instagram"  

urlpatterns = [
    #################################### Manage Account ####################################
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordChangeFormView.as_view(), name='password_change'),
    path('password_reset/', views.PasswordResetFormView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    #################################### Main Views ####################################
    path('', views.HomeView.as_view(), name='home'),
    path('privacy/', views.privacy, name='privacy'),

    #################################### Test View ####################################


    #################################### Accessibility ####################################
    # path('switch-language/', views.switch_language, name='switch_language'),

]
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

