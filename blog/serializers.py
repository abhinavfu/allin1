from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class BlogerSerializer(serializers.ModelSerializer):
    pic = serializers.FileField()
    class Meta:
        model = Bloger
        fields = '__all__'

    def validate(self, validated_data):
        if validated_data.get('name'):
            name = validated_data['name']
            if len(name) <= 2:
                raise serializers.ValidationError(
                    "Name must be more than 2 characters.")
        if validated_data.get('pic'):
            pic = validated_data['pic']
            if not str(pic).lower().endswith((".jpg" , ".jpeg" , ".png")):
                raise serializers.ValidationError(
                    "File is not supported")
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


class CreatePostSerializer(serializers.ModelSerializer):
    pic1 = serializers.FileField()
    class Meta:
        model = CreatePost
        fields = '__all__'

    def validate(self, validated_data):
        if validated_data.get('title'):
            title = validated_data['title']
            if len(title) <= 2:
                raise serializers.ValidationError(
                    "Title must be more than 2 characters.")
        if validated_data.get('pic1'):
            pic1 = validated_data['pic1']
            if not str(pic1).lower().endswith((".jpg" , ".jpeg" , ".png",".mp4",".mpeg")):
                raise serializers.ValidationError(
                    "File is not supported")
        return validated_data



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
