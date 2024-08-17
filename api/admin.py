from django.contrib import admin
from .models import *
from .forms import MonthArchiveForm



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'role')
    search_fields = ('name', 'phone_number', 'role')
    list_filter = ('role',)

@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'date_of_birth', 'sex')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('sex',)

@admin.register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'phone_number')
    search_fields = ('name', 'phone_number')
    list_filter = ('salary',)

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

@admin.register(MonthArchive)
class MonthArchiveAdmin(admin.ModelAdmin):
    form = MonthArchiveForm
    list_display = ('id', 'year', 'month', 'kid', 'tarif', 'left_sum', 'missday_count', 'missday_cost', 'is_paid')
    search_fields = ('year', 'month', 'kid__full_name')
    list_filter = ('year', 'month', 'is_paid')
    exclude = ('missday_count','left_sum')

    def save_model(self, request, obj, form, change):
        # Ensure the missday_count and left_sum are recalculated before saving
        obj.missday_count = len(json.loads(obj.missed_days))
        obj.left_sum = obj.tarif - (obj.missday_count * obj.missday_cost)
        
        # Automatically update is_paid if left_sum is 0.0 or less
        if obj.left_sum <= 0.0:
            obj.is_paid = True

        super().save_model(request, obj, form, change)




@admin.register(IncomeTransaction)
class IncomeTransactionAdmin(admin.ModelAdmin):
    list_display = ('kid', 'amount', 'date', 'type', 'comment')
    list_filter = ('type', 'date')
    search_fields = ('kid__full_name', 'comment')
    readonly_fields = ('date',)  # Make the date field read-only as it is auto-generated

    def has_add_permission(self, request):
        # Custom logic if needed to restrict adding transactions
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Custom logic if needed to restrict deleting transactions
        return super().has_delete_permission(request)
