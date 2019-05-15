from django.contrib import admin
from .models import Savalgaa, Hemjee, Helber, Drug_type, Storage_condition, Partner, Other_staff, Ordered_drug, Ordered_staff, Drug_resource, Staff_resource
# Register your models here.

admin.site.register(Savalgaa)
admin.site.register(Hemjee)
admin.site.register(Helber)
admin.site.register(Drug_type)
admin.site.register(Storage_condition)
admin.site.register(Partner)
admin.site.register(Other_staff)
admin.site.register(Ordered_drug)
admin.site.register(Ordered_staff)
admin.site.register(Drug_resource)
admin.site.register(Staff_resource)
