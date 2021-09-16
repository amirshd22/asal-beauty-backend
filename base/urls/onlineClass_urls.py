from django.urls import path
from base.views import onlineClass_views as views


urlpatterns  =  [
    path("", views.getAllClasses, name="getAllClasses"),
    path("class/<str:pk>/", views.getOrderById, name="getOrderById"),
    path("create/", views.createOrderForOnlineClasses, name="create"),
    path("verify/<str:transId>/", views.verifyPaidCondition, name="verify"),

]