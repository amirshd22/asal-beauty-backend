from rest_framework import serializers
from .models import UserProfile,RegisterStudentForOnlineClass,Booking,OnlineClass
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class OnlineClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineClass
        fields = "__all__"



class UserProfileSerializer(serializers.ModelSerializer):
    onlineClass = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'
    def get_onlineClass(self,obj):
        onlineClass = obj.onlineClass.all()
        serializer = OnlineClassesSerializer(onlineClass , many=True)
        return serializer.data
    


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'is_superuser', 'is_staff', "first_name", "last_name","email"]

    def get_profile(self, obj):
        profile = obj.userprofile
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data


class UserSerializerWithToken(UserSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "is_staff","access","profile","refresh"]

    def get_profile(self, obj):
        profile = obj.userprofile
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data
    
    def get_access(self, obj):
        token = RefreshToken.for_user(obj)
        token['email'] = obj.email
        token['username'] = obj.username
        token['name'] = obj.first_name
        token['id'] = obj.id
        return str(token.access_token)
    
    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)



class RegisterForClassSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    onlineClassName = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model=RegisterStudentForOnlineClass
        fields ='__all__'

    def get_onlineClassName(self,obj):
        onlineClass= obj.onlineClassName
        serializer = OnlineClassesSerializer(onlineClass, many=False)
        return serializer.data

    def get_user(self,obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
