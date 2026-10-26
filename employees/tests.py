from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from employees.models import Employee


class EmployeeCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="employee-manager",
            password="test-password",
        )
        self.employee = Employee.objects.create(
            joining_date="2025-01-15",
            name="Original Employee",
            age=30,
            mobile="0123456789",
            email="employee@example.com",
            education="Graduation",
            skills="Communication",
            salary="65000.00",
            experience="4.5",
        )

    def employee_data(self, **overrides):
        data = {
            "joining_date": "2025-02-20",
            "name": "New Employee",
            "age": "28",
            "mobile": "+1 555 123 4567",
            "email": "new.employee@example.com",
            "education": "Diploma",
            "skills": "Planning",
            "salary": "72500.50",
            "experience": "3.5",
        }
        data.update(overrides)
        return data

    def test_user_can_create_and_read_employee_records(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("add"), self.employee_data())

        self.assertRedirects(response, reverse("display"))
        created_employee = Employee.objects.get(email="new.employee@example.com")
        self.assertEqual(str(created_employee.salary), "72500.50")
        self.assertEqual(str(created_employee.experience), "3.5")

        response = self.client.get(reverse("display"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Original Employee")
        self.assertContains(response, "New Employee")
        self.assertContains(response, "72500.50")
        self.assertContains(response, "3.5 years")

    def test_invalid_employee_form_is_rendered_with_errors(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("add"),
            self.employee_data(age="not-a-number"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "age",
            "Enter a whole number.",
        )
        self.assertEqual(Employee.objects.count(), 1)

    def test_negative_salary_and_experience_are_rejected(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("add"),
            self.employee_data(salary="-1", experience="-0.5"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("salary", response.context["form"].errors)
        self.assertIn("experience", response.context["form"].errors)

    def test_empty_employee_post_is_validated(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("add"), {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].is_bound)
        self.assertIn("name", response.context["form"].errors)

    def test_user_can_update_employee_record(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("update", args=[self.employee.id]),
            self.employee_data(
                name="Updated Employee",
                email=self.employee.email,
                salary="80000.00",
                experience="5",
            ),
        )

        self.assertRedirects(response, reverse("display"))
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, "Updated Employee")
        self.assertEqual(str(self.employee.salary), "80000.00")
        self.assertEqual(str(self.employee.experience), "5.0")

    def test_employee_delete_requires_post_and_deletes_record(self):
        self.client.force_login(self.user)
        delete_url = reverse("delete", args=[self.employee.id])

        self.assertEqual(self.client.get(delete_url).status_code, 405)
        response = self.client.post(delete_url)

        self.assertRedirects(response, reverse("display"))
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("display"))

        self.assertRedirects(response, f"{reverse('log')}?next={reverse('display')}")


class AuthenticationTests(TestCase):
    def test_logout_requires_post_and_ends_the_session(self):
        user = User.objects.create_user(
            username="logout-user",
            password="test-password",
        )
        self.client.force_login(user)
        logout_url = reverse("logout")

        self.assertEqual(self.client.get(logout_url).status_code, 405)
        response = self.client.post(logout_url)

        self.assertRedirects(response, reverse("log"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_signup_rejects_mismatched_password_confirmation(self):
        response = self.client.post(
            reverse("signup"),
            {
                "txtname1": "new-user",
                "txtmail1": "new-user@example.com",
                "txtpswd1": "test-password",
                "txtpswd2": "different-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="new-user").exists())
        self.assertContains(response, "The passwords do not match.")

    def test_user_can_sign_up_and_log_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "txtname1": "new-user",
                "txtmail1": "new-user@example.com",
                "txtpswd1": "test-password",
                "txtpswd2": "test-password",
            },
        )

        self.assertRedirects(response, reverse("log"))
        response = self.client.post(
            reverse("log"),
            {"txtname": "new-user", "txtpswd": "test-password"},
        )

        self.assertRedirects(response, reverse("home"))
