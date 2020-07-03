from django.contrib import admin
from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views
from .models import Profile , User

urlpatterns = [
    path('' , views.index , name = 'readhome'),
    path('contact' , views.handlecontact , name = 'contact'),
    path('contactPage' , views.contactPage , name = 'contactPage'),
    path('shayarisearch' , views.shayarisearch , name = 'shayarisearch'),
    path('profile' , views.profile , name = 'profile'),
    path('search' , views.search , name = 'search'),
    path('settings' , views.setttings , name = 'settings'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='photo_settings_pass.html',
            success_url='/'
        ),
        name='change_password'
    ),
    path('notifications' , views.notifications , name = 'notifications'),
    path('deleteNoti' , views.deleteNoti , name = 'deleteNoti'),
    path('generalSettings' , views.generalSettings , name = 'generalSettings'),
    path('viewPost' , views.singlePost , name = 'viewPost'),
    path('viewExplorerPost' , views.singleExplorerPost , name = 'viewExplorerPost'),
    path('viewHashPost' , views.singleHashPost , name = 'viewHashPost'),
    path('viewHomePost' , views.singleHomePost , name = 'viewHomePost'),
    path('postComment' , views.postComment , name = 'postComment'),
    path('deleteComment' , views.deleteComment , name = 'deleteComment'),
    path('deletePost' , views.deletePost , name = 'deletePost'),
    path('quotes' , views.quotes , name = 'quotes'),
    path('searchPage' , views.searchPage , name = 'searchPage'),
    path('shayari' , views.shayari , name = 'shayari'),
    path('changePassword' , views.changePassword , name = 'changePassword'),
    path('hashtagFollow' , views.hashtagFollow , name = 'hashtagFollow'),
    path('searchProfile' , views.searchProfile , name = 'searchProfile'),
    path('searchHash' , views.searchHash , name = 'searchHash'),
    path('upload' , views.upload , name = 'upload'),
    path('explore' , views.explore , name = 'explore'),
    path('uploadProfile' , views.uploadProfile  , name = 'uploadProfile'),
    path('uploadPage' , views.uploadPage , name = 'uploadPage'),
    path('profileChange', views.profileChangePage , name='profileChange'),
    path('follow' , views.follow , name = 'follow'),
    path('follower' , views.follower , name = 'follower'),
    path('check' , views.check , name = 'check'),
    path('checkEmail' , views.checkEmail , name = 'checkEmail'),
    path('delete' , views.delete , name = 'delete'),
    path('following' , views.following , name = 'following'),
    path('like' , views.like , name = 'like'),
    path('save' , views.save , name = 'save'),
    path('postLiked' , views.postLiked , name = 'postLiked'),
    path('postSaved' , views.postSaved , name = 'postSaved'),
    path('signout', views.handlesignout, name='signout'),
    path('editprofile' , views.editProfile , name = 'editprofile'),
    path('feed' , views.feed , name = 'feed'),
]
