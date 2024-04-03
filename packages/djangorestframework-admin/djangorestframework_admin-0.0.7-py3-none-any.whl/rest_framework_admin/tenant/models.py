from django.contrib.auth import get_user_model
from django.db import models

from rest_framework_util.db.models.base import BaseModel, BaseRelModel


# Create your models here.
class Tenant(BaseModel):
    code = models.CharField('编码', max_length=64)
    config = models.JSONField('配置')

    user_rels = models.ManyToManyField(
        get_user_model(), through='TenantUserRel', through_fields=(
            'tenant', 'user'), related_name='tenant_rels')

    class Meta:
        db_table = 'admin_tenant'
        verbose_name = '租户表'

    def extended_strs(self):
        return [f'code={self.code}']

    @property
    def user_count(self):
        return self.user_rels.count()


class TenantUserRel(BaseRelModel):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    tenant = models.ForeignKey(Tenant, models.CASCADE)

    class Meta:
        db_table = 'admin_tenant_user_rel'
        verbose_name = '租户用户关联表'
        unique_together = ('user', 'tenant', 'delete_datetime')

    def extended_strs(self):
        return [f'tenant_id={self.tenant.id})', f'user_id={self.user.id}']
