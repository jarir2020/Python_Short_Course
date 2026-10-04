"""Django API tests for the complete first PowerTrack workflow."""

from rest_framework.test import APITestCase

from accounts.models import User
from outages.models import Assignment, OutageReport, ProgressUpdate


class PowerTrackWorkflowTests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer1",
            password="customer-password-123",
            role=User.Role.CUSTOMER,
            area="North Road",
        )
        self.other_customer = User.objects.create_user(
            username="customer2",
            password="customer-password-123",
            role=User.Role.CUSTOMER,
        )
        self.technician = User.objects.create_user(
            username="technician1",
            password="technician-password-123",
            role=User.Role.TECHNICIAN,
        )
        self.admin = User.objects.create_user(
            username="admin1",
            password="admin-password-123",
            role=User.Role.ADMIN,
            is_staff=True,
        )

    def test_customer_registration_and_token_login(self):
        registration = self.client.post(
            "/api/auth/register/",
            {
                "username": "newcustomer",
                "email": "newcustomer@example.com",
                "password": "A-very-strong-pass-9!",
                "area": "West Road",
            },
            format="json",
        )
        self.assertEqual(registration.status_code, 201)
        self.assertEqual(registration.data["user"]["role"], User.Role.CUSTOMER)
        self.assertTrue(registration.data["token"])

        login = self.client.post(
            "/api/auth/login/",
            {"username": "newcustomer", "password": "A-very-strong-pass-9!"},
            format="json",
        )
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.data["user"]["username"], "newcustomer")

    def create_report(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post(
            "/api/reports/",
            {"area": "North Road", "description": "Transformer is silent."},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        return response.data["id"]

    def test_customer_can_create_but_not_view_another_customers_report(self):
        report_id = self.create_report()

        own_response = self.client.get(f"/api/reports/{report_id}/")
        self.assertEqual(own_response.status_code, 200)
        self.assertEqual(own_response.data["status"], OutageReport.Status.REPORTED)

        self.client.force_authenticate(self.other_customer)
        other_response = self.client.get(f"/api/reports/{report_id}/")
        self.assertEqual(other_response.status_code, 404)

    def test_customer_cannot_choose_priority_or_status(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post(
            "/api/reports/",
            {
                "area": "South Road",
                "description": "Streetlights are off.",
                "priority": OutageReport.Priority.CRITICAL,
                "status": OutageReport.Status.RESOLVED,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["priority"], OutageReport.Priority.MEDIUM)
        self.assertEqual(response.data["status"], OutageReport.Status.REPORTED)

    def test_admin_assigns_a_technician_and_customer_cannot_assign(self):
        report_id = self.create_report()

        self.client.force_authenticate(self.customer)
        forbidden = self.client.post(
            f"/api/reports/{report_id}/assign/",
            {"technician": self.technician.id},
            format="json",
        )
        self.assertEqual(forbidden.status_code, 403)

        self.client.force_authenticate(self.admin)
        response = self.client.post(
            f"/api/reports/{report_id}/assign/",
            {"technician": self.technician.id, "notes": "Check the local transformer."},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], OutageReport.Status.ASSIGNED)
        self.assertEqual(response.data["assignment"]["technician"]["id"], self.technician.id)

    def test_technician_progress_resolves_report_for_customer(self):
        report_id = self.create_report()
        self.client.force_authenticate(self.admin)
        self.client.post(
            f"/api/reports/{report_id}/assign/",
            {"technician": self.technician.id},
            format="json",
        )

        self.client.force_authenticate(self.technician)
        for status_value, message in [
            (Assignment.Status.ACCEPTED, "Assignment accepted."),
            (Assignment.Status.IN_PROGRESS, "Crew is inspecting the transformer."),
            (Assignment.Status.RESOLVED, "Power restored and tested."),
        ]:
            response = self.client.post(
                f"/api/reports/{report_id}/progress/",
                {"status": status_value, "message": message},
                format="json",
            )
            self.assertEqual(response.status_code, 201)

        self.assertEqual(ProgressUpdate.objects.count(), 3)
        self.client.force_authenticate(self.customer)
        response = self.client.get(f"/api/reports/{report_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], OutageReport.Status.RESOLVED)
        self.assertIsNotNone(response.data["resolved_at"])
        self.assertEqual(len(response.data["progress_updates"]), 3)

        history = self.client.get(f"/api/reports/{report_id}/progress/")
        self.assertEqual(history.status_code, 200)
        self.assertEqual(len(history.data), 3)
