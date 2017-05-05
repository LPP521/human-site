from rest_framework import serializers
from django.contrib.auth.models import User
from human.models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name', )

class UserInfoSerializer(serializers.ModelSerializer):
    dep = DepartmentSerializer(read_only = True)
    class Meta:
        model = UserInfo
        fields = ('name', 'birth', 'dep', 'arms', 'level', 'vacation')

class UserSerializer(serializers.ModelSerializer):
    userinfo = UserInfoSerializer()
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email = validated_data.get('email')

        items = validated_data.get('userinfo')
        instance.userinfo.birth = items.get('birth')
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'userinfo')

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = ('date', 'salary', 'pension', 'medical', 'unemployment', 'housing', 'tax')

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ('name', 'mark', 'purchase')

class UserAssetSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only = True)
    class Meta:
        model = UserAsset
        fields = ('id', 'asset', 'borrow', 'back')
