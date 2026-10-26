from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employees'
    # Preserve the legacy migration label and database tables across the package rename.
    label = 'sales'
