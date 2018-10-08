from django.contrib import admin
from .models import (User, Offer, Order, Source, SpecOccasion, Notes, Inclusions)


admin.site.register(User)
admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(Source)
admin.site.register(SpecOccasion)
admin.site.register(Notes)
admin.site.register(Inclusions)
