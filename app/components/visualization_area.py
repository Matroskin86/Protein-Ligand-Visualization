import reflex as rx
from app.states.file_state import FileState
from app.components.pymol_viewer import pymol_viewer


def control_select(
    label: str, options: list[str], value: str, on_change: rx.event.EventType
) -> rx.Component:
    """Helper for select controls."""
    return rx.el.div(
        rx.el.label(
            label,
            class_name="text-[10px] uppercase font-bold text-gray-400 mb-1 block tracking-wide",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(options, lambda x: rx.el.option(x, value=x)),
                value=value,
                on_change=on_change,
                class_name="w-full bg-gray-50 border border-gray-200 text-gray-700 text-xs rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-2 outline-none appearance-none cursor-pointer hover:bg-gray-100 transition-colors",
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-2 top-1/2 -translate-y-1/2 h-3 w-3 text-gray-400 pointer-events-none",
            ),
            class_name="relative",
        ),
        class_name="w-32",
    )


def view_settings_panel() -> rx.Component:
    """Floating panel for visualization settings."""
    return rx.el.div(
        rx.el.div(
            rx.icon("sliders-horizontal", class_name="h-4 w-4 text-gray-400 mr-2"),
            rx.el.span(
                "View Settings", class_name="text-xs font-bold text-gray-500 uppercase"
            ),
            class_name="flex items-center mb-3 pb-2 border-b border-gray-100",
        ),
        rx.el.div(
            control_select(
                "Style",
                FileState.representation_options,
                FileState.representation,
                FileState.set_representation,
            ),
            control_select(
                "Color Scheme",
                FileState.color_options,
                FileState.color_scheme,
                FileState.set_color_scheme,
            ),
            class_name="flex flex-col gap-3",
        ),
        class_name="absolute top-4 right-4 bg-white/95 backdrop-blur-sm p-4 rounded-xl shadow-lg border border-gray-100 z-10 transition-all hover:shadow-xl",
    )


def icon_button(icon: str, on_click: rx.event.EventType, tooltip: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="h-5 w-5 text-gray-600"),
        on_click=on_click,
        class_name="p-2.5 bg-white rounded-xl shadow-sm border border-gray-200 hover:bg-gray-50 transition-all hover:-translate-y-0.5 active:translate-y-0 tooltip-trigger group/btn relative",
        title=tooltip,
    )


def view_controls() -> rx.Component:
    """Preset view controls."""
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "Orientation",
                class_name="text-[10px] uppercase font-bold text-gray-400 mb-1 px-1",
            ),
            rx.el.div(
                rx.el.button(
                    "Front",
                    on_click=FileState.set_view_preset("front"),
                    class_name="px-2 py-1 text-xs font-medium bg-white border border-gray-200 rounded hover:bg-gray-50",
                ),
                rx.el.button(
                    "Back",
                    on_click=FileState.set_view_preset("back"),
                    class_name="px-2 py-1 text-xs font-medium bg-white border border-gray-200 rounded hover:bg-gray-50",
                ),
                rx.el.button(
                    "Left",
                    on_click=FileState.set_view_preset("left"),
                    class_name="px-2 py-1 text-xs font-medium bg-white border border-gray-200 rounded hover:bg-gray-50",
                ),
                rx.el.button(
                    "Right",
                    on_click=FileState.set_view_preset("right"),
                    class_name="px-2 py-1 text-xs font-medium bg-white border border-gray-200 rounded hover:bg-gray-50",
                ),
                rx.el.button(
                    "Top",
                    on_click=FileState.set_view_preset("top"),
                    class_name="px-2 py-1 text-xs font-medium bg-white border border-gray-200 rounded hover:bg-gray-50",
                ),
                rx.el.button(
                    "Bottom",
                    on_click=FileState.set_view_preset("bottom"),
                    class_name="px-2 py-1 text-xs font-medium bg-white border border-gray-200 rounded hover:bg-gray-50",
                ),
                class_name="grid grid-cols-3 gap-1",
            ),
            class_name="flex flex-col gap-1",
        ),
        class_name="absolute top-4 left-4 bg-white/95 backdrop-blur-sm p-3 rounded-xl shadow-lg border border-gray-100 z-10 transition-all hover:shadow-xl",
    )


def visualization_controls() -> rx.Component:
    """Controls for the 3D viewer."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                icon_button("zoom-out", FileState.adjust_zoom(-1), "Zoom Out"),
                icon_button("zoom-in", FileState.adjust_zoom(1), "Zoom In"),
                class_name="flex gap-1 mr-2 pr-2 border-r border-gray-300",
            ),
            rx.el.div(
                icon_button("download", FileState.export_image, "Download PNG"),
                class_name="flex gap-1",
            ),
            class_name="flex gap-2 items-center bg-gray-100/50 p-1.5 rounded-2xl backdrop-blur-sm border border-gray-200/50",
        ),
        class_name="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2 z-10",
    )


def visualization_container() -> rx.Component:
    """The main visualization container with PyMOL backend."""
    return rx.el.div(
        pymol_viewer(),
        view_settings_panel(),
        view_controls(),
        visualization_controls(),
        class_name="w-full h-full relative bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden",
    )


def empty_state() -> rx.Component:
    """Shown when no file is selected."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("microscope", class_name="h-20 w-20 text-gray-200 mb-6"),
                rx.el.h2(
                    "No Molecule Selected",
                    class_name="text-2xl font-bold text-gray-400 mb-2",
                ),
                rx.el.p(
                    "Select a file from the sidebar or upload a new one to begin analysis.",
                    class_name="text-gray-400 text-center max-w-sm",
                ),
                class_name="flex flex-col items-center justify-center",
            ),
            class_name="w-full h-full border-4 border-dashed border-gray-200 rounded-3xl flex items-center justify-center",
        ),
        class_name="w-full h-full p-8",
    )


def visualization_area() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Visualization Workspace",
                    class_name="text-lg font-semibold text-gray-800",
                ),
                rx.cond(
                    FileState.selected_file != "",
                    rx.el.div(
                        rx.el.button(
                            rx.icon("download", class_name="h-4 w-4 mr-2"),
                            "Export PNG",
                            on_click=FileState.export_image,
                            class_name="flex items-center px-3 py-1.5 text-xs font-bold uppercase tracking-wide text-gray-600 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 hover:text-indigo-600 hover:border-indigo-200 transition-all shadow-sm",
                            title="Download current view as PNG image",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                ),
                class_name="flex items-center justify-between w-full",
            ),
            class_name="h-16 px-8 flex items-center border-b border-gray-100 bg-white",
        ),
        rx.el.div(
            rx.cond(
                FileState.selected_file != "",
                rx.el.div(visualization_container(), class_name="w-full h-full p-6"),
                empty_state(),
            ),
            class_name="flex-1 relative overflow-hidden bg-gray-50",
        ),
        class_name="flex-1 flex flex-col h-screen overflow-hidden",
    )