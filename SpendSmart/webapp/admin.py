from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Attachment)
admin.site.register(Borrows)
admin.site.register(Category)
admin.site.register(Credentials)
admin.site.register(Monthlycategorybudget)
admin.site.register(Split)
admin.site.register(Transaction)
admin.site.register(User)