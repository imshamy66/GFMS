from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homePage),
    path('signup/',views.signUp),
    path('login/',views.loginPage),
    path('profile/',views.profilePage),
    path('updateprofile/',views.updatePage),
    path('contact/',views.contactUs),
    path('about/',views.aboutUs),
    path('logout/',views.logout),
    path('welcome/',views.welcomePage),
    path('add-fund/',views.addFund),
    path('edit-fund/<int:num>/',views.editFund),
    path('fund-details/<int:num>/',views.fundDetails),
    path('state-fund/<int:num>/',views.stateFundList),
    path('forget-username/',views.forgetUsername),
    path('forget-otp/',views.forgetOtp),
    path('forget-password/',views.forgetPassword),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
