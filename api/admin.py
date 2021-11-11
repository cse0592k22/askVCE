from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import QuestionFlag, User, Department, Question, Tag, Answer, AnswerFlag


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'htno', 'user_name', 'first_name',
                     'last_name')
    list_filter = ('email', 'htno', 'user_name',
                   'first_name', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('htno', 'department', 'email', 'user_name', 'first_name',
                    'is_active', 'is_staff', )
    fieldsets = (
        (None, {'fields': ('htno', 'department', 'email',
         'user_name', 'first_name', 'last_name', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('phone', 'dob',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('htno', 'department', 'email', 'user_name', 'first_name', 'last_name', 'grad_year', 'password1', 'password2', 'is_staff', 'is_active',
                       'usefullness_score', 'phone', 'dob',)
        }),
    )


class DepartmentAdminConfig(admin.ModelAdmin):
    readonly_fields = ('code', 'name')


class QuestionAdminConfig(admin.ModelAdmin):
    model = Question
    list_display = ('title', 'scope',)


class AnswerAdminConfig(admin.ModelAdmin):
    model = Answer
    list_display = ('question',)


class AnswerFlagAdminConfig(admin.ModelAdmin):
    model = AnswerFlag
    list_display = ('user', 'reason',)


class QuestionFlagAdminConfig(admin.ModelAdmin):
    model = QuestionFlag
    list_display = ('question', 'reason',)


admin.site.register(Department, DepartmentAdminConfig)
admin.site.register(User, UserAdminConfig)
admin.site.register(Tag)
admin.site.register(Question, QuestionAdminConfig)
admin.site.register(QuestionFlag, QuestionFlagAdminConfig)
admin.site.register(Answer, AnswerAdminConfig)
admin.site.register(AnswerFlag, AnswerFlagAdminConfig)
