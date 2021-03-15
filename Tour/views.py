from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.utils.timezone import utc
from django.contrib import messages as django_messages
from .models import *
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.views.generic import View

from django.template.loader import get_template
from xhtml2pdf import pisa


def displayingallguides(request):
    alltourguides = Profile.objects.filter(user_type='GUIDE')
    return render(request,'Tour/allguides.html',{'allguides':alltourguides})


def trip_render_pdf_view(request,bookid ):#*args, **kwargs
    your_booking=Booking_guide.objects.get(id=bookid)
    #pk = kwargs.get('pk')
    #your_booking = get_object_or_404(Booking_guide,pk=pk)
    template_path = 'Tour/pdf2.html'
    context = {'your_booking': your_booking}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download:
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if display:
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>') 
    return response

def render_pdf_view(request):
    template_path = 'Tour/trip.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download:
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if display:
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response





# create your views here
#rendering the index,login and register templates
def index(request):
    return render(request, 'Tour/index.html')

def login_template(request):
    return render(request, 'Tour/login.html')

def register(request):
    return render(request, 'Tour/register.html')

#registering, login in and logout a user
def registeruser(request):
    if request.method =='POST':
        firstname = request.POST['firstname']
        secondname = request.POST['secondname']
        username = request.POST['username']
        country=request.POST['country']
        gender= request.POST['gender']
        password=request.POST['password']

        #create user
        user=User.objects.create_user(
            username=username,password=password
        )
        #add profile
        profile =user.profile
        profile.country=country
        profile.gender=gender
        profile.firstname = firstname
        profile.secondname=secondname
        profile.user_type='USER'
        profile.save()
        login(request,user)
        return redirect('Tour:home')

    else:
        return redirect('Tour:index')
#validate username
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
    'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_messagess'] = 'a user with this username already exists'
    return JsonResponse(data)

def loginuser(request):
	if request.method =='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		#check if the user has correct credentials
		if user is not None:
			login(request,user)
			return redirect('Tour:home')
		else:
			django_messages.warning(request, 'INVALID CREDENTIALS!!!')
			return render(request, 'Tour/index.html')
@login_required()
def logout_user(request):
	logout(request)
	return redirect('Tour:index')

#homepage 
@login_required()
def home(request):
    news = update.objects.all().order_by('-date_uploaded')#query the database for all update objects
    return render(request, 'Tour/home.html', {'news':news})

#hotel views
@login_required()
def hotels(request):
    resorts=hotel.objects.all().order_by('-price')
    #all_hotels=hotel.objects.all().order_by('-price')
    #querying all towns in db using value list and using distinct to prevent similar towns from appearing
    city=hotel.objects.values_list('town', flat=True).distinct()
    #querying all hotel names 
    hotelnames=hotel.objects.values_list('hotel_name', flat=True).distinct()
    return render(request, 'Tour/hotels.html', {'city':city, 'hotelnames':hotelnames, 'resorts':resorts})

#searching hotel per city   
@csrf_exempt
@login_required()
def hotel_city_search(request):
    if request.method =='POST':
        city=request.POST['city']#collect the form data which is the value of the city
        hotels=hotel.objects.filter(town=city)#filter all the hotels in the city 
        return render(request, 'Tour/hotel_city_search.html', {'hotels': hotels, 'city':city})
    else:
        city=hotel.objects.values_list('town',flat=True)
        return render(request, 'Tour/hotel_city_search.html', {'city':city})
#searching hotel per hotel_name
@csrf_exempt
@login_required()
def hotel_name_search(request):
    if request.method =='POST':
        searched_hotel=request.POST['hotel']
        available_hotels=hotel.objects.filter(hotel_name=searched_hotel)
        return render(request, 'Tour/hotel_name.html', {'available_hotels': available_hotels,'hotel_name':searched_hotel})
    else:
        return render(request, 'Tour/hotel_name.html')

#message views

@login_required()
def messages(request):
    users=User.objects.all()
    #users=Profile.objects.filter(user_type='GUIDE')
    count_texts=message.objects.filter(receiver=request.user.username, message_status=False).count()
    text_messages=message.objects.filter(receiver=request.user.username).order_by('-date_sent')
    #read_messages=message.objects.filter(receiver=request.user.username, message_status=True).order_by('-date_sent')
    return render(request, 'Tour/messages.html', {'users':users, 'msg':text_messages, 'count':count_texts})

