from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group,auth
from django.contrib import messages
from .models import airport, userairport, support, facility, airportfacility,threshold
from django.core.mail import send_mail
from plotly.offline import plot
from . import plots, plotstrolley, plotsboarding, plotssanitizer, plotswifi, plotsconveyor, plotsparking, plotskiosk, plotsfeedback, plotslanding
import plotly.graph_objects as go
import pandas as pd
from pymongo import MongoClient
# Create your views here.

#Home Page
def home(request):
    return render(request,'home.html')




#Contact Us Page
def contactus(request):
    return render(request,'contactus.html')



#Registered Airports List
def airportlist(request):
    airports = airport.objects.all()
    return render(request,'airportlist.html',{'airports':airports})




#Support Page
def sup(request):
    if request.method == 'POST':
        query = request.POST['query']
        email = request.POST['email']
        s = support.objects.create(query = query,email=email)
        s.save();
        messages.info(request,'Query Submitted')
        return redirect('/support')
    else:
        return render(request,'support.html')




#AAI Dashboard
def aaidashboard(request):
    airports = airport.objects.all()
    facilities = facility.objects.all()
    airfac = airportfacility.objects.all()
    if request.method == 'POST':
        air = request.POST.get('airport', None)
        date = request.POST.get('date', None)
        fac = request.POST.get('facility', None)
        print('Airport ---',air)
        if fac is None:
            return render(request,'facilitypartial.html',{'airports':airports,'facilities':facilities,'air':air, 'airfac':airfac})
        elif fac == 'Wifi':
            print('Wifi')
            chart = plotswifi.wifi_hour(date,air)
            return render(request,'wifipartial.html',context={'plot_div': chart})
        elif fac == 'Boarding Gate':
            print('Boarding')
            chart = plotsboarding.boarding_hour(date,air)
            return render(request,'boardingpartial.html',context={'plot_div': chart})
        elif fac == 'Conveyor Belt':
            chart = plotsconveyor.conveyor_belt_hour(date, air)
            return render(request,'conveyorpartial.html',context={'plot_div': chart})
        elif fac == 'Parking':
            chart = plotsparking.parking_hour(date, air)
            return render(request,'parkingpartial.html',context={'plot_div': chart})
        elif fac == 'Sanitizer':
            chart = plotssanitizer.sanitizer_hour(date,air)
            return render(request,'sanitizerpartial.html',context={'plot_div': chart})
        elif fac == 'Trolley':
            chart = plotstrolley.trolley_hour(date,air)
            return render(request,'trolleypartial.html',context={'plot_div': chart})
        elif fac == 'Self Check-In Kiosk':
            chart = plotskiosk.kiosk_hour(date,air)
            return render(request,'kioskpartial.html',context={'plot_div': chart})    
        return render(request,'partial.html')
    else:
        air = request.GET.get('airport', None)
        date = '2020-07-26'
        landing = plotslanding.top3(date,air)
        return render(request,'aaidashboard.html',context={'plot_div': landing ,'airports':airports,'facilities':facilities})





#Logout
def logout(request):
    auth.logout(request)
    return redirect('/')




#Login
def login(request):
    airports= airport.objects.all()
    userair = userairport.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None: 
            if user.is_superuser:
                auth.login(request,user)
                return redirect('/adminpage')
            elif user.groups.filter(name='AAI'):
                auth.login(request,user)
                return redirect('/aaidashboard')
            elif user.groups.filter(name='Airport Manager'):
                uid = User.objects.only('id').get(username=username).id
                aid = userairport.objects.only('air_id').get(user_id=uid).air_id
                if airport.objects.filter(id = aid, active=True).exists():
                    auth.login(request,user)
                    return redirect('/airportdashboard')
                else:
                    messages.info(request,'Not Registered')
                    return redirect('/login')
            elif user.groups.filter(name='Airport Staff'):
                uid = User.objects.only('id').get(username=username).id
                aid = userairport.objects.only('air_id').get(user_id=uid).air_id
                if airport.objects.filter(id = aid, active=True).exists():
                    auth.login(request,user)
                    return redirect('/staffdashboard')
                else:
                    messages.info(request,'Not Registered')
                    return redirect('/login')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/login')
    else:
        return render(request,'login.html')





