from rest_framework import serializers
from appdetails_app.models import App
from appdetails_app.serializers import AppSerializer
from tasks_app.models import TaskDetails
from user_app.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%A %B %d %Y %I:%M %p")
    app = AppSerializer(read_only=True)

    class Meta:
        model = TaskDetails
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def create(self, validated_data):
        # import pdb;pdb.set_trace()
        request = self.context.get('request')

        if 'screenshot' in request.FILES:
            validated_data['screenshot'] = request.FILES['screenshot']

        validated_data['created_by'] = request.user

        app_id = request.data.get('app_id')
        app = App.objects.get(id=app_id)
        validated_data['app'] = app

        instance = TaskDetails.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if 'screenshot' in request.FILES:
            if instance.screenshot:
                instance.screenshot.delete(save=False)

            instance.screenshot = request.FILES['screenshot']

        for attr, value in validated_data.items():
            if attr != 'screenshot':
                setattr(instance, attr, value)

        instance.updated_by = request.user
        instance.save()
        return instance

    # def validate_name(self, value):
    #     if not value:
    #         raise serializers.ValidationError("Name cannot be empty")
    #     return value
