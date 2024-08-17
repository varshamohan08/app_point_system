from rest_framework import serializers
from django.contrib.auth.models import User
from user_app.models import UserDetails

# Serializer for the UserDetails model
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['user_type', 'profile_pic']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.profile_pic:
            representation['profile_pic'] = '/media/profile_pic.jpg'  # Default profile pic
        return representation

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)
    user_type = serializers.ChoiceField(choices=UserDetails.USER_TYPE_CHOICES, write_only=True, required=False)
    userdetails = UserDetailsSerializer(read_only=True)  # Nested UserDetailsSerializer

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'user_type', 'userdetails']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
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
