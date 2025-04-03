from django.test import TestCase
from django.contrib.auth.models import Group
from .models import User
from .forms import CustomUserCreationForm
from django.core.exceptions import ValidationError

class UserModelTest(TestCase):

    def setUp(self):
        """Setup inicial para las pruebas"""
        self.hotel_owner = User.objects.create_user(
            username="hotel_owner",
            email="owner@example.com",
            phone_number="1234567890",
            is_hotel_owner=True,
            password="securepassword"
        )

        self.customer = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            phone_number="0987654321",
            is_customer=True,
            password="securepassword"
        )

    def test_user_creation(self):
        """Prueba si los usuarios se crean correctamente"""
        self.assertEqual(self.hotel_owner.username, "hotel_owner")
        self.assertEqual(self.customer.username, "customer")

    def test_unique_email(self):
        """Verifica que los emails sean únicos"""

        # Crear el primer usuario con un email determinado
        User.objects.create_user(
            username="first_user",
            email="owner@example.com",
            phone_number="1112223333",
            is_customer=True,
            password="securepassword"
        )

        # Intentar crear un segundo usuario con el mismo email
        user2 = User(
            username="duplicate_user",
            email="owner@example.com",  # Email duplicado
            phone_number="2223334444",
            is_customer=True,
            password="securepassword"
        )

        # Verificar que se lanza una ValidationError
        with self.assertRaises(ValidationError):
            user2.full_clean()  # Esto debe lanzar ValidationError

    def test_phone_number_validation(self):
        """Verifica que los números de teléfono sean de 10 dígitos"""
        invalid_user = User(username="invalid", email="invalid@example.com", phone_number="123")
        with self.assertRaises(ValidationError):  # Validación de teléfono debe lanzar ValidationError
            invalid_user.full_clean()

    def test_user_cannot_be_both_roles(self):
        """Verifica que un usuario no pueda ser hotel_owner y customer al mismo tiempo"""
        invalid_user = User(username="invalid_user", email="test@example.com", phone_number="1234567890",
                            is_hotel_owner=True, is_customer=True)
        with self.assertRaises(ValidationError):  # Se espera ValidationError aquí
            invalid_user.full_clean()


class UserFormTest(TestCase):

    def test_valid_form(self):
        """Prueba que un formulario válido cree un usuario correctamente"""
        form_data = {
            "username": "new_user",
            "email": "newuser@example.com",
            "phone_number": "1234567890",
            "is_hotel_owner": True,
            "is_customer": False,
            "password1": "TestPassword123",
            "password2": "TestPassword123"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number(self):
        """Prueba un formulario con un número de teléfono inválido"""
        form_data = {
            "username": "new_user",
            "email": "newuser@example.com",
            "phone_number": "12345",  # Inválido
            "is_hotel_owner": True,
            "is_customer": False,
            "password1": "TestPassword123",
            "password2": "TestPassword123"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)

    def test_user_cannot_have_both_roles(self):
        """Verifica que el formulario no permita usuarios con ambos roles"""
        form_data = {
            "username": "invalid_user",
            "email": "invalid@example.com",
            "phone_number": "1234567890",
            "is_hotel_owner": True,
            "is_customer": True,  # No permitido
            "password1": "TestPassword123",
            "password2": "TestPassword123"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)  # La validación general se guarda en __all__

    def test_group_assignment(self):
        """Verifica que un usuario se asigne correctamente a un grupo"""
        group_owner, _ = Group.objects.get_or_create(name="hotel_owner")
        group_customer, _ = Group.objects.get_or_create(name="customer")

        user = User.objects.create_user(
            username="group_test_user",
            email="group_test@example.com",
            phone_number="1234567890",
            is_customer=True,
            password="securepassword"
        )

        self.assertTrue(user.groups.filter(name="customer").exists())
        self.assertFalse(user.groups.filter(name="hotel_owner").exists())