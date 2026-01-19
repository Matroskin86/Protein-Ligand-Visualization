import reflex as rx
from typing import TypedDict
import time
import os
import asyncio
import uuid
import logging
import shutil
from pathlib import Path

try:
    import pymol
    from pymol import cmd

    os.environ["PYMOL_LICENSE_FILE"] = ""
    try:
        pymol.finish_launching(["pymol", "-cq"])
    except Exception as e:
        logging.exception(f"Error launching PyMOL: {e}")
    PYMOL_AVAILABLE = True
except ImportError as e:
    PYMOL_AVAILABLE = False
    logging.exception(f"PyMOL not found. Visualization will not work. Error: {e}")


class FileInfo(TypedDict):
    name: str
    size: str
    type: str
    uploaded_at: str


class FileState(rx.State):
    """State management for file uploads and selection."""

    uploaded_files: list[FileInfo] = [
        {
            "name": "practice.pdb",
            "size": "Sample",
            "type": "PDB",
            "uploaded_at": "Default",
        }
    ]
    selected_file: str = "practice.pdb"
    is_uploading: bool = False
    generated_image: str = "/placeholder.svg"
    is_rendering: bool = False
    render_error: str = ""
    representation: str = "cartoon"
    color_scheme: str = "chain"
    view_preset: str = "front"
    zoom_level: int = 0
    representation_options: list[str] = [
        "cartoon",
        "surface",
        "sticks",
        "spheres",
        "ribbon",
        "lines",
        "dots",
        "mesh",
    ]
    color_options: list[str] = [
        "chain",
        "element",
        "ss",
        "rainbow",
        "b-factor",
        "red",
        "blue",
        "green",
        "gray",
    ]
    accepted_files: dict[str, list[str]] = {
        "chemical/x-pdb": [".pdb"],
        "chemical/x-mol2": [".mol2"],
        "chemical/x-sdf": [".sdf"],
        "text/plain": [".cif", ".xyz", ".gro"],
    }

    @rx.event
    async def load_default_data(self):
        """Initialize the app by copying the default asset to the upload dir."""
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        target_path = upload_dir / "practice.pdb"
        source_path = Path("assets/practice.pdb")
        if not target_path.exists():
            try:
                if source_path.exists():
                    await asyncio.to_thread(shutil.copy, source_path, target_path)
                    logging.info(f"Copied {source_path} to {target_path}")
                else:
                    logging.warning(f"Default file {source_path} not found in assets.")
            except Exception as e:
                logging.exception(f"Failed to copy default file: {e}")
        yield FileState.trigger_render

    @rx.event
    def set_representation(self, style: str):
        """Update the molecular representation style."""
        self.representation = style
        return FileState.trigger_render

    @rx.event
    def set_color_scheme(self, color: str):
        """Update the color scheme."""
        self.color_scheme = color
        return FileState.trigger_render

    @rx.event
    def set_view_preset(self, preset: str):
        """Set the camera view preset."""
        self.view_preset = preset
        return FileState.trigger_render

    @rx.event
    def adjust_zoom(self, delta: int):
        """Adjust zoom level."""
        self.zoom_level += delta
        self.zoom_level = max(-5, min(15, self.zoom_level))
        return FileState.trigger_render

    @rx.event
    def export_image(self):
        """Trigger image export (handled via browser download of the current image)."""
        return rx.download(
            url=f"/_upload/{self.generated_image}",
            filename=f"render_{self.selected_file}.png",
        )

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the file upload process."""
        if not files:
            yield rx.toast("No files selected", duration=3000)
            return
        self.is_uploading = True
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        count = 0
        last_file_name = ""
        for file in files:
            upload_data = await file.read()
            outfile = upload_dir / file.name
            with outfile.open("wb") as f:
                f.write(upload_data)
            size_bytes = len(upload_data)
            if size_bytes < 1024:
                size_str = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            else:
                size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
            file_info: FileInfo = {
                "name": file.name,
                "size": size_str,
                "type": file.name.split(".")[-1].upper(),
                "uploaded_at": time.strftime("%Y-%m-%d %H:%M"),
            }
            self.uploaded_files = [
                f for f in self.uploaded_files if f["name"] != file.name
            ]
            self.uploaded_files.append(file_info)
            count += 1
            last_file_name = file.name
        self.is_uploading = False
        yield rx.toast(f"Successfully uploaded {count} files", duration=3000)
        if not self.selected_file and last_file_name:
            self.selected_file = last_file_name
            yield FileState.trigger_render

    @rx.event
    async def select_file(self, filename: str):
        """Select a file for visualization and trigger load."""
        self.selected_file = filename
        yield FileState.trigger_render

    @rx.event
    async def delete_file(self, filename: str):
        """Remove a file from the list."""
        self.uploaded_files = [f for f in self.uploaded_files if f["name"] != filename]
        if self.selected_file == filename:
            self.selected_file = (
                "" if not self.uploaded_files else self.uploaded_files[0]["name"]
            )
            if self.selected_file:
                yield FileState.trigger_render
            else:
                self.generated_image = "/placeholder.svg"

    @rx.event
    async def trigger_render(self):
        """Start the background rendering process."""
        if not self.selected_file:
            return
        self.is_rendering = True
        yield FileState.render_molecule

    @rx.event(background=True)
    async def render_molecule(self):
        """Background task to render the molecule using PyMOL."""
        async with self:
            if not PYMOL_AVAILABLE:
                self.render_error = "PyMOL backend not available."
                self.is_rendering = False
                return
            upload_dir = rx.get_upload_dir()
            file_path = upload_dir / self.selected_file
            if not file_path.exists():
                self.render_error = "File not found."
                self.is_rendering = False
                return
            current_file = str(file_path)
            rep_style = self.representation
            color_mode = self.color_scheme
            view_preset = self.view_preset
            zoom_val = self.zoom_level
        output_filename = f"render_{uuid.uuid4().hex[:8]}.png"
        output_path = upload_dir / output_filename
        try:
            await asyncio.to_thread(
                self._run_pymol_render,
                current_file,
                output_path,
                rep_style,
                color_mode,
                view_preset,
                zoom_val,
            )
            async with self:
                self.generated_image = output_filename
                self.render_error = ""
                self.is_rendering = False
        except Exception as e:
            logging.exception(f"Rendering failed: {e}")
            async with self:
                self.render_error = f"Rendering failed: {str(e)}"
                self.is_rendering = False

    def _run_pymol_render(self, file_path, output_path, style, color, view, zoom):
        """Synchronous PyMOL commands run in thread."""
        try:
            file_path_str = str(file_path)
            output_path_str = str(output_path)
            cmd.reinitialize()
            cmd.load(file_path_str)
            cmd.hide("all")
            if style == "cartoon":
                cmd.show("cartoon")
            elif style == "surface":
                cmd.show("surface")
            elif style == "sticks":
                cmd.show("sticks")
            elif style == "spheres":
                cmd.show("spheres")
            elif style == "ribbon":
                cmd.show("ribbon")
            elif style == "lines":
                cmd.show("lines")
            elif style == "dots":
                cmd.show("dots")
            elif style == "mesh":
                cmd.show("mesh")
            else:
                cmd.show("cartoon")
            if color == "chain":
                cmd.util.cbc()
            elif color == "element":
                cmd.util.cba()
                cmd.color("green", "carbon")
            elif color == "ss":
                cmd.util.cbss()
            elif color == "rainbow":
                cmd.spectrum("count", "rainbow")
            elif color == "b-factor":
                cmd.spectrum("b", "blue_white_red")
            elif color in ["red", "blue", "green", "gray"]:
                cmd.color(color, "all")
            cmd.orient()
            if view == "back":
                cmd.turn("y", 180)
            elif view == "left":
                cmd.turn("y", 90)
            elif view == "right":
                cmd.turn("y", -90)
            elif view == "top":
                cmd.turn("x", 90)
            elif view == "bottom":
                cmd.turn("x", -90)
            buffer_val = -1 * zoom * 1.5
            if buffer_val < -5:
                buffer_val = -5
            cmd.zoom("all", buffer=buffer_val)
            cmd.ray(1200, 900)
            cmd.png(output_path_str)
        except Exception as e:
            logging.exception(f"PyMOL execution error: {e}")
            raise e

    @rx.var
    def has_files(self) -> bool:
        return len(self.uploaded_files) > 0

    @rx.var
    def current_file_info(self) -> FileInfo | None:
        """Get info for the currently selected file."""
        for f in self.uploaded_files:
            if f["name"] == self.selected_file:
                return f
        return None