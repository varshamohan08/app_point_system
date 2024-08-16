from rest_framework import serializers
from appdetails_app.models import App, AppCategory #, AppSubCategory
from tasks_app.models import TaskDetails
from user_app.serializers import UserSerializer
{
    "name": "Social",
    "category": 1
}
class AppCategorySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = AppCategory
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = str(representation['name']).title()
        representation['select_bln'] = False
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        validated_data['name'] = str(request.data.get('name')).title()
        instance = AppCategory.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for attr, value in validated_data.items():
            if attr == 'name':
                value = str(value).title()
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty")
        return value

# class AppSubCategorySerializer(serializers.ModelSerializer):
#     created_by = UserSerializer(read_only=True)
#     category = AppCategorySerializer(read_only=True)

#     class Meta:
#         model = AppSubCategory
#         fields = '__all__'

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         return representation

#     def create(self, validated_data):
#         request = self.context.get('request')
        
#         try:
#             category = AppCategory.objects.get(id=request.data.get("category"))
#         except AppCategory.DoesNotExist:
#             raise serializers.ValidationError("Invalid category_id provided.")
        
#         validated_data['created_by'] = request.user
#         validated_data['category'] = category
#         instance = AppSubCategory.objects.create(**validated_data)
#         return instance

#     def update(self, instance, validated_data):
#         request = self.context.get('request')
#         category_id = validated_data.get("category_id")

#         try:
#             category = AppCategory.objects.get(category_id=category_id)
#         except AppCategory.DoesNotExist:
#             raise serializers.ValidationError("Invalid category_id provided.")
        
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
        
#         instance.updated_by = request.user
#         instance.save()
#         return instance

#     def validate_name(self, value):
#         if not value.strip():
#             raise serializers.ValidationError("Name cannot be empty")
#         return value


class AppSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    category = AppCategorySerializer(read_only=True)
    sub_category = AppCategorySerializer(read_only=True)  # Same serializer, different field
    icon = serializers.ImageField(read_only=True, required=False)
    
    class Meta:
        model = App
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = str(representation['name']).title()
        if TaskDetails.objects.filter(app_id=representation.get('id'), created_by=representation.get('created_by', {}).get('id')).exists():
            representation['task_completed_bln'] = True
            representation['task_completed_bln'] = True

        return representation

    def create(self, validated_data):

        request = self.context.get('request')
        validated_data['created_by'] = request.user

        if 'icon' in request.FILES:
            validated_data['icon'] = request.FILES['icon']

        category_id = request.data.get('category')
        sub_category_id = request.data.get('sub_category')

        category = AppCategory.objects.get(id=category_id)
        sub_category = AppCategory.objects.get(id=sub_category_id)

        validated_data['category'] = category
        validated_data['sub_category'] = sub_category
        validated_data['name'] = str(request.data.get('name')).title()
        
        instance = App.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        # import ipdb; ipdb.set_trace()
        print("up")
        request = self.context.get('request')

        if 'icon' in request.FILES:
            if instance.icon:
                instance.icon.delete(save=False)

            instance.icon = request.FILES['icon']

        

        for attr, value in validated_data.items():
            if attr != 'icon':
                if attr == 'name':
                    value = str(value).title()
                setattr(instance, attr, value)

        instance.updated_by = request.user
        instance.save()
        return instance

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty")
        return value
