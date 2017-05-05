from human.models import *
from human.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


# Create your views here.

class UserDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
        
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoDetail(APIView):
    def get_object(self, pk):
        try:
            return UserInfo.objects.get(user=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

class SalaryList(APIView):
    def get_object(self, pk):
        try:
            return Salary.objects.filter(user=pk)
        except Salary.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        salary = self.get_object(pk)
        serializer = SalarySerializer(salary, many=True)
        return Response(serializer.data)

class AssetList(APIView):
    def get_object(self, pk):
        try:
            return UserAsset.objects.filter(user=pk)
        except UserAsset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        userAsset = self.get_object(pk)
        serializer = UserAssetSerializer(userAsset, many=True)
        return Response(serializer.data)
