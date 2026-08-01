# teacher/admin.py
from django.contrib import admin
from .models import Teacher, Subject, TeacherWorkload, Transaction, Contract

admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(TeacherWorkload)
admin.site.register(Transaction)
admin.site.register(Contract)