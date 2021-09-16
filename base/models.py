from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

# Todo just remember to add selected days and sessions and also services

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    transId = models.CharField(max_length=500, null=True , blank=True)
    isPaid= models.BooleanField(default=False)
    paidAt=  models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt=  models.DateTimeField(auto_now_add=True)
    selectedDay= models.CharField(max_length=500, null=True , blank=True)
    selectedSession= models.CharField(max_length=500, null=True , blank=True)
    selectedService= models.CharField(max_length=500, null=True , blank=True)
    def __str__(self):
        return f"{self.selectedDay}-{self.user.first_name}"



class OnlineClass(models.Model):
    name = models.CharField(max_length=500 , null=True , blank=True)
    amountOfStudents = models.IntegerField(null=True , blank=True)
    available = models.BooleanField(default=False, null=True, blank=True)
    totalPrice = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True , blank=True)
    hasOff = models.CharField(max_length=500 , null=True , blank=True)
    roomId= models.CharField(max_length=500 , null=True , blank=True)
    teacher = models.CharField(max_length=500 , null=True , blank=True)
    def __str__(self):
        return self.name


class RegisterStudentForOnlineClass(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    onlineClassName = models.ForeignKey(OnlineClass, on_delete=models.CASCADE, null=True)
    isPaid= models.BooleanField(default=False)
    paidAt=  models.DateTimeField(auto_now_add=False, null=True, blank=True)
    totalPrice = models.IntegerField(null=True, blank=True)
    createdAt=  models.DateTimeField(auto_now_add=True)
    registered = models.BooleanField(default=False, null=True , blank=True)
    transId = models.CharField(max_length=500, null=True , blank=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.registered}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    onlineClass = models.ManyToManyField(OnlineClass, related_name="onlineClass",blank=True)
    phoneNumber = models.CharField(max_length=500, null=True , blank=True)
    username = models.CharField(max_length=500, null=True , blank=True)
    password = models.CharField(max_length=500, null=True , blank=True)

    def __str__(self):
        return self.user.username