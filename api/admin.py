from django.contrib import admin

from .models import Course, User, Participant


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'start_date')
    search_fields = ['name']
    list_filter = ['start_date']
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'role',
        'email')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
    list_editable = ('role',)


class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'course_name',
        'user')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Participant, ParticipantAdmin)
