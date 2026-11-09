import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Project, Experience


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



# ==========================================================
# TEST EXPERIENCE
# ==========================================================
class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", email="owner@example.com", password="password123"
        )

        self.editor = User.objects.create_user(
            username="editor",
            password="password123"
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(self.editor_group)

        self.user = User.objects.create_user(
            username="user",
            password="password123"
        )

        self.experience = Experience.objects.create(
            title="Software Engineering Intern",
            description="Worked on software development.",
            category="internship",
            thumbnail="https://example.com/image.jpg"
        )

        self.list_url = reverse("api:experience_list")
        self.detail_url = reverse("api:experience_detail", kwargs={"experience_id": self.experience.id})
        self.star_url = reverse("api:experience_star", kwargs={"experience_id": self.experience.id})
        self.valid_payload = {
            "title": "Research Assistant",
            "description": "Conducted research activities.",
            "category": "research",
            "thumbnail": "https://example.com/research.jpg"
        }

    def test_get_experience_list(self):
        # Pengunjung tanpa login boleh melihat daftar Experience.
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Software Engineering Intern"
        )

    def test_search_experience_by_title(self):
        # Pencarian dilakukan berdasarkan title.
        response = self.client.get(
            self.list_url,
            {"title": "Software Engineering"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Software Engineering Intern"
        )

    def test_search_experience_not_found(self):
        # Pencarian dengan title yang tidak cocok menghasilkan daftar kosong.
        response = self.client.get(
            self.list_url,
            {"title": "Nonexistent Experience"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_experience_detail(self):
        # Pengunjung boleh melihat detail Experience.
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["title"],
            "Software Engineering Intern"
        )

    def test_get_experience_not_found(self):
        # Detail Experience yang tidak tersedia menghasilkan 404.
        response = self.client.get(
            reverse(
                "api:experience_detail",
                kwargs={
                    "experience_id": "00000000-0000-0000-0000-000000000000"
                }
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_anonymous_cannot_create_experience(self):
        # Pengunjung tidak boleh membuat Experience.
        initial_count = Experience.objects.count()
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), initial_count)

    def test_anonymous_cannot_update_experience(self):
        # Pengunjung tidak boleh mengubah Experience.
        original_title = self.experience.title
        response = self.client.patch(
            self.detail_url,
            {"title": "Hacked Title"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, original_title)

    def test_anonymous_cannot_delete_experience(self):
        # Pengunjung tidak boleh menghapus Experience.
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Experience.objects.filter(pk=self.experience.pk).exists()
        )

    def test_regular_user_cannot_create_experience(self):
        # Pengguna biasa tidak boleh membuat Experience.
        self.client.force_authenticate(user=self.user)
        initial_count = Experience.objects.count()
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), initial_count)

    def test_regular_user_cannot_update_experience(self):
        # Pengguna biasa tidak boleh mengubah Experience.
        self.client.force_authenticate(user=self.user)
        original_title = self.experience.title
        response = self.client.patch(
            self.detail_url,
            {"title": "Hacked Title"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, original_title)

    def test_regular_user_cannot_delete_experience(self):
        # Pengguna biasa tidak boleh menghapus Experience.
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Experience.objects.filter(pk=self.experience.pk).exists()
        )

    
    def test_editor_can_update_experience(self):
        # Editor boleh mengubah Experience.
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(
            self.detail_url,
            {"title": "Updated by Editor"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated by Editor")

    def test_editor_cannot_create_experience(self):
        # Editor tidak boleh membuat Experience.
        self.client.force_authenticate(user=self.editor)
        initial_count = Experience.objects.count()
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), initial_count)

    def test_editor_cannot_delete_experience(self):
        # Editor tidak boleh menghapus Experience.
        self.client.force_authenticate(user=self.editor)
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Experience.objects.filter(pk=self.experience.pk).exists()
        )

    def test_owner_can_create_experience(self):
        # Superuser boleh membuat Experience.
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Experience.objects.filter(
                title="Research Assistant"
            ).exists()
        )

    def test_owner_can_update_experience(self):
        # Superuser boleh mengubah Experience.
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url,
            {"title": "Updated by Owner"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated by Owner")

    def test_owner_can_delete_experience(self):
        # Superuser boleh menghapus Experience.
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Experience.objects.filter(pk=self.experience.pk).exists()
        )


    def test_create_experience_with_invalid_title(self):
        # Title kosong tidak boleh diterima.
        self.client.force_authenticate(user=self.owner)
        invalid_payload = self.valid_payload.copy()
        invalid_payload["title"] = ""
        initial_count = Experience.objects.count()

        response = self.client.post(
            self.list_url,
            invalid_payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Experience.objects.count(), initial_count)

    def test_create_experience_strips_html_tags(self):
        # Tag HTML pada title harus dibersihkan oleh serializer.
        self.client.force_authenticate(user=self.owner)
        payload = self.valid_payload.copy()
        payload["title"] = "<b>Research Assistant</b>"
        response = self.client.post(
            self.list_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Research Assistant")


    def test_read_only_fields_cannot_be_modified(self):
        # Field hasil perhitungan tidak boleh diubah melalui API.
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url,
            {
                "title": "Updated Title",
                "star_count": 999,
                "is_starred": True,
                "is_ongoing": False
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated Title")
        self.assertEqual(self.experience.starred_by.count(), 0)
        self.assertTrue(self.experience.is_ongoing)


    def test_anonymous_cannot_star_experience(self):
        # Pengunjung tanpa login tidak boleh memberi star.
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_regular_user_can_star_experience(self):
        # Pengguna biasa boleh memberi star.
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.experience.starred_by.filter(pk=self.user.pk).exists())
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])

    def test_regular_user_can_unstar_experience(self):
        # Pengguna biasa boleh membatalkan star.
        self.experience.starred_by.add(self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.experience.starred_by.filter(pk=self.user.pk).exists())
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    
    def test_csrf_protection_for_experience_api(self):
        # Menggunakan client dengan pemeriksaan CSRF aktif.
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.force_authenticate(user=None)
        csrf_client.login(username="owner", password="password123")

        # Mengambil halaman Experience untuk mendapatkan cookie CSRF.
        page_response = csrf_client.get(reverse("main:show_experience"))
        self.assertEqual(page_response.status_code, status.HTTP_200_OK)

        csrf_token = csrf_client.cookies["csrftoken"].value
        # POST tanpa token CSRF harus ditolak.
        response_without_csrf = csrf_client.post(
            self.list_url,
            self.valid_payload,
            format="json"
        )
        self.assertEqual(response_without_csrf.status_code, status.HTTP_403_FORBIDDEN)

        # POST dengan token CSRF harus berhasil.
        response_with_csrf = csrf_client.post(
            self.list_url,
            self.valid_payload,
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertEqual(response_with_csrf.status_code, status.HTTP_201_CREATED)
