from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from django.db.models.signals import post_save#defines a set of signals sent by the model system
from django.dispatch import receiver

#signals allow certain senders to notify a set of receivers that some action has taken place(dispatch signals)
#sent at the end of the save() method..post_save
#receivers- when they  receive signals,they  then do something
class Profile(models.Model):
	gender_choices = (
		('MALE', 'MALE'),
		('FEMALE', 'FEMALE'),
		)
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	firstname=models.CharField(max_length=1000, blank=True)
	secondname=models.CharField(max_length=500, blank=True)
	user_type=models.CharField(max_length=500, blank=True)
	country=models.CharField(max_length=100, blank=True)
	gender=models.CharField(max_length=50, choices=gender_choices, blank=True)
	profile_image=models.ImageField(upload_to='images/',default='image')
	languages=models.CharField(max_length=1000, blank=True)
	location=models.CharField(max_length=500, blank=True)
	contact=models.CharField(max_length=500, blank=True)
	bio=models.CharField(max_length=500,blank=True)
	passport_no = models.CharField(max_length=1000)
	book_status = models.BooleanField(default=False)
	#likes = models.PositiveIntegerField(blank=True,default=0)

	class Meta:
		verbose_name = 'User_Profile'
		verbose_name_plural = 'User Profiles'

	#string represantion of the object 
	def __str__(self):
		return self.user.username

	@receiver(post_save, sender=User)
	def create_user_profile(sender,instance,created,**kwargs):
		if created:
			Profile.objects.create(user=instance)
	@receiver(post_save, sender=User)
	def save_user_profile(sender,instance,created,**kwargs):
		instance.profile.save()
#tour guides likes model
class TourGuide_Likes(models.Model):
	person_liking = models.ForeignKey(User, on_delete=models.CASCADE)
	person_liked = models.ForeignKey(Profile, on_delete = models.CASCADE)
	time_liking = models.DateTimeField()

	verbose_name = 'Like'
	verbose_name_plural = 'Likes'
	def __str__(self):
		return self.person_liked.firstname
	

class LIKE(models.Model):
	guide=models.ForeignKey(Profile, on_delete = models.CASCADE)
	#person_liking = models.ForeignKey(User, on_delete=models.CASCADE)
	#tourist=models.ForeignKey(User, on_delete = models.CASCADE, blank=True)
	#time_liking = models.DateTimeField(blank=True)

	class Meta:
		verbose_name = 'Like'
		verbose_name_plural = 'Likes'
	def __str__(self):
		return self.guide.firstname

#news model 
class update(models.Model):
    headline=models.CharField(max_length=100)
    text=models.CharField(max_length=2000)
    image=models.ImageField(upload_to='images/')
    date_uploaded=models.DateField()

    class Meta:
    	#db_table = 'update'
    	verbose_name = 'New'
    	verbose_name_plural = 'News'

    def __str__(self):
        return self.headline
    #property to check if news were posted today--can be accessed like a regular property
    @property
    def posted_today(self):
        return date.today() == self.date_uploaded


#hotel model
class hotel(models.Model):
	hotel_image=models.ImageField(upload_to='images/')
	hotel_name=models.CharField(max_length=100)
	location=models.CharField(max_length=100)
	town=models.CharField(max_length=100)
	price=models.FloatField(max_length=100)
	website=models.URLField(max_length=1000)
	contacts=models.CharField(max_length=1000)

	class Meta:
		verbose_name = 'Hotel'
		verbose_name_plural = 'Hotels'
	
	def __str__(self):
		return self.hotel_name+' '+self.location
#message models
class message(models.Model):
	sender=models.CharField(max_length=100)
	receiver=models.CharField(max_length=100)
	subject=models.CharField(max_length=500, default='NO SUBJECT')
	text=models.TextField(max_length=2000, blank=True, null=True)
	message_status=models.BooleanField(default=False)
	date_sent=models.DateTimeField(max_length=20)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		verbose_name = 'Message'
		verbose_name_plural = 'Messages'

	def __str__(self):
		today=str(self.date_sent).split('.',2)
		date_today=today[0]
		return self.sender + ' '+ date_today
    

