from django.contrib import admin
from django.urls import path
from . import views
app_name = "library"


urlpatterns = [
    path('about/library-usage',views.library_usage,name="library_usage"),
    path('about/visitor-usage',views.visitor_usage,name="visitor_usage"),
    path('lib_login',views.lib_login,name="lib_login"),
    path('lib_register',views.lib_register,name="lib_register"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('lib_logout',views.lib_logout,name="lib_logout"),
    path('visitor-page',views.visitor,name="visitor"),
    path('sell/<int:id>',views.sellbook,name="sellbook"),
    path('receive/<int:id>',views.receivebook,name="receivebook"),
    path('addbook',views.addbook,name="addbook"),
    path('delete/<int:id>',views.deletebook,name="deletebook"),
    path('detail/<int:id>',views.detailbook,name="detailbook"),
    path('library/<int:id>',views.library,name="library"),
]
