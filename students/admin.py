from django.contrib import admin

<<<<<<< HEAD

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'status', 'balance', 'owner', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone_number', 'passport_number')
    readonly_fields = ('id', 'frozen_at', 'archived_at', 'created_at', 'updated_at')
=======
# Register your models here.
>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1
