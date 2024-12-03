from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.forms import RegistrationForm
from app.models import Pedido, Producto, ProductoCesta, ProductoPedido

# Create your tests here.
class RegistrationFormTest(TestCase):
    def setUp(self):
        # Crear un usuario existente para probar la validación del correo
        User.objects.create_user(username="existinguser", email="test@example.com", password="testpassword123")

    def test_form_valid_data(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_passwords_do_not_match(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'DifferentPassword123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Las contraseñas no coinciden.", form.errors.get('__all__'))

    def test_form_email_already_exists(self):
        form_data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Este correo electrónico ya está en uso. Por favor, ingrese otro.", form.errors.get('email'))

    def test_form_weak_password(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'weak',  
            'confirm_password': 'weak'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This password is too short. It must contain at least 8 characters.", form.errors.get('password')[0])

    def test_form_short_username(self):
        form_data = {
            'username': 'abc',  
            'email': 'newuser@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("El nombre de usuario debe tener al menos 4 caracteres.", form.errors.get('username'))

    def test_form_blank_fields(self):
        form_data = {}  
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors.get('username'))
        self.assertIn("This field is required.", form.errors.get('email'))
        self.assertIn("This field is required.", form.errors.get('password'))

class ProductoTestCase(TestCase):
    def setUp(self):
        # Crear un producto para las pruebas
        self.producto = Producto.objects.create(
            nombre="Producto 1",
            descripcion="Descripción del producto",
            imagen="producto1.jpg",
            precio=100.50,
            cantidad=10,
            categoria="Velas e Inciensos"
        )

    def test_producto_creado_correctamente(self):
        # Verificar que el producto fue creado correctamente
        producto = Producto.objects.get(nombre="Producto 1")
        self.assertEqual(producto.precio, 100.50)
        self.assertEqual(producto.cantidad, 10)

    def test_producto_categoria(self):
        # Verificar que la categoría del producto es correcta
        self.assertEqual(self.producto.categoria, "Velas e Inciensos")
    
    def test_producto_cantidad_negativa(self):
    # Intentar crear un producto con una cantidad negativa
        producto_invalido = Producto(
            nombre="Producto Invalido",
            descripcion="Descripción del producto",
            imagen="producto_invalido.jpg",
            precio=50.00,
            cantidad=-5,  # Cantidad negativa
            categoria="Velas e Inciensos"
        )
        with self.assertRaises(ValidationError):
            producto_invalido.full_clean()
        
 
    def test_producto_sin_nombre(self):
    # Intentar crear un producto sin nombre
        producto_sin_nombre= Producto.objects.create(
            descripcion="Descripción sin nombre",
            imagen="producto_sin_nombre.jpg",
            precio=50.00,
            cantidad=10,
            categoria="Velas e Inciensos"
        )
        with self.assertRaises(ValidationError):
            producto_sin_nombre.full_clean()
        
    
    def test_producto_precio_negativo(self):
    # Intentar crear un producto con un precio negativo
            producto_precio_negativo = Producto.objects.create(
                nombre="Producto con precio negativo",
                descripcion="Descripción del producto",
                imagen="producto_precio_negativo.jpg",
                precio=-100.00,  # Precio negativo
                cantidad=10,
                categoria="Velas e Inciensos"
            )
            with self.assertRaises(ValidationError):
                producto_precio_negativo.full_clean()
        

class ProductoCestaTestCase(TestCase):
    def setUp(self):
        # Crear un usuario
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        # Crear un producto
        self.producto = Producto.objects.create(
            nombre="Producto 1",
            descripcion="Descripción del producto",
            imagen="producto1.jpg",
            precio=100.50,
            cantidad=10,
            categoria="Velas e Inciensos"
        )
        # Crear un producto en la cesta
        self.producto_cesta = ProductoCesta.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad=2
        )

    def test_producto_cesta_creado_correctamente(self):
        # Verificar que el producto se agregó correctamente a la cesta
        producto_cesta = ProductoCesta.objects.get(usuario=self.user)
        self.assertEqual(producto_cesta.cantidad, 2)
        self.assertEqual(producto_cesta.producto.nombre, "Producto 1")
    
class PedidoTestCase(TestCase):
    def setUp(self):
        # Crear un pedido
        self.pedido = Pedido.objects.create(
            email="test@example.com",
            direccion="Calle Ficticia 123",
            codigo_postal="12345",
            total=200.00,
            estado=Pedido.EstadoPedido.PENDIENTE
        )

    def test_pedido_creado_correctamente(self):
        # Verificar que el pedido se creó correctamente
        pedido = Pedido.objects.get(email="test@example.com")
        self.assertEqual(pedido.estado, Pedido.EstadoPedido.PENDIENTE)
        self.assertEqual(pedido.total, 200.00)

    def test_estado_pedido(self):
        # Verificar que el estado por defecto es "PENDIENTE"
        self.assertEqual(self.pedido.estado, Pedido.EstadoPedido.PENDIENTE)

    def test_pedido_sin_email(self):
    # Intentar crear un pedido sin email
          # O ValidationError si es más apropiado
            pedido_no_mail = Pedido.objects.create(
                direccion="Calle Ficticia 123",
                codigo_postal="12345",
                total=200.00,
                estado=Pedido.EstadoPedido.PENDIENTE
            )
            with self.assertRaises(ValidationError):
                pedido_no_mail.full_clean()


    def test_pedido_con_total_negativo(self):
    # Intentar crear un pedido con un total negativo
        
            pedido_con_total_negativo= Pedido.objects.create(
                email="test@example.com",
                direccion="Calle Ficticia 123",
                codigo_postal="12345",
                total=-200.00,  # Total negativo
                estado=Pedido.EstadoPedido.PENDIENTE
            )
            with self.assertRaises(ValidationError):
                pedido_con_total_negativo.full_clean()

    def test_pedido_con_estado_invalido(self):
    # Intentar crear un pedido con un estado inválido
         # O IntegrityError, dependiendo de cómo se maneje la validación
            pedido_con_estado_invalido=Pedido.objects.create(
                email="test@example.com",
                direccion="Calle Ficticia 123",
                codigo_postal="12345",
                total=200.00,
                estado="INVALIDO"  # Estado inválido
            )
            with self.assertRaises(ValidationError):
                pedido_con_estado_invalido.full_clean()


class ProductoPedidoTestCase(TestCase):
    def setUp(self):
        # Crear un producto y un pedido
        self.producto = Producto.objects.create(
            nombre="Producto 1",
            descripcion="Descripción del producto",
            imagen="producto1.jpg",
            precio=100.50,
            cantidad=10,
            categoria="Electrónica"
        )
        self.pedido = Pedido.objects.create(
            email="test@example.com",
            direccion="Calle Ficticia 123",
            codigo_postal="12345",
            total=200.00,
            estado=Pedido.EstadoPedido.PENDIENTE
        )
        # Crear un producto en el pedido
        self.producto_pedido = ProductoPedido.objects.create(
            pedido=self.pedido,
            producto=self.producto,
            cantidad=2
        )

    def test_producto_pedido_creado_correctamente(self):
        # Verificar que el producto se agregó correctamente al pedido
        producto_pedido = ProductoPedido.objects.get(pedido=self.pedido)
        self.assertEqual(producto_pedido.cantidad, 2)
        self.assertEqual(producto_pedido.producto.nombre, "Producto 1")

class HomeViewTests(TestCase):
    def test_home_view(self):
        # Crear un producto de prueba
        Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción del producto",
            imagen="producto_test.jpg",
            precio=100.00,
            cantidad=10,
            categoria="Categoría Test"
        )
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto Test')

    def test_product_not_found(self):
        response = self.client.get('/product/9999/')  # Producto con ID no existente
        self.assertEqual(response.status_code, 404)

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

    def test_login_view_valid_user(self):
        response = self.client.post(reverse('login'), {'email': 'test@example.com', 'password': 'password123'})
        self.assertRedirects(response, '/')

class RegisterViewTests(TestCase):
    def test_register_view_valid_form(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 200)


class CestaViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción del producto",
            imagen="producto_test.jpg",
            precio=50.00,
            cantidad=10,
            categoria="Categoría Test"
        )
        ProductoCesta.objects.create(usuario=self.user, producto=self.producto, cantidad=2)

    def test_cesta_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cesta'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto Test')
        self.assertContains(response, '100.00') 

class AgregarACestaViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción del producto",
            imagen="producto_test.jpg",
            precio=50.00,
            cantidad=10,
            categoria="Categoría Test"
        )

    def test_agregar_a_cesta_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('agregar_a_cesta', args=['Producto Test']), {'cantidad': 2})
        self.assertEqual(response.status_code, 302)
        


class PedidosViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción del producto",
            imagen="producto_test.jpg",
            precio=100.00,
            cantidad=10,
            categoria="Categoría Test"
        )
        self.pedido = Pedido.objects.create(
            email=self.user.email,
            direccion="Calle Ficticia 123",
            codigo_postal="12345",
            total=200.00,
            estado=Pedido.EstadoPedido.PENDIENTE
        )
        ProductoPedido.objects.create(pedido=self.pedido, producto=self.producto, cantidad=2)

    def test_pedidos_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('pedidos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto Test')
