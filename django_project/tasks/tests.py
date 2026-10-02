"""Django and DRF tests for the task API."""

import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


User = get_user_model()


class TaskModelTests(TestCase):
    """Test model defaults and relationships independently of HTTP."""

    def test_task_defaults_and_user_relationship(self) -> None:
        user = User.objects.create_user(username="model-user", password="pass")
        task = Task.objects.create(owner=user, title="Learn models")

        self.assertEqual(task.status, Task.Status.TODO)
        self.assertEqual(user.tasks.get(), task)
        self.assertEqual(str(task), "Learn models")


class TaskApiTests(APITestCase):
    """Test authentication, serialization, ownership, and CRUD endpoints."""

    def setUp(self) -> None:
        self.alice = User.objects.create_user(username="alice", password="pass")
        self.bob = User.objects.create_user(username="bob", password="pass")
        self.list_url = reverse("task-list")

    def test_health_endpoint_is_public(self) -> None:
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"status": "ok"})

    def test_task_list_requires_authentication(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_create_sets_owner_and_serializes_task(self) -> None:
        self.client.force_authenticate(user=self.alice)

        response = self.client.post(
            self.list_url,
            {"title": "Learn serializers", "description": "Convert model data"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["owner"], self.alice.pk)
        self.assertEqual(Task.objects.get().owner, self.alice)

    def test_user_can_only_list_and_retrieve_own_tasks(self) -> None:
        own_task = Task.objects.create(owner=self.alice, title="Alice task")
        other_task = Task.objects.create(owner=self.bob, title="Bob task")
        self.client.force_authenticate(user=self.alice)

        list_response = self.client.get(self.list_url)
        other_detail_response = self.client.get(
            reverse("task-detail", args=[other_task.pk])
        )

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in list_response.data], [own_task.pk])
        self.assertEqual(
            other_detail_response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_blank_title_is_rejected_by_serializer(self) -> None:
        self.client.force_authenticate(user=self.alice)

        response = self.client.post(
            self.list_url,
            {"title": "   "},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
