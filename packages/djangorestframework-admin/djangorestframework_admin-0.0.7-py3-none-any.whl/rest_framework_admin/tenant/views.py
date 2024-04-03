# Create your views here.
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_admin.tenant import serializers
from rest_framework_admin.tenant.filters import TenantFilter, TenantRelatedUserFilter
from rest_framework_admin.tenant.models import Tenant, TenantUserRel
from rest_framework_admin.tenant.permissions import TenantModelPermission, TenantRelatedUserModelPermission
from rest_framework_admin.tenant.serializers import TenantModelSerializer
from rest_framework_util.exceptions import HTTP403
from rest_framework_util.viewsets import BaseModeViewSet, BaseRelModelViewSet


@extend_schema_view(
    switch=extend_schema(summary='启用、禁用'),
)
class TenantModelViewSet(BaseModeViewSet):
    """ 租户管理 """
    queryset = Tenant.objects.filter().order_by('-create_datetime').all()
    serializer_class = TenantModelSerializer
    serializer_module = serializers
    filterset_class = TenantFilter
    search_fields = ['id', 'name']
    ordering_fields = ['name', 'create_datetime']
    permission_classes = (TenantModelPermission,)

    def perform_destroy(self, instance):
        if instance.user_rels.exists():
            raise HTTP403(_('存在关联用户，不允许删除'))
        instance.delete(delete_user_id=self.request.user.id)


@extend_schema_view()
class TenantRelatedUserModelViewSet(BaseRelModelViewSet):
    """ 关联的用户管理 """
    parent_model = Tenant
    lookup_field = 'user_id'
    queryset = TenantUserRel.objects.all()
    serializer_class = serializers.TenantRelatedUserModelSerializer
    filterset_class = TenantRelatedUserFilter
    search_fields = ['user__username', 'user__nickname']
    ordering_fields = [
        'create_datetime',
        'user__username',
        'user__create_datetime']
    ordering = ['-create_datetime']
    permission_classes = (TenantRelatedUserModelPermission,)
