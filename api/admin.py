from django.contrib import admin
from .models import User, Kid, Teacher, Group, Journal, Attendance, MonthArchive
from .forms import MonthArchiveForm

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'role')
    search_fields = ('name', 'phone_number', 'role')
    list_filter = ('role',)

@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'date_of_birth', 'gender')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('gender',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone_number')
    search_fields = ('name', 'phone_number')
    list_filter = ('address',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher')
    search_fields = ('teacher__name',)
    list_filter = ('teacher',)
    filter_horizontal = ('kids',)

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'month', 'missday_cost', 'tarif', 'total_sum')
    search_fields = ('group__teacher__name', 'month')
    list_filter = ('group', 'month')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'kid', 'date', 'arrived')
    search_fields = ('kid__full_name', 'date')
    list_filter = ('date', 'arrived')

@admin.register(MonthArchive)
class MonthArchiveAdmin(admin.ModelAdmin):
    form = MonthArchiveForm
    list_display = ('id', 'year', 'month_name', 'kid', 'tarif', 'left_sum', 'missday_count', 'missday_cost', 'is_paid')
    search_fields = ('year', 'month_name', 'kid__full_name')
    list_filter = ('year', 'month_name', 'is_paid')
