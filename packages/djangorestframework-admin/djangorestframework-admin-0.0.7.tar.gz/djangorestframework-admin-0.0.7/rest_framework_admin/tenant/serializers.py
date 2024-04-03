#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/17
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_admin.role.configs import SubjectTypeEnum
from rest_framework_admin.role.models import RoleSubjectRel, Role
from rest_framework_admin.tenant.configs import DefaultRoleEnum
from rest_framework_admin.user.models import User
from rest_framework_util.serializers import (
    BaseSwitchModelSerializer,
    BaseModelSerializer,
    BaseRelatedModelSerializer,
    BaseSelectionModelSerializer,
    BaseRelModelSerializer)
from rest_framework_admin.tenant.models import Tenant, TenantUserRel


class TenantModelSerializer(BaseModelSerializer, serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=64, validators=[
            UniqueValidator(
                queryset=Tenant.objects.filter())])
    config = serializers.JSONField(default={})

    class Meta(BaseModelSerializer.Meta):
        model = Tenant
        fields = BaseModelSerializer.Meta.fields + \
            ('user_count', 'config')

    def create(self, validated_data):
        instance = super().create(validated_data)
        rel = TenantUserRel(
            user=instance.create_user,
            tenant=instance,
            create_user=instance.create_user
        )
        rel.save()
        role_rel = RoleSubjectRel(
            subject_id=instance.create_user.id,
            subject_type=SubjectTypeEnum.user.name,
            role=Role.objects.get(id=DefaultRoleEnum.owner.value.id),
            scope_id=instance.id,
            create_user=instance.create_user
        )
        role_rel.save()
        return instance


class RelatedTenantModelSerializer(BaseRelatedModelSerializer):
    class Meta(BaseRelatedModelSerializer.Meta):
        model = Tenant


class SwitchTenantModelSerializer(BaseSwitchModelSerializer):

    class Meta(BaseSwitchModelSerializer.Meta):
        model = Tenant


class SelectionTenantModelSerializer(BaseSelectionModelSerializer):

    class Meta(BaseSelectionModelSerializer.Meta):
        model = Tenant


class TenantRelatedUserModelSerializer(BaseRelModelSerializer):
    id = serializers.CharField(source='user_id', read_only=True)
    name = serializers.CharField(source='user__username', read_only=True)
    user_ids = serializers.ListField(
        min_length=1,
        max_length=10,
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()))

    class Meta(BaseModelSerializer.Meta):
        model = TenantUserRel
        fields = BaseModelSerializer.Meta.fields + ('user_ids', )
        read_only_fields = BaseModelSerializer.Meta.read_only_fields

    def create(self, validated_data):
        for user in validated_data.pop('user_ids'):
            instance = TenantUserRel.objects.filter(
                user_id=user.id,
                tenant_id=validated_data['tenant_id']).first()
            if instance is None:
                validated_data['user_id'] = user.id
                instance = super().create(validated_data)
        return instance
