import random
import string
import os
import datetime

import bcrypt

from modelo.usuario import Usuario
from modelo.cliente import Cliente
from modelo.repartidor import Repartidor
from dao.usuario_dao import UsuarioDAO
from dao.cliente_dao import ClienteDAO
from dao.repartidor_dao import RepartidorDAO
from dao.recuperacion_dao import RecuperacionDAO


class AuthService:

    def __init__(self):
        self.usuario_dao    = UsuarioDAO()
        self.cliente_dao    = ClienteDAO()
        self.repartidor_dao = RepartidorDAO()
        self.recuperacion_dao = RecuperacionDAO()

    def registrar_cliente(self, cedula, nombre, correo, password,
                          telefono, numero_tarjeta="",
                          latitud=None, longitud=None):
        if self.usuario_dao.buscar_por_correo(correo):
            return {"exito": False, "mensaje": "El correo ya esta registrado"}
        if self.usuario_dao.buscar_por_cedula(cedula):
            return {"exito": False, "mensaje": "La cedula ya esta registrada"}

        usuario = Usuario.nuevo(cedula, nombre, correo, password,
                                telefono, "CLIENTE", latitud, longitud)
        usuario_guardado = self.usuario_dao.guardar(usuario)
        if not usuario_guardado:
            return {"exito": False, "mensaje": "Error al crear usuario"}

        cliente = Cliente.nuevo(usuario_guardado.get_id(), numero_tarjeta)
        if not self.cliente_dao.guardar(cliente):
            return {"exito": False, "mensaje": "Error al crear cliente"}

        return {"exito": True,
                "mensaje": "Cliente registrado correctamente",
                "id": usuario_guardado.get_id()}

    def registrar_repartidor(self, cedula, nombre, correo, password,
                             telefono, numero_tarjeta="",
                             latitud=None, longitud=None):
        if self.usuario_dao.buscar_por_correo(correo):
            return {"exito": False, "mensaje": "El correo ya esta registrado"}
        if self.usuario_dao.buscar_por_cedula(cedula):
            return {"exito": False, "mensaje": "La cedula ya esta registrada"}

        usuario = Usuario.nuevo(cedula, nombre, correo, password,
                                telefono, "REPARTIDOR", latitud, longitud)
        usuario_guardado = self.usuario_dao.guardar(usuario)
        if not usuario_guardado:
            return {"exito": False, "mensaje": "Error al crear usuario"}

        repartidor = Repartidor.nuevo(usuario_guardado.get_id(), numero_tarjeta)
        if not self.repartidor_dao.guardar(repartidor):
            return {"exito": False, "mensaje": "Error al crear repartidor"}

        return {"exito": True,
                "mensaje": "Repartidor registrado correctamente",
                "id": usuario_guardado.get_id()}


    def login(self, correo, password):
        usuario = self.usuario_dao.buscar_por_correo(correo)
        if not usuario:
            return {"exito": False, "mensaje": "Correo o contrasena incorrectos"}

        if not usuario.verificar_password(password):
            return {"exito": False, "mensaje": "Correo o contrasena incorrectos"}

        if usuario.get_rol() == "CLIENTE":
            cliente = self.cliente_dao.buscar_por_id(usuario.get_id())
            if cliente and not cliente.esta_activo():
                return {"exito": False,
                        "mensaje": "Tu cuenta esta suspendida. Contacta al administrador."}

        if usuario.get_rol() == "REPARTIDOR":
            repartidor = self.repartidor_dao.buscar_por_id(usuario.get_id())
            if repartidor and repartidor.estado == "SUSPENDIDO":
                return {"exito": False,
                        "mensaje": "Tu cuenta esta suspendida. Contacta al administrador."}

        return {
            "exito":  True,
            "mensaje": "Login exitoso",
            "id":     usuario.get_id(),
            "nombre": usuario.nombre,
            "rol":    usuario.get_rol()
        }

    def _generar_codigo(self, longitud=6):
        return "".join(random.choices(string.digits, k=longitud))

    def solicitar_recuperacion(self, correo_o_telefono, metodo):
        usuario = (self.usuario_dao.buscar_por_correo(correo_o_telefono)
                   or self.usuario_dao.buscar_por_telefono(correo_o_telefono))
        if not usuario:
            return {"exito": True,
                    "mensaje": "Si el dato esta registrado, recibiras el codigo en breve"}

        codigo = self._generar_codigo()
        expira = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

        self.recuperacion_dao.guardar(usuario.get_id(), codigo, expira)

        if metodo == "email":
            enviado = self._enviar_email(usuario.correo, usuario.nombre, codigo)
        else:
            enviado = self._enviar_sms(usuario.telefono, codigo)

        if not enviado:
            return {"exito": False,
                    "mensaje": f"No se pudo enviar el codigo por {metodo}. Intentalo de nuevo."}

        return {"exito": True,
                "mensaje": f"Codigo enviado por {metodo}"}

    def verificar_codigo(self, correo_o_telefono, codigo):
        usuario = (self.usuario_dao.buscar_por_correo(correo_o_telefono)
                   or self.usuario_dao.buscar_por_telefono(correo_o_telefono))
        if not usuario:
            return {"exito": False, "mensaje": "Usuario no encontrado"}

        rec = self.recuperacion_dao.buscar_por_usuario(usuario.get_id())
        if not rec:
            return {"exito": False, "mensaje": "No hay un codigo activo para este usuario"}

        ahora = datetime.datetime.utcnow()
        if ahora > rec["expira"]:
            self.recuperacion_dao.eliminar(usuario.get_id())
            return {"exito": False, "mensaje": "El codigo ha expirado. Solicitalo de nuevo"}

        if rec["codigo"] != codigo:
            return {"exito": False, "mensaje": "Codigo incorrecto"}

        self.recuperacion_dao.marcar_verificado(usuario.get_id())
        return {"exito": True, "mensaje": "Codigo verificado correctamente"}

    def cambiar_password(self, correo_o_telefono, codigo, nueva_password):
        if len(nueva_password) < 8:
            return {"exito": False,
                    "mensaje": "La contrasena debe tener al menos 8 caracteres"}

        usuario = (self.usuario_dao.buscar_por_correo(correo_o_telefono)
                   or self.usuario_dao.buscar_por_telefono(correo_o_telefono))
        if not usuario:
            return {"exito": False, "mensaje": "Usuario no encontrado"}

        rec = self.recuperacion_dao.buscar_por_usuario(usuario.get_id())
        if not rec:
            return {"exito": False, "mensaje": "No hay un proceso de recuperacion activo"}

        if rec["codigo"] != codigo:
            return {"exito": False, "mensaje": "Codigo incorrecto"}

        if not rec.get("verificado"):
            return {"exito": False, "mensaje": "El codigo no ha sido verificado"}

        ahora = datetime.datetime.utcnow()
        if ahora > rec["expira"]:
            self.recuperacion_dao.eliminar(usuario.get_id())
            return {"exito": False, "mensaje": "El codigo ha expirado"}

        nueva_hash = bcrypt.hashpw(
            nueva_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        ok = self.usuario_dao.actualizar_contrasena(usuario.get_id(), nueva_hash)
        if not ok:
            return {"exito": False, "mensaje": "Error al actualizar la contrasena"}

        self.recuperacion_dao.eliminar(usuario.get_id())
        return {"exito": True, "mensaje": "Contrasena actualizada correctamente"}

    def _enviar_email(self, destinatario, nombre, codigo):
        import urllib.request
        import json

        api_key       = os.environ.get("SENDGRID_API_KEY", "")
        email_from    = os.environ.get("EMAIL_REMITENTE", "noreply@cletaeats.com")

        if not api_key:
            print("[EMAIL] SENDGRID_API_KEY no configurada")
            return False

        payload = {
            "personalizations": [{
                "to": [{"email": destinatario}],
                "subject": "Tu codigo de recuperacion — CletaEats"
            }],
            "from": {"email": email_from, "name": "CletaEats"},
            "content": [{
                "type": "text/html",
                "value": f"""
                <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;padding:24px;
                            border-radius:12px;border:1px solid #e0e0e0">
                  <h2 style="color:#00695c">Hola, {nombre} 👋</h2>
                  <p>Recibimos una solicitud para recuperar tu contrasena en <strong>CletaEats</strong>.</p>
                  <p>Tu codigo de verificacion es:</p>
                  <div style="font-size:36px;font-weight:bold;letter-spacing:8px;
                              color:#00695c;text-align:center;padding:16px;
                              background:#f0faf7;border-radius:8px;margin:16px 0">
                    {codigo}
                  </div>
                  <p style="color:#757575;font-size:13px">
                    Este codigo expira en <strong>15 minutos</strong>.
                    Si no solicitaste esto, ignora este mensaje.
                  </p>
                </div>
                """
            }]
        }

        try:
            req = urllib.request.Request(
                "https://api.sendgrid.com/v3/mail/send",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type":  "application/json"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status in (200, 202)
        except Exception as e:
            print(f"[EMAIL] Error al enviar: {e}")
            return False

    def _enviar_sms(self, telefono, codigo):
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
        auth_token  = os.environ.get("TWILIO_AUTH_TOKEN", "")
        from_number = os.environ.get("TWILIO_PHONE_FROM", "")

        if not account_sid or not auth_token:
            print(f"[SMS-DEV] Codigo para {telefono}: {codigo}")
            return True

        import urllib.request
        import urllib.parse
        import base64

        try:
            payload = urllib.parse.urlencode({
                "To":   telefono if telefono.startswith("+") else f"+506{telefono}",
                "From": from_number,
                "Body": f"Tu codigo CletaEats es: {codigo}. Expira en 15 min."
            }).encode("utf-8")

            credentials = base64.b64encode(
                f"{account_sid}:{auth_token}".encode()
            ).decode()

            url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
            req = urllib.request.Request(
                url, data=payload,
                headers={"Authorization": f"Basic {credentials}"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status in (200, 201)
        except Exception as e:
            print(f"[SMS] Error al enviar: {e}")
            return False