#viewing a single message
@login_required
def message_view(request):
    if request.method =='POST':
        id=request.POST['id']
        current_chat=message.objects.filter(id=id)
        return render(request, 'Tour/read.html', {'chat':current_chat})
    else:
        current_chat = chat.objects.filter(id=id)
        return render(request, 'Tour/read.html', {'chat': current_chat})


#submitting a message
@login_required 
@csrf_exempt
def submit_messages(request):
    if request.method =='POST':
        sender=request.user.username
        subject=request.POST['subject']
        text=request.POST['message']
        recipient=request.POST['receiver']
        parent=request.POST.get('parent')
        today=datetime.datetime.now()
        c=message(sender=sender,text=text,subject=subject,parent=parent,receiver=recipient,date_sent=today)

        try:
            c.save()
            django_messages.success(request, 'Message Sent successfully')
            return redirect('Tour:load')

        except:
            django_messages.error(request, 'Unable to Send Message')
            return redirect('Tour:load')

    else:
        #user=request.user.username
        #message_count=message.objects.filter(receiver=user).count()
        m#essage_me=message.objects.filter(receiver=user,sender=user)
        return  render(request, 'Tour/messages.html')#{'texts':message_count})
#submitting a to guide message
@login_required 
@csrf_exempt
def sending_toguide(request):
    if request.method =='POST':
        sender=request.user.username
        subject=request.POST['subject']
        text=request.POST['message']
        recipient=request.POST['receiver']
        parent=request.POST.get('parent')
        today=datetime.datetime.now()
        c=message(sender=sender,text=text,subject=subject,parent=parent,receiver=recipient,date_sent=today)

        try:
            c.save()
            django_messages.success(request, 'Message Sent successfully')
            return redirect('Tour:guide')

        except:
            django_messages.error(request, 'Unable to Send Message')
            return redirect('Tour:guide')

    else:
        #user=request.user.username
        #message_count=message.objects.filter(receiver=user).count()
        m#essage_me=message.objects.filter(receiver=user,sender=user)
        return  render(request, 'Tour/guides.html')#{'texts':message_count})
#submitting a reply 
@csrf_exempt
def send_replies(request):
    if request.method =='POST':
        sender=request.user.username
        subject=request.POST['subject']
        text=request.POST['message']
        #parent=request.POST.get(id=parentid)
        parentid=request.POST.get('parent')
        parent=message.objects.get(id=parentid)
        recipient=request.POST['receiver']
        today=datetime.datetime.now()
        reply=message(sender=sender,text=text,subject=subject,parent=parent,receiver=recipient,date_sent=today)

        try:
            reply.save()
            django_messages.success(request, 'Message Sent successfully ')
            return redirect('Tour:load')

        except:
            django_messages.error(request, 'Unable to Send Message')
            return redirect('Tour:load')

    else:
        #user=request.user.username
        #message_count=message.objects.filter(receiver=user).count()
        #message_me=message.objects.filter(receiver=user,sender=user)
        return  render(request, 'Tour/load.html')#,{'texts':message_count})


def sites(request):
    wildlife = site.objects.filter(site_type='WILDLIFE')
    marine = site.objects.filter(site_type='MARINE')
    museums = site.objects.filter(site_type='MUSEUM')
    return render(request, 'Tour/attractionsites.html',{'wildlife':wildlife, 'marine':marine, 'museums':museums})
def all_activities(request):
    all_activities = Activity.objects.all()
    return render(request, 'Tour/activities.html',{'all_activities':all_activities})
def all_events(request):
    all_events= Event.objects.all()
    return render(request, 'Tour/events.html',{'all_events':all_events})

def guides(request):
    username=request.user.username
    user=User.objects.get(username=username)
    user_profile=user.profile
    guide_likes=TourGuide_Likes.objects.all().count()
    tourist_likes=TourGuide_Likes.objects.filter(person_liking=user) 
    booking_request=Booking_guide.objects.filter(touristguide=user_profile,book_status=False,guide_response=0).count()
    new_request=Booking_guide.objects.filter(touristguide=user_profile, book_status=False, guide_response=0)
    booking_status=Booking_guide.objects.filter(tourist=user, book_status=False)
    count_guide=Profile.objects.filter(user_type='GUIDE').count()
    available_guides=Profile.objects.filter(user_type='GUIDE',book_status=False).count()
    guides=Profile.objects.filter(user_type='GUIDE',book_status=False)
    completed_tours=Booking_guide.objects.filter(tourist=user,guide_response=1).count()
    guide_completed_tours=Booking_guide.objects.filter(touristguide=user_profile,guide_response=1).count()
    return  render(request, 'Tour/guides.html',{'guides':guides, 'count_guide':count_guide, 
        'count':booking_request, 'booking_status':booking_status,'all_guides':count_guide,
        'available_guides':available_guides,'guide_likes':guide_likes,'tourist_likes':tourist_likes,
        'completed_tours':completed_tours,'new_request':new_request,'guide_completed_tours':guide_completed_tours})
