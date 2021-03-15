from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . views import search_view

app_name = 'Tour'

urlpatterns = [

    path('', views.index, name='index'), 
    path('login/', views.login_template, name='login'),
    path('register/', views.register, name='register'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('registeruser/', views.registeruser, name='registeruser'),
    path('logout', views.logout_user, name='logout'),
    path('home/', views.home, name='home'), 
    path('hotels', views.hotels, name='hotels'),
    path('hotel_city_search', views.hotel_city_search,name='hotelsearch'),
    path('hotel_name_search', views.hotel_name_search,name='hotelname'),
    path('messages', views.messages,name='messages'),
    path('send_messages', views.submit_messages,name='sendmessage'),
    path('send_message_toguide', views.sending_toguide, name="sending_toguide"),
    path('message_view', views.message_view, name='message_view'),
    path('send_replies', views.send_replies,name='send_replies'),
    path('sites', views.sites,name='sites'),
    path('all_activities', views.all_activities, name='all_activities'),
    path('all_events', views.all_events, name='all_events'),
    path('guide', views.guides, name='guide'),
    path('search/', search_view.as_view(), name='search'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/<int:car_id>', views.car_details, name='car_details'),
    path('booking/', views.booking_car, name='book_car'),
    path('load/', views.load, name='load'),
    path('msgg/', views.msgg,name="msgg"),
    path('publichat/', views.public_chats, name="publichat"),
    path('sending_chat/', views.sending_chat, name="sending_chat"),
    path('bookingguide', views.bookingguide, name="bookingguide"),

    path('readnotification', views.readnotification, name="readnotification"),
    path('confirm/', views.confirm, name="confirm"),
    path('archive', views.archive, name="archive"),
    path('completedtours', views.completedtours, name="completedtours"),
    path('bookform/<int:guideid>', views.bookform, name="bookform"),
    path('like_guide', views.like_guide, name="like_guide"),
    path('validate_username', views.validate_username, name="validate_username"),
    path('trying', views.trying, name="trying"),

    path('renderpdf', views.render_pdf_view, name="renderpdf"),
    path('alltourguides', views.displayingallguides, name="alltourguides"),
    path('guidepdf/<int:bookid>', views.trip_render_pdf_view, name="guidepdf"),
    path('trip', views.trip, name="trip"),
    path('search_shortcut', views.search_hotel_base, name="search_shortcut"),
    path('become_guide', views.become_guide, name='become_guide'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)