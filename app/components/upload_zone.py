import reflex as rx
from app.states.file_state import FileState


def upload_zone() -> rx.Component:
    """Component for uploading molecular files."""
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.el.div(
                    rx.icon("cloud-upload", class_name="h-8 w-8 text-indigo-500 mb-2"),
                    rx.el.p(
                        "Drag & drop or click to upload",
                        class_name="text-sm font-medium text-gray-700 text-center",
                    ),
                    rx.el.p(
                        "PDB, SDF, MOL2, CIF",
                        class_name="text-xs text-gray-400 mt-1 text-center",
                    ),
                    class_name="flex flex-col items-center justify-center p-6 border-2 border-dashed border-indigo-200 hover:border-indigo-400 rounded-xl bg-indigo-50/30 transition-colors cursor-pointer group-hover:bg-indigo-50",
                ),
                class_name="group",
            ),
            id="molecule_upload",
            accept=FileState.accepted_files,
            multiple=True,
            max_files=10,
            class_name="w-full",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files("molecule_upload"),
                lambda file: rx.el.div(
                    rx.el.div(
                        rx.icon("file", class_name="h-4 w-4 text-indigo-400 mr-2"),
                        rx.el.span(
                            file, class_name="text-sm text-gray-600 truncate flex-1"
                        ),
                        class_name="flex items-center w-full",
                    ),
                    class_name="flex items-center p-2 bg-white border border-gray-100 rounded-lg shadow-sm",
                ),
            ),
            class_name="flex flex-col gap-2 mt-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.cond(
                    FileState.is_uploading,
                    rx.el.span(
                        rx.icon(
                            "loader_circle", class_name="animate-spin h-4 w-4 mr-2"
                        ),
                        "Uploading...",
                        class_name="flex items-center",
                    ),
                    "Upload Files",
                ),
                on_click=FileState.handle_upload(
                    rx.upload_files(upload_id="molecule_upload")
                ),
                disabled=FileState.is_uploading,
                class_name="flex-1 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white text-sm font-semibold py-2.5 px-4 rounded-lg transition-all shadow-sm hover:shadow active:scale-[0.98] flex justify-center items-center",
            ),
            rx.el.button(
                "Clear",
                on_click=rx.clear_selected_files("molecule_upload"),
                class_name="bg-gray-100 hover:bg-gray-200 text-gray-600 text-sm font-semibold py-2.5 px-4 rounded-lg transition-colors",
            ),
            class_name="flex gap-2 mt-4",
        ),
        class_name="p-4 bg-white rounded-2xl shadow-sm border border-gray-100",
    )