#search
class search_view(ListView): 
    model=hotel
    template_name='Tour/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = hotel.objects.filter(
                Q(hotel_name__icontains=query)|Q(town__icontains=query)
                )
        if object_list :
            return object_list
        else:
            return render(request,'Tour/search.html',{"search results not found!!"})

#dashboard for cars
def dashboard(request):
    available_cars = car.objects.all().order_by('-price')
    return render(request,'Tour/dashboard.html', {'cars':available_cars})
#car details
def car_details(request,car_id):
    thecar = car.objects.get(id=car_id)
    return render(request,'Tour/car_details.html', {'car':thecar})
    
#booking view
@csrf_exempt
def booking_car(request,*args):
    if request.method =='POST':
        username=request.user.username
        user=User.objects.get(username=username)
        carid=request.POST['car_id']
        carbooked=car.objects.get(id=carid)
        rentalcity=request.POST['town']
        instructions=request.POST['instructions']
        timebooked=datetime.datetime.now()
        returndate=datetime.datetime.now()
        bk=Booking(requestUser=user,car_booked=carbooked,time_booked=timebooked,rental_city=rentalcity,return_date=returndate,instructions=instructions)
        try:
            bk.save()
            return redirect('Tour:dashboard')
        except:
            return redirect('Tour:dashboard')
    else:
        return render(request,'Tour/dashboard.html')


#displaying message view
@login_required
def load(request):
    users=User.objects.all()
    new_chats = publichat.objects.filter(chat_status=False).count()
    #all_messages=message.objects.all().order_by('-date_sent')
    send_messages=message.objects.filter(sender=request.user.username).order_by('-date_sent')
    count_send=message.objects.filter(sender=request.user.username, message_status=False).count()
    count_texts=message.objects.filter(receiver=request.user.username, message_status=False).count()
    text_messages=message.objects.filter(receiver=request.user.username).order_by('-date_sent')
    #chats=publichat.objects.all().order_by('-time_sent')
    return render(request, 'Tour/load.html', {'text_messages':text_messages, 'users':users, 'count':count_texts,'new_chats':new_chats})

@login_required
@csrf_exempt
def msgg(request):
    if request.method =='POST':
        message_id=request.POST.get('id')#['id']
        current_chat=message.objects.get(pk=message_id)
        current_chat.message_status = True
        current_chat.save()
        return render(request, 'Tour/like.html', {'chat':current_chat})
    else:
        current_chat = chat.objects.filter(id=id)
        return render(request, 'Tour/like.html', {'chat': current_chat})


@login_required      
def public_chats(request):
    public_chats = publichat.objects.all().order_by('-time_sent')
    for x in public_chats:
        x.chat_status = True;
        x.save()
    return render(request, 'Tour/publichat.html', {'public_chats':public_chats} )
#sending a chat
@login_required 
def sending_chat(request):
    if request.method =='POST':
        username=request.user.username
        user=User.objects.get(username=username)
        time_sent=datetime.datetime.now()
        text=request.POST['message']
        chat=publichat(user=user, time_sent=time_sent, text=text)
        try:
            chat.save()
            django_messages.success(request,"message send successfully")
            return redirect("Tour:load")
        except:
            django_messages.error(request,"unable to send the message")
            return redirect("Tour:load")
    else:
        return render(request,'Tour/load.html')
#booking a guide by a tourist
@login_required 
def bookingguide(request):
    if request.method == 'POST':
        username=request.user.username
        tourist=User.objects.get(username=username)
        pass_number=request.POST['passportnumber']
        touristguide=Profile.objects.get(passport_no=pass_number)
        #touristguide.book_status = True
        #touristguide.save()
        arrival = datetime.datetime.now()
        #departure = request.POST['departure'] 
        #staytime = request.POST['staytime']
        staytime = "20 days"
        instructions = request.POST['instructions']


        choosen_sites = request.POST.getlist("sites", None)
        choosen_activities = request.POST.getlist("activities", None)
        choosen_events = request.POST.getlist("events", None)
    
        #activities = request.POST.getlist("activities", None)
        #events = request.POST.getlist("events", None)


        bkguide=Booking_guide(touristguide=touristguide, tourist=tourist, arrival=arrival, staytime=staytime, instructions=instructions)


        try:
            bkguide.save()
            bkguide.sites.set(choosen_sites)
            bkguide.activities.set(choosen_activities)
            bkguide.events.set(choosen_events)
            django_messages.success(request, 'Your booking request has been received successfully, Wait for reply from your tour guide')
            return redirect("Tour:guide")
        except:
            django_messages.error(request, 'Your booking has failed!! try again')
            return redirect("Tour:guide")
    else:
        return render(request, 'Tour/guides.html')