#Airport Dashboard
def airportdashboard(request):
    facilities = facility.objects.all()
    userair = userairport.objects.all()
    airfac = airportfacility.objects.all()
    airports = airport.objects.all()
    if request.method == 'POST':
        date = request.POST.get('date', None)
        fac = request.POST.get('facility', None)
        print('date',date, 'facility', fac)
        current_user = request.user
        a_id = userairport.objects.only('air_id').get(user_id = current_user.id).air_id
        code = airport.objects.only('icao_code').get(id = a_id).icao_code
        print(code)    
        if fac == 'Wifi':
            chart = plotswifi.wifi_hour(date,code)
            return render(request,'wifipartial.html',context={'plot_div': chart})
        elif fac == 'Boarding Gate':
            chart = plotsboarding.boarding_hour(date,code)
            return render(request,'boardingpartial.html',context={'plot_div': chart})
        elif fac == 'Conveyor Belt':
            chart = plotsconveyor.conveyor_belt_hour(date, code)
            return render(request,'conveyorpartial.html',context={'plot_div': chart})
        elif fac == 'Parking':
            chart = plotsparking.parking_hour(date, code)
            return render(request,'parkingpartial.html',context={'plot_div': chart})
        elif fac == 'Sanitizer':
            chart = plotssanitizer.sanitizer_hour(date,code)
            return render(request,'sanitizerpartial.html',context={'plot_div': chart})
        elif fac == 'Trolley':
            chart = plotstrolley.trolley_hour(date,code)
            return render(request,'trolleypartial.html',context={'plot_div': chart})
        elif fac == 'Self Check-In Kiosk':
            chart = plotskiosk.kiosk_hour(date ,code)
            return render(request,'kioskpartial.html',context={'plot_div': chart})
        return render(request,'partial.html',context={'plot_div': chart})
    else:
        date =request.GET.get('date',None)
        current_user = request.user
        a_id = userairport.objects.only('air_id').get(user_id = current_user.id).air_id
        code = airport.objects.only('icao_code').get(id = a_id).icao_code
        landing= plotsfeedback.feedback_avgutil(code)
        return render(request,'airportdashboard.html',context={'plot_div': landing ,'facilities' : facilities,'userair' : userair,'airfac':airfac,'airports':airports})



#Staff Dashboard
def staffdashboard(request):
    facilities = facility.objects.all()
    userair = userairport.objects.all()
    airfac = airportfacility.objects.all()
    airports = airport.objects.all()
    if request.method == 'POST':
        date = request.POST.get('date', None)
        fac = request.POST.get('facility', None)
        print('date',date, 'facility', fac)
        current_user = request.user
        a_id = userairport.objects.only('air_id').get(user_id = current_user.id).air_id
        code = airport.objects.only('icao_code').get(id = a_id).icao_code
        print(code)    
        if fac == 'Wifi':
            chart = plotswifi.wifi_hour(date,code)
            return render(request,'wifipartial.html',context={'plot_div': chart})
        elif fac == 'Boarding Gate':
            chart = plotsboarding.boarding_hour(date,code)
            return render(request,'boardingpartial.html',context={'plot_div': chart})
        elif fac == 'Conveyor Belt':
            chart = plotsconveyor.conveyor_belt_hour(date,code)
            return render(request,'conveyorpartial.html',context={'plot_div': chart})
        elif fac == 'Parking':
            chart = plotsparking.parking_hour(date, code)
            return render(request,'parkingpartial.html',context={'plot_div': chart})
        elif fac == 'Sanitizer':
            chart = plotssanitizer.sanitizer_hour(date,code)
            return render(request,'sanitizerpartial.html',context={'plot_div': chart})
        elif fac == 'Trolley':
            chart = plotstrolley.trolley_hour(date,code)
            return render(request,'trolleypartial.html',context={'plot_div': chart})
        elif fac == 'Self Check-In Kiosk':
            chart = plotskiosk.kiosk_hour(date,code)
            return render(request,'kioskpartial.html',context={'plot_div': chart})
        return render(request,'partial.html',context={'plot_div': chart})
    else:
        date =request.GET.get('date',None)
        current_user = request.user
        a_id = userairport.objects.only('air_id').get(user_id = current_user.id).air_id
        code = airport.objects.only('icao_code').get(id = a_id).icao_code
        landing= plotsfeedback.feedback_avgutil(code)
        return render(request,'staffdashboard.html',context={'plot_div': landing ,'facilities' : facilities,'userair' : userair,'airfac':airfac,'airports':airports})

   
#Admin page after logging in
def adminpage(request):
    return render(request,'admin.html')





