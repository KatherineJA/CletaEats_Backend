import random
import string
from dao.repartidor_dao import RepartidorDAO
from dao.usuario_dao import UsuarioDAO
from modelo.repartidor import Repartidor
from modelo.usuario import Usuario  # <-- IMPORTANTE: Lo importamos para usar bcrypt


class RepartidorService:
    def __init__(self):
        self.repartidor_dao = RepartidorDAO()
        self.usuario_dao = UsuarioDAO()

    def registrar_repartidor(self, datos):
        # 1. Verificar si la cédula ya existe
        if self.repartidor_dao.buscar_por_cedula(datos['cedula']):
            return {"exito": False, "mensaje": "La cédula ya está registrada"}

        # 2. Lógica de Contraseña (Autónomo vs Administrador)
        password_provisto = datos.get('password')
        fue_generada = False

        if password_provisto:
            # El repartidor se registra a sí mismo usando el form
            password_final = password_provisto
        else:
            # Lo registra el administrador (no envió password en el JSON)
            # Generamos una contraseña alfanumérica de 8 caracteres
            caracteres = string.ascii_letters + string.digits
            password_final = ''.join(random.choice(caracteres) for i in range(8))
            fue_generada = True

        # 3. Crear el Usuario (Usamos Usuario.nuevo para que aplique el bcrypt)
        nuevo_usuario = Usuario.nuevo(datos['correo'], password_final, 'repartidor')
        usuario_guardado = self.usuario_dao.guardar(nuevo_usuario)

        if not usuario_guardado:
            return {"exito": False, "mensaje": "Error al crear credenciales de usuario"}

        # 4. Crear el repartidor ligado a ese usuario
        nuevo_rep = Repartidor.nuevo(
            usuario_guardado.get_id(), datos['cedula'], datos['nombre'], datos['correo'],
            datos['direccion'], datos['telefono'], datos['tarjeta']
        )

        if self.repartidor_dao.guardar(nuevo_rep):
            respuesta = {"exito": True, "mensaje": "Repartidor registrado correctamente"}

            # Si la generó el admin, simulamos el correo y la devolvemos en el JSON para probar
            if fue_generada:
                print("\n--- SIMULACIÓN DE ENVÍO DE CORREO ---")
                print(f"Para: {datos['correo']}")
                print(f"Asunto: Bienvenido a CletaEats - Credenciales de acceso")
                print(f"Cuerpo: Tu contraseña generada automáticamente es: {password_final}")
                print("-------------------------------------\n")

                # Opcional: Mandarla en la respuesta de Postman para no tener que ver la consola
                respuesta["password_temporal"] = password_final

            return respuesta

        return {"exito": False, "mensaje": "Error al registrar datos del repartidor"}

    def listar_repartidores_limpios(self):
        """
        Obtiene la lista de repartidores con cero amonestaciones
        """
        try:
            repartidores = self.repartidor_dao.obtener_disponibles_sin_faltas()
            return {"exito": True, "repartidores": repartidores}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al obtener reporte: {str(e)}"}