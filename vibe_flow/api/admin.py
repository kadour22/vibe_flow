from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Notification)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Message)

