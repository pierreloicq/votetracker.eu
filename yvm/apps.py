from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class YvmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yvm'

# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#overriding-the-default-admin-site
# class MyAdminConfig(AdminConfig):
#     default_site = "yvm.admin.MyAdminSite"