from django.shortcuts import render
import json
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http.response import Http404, JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from .models import *
from .serializers import ddbserialize

# Create your views here.


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def index(request):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = "server is live, current time is :"
    return Response(data=message + date, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def Register(request):
    if request.method == "GET":
        interval = int(request.query_params.get("time_interval"))
        register = str(request.query_params.get("register"))
        if "RegisterValues" in register:
            registermodel = globals()[register]
            data = registermodel.objects.order_by("-id")[: ((interval * 60) / 5)][::-1]
            # print(data)
            serial = ddbserialize(data, many=True)
            # print(serial.data)
            return Response(data=serial.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def Register_card(request):
    if request.method == "GET":
        registers = []
        data = {}
        registermodel = globals()
        for key in registermodel:
            if "RegisterValues" in str(key):
                registers.append(key)
        for reg in registers:
            data.update({reg: globals()[reg].objects.all().last().active_power_tot})
        return JsonResponse(data)
