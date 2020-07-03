from django.contrib import admin
from django.urls import path , include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


admin.site.site_header = "QuotesBook Admin"
admin.site.site_title  = "QuotesBook Admin"
admin.site.index_title = "Welcome to QuotesBook Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , views.index , name = 'home'),
    path('searchget' , views.searchget , name = 'searchget'),
    path('shayari' , views.shayari , name = 'shayari'),
    path('signup', views.handlesignup, name='signup'),
    path('signupPage', views.signupPage, name='signupPage'),
    path('signin', views.handlesignin, name='signin'),
    path('signinPage', views.signinPage, name='signinPage'),
    path('signout', views.handlesignout, name='signout'),
    path('forgotPass' , auth_views.PasswordResetView.as_view(
                template_name = 'photo_forgot_pass.html',
                success_url = '/'
            ),
             name = 'forgotPass'
        ),

      path('reset_password_sent/',
           auth_views.PasswordResetDoneView.as_view(),
           name="password_reset_done"),

      path('reset/<uidb64>/<token>/',
           auth_views.PasswordResetConfirmView.as_view(template_name="photo_change_pass.html"),
           name="password_reset_confirm"),

      path('reset_password_complete/',
           auth_views.PasswordResetCompleteView.as_view(template_name = 'Photo_change_success.html'),
           name="password_reset_complete"),

      path('read/' , include('read.urls')),
    path('accounts' , include('allauth.urls')),

] + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)