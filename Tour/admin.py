from django.contrib import admin
from .models import Profile, update, hotel, message, car, Booking, publichat, Booking_guide, TourGuide_Likes, site, Activity, Event, Guide_application

# Register your models here.
admin.site.site_title="Kenya Tours admin"
admin.site.site_header="Kenya Tours Administration Portal"
admin.site.index_title="Welcome To Kenya Tours administration Portal"
admin.site.register(Profile)
class updateAdmin(admin.ModelAdmin):
	list_display = ('headline', 'date_uploaded')
admin.site.register(update, updateAdmin)
admin.site.register(hotel)
admin.site.register(message)
#admin.site.register(car)
#admin.site.register(Booking)
admin.site.register(publichat)
admin.site.register(Booking_guide)
admin.site.register(TourGuide_Likes)
admin.site.register(site)
admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(Guide_application)
