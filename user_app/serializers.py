from rest_framework import serializers
from django.contrib.auth.models import User

from user_app.models import UserDetails

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)
    user_type = serializers.ChoiceField(choices=UserDetails.USER_TYPE_CHOICES, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'user_type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['userdetails'] = UserDetails.objects.get(user = instance)
        if not representation['userdetails'].profile_pic:
            representation['userdetails'].profile_pic = '/media/profile_pic.jpg'
        return representation

    def validate(self, data):
        email = data.get('email')
        instance = self.instance

        if User.objects.exclude(pk=instance.pk if instance else None).filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")

        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_type = validated_data.pop('user_type', 'user')

        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
        instance.username = instance.email
        instance.save()

        UserDetails.objects.create(user=instance, user_type=user_type)

        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
        instance.username = instance.email
        instance.save()
        return instance
