from django.urls import path

from . import views
app_name='dashboard'
urlpatterns = [
	path('',views.home,name='home'),
	path('contactus',views.contactus,name='contactus'),
	path('aaidashboard',views.aaidashboard,name='aaidashboard'),
	path('support',views.sup,name='support'),
	path('airportdashboard',views.airportdashboard,name='airportdashboard'),
	path('staffdashboard',views.staffdashboard,name='staffdashboard'),
	path('login',views.login,name='login'),
	path('registeraai',views.registeraai,name='registeraai'),
	path('registermanager',views.registermanager,name='registermanager'),
	path('registerstaff',views.registerstaff,name='registerstaff'),
	path('enablefacility',views.enablefacility,name='enablefacility'),
	path('adminpage',views.adminpage,name='adminpage'),
        path('logout',views.logout,name='logout'),
	path('addairport',views.addairport,name='addairport'),
	path('forgotpassword',views.forgotpassword,name='forgotpassword'),
        path('resetpassword',views.resetpassword,name='resetpassword'),
        path('changethreshold',views.changethreshold,name='changethreshold'),
        path('airportlist',views.airportlist,name='airportlist'),
	path('unregisterairport',views.unregisterairport,name="unregisterairport"),
        path('reregisterairport',views.reregisterairport,name="reregisterairport"),
	path('alerts',views.alerts,name="alerts"),

   ]

