import uuid
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from students.models import Student

User = get_user_model()


class StudentAndFinanceTestCase(APITestCase):

    def setUp(self):
        # Unikal foydalanuvchilar va ma'lumotlar yaratish
        self.unique_id = uuid.uuid4().hex[:6]

        # Admin / Staff user (403 va Permission xatoliklarining oldini olish uchun)
        self.admin_user = User.objects.create_user(
            username=f"admin_{self.unique_id}",
            email=f"admin_{self.unique_id}@eduerp.uz",
            password="Password123!",
            is_staff=True,
            is_superuser=True,
        )

        # Oddiy student user
        self.student_user = User.objects.create_user(
            username=f"student_{self.unique_id}",
            email=f"student_{self.unique_id}@eduerp.uz",
            password="Password123!",
        )

        # Student obyekti ('user' emas, 'owner' bilan yaratilgan)
        self.student = Student.objects.create(
            owner=self.student_user,
            first_name="Ozodbek",
            last_name="Fayzullayev",
            phone_number=f"+99890{uuid.uuid4().hex[:7]}",
            balance=Decimal("0.00"),
        )

    # ===================================================================
    # 1. STUDENT MODULI TESTLARI
    # ===================================================================

    def test_get_student_list_authenticated(self):
        """Tizimga kirgan foydalanuvchi talabalar ro'yxatini olishi"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/api/v1/students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_student_detail(self):
        """Studentning profil ma'lumotlarini olish"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f"/api/v1/students/{self.student.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student(self):
        """Yangi student profili yaratish (POST /api/v1/students/)"""
        self.client.force_authenticate(user=self.admin_user)

        new_user = User.objects.create_user(
            username=f"newstudent_{self.unique_id}",
            email=f"newstudent_{self.unique_id}@eduerp.uz",
            password="Password123!",
        )

        payload = {
            "owner": new_user.id,
            "first_name": "Ali",
            "last_name": "Valiyev",
            "phone_number": f"+99891{uuid.uuid4().hex[:7]}",
            "balance": "0.00",
        }

        response = self.client.post("/api/v1/students/", payload, format="json")
        self.assertIn(
            response.status_code, 
            [status.HTTP_201_CREATED, status.HTTP_200_OK]
        )

    def test_update_student_info(self):
        """Student ma'lumotlarini tahrirlash (PATCH /api/v1/students/{id}/)"""
        self.client.force_authenticate(user=self.admin_user)
        payload = {"first_name": "Ozodbek_Updated"}

        response = self.client.patch(
            f"/api/v1/students/{self.student.id}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, "Ozodbek_Updated")

    def test_delete_student(self):
        """Student profilini o'chirish (DELETE /api/v1/students/{id}/)"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/api/v1/students/{self.student.id}/")
        self.assertIn(
            response.status_code, 
            [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]
        )
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())

    # ===================================================================
    # 2. FINANCE / BALANCE TESTLARI
    # ===================================================================

    def test_unauthenticated_access_denied(self):
        """Tizimga kirmagan so'rov rad etilishi (401 Unauthorized)"""
        response = self.client.get("/api/v1/students/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_balance_update_by_admin(self):
        """Admin tomonidan student balansini o'zgartirish"""
        self.client.force_authenticate(user=self.admin_user)
        payload = {"balance": "500000.00"}

        response = self.client.patch(
            f"/api/v1/students/{self.student.id}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.balance, Decimal("500000.00"))