import reflex as rx
from app.components.upload_zone import upload_zone
from app.components.file_list import file_list


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("dna", class_name="h-6 w-6 text-white"),
                    class_name="h-10 w-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200",
                ),
                rx.el.div(
                    rx.el.h1(
                        "BioViz",
                        class_name="text-xl font-bold text-gray-900 leading-none",
                    ),
                    rx.el.p(
                        "Platform",
                        class_name="text-xs font-semibold text-indigo-600 tracking-wide",
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center p-6 border-b border-gray-100",
            ),
            rx.el.div(
                rx.el.div(upload_zone(), class_name="p-4"),
                rx.el.div(class_name="h-px bg-gray-100 mx-4 mb-4"),
                rx.el.div(file_list(), class_name="px-4 pb-4 flex-1 overflow-y-auto"),
                class_name="flex flex-col flex-1 overflow-hidden",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "circle_gauge", class_name="h-4 w-4 text-gray-400 mr-2"
                        ),
                        rx.el.span(
                            "Help & Support",
                            class_name="text-sm font-medium text-gray-600",
                        ),
                        class_name="flex items-center cursor-pointer hover:text-indigo-600 transition-colors",
                    ),
                    class_name="flex items-center justify-between",
                ),
                class_name="p-4 border-t border-gray-100 bg-gray-50/50",
            ),
            class_name="flex flex-col h-full bg-white border-r border-gray-200 w-80 shadow-[4px_0_24px_-12px_rgba(0,0,0,0.1)] relative z-10",
        ),
        class_name="h-screen shrink-0",
    )