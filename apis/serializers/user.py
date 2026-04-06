from django.contrib.auth import get_user_model
from rest_framework import serializers

User=get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['email','password1','password2']

    def validate(self,data):
        if data['password1']!=data['password2']:
            raise serializers.ValidationError("password don't match")
        return data

    def create(self,validated_data):
        user=User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password1')
            # role is set default to customer
        )
        return user
