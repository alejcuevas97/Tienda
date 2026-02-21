import reflex as rx
import httpx
import asyncio

# La dirección donde vive tu Django
API_URL = "http://localhost:8000/api/v1/tienda/"

class State(rx.State):
    """El cerebro de la aplicación: maneja los datos y la comunicación con Django."""
    
    # Lista de productos recuperados
    productos: list[dict] = []
    
    # Variables para el formulario de creación
    form_nombre: str = ""
    form_descripcion: str = ""
    form_precio: str = ""

    async def cargar_productos(self):
        """Consulta la API de Django para refrescar la lista."""
        async with httpx.AsyncClient() as client:
            try:
                # Tu endpoint GET es /api/v1/tienda/
                resp = await client.get(API_URL)
                if resp.status_code == 200:
                    self.productos = resp.json()
            except Exception as ex:
                print(f"Error de conexión: {ex}")

    async def guardar_producto(self):
        """Envía los datos del formulario a Django."""
        if not self.form_nombre or not self.form_precio:
            return # Validación básica

        nuevo_producto = {
            "nombre": self.form_nombre,
            "descripcion": self.form_descripcion,
            "precio": float(self.form_precio)
        }

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(API_URL, json=nuevo_producto)
                if resp.status_code == 201:
                    # Si tuvo éxito, recargamos la lista y limpiamos el formulario
                    await self.cargar_productos()
                    self.form_nombre = ""
                    self.form_descripcion = ""
                    self.form_precio = ""
            except Exception as ex:
                print(f"Error al guardar: {ex}")

    async def eliminar_producto(self, id_prod: int):
        """Elimina un producto usando su ID."""
        # Tu urls.py define la ruta como 'v1/tienda/<int:id>' sin slash final
        url_delete = f"{API_URL}{id_prod}"
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.delete(url_delete)
                if resp.status_code == 200:
                    await self.cargar_productos()
            except Exception as ex:
                print(f"Error al eliminar: {ex}")

def row_producto(producto: dict):
    """Componente visual para cada fila de la tabla."""
    return rx.table.row(
        rx.table.cell(producto["nombre"]),
        rx.table.cell(producto["descripcion"]),
        rx.table.cell(f"${producto['precio']}"),
        rx.table.cell(
            rx.button(
                "Eliminar",
                on_click=lambda: State.eliminar_producto(producto["id"]),
                color_scheme="red",
                variant="soft"
            )
        )
    )

def index():
    """La vista principal."""
    return rx.container(
        rx.vstack(
            rx.heading("Gestión de Inventario", size="8", margin_bottom="1em"),
            
            # --- Formulario de Ingreso ---
            rx.card(
                rx.vstack(
                    rx.heading("Nuevo Producto", size="4"),
                    rx.input(
                        placeholder="Nombre del producto", 
                        value=State.form_nombre, 
                        on_change=State.set_form_nombre
                    ),
                    rx.input(
                        placeholder="Descripción", 
                        value=State.form_descripcion, 
                        on_change=State.set_form_descripcion
                    ),
                    rx.input(
                        placeholder="Precio", 
                        value=State.form_precio, 
                        on_change=State.set_form_precio,
                        type="number"
                    ),
                    rx.button("Guardar en Django", on_click=State.guardar_producto, width="100%"),
                    spacing="3"
                ),
                width="100%",
                max_width="400px"
            ),

            # --- Tabla de Datos ---
            rx.divider(),
            rx.heading("Catálogo Actual", size="5"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Nombre"),
                        rx.table.column_header_cell("Descripción"),
                        rx.table.column_header_cell("Precio"),
                        rx.table.column_header_cell("Acción"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(State.productos, row_producto)
                ),
                width="100%"
            ),
            spacing="5",
            align="center",
            padding_top="2em"
        ),
        # Evento mágico: Cargar datos apenas se abre la página
        on_mount=State.cargar_productos
    )

app = rx.App()
app.add_page(index)