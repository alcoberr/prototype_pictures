import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import jayjay

from PIL import Image, ImageTk

from ui.labeler_frame import LabelerFrame
from ui.review_frame import ReviewFrame
from ui.label_order_frame import LabelOrderFrame
from ui.page_planner_frame import PagePlannerFrame

import sys
from pathlib import Path
import shutil

def resource_path(relative_path):

    try:

        base_path = Path(
            sys._MEIPASS
        )

    except Exception:

        base_path = Path(
            __file__
        ).resolve().parent

    return base_path / relative_path

class MainGUI:



    def __init__(self, root):

        self.workspace_folder = (
            Path.home()
            / "PictureReportWorkspace"
        )
        self.root = root

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_application_close
        )

        

        self.root.title(
            "Picture Report Generator"
        )

        self.root.geometry(
            "1600x900"
        )

        self.root.minsize(
            1200,
            800
        )

        self.project_folder = None
        self.active_folder = None

        self.ralph_image = None
        self.original_logo = None

        self.build_ui()

    def on_application_close(self):

        try:

            self.sync_workspace_to_project()

        except Exception as ex:

            print(
                "Sync error:",
                ex
            )

        self.root.destroy()
    # ======================================
    # UI
    # ======================================

    def sync_workspace_to_project(self):

        if not self.project_folder:
            return

        files_to_sync = [
            "labels.json",
            "report_structure.json",
            "label_order.json",
            "page_plan.json",
            "Prototype_Report.xlsx"
        ]

        for filename in files_to_sync:

            source = (
                self.workspace_folder /
                filename
            )

            destination = (
                self.project_folder /
                filename
            )

            if source.exists():

                shutil.copy2(
                    source,
                    destination
                )

    def load_project_to_workspace(
    self,
    source_folder
):

        self.workspace_folder.mkdir(
            exist_ok=True
        )

        for item in self.workspace_folder.iterdir():

            if item.is_file():

                item.unlink()

        image_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".tif",
            ".tiff",
            ".webp"
        }

        project_files = {
            "labels.json",
            "report_structure.json",
            "label_order.json",
            "page_plan.json",
            "Prototype_Report.xlsx"
        }

        for file in source_folder.iterdir():

            if (
                file.is_file()
                and
                (
                    file.suffix.lower() in image_extensions
                    or
                    file.name in project_files
                )
            ):

                shutil.copy2(
                    file,
                    self.workspace_folder /
                    file.name
                )

    def build_ui(self):

        self.sidebar = ttk.Frame(
            self.root,
            width=250
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )

        self.content = ttk.Frame(
            self.root
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        ttk.Label(
            self.sidebar,
            text="Picture Report",
            font=(
                "Segoe UI",
                16,
                "bold"
            )
        ).pack(
            pady=20
        )

        ttk.Button(
            self.sidebar,
            text="Browse Folder",
            command=self.select_folder
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

        ttk.Button(
            self.sidebar,
            text="Dashboard",
            command=self.show_dashboard
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

        ttk.Separator(
            self.sidebar
        ).pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.label_btn = ttk.Button(
            self.sidebar,
            text="Label Photos",
            command=self.show_labeler
        )

        self.review_btn = ttk.Button(
            self.sidebar,
            text="Review Labels",
            command=self.show_review
        )

        self.order_btn = ttk.Button(
            self.sidebar,
            text="Order Figures",
            command=self.show_order
        )

        self.plan_btn = ttk.Button(
            self.sidebar,
            text="Page Planner",
            command=self.show_page_planner
        )

        self.export_btn = ttk.Button(
            self.sidebar,
            text="Generate Report",
            command=self.generate_report
        )

        self.label_btn.pack(
            fill="x",
            padx=10,
            pady=2
        )

        self.review_btn.pack(
            fill="x",
            padx=10,
            pady=2
        )

        self.order_btn.pack(
            fill="x",
            padx=10,
            pady=2
        )

        self.plan_btn.pack(
            fill="x",
            padx=10,
            pady=2
        )

        self.export_btn.pack(
            fill="x",
            padx=10,
            pady=2
        )

        self.folder_label = ttk.Label(
            self.sidebar,
            text="No Folder Selected",
            wraplength=220
        )

        self.folder_label.pack(
            fill="x",
            padx=10,
            pady=20
        )
        ttk.Label(
            self.sidebar,
            text="Serial Number"
        ).pack(
            anchor="w",
            padx=10
        )

        self.serial_number_var = tk.StringVar()

        self.serial_entry = ttk.Entry(
            self.sidebar,
            textvariable=self.serial_number_var
        )

        self.serial_entry.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        # -------------------------------
        # Ralph Footer
        # -------------------------------

        footer = ttk.Frame(
            self.sidebar
        )

        footer.pack(
            side="bottom",
            fill="both",
            expand=True
        )

        self.logo_label = ttk.Label(
            footer
        )

        self.logo_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        try:

            logo_path = resource_path(
                "ralph.png"
            )

            if logo_path.exists():

                self.original_logo = (
                    Image.open(
                        logo_path
                    )
                )

                self.logo_label.bind(
                    "<Configure>",
                    self.resize_logo
                )

        except Exception as ex:

            print(
                "Logo error:",
                ex
            )

        self.show_dashboard()

    # ======================================
    # Ralph Image
    # ======================================

    def resize_logo(self, event):

        if not self.original_logo:
            return

        width = max(
            event.width,
            1
        )

        height = max(
            event.height,
            1
        )

        image = (
            self.original_logo.copy()
        )

        image.thumbnail(
            (
                width,
                height
            ),
            Image.Resampling.LANCZOS
        )

        self.ralph_image = (
            ImageTk.PhotoImage(
                image
            )
        )

        self.logo_label.configure(
            image=self.ralph_image
        )

    # ======================================
    # Screen Management
    # ======================================

    def clear_content(self):

        for widget in (
            self.content.winfo_children()
        ):
            widget.destroy()

    # ======================================
    # Dashboard
    # ======================================

    def show_dashboard(self):

        self.sync_workspace_to_project()

        self.clear_content()

        frame = ttk.Frame(
            self.content
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        ttk.Label(
            frame,
            text="Picture Report Dashboard",
            font=(
                "Segoe UI",
                20,
                "bold"
            )
        ).pack(
            pady=20
        )

        if not self.project_folder:

            ttk.Label(
                frame,
                text="Select a folder to begin."
            ).pack(
                pady=20
            )

            return

        ttk.Label(
            frame,
            text=f"Folder:\n{self.project_folder}"
        ).pack(
            pady=10
        )

        status_frame = ttk.LabelFrame(
            frame,
            text="Project Status"
        )

        status_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        checks = [
            "labels.json",
            "report_structure.json",
            "label_order.json",
            "page_plan.json",
            "Prototype_Report.xlsx"
        ]

        for filename in checks:

            if self.active_folder:

                exists = (
                    self.active_folder /
                    filename
                ).exists()

            else:

                exists = False

            icon = (
                "✅"
                if exists
                else "❌"
            )

            tk.Label(
                status_frame,
                text=f"{icon} {filename}",
                anchor="w"
            ).pack(
                fill="x",
                padx=10,
                pady=2
            )

    # ======================================
    # Pages
    # ======================================

    def show_labeler(self):

        if not self.project_folder:
            return

        self.clear_content()

        LabelerFrame(
            self.content,
            self.active_folder
        ).pack(
            fill="both",
            expand=True
        )

    def show_review(self):

        if not self.project_folder:
            return

        self.clear_content()

        ReviewFrame(
            self.content,
            self.active_folder
        ).pack(
            fill="both",
            expand=True
        )

    def show_order(self):

        if not self.project_folder:
            return

        self.clear_content()

        LabelOrderFrame(
            self.content,
            self.active_folder
        ).pack(
            fill="both",
            expand=True
        )

    def show_page_planner(self):

        if not self.project_folder:
            return

        self.clear_content()

        PagePlannerFrame(
            self.content,
            self.active_folder
        ).pack(
            fill="both",
            expand=True
        )

    def generate_report(self):

        if not self.project_folder:
            return

        try:

            output_file = jayjay.main(
                self.active_folder,
                self.serial_number_var.get().strip()
            )
            self.sync_workspace_to_project()

            self.show_dashboard()

            from tkinter import messagebox

            messagebox.showinfo(
                "Report Generated",
                f"Created:\n\n{output_file}"
            )

        except Exception as ex:

            from tkinter import messagebox

            messagebox.showerror(
                "Export Error",
                str(ex)
            )

    # ======================================
    # Folder Selection
    # ======================================

    def select_folder(self):

        folder = (
            filedialog.askdirectory()
        )

        if not folder:
            return

        self.project_folder = Path(
            folder
        )

        self.load_project_to_workspace(
            self.project_folder
        )

        self.active_folder = (
            self.workspace_folder
        )

        self.folder_label.config(
            text=str(
                self.project_folder
            )
        )

        self.show_dashboard()


if __name__ == "__main__":

    root = tk.Tk()

    MainGUI(root)

    root.mainloop()