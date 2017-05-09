from human.models import *
from human.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import datetime

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

class AttendanceList(APIView):
    def post(self, request, format=None):
        request.data['date'] = request.data.get('date', datetime.datetime.now()) 
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendanceDetail(APIView):
    def get_object(self, pk, **params):
        try:
            return Attendance.objects.filter(user=pk, **params)
        except UserAsset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        filters = {}
        for param in request.query_params:
            filters[param] = request.query_params[param]
        print(filters)
        Attendance = self.get_object(pk, **filters)
        serializer = AttendanceSerializer(Attendance, many=True)
        return Response(serializer.data)

class VacationDetail(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        print(request.data['start'].split('-'))
        user = request.data['user']
        start = request.data['start'].split('-')
        end = request.data['end'].split('-')
        days = (datetime.datetime(int(end[0]), int(end[1]), int(end[2])) - datetime.datetime(int(start[0]), int(start[1]), int(start[2]))).days
        serializers = []
        flag = True
        for x in range(days + 1):
            data = {
                'date': (datetime.datetime(int(start[0]), int(start[1]), int(start[2]), 0 , 0 ,0) + datetime.timedelta(days = x)),
                'user': user,
                'status': 4
            }
            serializer = AttendanceSerializer(data=data)
            serializers.append(serializer)

        print(serializers)
        for serializer in serializers:
            if not serializer.is_valid():
                flag = False
        
        if flag:
            for serializer in serializers:
                serializer.save()
            return Response({"message": "success", "error": 0})
        else:
            return Response({"message": "error", "error": 1})
                

        