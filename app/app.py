import reflex as rx
from app.components.sidebar import sidebar
from app.components.visualization_area import visualization_area
from app.states.file_state import FileState


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        visualization_area(),
        class_name="flex h-screen w-screen bg-white font-['Inter'] overflow-hidden",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.script(src="https://unpkg.com/ngl@2.0.0-dev.37/dist/ngl.js"),
    ],
)
app.add_page(index, route="/", on_load=FileState.load_default_data)