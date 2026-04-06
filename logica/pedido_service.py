from dao.combo_dao import ComboDAO
# Importar PedidoDAO y RepartidorDAO cuando estén creados

class PedidoService:
    def __init__(self):
        self.combo_dao = ComboDAO()

    def calcular_monto_combo(self, numero):
        # El primer combo vale 4000, y así aumenta de 1000 en 1000
        return 4000.00 + ((numero - 1) * 1000.00)

    def crear_pedido(self, cliente_id, restaurante_id, lista_combos):
        subtotal = 0
        detalles = []

        for item in lista_combos:  # item = {"numero": 1, "cantidad": 2}
            precio = self.calcular_monto_combo(item['numero'])
            subtotal += precio * item['cantidad']
            detalles.append({
                "numero": item['numero'],
                "cantidad": item['cantidad'],
                "precio": precio
            })

        costo_envio = 1000.00  # Simplificado para el ejemplo[cite: 1]
        iva = (subtotal + costo_envio) * 0.13
        total = subtotal + costo_envio + iva

        # Aquí llamarías al DAO para guardar en la BD
        return {
            "exito": True,
            "resumen": {
                "subtotal": subtotal,
                "envio": costo_envio,
                "iva": iva,
                "total": total
            }
        }