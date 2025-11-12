from rest_framework import serializers
from .models import CustomUser, Role, Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class RoleSerializer(serializers.ModelSerializer):
    # Permite asignar permisos por ID al crear/editar
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        write_only=True
    )
    # Muestra detalle de permisos al hacer GET
    permissions_detail = PermissionSerializer(source='permissions', many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions', 'permissions_detail']


class CustomUserSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        source='role',
        queryset=Role.objects.all(),
        write_only=True
    )
    roles = RoleSerializer(source='role', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'password',
            'lastname',
            'country',
            'email',
            'role_id',
            'roles'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }


    def create(self, validated_data):
        request_user = self.context['request'].user
        if not request_user.is_admin() and validated_data.get('role') and validated_data['role'].name == 'Admin':
            raise serializers.ValidationError("No podés asignar el rol Admin")

        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user




    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['username'] = attrs.get('email')  # reusar como username
        return super().validate(attrs)