@login_required 
def readnotification(request): 
    username=request.user.username
    user=User.objects.get(username=username)
    user_profile=user.profile
    notification_tourist=Booking_guide.objects.filter(tourist=user,book_status=False)
    notification=Booking_guide.objects.filter(touristguide=user_profile,book_status=False)
    return render(request,'Tour/notification.html',{'notification':notification,'notification_tourist':notification_tourist})
#getting the tourist guide response
@login_required 
def confirm(request):
    if request.method == 'POST':
        username=request.user.username
        user=User.objects.get(username=username)
        user_profile=user.profile
        guide_response=request.POST['choice']
        if guide_response == "1" :
            user_profile.book_status = True
            user_profile.save()
        if guide_response == "2" :
            user_profile.book_status = False
            user_profile.save()
        bookingid=request.POST['id']
        confirmed=Booking_guide.objects.get(id=bookingid)
        confirmed.guide_response = guide_response
        #confirmed.book_status = True
        confirmed.save()
        return redirect('Tour:guide')
    return render(request, 'Tour/guides.html')
@login_required 
def archive(request):
    if request.method == 'POST':
        bookingid=request.POST['id']
        confirmed=Booking_guide.objects.get(id=bookingid)
        tourist_response=request.POST['choice']
        confirmed.book_status = tourist_response
        #confirmed.book_status = True
        confirmed.save()
        return redirect('Tour:guide')
    return render(request, 'Tour/guides.html')
#showing the completed tours of the tourist and tour guide
@login_required 
def completedtours(request):
    username=request.user.username
    user=User.objects.get(username=username)
    guide_profile=user.profile
    all_tours=Booking_guide.objects.filter(tourist=user,guide_response=1)
    guide_tours=Booking_guide.objects.filter(touristguide=guide_profile,guide_response=1)
    return render(request,'Tour/alltours.html', {'all_tours':all_tours, 'guide_tours':guide_tours })
#bookform for the tourist to book the tour guide
@login_required 
def bookform(request, guideid):
    currentguide=Profile.objects.get(id=guideid)
    events=Event.objects.all()
    activities=Activity.objects.all()
    sites=site.objects.all()
    return render(request,'Tour/bookform.html',{'currentguide':currentguide,'events':events, 'activities':activities,'sites':sites})
#likes of a tour guide
@login_required 
def like_guide(request):
    if request.method == 'GET':
        user = request.user.username
        person_liking = User.objects.get(username=user)
        guide_id = request.GET['guideid']
        person_liked = Profile.objects.get(id=guide_id)
        time_liking = datetime.datetime.now()
        m=TourGuide_Likes(person_liking=person_liking, person_liked=person_liked, time_liking=time_liking)
        m.save()
        return HttpResponse('success') 
    else:
        return HttpResponse("unsuccesful")
#getting a single message that has been clicked
@login_required 
def trying(request):
    if request.method == 'GET':
        messageid = request.GET['message_id']
        requestedmessage = message.objects.get(id=messageid)
        requestedmessage.message_status = True
        requestedmessage.save()
        ser_instance = serializers.serialize('json', [requestedmessage,])
        return JsonResponse({ "instance":ser_instance}, safe=False, status=200)
    else:
        return JsonResponse("error", status=400)


def trip(request):
    events=Event.objects.all()
    activities=Activity.objects.all()
    sites=site.objects.all()
    return render(request, 'Tour/plannedtrips.html',{'events':events, 'activities':activities,'sites':sites})


@csrf_exempt
@login_required()
def search_hotel_base(request):
    if request.method =='POST':
        hotel_name_search=request.POST['input_field']#collect the form data which is the value of the city
        searched_user_hotel=hotel.objects.filter(hotel_name=hotel_name_search)#filter all the hotels in the city 
        return render(request, 'Tour/searched_hotel_results.html', {'searched_user_hotel': searched_user_hotel})
    else:
        #city=hotel.objects.values_list('town',flat=True)
        return render(request, 'Tour/searched_hotel_results.html')

@csrf_exempt
@login_required
def become_guide(request):
    return render(request,'Tour/become_guide.html')