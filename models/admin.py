#coding=utf-8
import json
from simplejson import dumps
from django.contrib import admin
from django.shortcuts import render_to_response

from .models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","card_number","student_number","username","usage","default_money")
    search_fields = ("student_number","username","card_number",)
    list_filter = ["usage"]

@admin.register(AmmeterGroup)
class AmmeterGroupAdmin(admin.ModelAdmin):
    list_display = ("id","ammeterGroup_number","ammeterGroup_name","valid_number","sum_number",)
    search_fields = ("ammeterGroup_number","ammeterGroup_name",)

@admin.register(Ammeter)
class AmmeterAdmin(admin.ModelAdmin):
    list_display = ("id","ammeter_number","name","status","group",)
    search_fields = ("ammeter_number","name","group",)
    list_filter = ["status"]


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    def display_charge_process(self,request,queryset):
        charge = queryset[0]
        nodes = Node.objects.filter(charge=charge)
        if(nodes):
            data = []
            for node in nodes:
                time = node.time
                dic = {"year":time.year,"month":time.month,"day":time.day,"hour":time.hour,"minute":time.minute,"second":time.second,"voltage":node.voltage_value,"current":node.current_value}
                data.append(dic)
                print u'电压：%s,电流：%s,时间：%s'% (node.voltage_value, node.current_value,node.time)
            return render_to_response("display_charge_process.html",{"data":json.dumps(data)})

    display_charge_process.short_description = u'展示充电过程（仅一条充电记录）'
    actions = ['display_charge_process']
    list_display = ("id","user","ammeter","status","start_time","end_time","overtime","message")
    search_fields = ("user__username","ammeter__ammeter_number",)
    list_filter = ["status"]

admin.site.register(Account)
admin.site.register(Node)

