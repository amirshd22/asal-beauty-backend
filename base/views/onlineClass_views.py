from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
import requests
from base.serializers import OnlineClassesSerializer,RegisterForClassSerializer
from base.models import OnlineClass,RegisterStudentForOnlineClass,UserProfile
from datetime import datetime
import json


@api_view(['GET'])
def getAllClasses(request):
    classes = OnlineClass.objects.all()
    serializer = OnlineClassesSerializer(classes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def createOrderForOnlineClasses(request):
    user = request.user
    data = request.data
    Class = OnlineClass.objects.get(id= data["classId"])

    orderCred = {
        'pin' : 'DDEDA3FDE514AC556515',
        'amount' : int(Class.totalPrice)*float(Class.hasOff),
        'callback' : 'http://localhost:3000/verify/',   
    }
    if len(user.userprofile.onlineClass.all()) == 0: 
            try:
                response = requests.post("https://panel.aqayepardakht.ir/api/create", data=orderCred)
                if response.status_code == 200 and not response.text.replace('-',"").isdigit():
                    registeredClass = RegisterStudentForOnlineClass.objects.create(
                        user=user,
                        totalPrice = int(Class.totalPrice),
                        transId = response.text,
                        onlineClassName= Class
                    )
                    serializer = RegisterForClassSerializer(registeredClass , many=False)
                    print(serializer.data)
                    return Response(serializer.data)
                else:
                    return Response({"details": "درخواست با خطا مواجه شد"} , status= status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"details": f"{e}"})
    else:
        for i in user.userprofile.onlineClass.all():
            if i.id == Class.id:
                return Response({"details": "شما در این کلاس ثبت نام کرده اید"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    response = requests.post("https://panel.aqayepardakht.ir/api/create", data=orderCred)
                    if response.status_code == 200 and not response.text.replace('-',"").isdigit():
                        registeredClass = RegisterStudentForOnlineClass.objects.create(
                            user=user,
                            totalPrice = int(Class.totalPrice),
                            transId = response.text,
                            onlineClassName= Class
                        )
                        serializer = RegisterForClassSerializer(registeredClass , many=False)
                        print(serializer.data)
                        return Response(serializer.data)
                    else:
                        return Response({"details": "درخواست با خطا مواجه شد"} , status= status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({"details": f"{e}"})

        
    return Response({"details":f"{Class}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getOrderById(request, pk):
    user = request.user
    try:
        order= RegisterStudentForOnlineClass.objects.get(transId=pk)
        if user == order.user:
            serializer = RegisterForClassSerializer(order , many=False)
            return Response(serializer.data)
        else:
            return Response({"details": "Not authorize to view this order"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'details': "Order does not exist"}, status= status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def verifyPaidCondition(request, transId):
    user = request.user
    registeredClass = RegisterStudentForOnlineClass.objects.get(transId=transId)
    profile = UserProfile.objects.get(user=user)
    className = OnlineClass.objects.get(name=registeredClass.onlineClassName.name)
    data = {
    'pin' : 'DDEDA3FDE514AC556515',
    'amount' : int(registeredClass.totalPrice),
    'transid' : registeredClass.transId
    }
    
    try:
        response = "1"
        # response = requests.post('https://panel.aqayepardakht.ir/api/verify', data = data)
        if response == "1":
            try:
                skyroomData = {
                    "action": "createUser",
                    "params": {
                        "username": str(user.email),
                        "password": "123456",
                        "nickname": str(user.first_name),
                    }
                }
                jsonSkyRoomData = json.dumps(skyroomData, indent=2)
                headers = {
                    "Content-Type": "application/json; charset=utf-8"
                }
                skyroom_response = requests.post("https://www.skyroom.online/skyroom/api/apikey-12365665-1-d012a4625c525a18d033a7a62939d170",data=jsonSkyRoomData, headers=headers)
                print(skyroom_response.content)
                print(jsonSkyRoomData)
                if b'{"ok":true' in skyroom_response.content:
                    profile.username = user.email
                    profile.password = "123456"
                    registeredClass.isPaid = True
                    registeredClass.paidAt = datetime.now()
                    registeredClass.registered = True
                    profile.onlineClass.set([className]) 
                    profile.save()
                    registeredClass.save()
                    return Response({"message": "پرداخت با موفقیت انجام شد"}, status=status.HTTP_200_OK)
                else:
                    return Response({"details": skyroom_response.text})
            except Exception as e:
                return Response(f"{e}")
        elif response.status_code == 200 and response.text =='0':
            print(response, "else if error")
            return Response({"details": "پرداخت با موفقیت انجام نشد"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(response, "else Error")
            return Response({"details": response.text}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f"error {e}")
