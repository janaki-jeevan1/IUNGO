# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


# Register your models here.

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'location']
    search_fields = ['user']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']


class WalkinCustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email']
    search_fields = ['name']


class DesignAdmin(admin.ModelAdmin):
    list_display = ['design_name', 'user']
    search_fields = ['user']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'user']
    search_fields = ['user']


SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(sub_category, SubCategoryAdmin)
admin.site.register(WalkinCustomer, WalkinCustomerAdmin)
admin.site.register(Design, DesignAdmin)
admin.site.register(Project, ProjectAdmin)
