from rest_framework import serializers
from .models import App


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = "__all__"

    def validate(self, validated_data):
        if validated_data.get('points'):
            points = validated_data['points']
            if type(points) != int:
                raise serializers.ValidationError(
                    "Points must be integer type.")

        if validated_data.get('picapp'):
            picapp = validated_data['picapp']
            if str(picapp).endswith('.jpg') or str(picapp).endswith('.jpeg') or str(picapp).endswith('.png'):
                pass
            else:
                raise serializers.ValidationError(
                    "Picture must be in .jpeg or .jpg or .png format only.")
        return validated_data
