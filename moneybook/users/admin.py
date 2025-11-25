from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # 리스트에서 보이는 컬럼
    list_display = (
        "username",
        "email",
        "phone",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )

    # 기본 UserAdmin의 fieldsets + 커스텀 필드
    fieldsets = BaseUserAdmin.fieldsets + (
        ("추가 정보", {"fields": ("phone",)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("추가 정보", {"fields": ("phone",)}),
    )
