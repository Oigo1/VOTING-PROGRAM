from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Contestant)
admin.site.register(Vote)
admin.site.register(Category)