#AAI Registration Page
def registeraai(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('/registeraai')
            else:
                user = User.objects.create_user(username=email, password = password1,email=email)
                user.save();
                AAI = Group.objects.get(name='AAI')
                AAI.user_set.add(user)
                user.save();
                subject = 'Confirmation Mail'
                message = f'Hello {user.username}. Your Credentials Email : {user.email}. Set new password through the given link http://sihserver:8088/resetpassword '
                email_from = 'voidderivatives2020@gmail.com'
                recepient_list = [user.email,] 
                send_mail(subject,message,email_from,recepient_list)
                return redirect('/adminpage')
        else:
            messages.info(request,"Password not matched")
            return redirect('/registeraai')
        return redirect('/')
    else:
        return render(request,'aairegister.html')



#Airport Manager Registration Page
def registermanager(request):
    airports = airport.objects.all()
    if request.method == 'POST':
        air = request.POST['airportId']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('/registermanager')
            else:
                user = User.objects.create_user(username=email, password = password1,email=email)
                user.save();
                AirportManager = Group.objects.get(name='Airport Manager')
                AirportManager.user_set.add(user)
                user.save();
                aa = airport.objects.only('id').get(airport_name = air).id
                u = User.objects.only('id').get(email = email).id
                a = userairport(air_id=aa,user_id=u)
                a.save();
                subject = 'Confirmation Mail'
                message = f'Hello {user.username}. Your Credentials Email : {user.email}. Set new password through the given link http://sihserver:8088/resetpassword '
                email_from = 'voidderivatives2020@gmail.com'
                recepient_list = [user.email,] 
                send_mail(subject,message,email_from,recepient_list)
                return redirect('/aaidashboard')
        else:
            messages.info(request,"Password not matched")
            return redirect('/registermanager')
        return redirect('/')
    else:
        return render(request,'managerregister.html',{'airports' : airports})



    
# Airport Staff Registration Page
def registerstaff(request):
    airports = airport.objects.all()
    userair  = userairport.objects.all()
    if request.method == 'POST':
        air = request.POST['airportId']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2 :
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('/registerstaff')
            else:
                user = User.objects.create_user(username=email,password=password1,email=email)
                user.save();
                AirportStaff = Group.objects.get(name ='Airport Staff')
                AirportStaff.user_set.add(user)
                user.save();
                aa = airport.objects.only('id').get(airport_name = air).id
                u = User.objects.only('id').get(email = email).id
                a = userairport(air_id=aa,user_id=u)
                a.save();
                subject = 'Confirmation Mail'
                message = f'Hello {user.username}. Your Credentials Email : {user.email}. Set new password through the given link http://sihserver:8088/resetpassword '
                email_from = 'voidderivatives2020@gmail.com'
                recepient_list = [user.email,] 
                send_mail(subject,message,email_from,recepient_list)
                return redirect('/airportdashboard')
        else:
            messages.info(request,'Password not matched')
            return redirect('/registerstaff')
        return redirect('/')
    else:
        return render(request,'staffregister.html',{'airports':airports,'userair':userair})
   



#Enable Facility At Airports
def enablefacility(request):
    airfac = {}
    a = {}
    facilities = facility.objects.all()
    if request.method == 'POST':
        fac = request.POST.getlist('fac[]')
        abc = [int(i) for i in fac]
        current_user = request.user
        a_id = userairport.objects.only('air_id').get(user_id = current_user.id).air_id
        for f in facilities:
            if f.id in abc:
                status = True
            else:
                status = False
            if airportfacility.objects.filter(air_id=a_id,fac_id = f.id).exists():
                obj = airportfacility.objects.filter(air_id=a_id).get(fac_id = f.id)
                obj.status = status
                obj.save();
            else:
                obj1 = airportfacility(status = status,air_id = a_id, fac_id = f.id)
                obj1.save();
        return redirect('/airportdashboard')
    else:
        current_user= request.user
        a_id = userairport.objects.only('air_id').get(user_id = current_user.id).air_id
        airport_facility = airportfacility.objects.filter(air_id = a_id)
        for i in airport_facility:
            airfac = {i.fac_id : i.status}
            a.update(airfac)
        return render(request,'enablefacility.html',{'facilities' : facilities,'a' : a})

    


#Add new airports
def addairport(request):
    if request.method == 'POST':
        atype = request.POST['atype']
        iata = request.POST['iata']
        icao = request.POST['icao']
        name = request.POST['name']
        category = request.POST['category']
        state = request.POST['state']
        city = request.POST['city']
        if airport.objects.filter(icao_code = icao).exists():
            messages.info(request,'ICAO Code Already Exists')
            return redirect('/addairport')
        elif airport.objects.filter(iata_code = iata).exists():
            messages.info(request,'IATA Code Already Exists')
            return redirect('/addairport')
        elif airport.objects.filter(airport_name = name).exists():
            messages.info(request,'Airport Name Already Exists')
            return redirect('/addairport')
        else:
            air = airport(iata_code =iata,icao_code=icao,airport_name=name,category=category,city=city,state=state,type=atype)
            air.save();
        return redirect('/aaidashboard')
    else:
        return render(request,'addairport.html')



#Forgot Password
def forgotpass(request):
    if request.method == 'POST':
        code = request.POST['icao']
        mail = request.POST['email']
        if User.objects.filter(email=mail).exists():
            if airport.objects.filter(icao_code=code).exists():
                user = User.objects.only('id').get(email =mail).id
                air = airport.objects.only('id').get(icao_code=code).id
                a = userairport.objects.filter(user_id=user).get(air_id=air)
                if a.air_id == air:
                    print(mail)
                    return redirect('/resetpassword')
                else:
                    messages.info(request,'Wrong ICAO Code or Email Address')
                    return redirect('/forgotpassword')
            else:
                messages.info(request,"ICAO Code Doesn't Exists")
                return redirect('/forgotpassword')
        else:
            messages.info(request,"Email Address Doesn't Exists")
            return redirect('/forgotpassword')
    else:
        return render(request,'forgotpassword.html')




#Reset Password
def resetpassword(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        username = request.POST['username']
        password2 = request.POST['password2']
        if User.objects.filter(username=username).exists():
            if password1 == password2:
                user = User.objects.get(username=username)
                user.set_password(password1)
                user.save();
                return redirect('/login')
            else:
                messages.info(request,'Password not matched')
                return redirect('/resetpassword')
        else:
            messages.info(request,"Username doesn't exists" )
            return redirect('/resetpassword')
    else:
        return render(request,'resetpassword.html')



#Change Threshold Values for facilities
def changethreshold(request):
    airports = airport.objects.all()
    facilities=facility.objects.all()
    airfac = airportfacility.objects.all()
    userair  = userairport.objects.all()
    if request.method == 'POST':
        air = request.POST['airportId']
        fac = request.POST['facility']
        s_type = request.POST['stype']
        t_type = request.POST['ttype']
        lvalue  = request.POST['lowvalue']
        hvalue  = request.POST['highvalue']
        cap = request.POST['capacity']
        a_id = airport.objects.only('id').get(airport_name = air).id
        f_id = facility.objects.only('id').get(name = fac).id
        airfac = airportfacility.objects.filter(air_id=a_id).get(fac_id = f_id)
        t = threshold.objects.create(sensor_type = s_type,threshold_value_low = lvalue,threshold_value_high = hvalue,threshold_type = t_type,capacity = cap,airfac_id = airfac.id)
        t.save();
        return redirect('/airportdashboard')
    else:
        return render(request,'threshold.html',{'airports':airports,'facilities':facilities,'userair':userair,'airfac':airfac})

    



#Unregister Airport 
def unregisterairport(request):
    if request.method == "POST":
        code = request.POST['icao']
        if airport.objects.filter(icao_code=code).exists():
            a_id = airport.objects.only('id').get(icao_code=code).id
            airports = airport.objects.all()
            for a in airports:
                if a.id == a_id:
                   a.status = False
                   a.save();
                   return redirect('/aaidashboard')
        else:
            messages.info(request,'Invaid ICAO Code')
            return redirect('/unregisterairport')
    else:
        return render(request,'unregisterairport.html')



#Re-register Airport
def reregisterairport(request):
    airports = airport.objects.all()
    if request.method == "POST":
        code = request.POST['icao']
        if airport.objects.filter(icao_code=code).exists():
            a_id = airport.objects.only('id').get(icao_code=code).id
            for a in airports:
                if a.id == a_id:
                   a.status = True
                   a.save();
                   return redirect('/aaidashboard')
        else:
            messages.info(request,'Invaid ICAO Code')
            return redirect('/reregisterairport')
    else:
        return render(request,'reregisterairport.html')

