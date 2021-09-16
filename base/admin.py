from django.contrib import admin
from .models import Booking, OnlineClass, UserProfile,RegisterStudentForOnlineClass
# Register your models here.


admin.site.register(Booking)
admin.site.register(OnlineClass)
admin.site.register(UserProfile)
admin.site.register(RegisterStudentForOnlineClass)
