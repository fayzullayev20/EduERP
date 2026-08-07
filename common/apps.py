from django.apps import AppConfig


<<<<<<<< HEAD:common/apps.py
class CommonConfig(AppConfig):
========
class TeacherConfig(AppConfig):
>>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1:teachers/apps.py
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
