from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication,permissions
from rest_framework import serializers

from api.serializers import UserSerializer,TodoSerialziser

from todoapp.models import Todos

class RegistrationView(APIView):

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class TodosView(ViewSet):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self,request,*args,**kwargs):
        serializer=TodoSerialziser(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
         
    def list(self,request,*args,**kwargs):
        # list todos of logged-in user
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerialziser(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.user != request.user:
            raise serializers.ValidationError("permission denied")
        else:
            todo_object.delete()
            return Response(data={"message":"deleted....."})    
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerialziser(data=request.data,instance=qs)
        if qs.user != request.user:
            raise serializers.ValidationError("permission denied")
        elif serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerialziser(qs)
        return Response(data=serializer.data)
    