from rest_framework import serializers
from .models import Todo
from django.template.defaultfilters import slugify


class TodoSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        # fields = "__all__"
        exclude = ['created_at', 'updated_at']

    def get_slug(self, obj):
        return slugify(obj.todo_title)

    def validate(self, validated_data):
        if validated_data.get('todo_title'):
            todo_title = validated_data['todo_title']
            if len(todo_title) <= 2:
                raise serializers.ValidationError(
                    "Todo Title must be more than 2 characters.")
        return validated_data
