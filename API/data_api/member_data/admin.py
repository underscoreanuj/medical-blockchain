from django.contrib import admin
from .models import Member, Episode, Medical, Emergency, Pharmacy, Lab

admin.site.register(Member)
admin.site.register(Episode)
admin.site.register(Medical)
admin.site.register(Emergency)
admin.site.register(Pharmacy)
admin.site.register(Lab)
