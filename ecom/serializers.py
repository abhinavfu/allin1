from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class BuyerSerializer(serializers.ModelSerializer):
    pic = serializers.FileField()
    class Meta:
        model = Buyer
        fields = '__all__'
        
    def validate(self, validated_data):
        if validated_data.get('name'):
            name = validated_data['name']
            if len(name) <= 2:
                raise serializers.ValidationError("Name must be more than 2 characters.")
        
        file_format = (".jpg" , ".jpeg" , ".png")
        if validated_data.get('pic'):
            pic = validated_data['pic']
            if not str(pic).lower().endswith(file_format):
                raise serializers.ValidationError(
                    f"File is not supported. Supported files extensions : {file_format}")
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class ProductSerializer(serializers.ModelSerializer):
    pic1 = serializers.FileField()
    pic2 = serializers.FileField()
    pic3 = serializers.FileField()
    pic4 = serializers.FileField()
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, validated_data):
        if validated_data.get('name'):
            name = validated_data['name']
            if len(name) <= 2:
                raise serializers.ValidationError("Name must be more than 2 characters.")
        if validated_data.get('price'):
            price = validated_data['price']
            if price <= 1:
                raise serializers.ValidationError("Price must be greater than 1.")
        if validated_data.get('discount'):
            discount = validated_data['discount']
            if discount < 0:
                raise serializers.ValidationError("Discount must be zero or greater than zero.")
        
        # for image or video files extension validation
        file_format = (".jpg" , ".jpeg" , ".png", ".avif", ".mp4", ".mpeg")
        if validated_data.get('pic1'):
            pic = validated_data['pic1']
            if not str(pic).lower().endswith(file_format):
                raise serializers.ValidationError(
                    f"File is not supported. Supported files extensions : {file_format}")
        if validated_data.get('pic2'):
            pic = validated_data['pic2']
            if not str(pic).lower().endswith(file_format):
                raise serializers.ValidationError(
                    f"File is not supported. Supported files extensions : {file_format}")
        if validated_data.get('pic3'):
            pic = validated_data['pic3']
            if not str(pic).lower().endswith(file_format):
                raise serializers.ValidationError(
                    f"File is not supported. Supported files extensions : {file_format}")
        if validated_data.get('pic4'):
            pic = validated_data['pic4']
            if not str(pic).lower().endswith(file_format):
                raise serializers.ValidationError(
                    f"File is not supported. Supported files extensions : {file_format}")
        return validated_data



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
    
    def validate(self, validated_data):
        if validated_data.get('name'):
            name = validated_data['name']
            if len(name) <= 2:
                raise serializers.ValidationError("Name must be more than 2 characters.")
        return validated_data

class ShipmentSerializer(serializers.ModelSerializer):
    pic = serializers.FileField()
    class Meta:
        model = Shipment
        fields = '__all__'
    
    def validate(self, validated_data):
        if validated_data.get('name'):
            name = validated_data['name']
            if len(name) <= 2:
                raise serializers.ValidationError("Name must be more than 2 characters.")
            
        file_format = (".jpg" , ".jpeg" , ".png")
        if validated_data.get('pic'):
            pic = validated_data['pic']
            if not str(pic).lower().endswith(file_format):
                raise serializers.ValidationError(
                    f"File is not supported. Supported files extensions : {file_format}")
        return validated_data    