import reflex as rx
from app.states.file_state import FileState, FileInfo


def file_item(file: FileInfo) -> rx.Component:
    """Renders a single file item in the list."""
    is_selected = FileState.selected_file == file["name"]
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "file-text",
                        class_name="h-8 w-8 text-gray-400 p-1.5 bg-gray-50 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.p(
                            file["name"],
                            class_name="text-sm font-semibold text-gray-800 truncate",
                        ),
                        rx.el.div(
                            rx.el.span(
                                file["type"],
                                class_name="text-[10px] uppercase font-bold text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded mr-2",
                            ),
                            rx.el.span(
                                file["size"], class_name="text-xs text-gray-400"
                            ),
                            class_name="flex items-center mt-0.5",
                        ),
                        class_name="flex flex-col items-start overflow-hidden ml-3 flex-1",
                    ),
                    class_name="flex items-center w-full",
                ),
                class_name="w-full text-left",
            ),
            on_click=FileState.select_file(file["name"]),
            class_name="flex-1 min-w-0",
        ),
        rx.el.button(
            rx.icon(
                "trash-2",
                class_name="h-4 w-4 text-gray-400 hover:text-red-500 transition-colors",
            ),
            on_click=FileState.delete_file(file["name"]),
            class_name="p-2 ml-2 hover:bg-red-50 rounded-lg transition-colors group/delete",
        ),
        class_name=rx.cond(
            is_selected,
            "flex items-center p-3 rounded-xl bg-indigo-50 border border-indigo-200 shadow-sm transition-all relative",
            "flex items-center p-3 rounded-xl bg-white border border-transparent hover:border-gray-200 hover:shadow-sm transition-all relative",
        ),
    )


def file_list() -> rx.Component:
    """Component to display the list of uploaded files."""
    return rx.el.div(
        rx.el.h3(
            "Uploaded Molecules",
            class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 px-1",
        ),
        rx.cond(
            FileState.has_files,
            rx.el.div(
                rx.foreach(FileState.uploaded_files, file_item),
                class_name="flex flex-col gap-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("test-tube", class_name="h-8 w-8 text-gray-300 mb-2"),
                    rx.el.p(
                        "No molecules yet",
                        class_name="text-sm font-medium text-gray-400",
                    ),
                    rx.el.p(
                        "Upload files to begin", class_name="text-xs text-gray-300"
                    ),
                    class_name="flex flex-col items-center justify-center py-8 px-4 text-center border-2 border-dashed border-gray-100 rounded-xl",
                ),
                class_name="mt-2",
            ),
        ),
        class_name="flex-1 overflow-y-auto pr-1",
    )