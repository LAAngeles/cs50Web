from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(New_Listings)
admin.site.register(add_watchlist)
admin.site.register(New_Coments)
admin.site.register(New_bid)
admin.site.register(close_listing_action)