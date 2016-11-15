from django.contrib import admin
from .models import Teacher, Vote, Student


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')

    class Meta:
        model = Teacher


class VoteAdmin(admin.ModelAdmin):
    list_display = ('get_teacher_name', 'get_username', 'create_time')

    def get_teacher_name(self, obj):
        return obj.teacher.name

    def get_username(self, obj):
        return obj.user.username

    get_teacher_name.admin_order_field = 'teacher'
    get_teacher_name.short_description = 'Teacher Name'
    get_username.admin_order_field = 'user'
    get_username.short_description = 'username'

    class Meta:
        model = Vote


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Student)