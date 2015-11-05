from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from aikiblog.models import *


class AttackAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CustomUserAdmin(UserAdmin):
    list_display = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('email', 'avatar', 'first_name', 'last_name',
                                         'start_year', 'about_text', 'sex')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Groups'), {'fields': ('groups',)}),
    )


class DojoAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class SenseiAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class StandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class TechniqueAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class TechTrenAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date', 'stand', 'attack', 'technique',)
    exclude = ('slug',)


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('slug',)
    prepopulated_fields = {'slug': ('user', 'date', 'place')}


class TrainingCommentAdmin(admin.ModelAdmin):
    list_display = ('training', 'text')

admin.site.register(Attack, AttackAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Dojo, DojoAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Sensei, SenseiAdmin)
admin.site.register(Stand, StandAdmin)
admin.site.register(Technique, TechniqueAdmin)
admin.site.register(TechTren, TechTrenAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(TrainingComment, TrainingCommentAdmin)


