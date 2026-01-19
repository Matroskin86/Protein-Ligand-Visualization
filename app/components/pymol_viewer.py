import reflex as rx
from app.states.file_state import FileState


def pymol_viewer() -> rx.Component:
    """Component that renders the server-side generated PyMOL image."""
    return rx.el.div(
        rx.image(
            src=rx.get_upload_url(FileState.generated_image),
            alt="Molecular Visualization",
            class_name="w-full h-full object-contain bg-white transition-opacity duration-300",
            loading="eager",
        ),
        rx.cond(
            FileState.is_rendering,
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "loader_circle",
                        class_name="animate-spin h-10 w-10 text-indigo-600 mb-3",
                    ),
                    rx.el.p(
                        "Rendering high-quality ray-traced image...",
                        class_name="text-sm font-semibold text-gray-700",
                    ),
                    rx.el.p(
                        "Powered by PyMOL", class_name="text-xs text-gray-400 mt-1"
                    ),
                    class_name="bg-white/90 backdrop-blur px-8 py-6 rounded-2xl shadow-lg border border-gray-100 flex flex-col items-center",
                ),
                class_name="absolute inset-0 flex items-center justify-center z-10 bg-white/30 backdrop-blur-[1px] transition-all duration-300",
            ),
        ),
        rx.cond(
            FileState.render_error != "",
            rx.el.div(
                rx.el.div(
                    rx.icon("cigarette", class_name="h-10 w-10 text-red-500 mb-2"),
                    rx.el.p(
                        FileState.render_error,
                        class_name="text-sm font-medium text-red-600 text-center",
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-lg border border-red-100 flex flex-col items-center max-w-xs",
                ),
                class_name="absolute inset-0 flex items-center justify-center z-10 bg-gray-50/50",
            ),
        ),
        class_name="w-full h-full relative z-0 bg-white flex items-center justify-center",
    )