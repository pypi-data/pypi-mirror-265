#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2024/3/31
from enum import Enum

from rest_framework_admin.role.configs import DefaultRoleView, RoleTypeEnum
from rest_framework_admin.user.configs import DefaultUserEnum

ROLE_SCOPE_TYPE = 'tenant'


class DefaultRoleEnum(Enum):
    owner = DefaultRoleView(id='0' * 28 + '1000', name='拥有者', weight=100)
    admin = DefaultRoleView(id='0' * 28 + '1001', name='管理员', weight=90)
    user = DefaultRoleView(id='0' * 28 + '1002', name='用户', weight=10)


DEFAULT_ROLE_DATA = {
    'create_user_id': DefaultUserEnum.owner.value.id,
    'type': RoleTypeEnum.builtin.name,
    'scope_type': ROLE_SCOPE_TYPE
}
