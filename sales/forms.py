from django import forms

from employees.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            "joining_date",
            "name",
            "age",
            "mobile",
            "email",
            "education",
            "skills",
            "salary",
            "experience",
        )
        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"}),
            "mobile": forms.TextInput(attrs={"inputmode": "tel"}),
            "salary": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "experience": forms.NumberInput(attrs={"min": "0", "step": "0.1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget_class = (
                "form-select"
                if isinstance(field.widget, forms.Select)
                else "form-control"
            )
            field.widget.attrs["class"] = widget_class
