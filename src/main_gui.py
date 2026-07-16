import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import jayjay

from PIL import Image, ImageTk

from ui.labeler_frame import LabelerFrame
from ui.review_frame import ReviewFrame
from ui.label_order_frame import LabelOrderFrame
from ui.page_planner_frame import PagePlannerFrame


class MainGUI:

    def __init__(self, root):

        self.root = root

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

        self.ralph_image = None
        self.original_logo = None

        self.build_ui()

    # ======================================
    # UI
    # ======================================

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

            logo_path = (
                Path(__file__).resolve().parent
                / "ralph.png"
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

            exists = (
                self.project_folder /
                filename
            ).exists()

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
            self.project_folder
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
            self.project_folder
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
            self.project_folder
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
            self.project_folder
        ).pack(
            fill="both",
            expand=True
        )

    def generate_report(self):

        if not self.project_folder:
            return

        try:

            output_file = jayjay.main(
                self.project_folder,
                self.serial_number_var.get().strip()
            )

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

        self.project_folder = (
            Path(folder)
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