#car model
class car(models.Model):
	brand = models.CharField(max_length=500)
	price = models.FloatField(max_length=20)
	name = models.CharField(max_length=1000)
	car_image = models.ImageField(upload_to='images/')

	#string representation
	def __str__(self):
		return self.name
#booking model for a car
class Booking(models.Model):
	requestUser = models.ForeignKey(User, on_delete=models.CASCADE)
	car_booked = models.ForeignKey(car,on_delete=models.CASCADE)
	time_booked = models.DateTimeField(max_length=20)
	rental_city = models.CharField(max_length=1000)
	book_status = models.BooleanField(default=False)
	return_date = models.DateTimeField(max_length=20)
	instructions = models.TextField(max_length=1000)
	#hire_type = models.CharField(max_length=100)

	def __str__(self):
		return self.requestUser.username

#all public chats
class publichat(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    time_sent=models.DateTimeField()
    chat_status=models.BooleanField(default=False)

    class Meta:
    	verbose_name = 'public-chat'
    	verbose_name_plural = 'Public Chats'

    def __str__(self):
        today=str(self.time_sent).split('.',2)
        date_today=today[0]
        return  str(self.user)

#all sites
class site(models.Model):
	name = models.CharField(max_length=500)
	site_image = models.ImageField(upload_to='images/')
	location = models.CharField(max_length=500)
	description = models.CharField(max_length=2000)
	site_type = models.CharField(max_length=500)

	class Meta:
		verbose_name = 'Attraction site'
		verbose_name_plural = 'Attraction Sites'
	def __str__(self):
		return self.name
#all activities		
class Activity(models.Model):
	activityName = models.CharField(max_length=500)
	activity_image = models.ImageField(upload_to='images/')
	location = models.CharField(max_length=500)
	activity_description = models.CharField(max_length=2000)

	class Meta:
		verbose_name = 'Activitity'
		verbose_name_plural = 'Activities'

	def __str__(self):
		return self.activityName
#all events	 
class Event(models.Model):
	eventName = models.CharField(max_length=500)
	event_image = models.ImageField(upload_to='images/')
	event_location = models.CharField(max_length=500)
	event_description = models.CharField(max_length=2000)

	class Meta:
		verbose_name = 'Event'
		verbose_name_plural = 'Events'

	def __str__(self):
		return self.eventName
	
#all booking for a tour guide
class Booking_guide(models.Model):
	pending = 0
	succesful = 1
	declined = 2

	guide_choices = (
		(pending, ('pending')),
		(succesful, ('succesful')),
		(declined, ('declined')),

		)   	
	touristguide = models.ForeignKey(Profile, on_delete=models.CASCADE)
	tourist = models.ForeignKey(User, on_delete=models.CASCADE)
	arrival = models.DateTimeField()
	staytime = models.CharField(max_length=20)
	instructions = models.CharField(max_length=1000)
	book_status = models.BooleanField(default=False)
	if_read = models.BooleanField(default=False)
	guide_response = models.PositiveSmallIntegerField(choices=guide_choices,default=pending)
	sites = models.ManyToManyField(site,blank=True)
	activities = models.ManyToManyField(Activity,blank=True)
	events = models.ManyToManyField(Event,blank=True)
	#departure = models.DateField(default='NO SUBJECT')
	#created_date = DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name = 'Booking Tour Guide'
		verbose_name_plural = 'Bookings for Tour Guide'

	def __str__(self):
		return self.tourist.username
class Guide_application(models.Model):
	applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
	id_copy = models.FileField(upload_to='documents/', default='document')
	application_time = models.DateTimeField()

	class Meta:
		verbose_name = 'Guide application'
		verbose_name_plural = 'Guide applications'

	def __str__(self):
		return self.applicant.firstname
		
