from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


# from ..models import Product,Order,OrderItem,ShippingAddress,Reviews
from ..serializers import  UserSerializer, UserSerializerWithToken

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView



class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        username = data.get('email')
        email = data.get('email')
        password = data.get('password')
        firstName = data.get("firstName")
        lastName= data.get("lastName")
        messages = {'errors':[]}
        if username == None:
            messages['errors'].append('username can\'t be empty')
        if email == None:
            messages['errors'].append('Email can\'t be empty')
        if password == None:
            messages['errors'].append('Password can\'t be empty')
        if User.objects.filter(email=email).exists():
            messages['errors'].append("Account already exists with this email id.")    
        if User.objects.filter(username__iexact=username).exists():
            messages['errors'].append("Account already exists with this username.") 
        if len(messages['errors']) > 0:
            return Response({"details":messages['errors']},status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                first_name= firstName,
                last_name =lastName,

            )
            serializer = UserSerializerWithToken(user, many=False)
        except Exception as e:
            print(e)
            return Response({'details':f'{e}'},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['name'] = user.first_name
        token['id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def profile(request):
    user = request.user
    serializer = UserSerializer(user , many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def updateUserProfile(request):
    user = request.user

    data = request.data
    user.first_name = data["firstName"]
    user.last_name = data["lastName"]
    user.username = data["email"]
    user.email = data["email"]

    if data["password"] != "":
        user.password = make_password(data["password"])

    user.save()

    serializer = UserSerializerWithToken(user , many=False)
    return Response(serializer.data)