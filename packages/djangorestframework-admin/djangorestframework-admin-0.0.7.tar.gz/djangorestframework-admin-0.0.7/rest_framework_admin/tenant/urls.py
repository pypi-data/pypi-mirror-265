#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/17
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['urlpatterns']

from django.urls import path, include, re_path
from rest_framework import routers

from rest_framework_admin.tenant import views

tenant_router = routers.DefaultRouter()
tenant_router.register(r'^tenants', views.TenantModelViewSet)

tenant_related_user_router = routers.DefaultRouter()
tenant_related_user_router.register(
    r'^users',
    views.TenantRelatedUserModelViewSet,
    basename='tenant_related_user_router')


urlpatterns = [
    path(r'', include(tenant_router.urls)),
    re_path(
        r'tenants/(?P<tenant_id>[a-z0-9A-Z\-]{32})/',
        include(
            tenant_related_user_router.urls)),
]
