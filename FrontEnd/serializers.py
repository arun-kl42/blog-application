from rest_framework import serializers
from FrontEnd.models import BlogUser, Blog
from django.contrib.auth import get_user_model

User = get_user_model()


class CKEditorField(serializers.CharField):
    def to_internal_value(self, value):
        # Custom logic to handle CKEditor data if needed
        return super().to_internal_value(value)

    def to_representation(self, value):
        # Custom logic to represent CKEditor data if needed
        return super().to_representation(value)


class BlogUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = ['id', 'username', 'email', 'password', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        # If password is provided, hash it
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')  # Remove the password from validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BlogSerializers(serializers.ModelSerializer):
    description = CKEditorField()

    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ["id"]
