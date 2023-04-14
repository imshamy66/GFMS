from django.contrib import admin
from .models import *

@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ["id","name","username","phone","email","pincode","city","state"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id","name","phone","email","subject","message","status"]

@admin.register(NewsLatter)
class NewsLatter(admin.ModelAdmin):
    list_display = ["id","email"]

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ["id","name","pic"]

@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ["id","fund_title","state","status","username"]
