import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp"
}


class PictureReportGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Picture Report Generator"
        )

        self.root.geometry(
            "1200x700"
        )

        self.root.minsize(
            1000,
            650
        )

        self.project_folder = None

        self.build_gui()

    def build_gui(self):

        # ==========================
        # TOP BAR
        # ==========================

        top = ttk.Frame(self.root)

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Button(
            top,
            text="Browse Folder",
            command=self.select_folder
        ).pack(
            side="left"
        )

        ttk.Button(
            top,
            text="Refresh",
            command=self.refresh_project
        ).pack(
            side="left",
            padx=5
        )

        self.folder_label = ttk.Label(
            top,
            text="No Folder Selected"
        )

        self.folder_label.pack(
            side="left",
            padx=15
        )

        # ==========================
        # MAIN FRAME
        # ==========================

        main = ttk.Frame(self.root)

        main.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        main.columnconfigure(
            0,
            weight=1
        )

        main.columnconfigure(
            1,
            weight=2
        )

        main.rowconfigure(
            1,
            weight=1
        )

        # ==========================
        # STATUS PANEL
        # ==========================

        status_frame = ttk.LabelFrame(
            main,
            text="Project Status"
        )

        status_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.labels_status = ttk.Label(
            status_frame,
            text="labels.json"
        )

        self.order_status = ttk.Label(
            status_frame,
            text="label_order.json"
        )

        self.plan_status = ttk.Label(
            status_frame,
            text="page_plan.json"
        )

        self.report_status = ttk.Label(
            status_frame,
            text="Prototype_Report.xlsx"
        )

        self.labels_status.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.order_status.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.plan_status.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.report_status.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        # ==========================
        # IMAGE SUMMARY
        # ==========================

        summary_frame = ttk.LabelFrame(
            main,
            text="Image Summary"
        )

        summary_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.total_images_var = tk.StringVar(
            value="0"
        )

        self.labeled_images_var = tk.StringVar(
            value="0"
        )

        self.unlabeled_images_var = tk.StringVar(
            value="0"
        )

        self.orphaned_var = tk.StringVar(
            value="0"
        )

        ttk.Label(
            summary_frame,
            text="Total Images:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        ttk.Label(
            summary_frame,
            textvariable=self.total_images_var
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        ttk.Label(
            summary_frame,
            text="Labeled Images:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        ttk.Label(
            summary_frame,
            textvariable=self.labeled_images_var
        ).grid(
            row=1,
            column=1,
            sticky="w"
        )

        ttk.Label(
            summary_frame,
            text="Unlabeled Images:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        ttk.Label(
            summary_frame,
            textvariable=self.unlabeled_images_var
        ).grid(
            row=2,
            column=1,
            sticky="w"
        )

        ttk.Label(
            summary_frame,
            text="Orphaned Labels:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        ttk.Label(
            summary_frame,
            textvariable=self.orphaned_var
        ).grid(
            row=3,
            column=1,
            sticky="w"
        )

        # ==========================
        # ISSUE LISTS
        # ==========================

        lists_frame = ttk.Frame(main)

        lists_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5
        )

        lists_frame.columnconfigure(
            0,
            weight=1
        )

        lists_frame.columnconfigure(
            1,
            weight=1
        )

        lists_frame.rowconfigure(
            0,
            weight=1
        )

        unlabeled_frame = ttk.LabelFrame(
            lists_frame,
            text="Unlabeled Images"
        )

        unlabeled_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5
        )

        self.unlabeled_list = tk.Listbox(
            unlabeled_frame
        )

        self.unlabeled_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        orphaned_frame = ttk.LabelFrame(
            lists_frame,
            text="Orphaned Labels"
        )

        orphaned_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5
        )

        self.orphaned_list = tk.Listbox(
            orphaned_frame
        )

        self.orphaned_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ==========================
        # TOOLS
        # ==========================

        tools = ttk.LabelFrame(
            self.root,
            text="Tools"
        )

        tools.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.label_btn = ttk.Button(
            tools,
            text="Label Photos"
        )

        self.review_btn = ttk.Button(
            tools,
            text="Review Labels"
        )

        self.order_btn = ttk.Button(
            tools,
            text="Order Figures"
        )

        self.plan_btn = ttk.Button(
            tools,
            text="Build Page Plan"
        )

        self.export_btn = ttk.Button(
            tools,
            text="Generate Report"
        )

        self.label_btn.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.review_btn.pack(
            side="left",
            padx=5
        )

        self.order_btn.pack(
            side="left",
            padx=5
        )

        self.plan_btn.pack(
            side="left",
            padx=5
        )

        self.export_btn.pack(
            side="left",
            padx=5
        )

        # ==========================
        # FOOTER STATUS
        # ==========================

        footer = ttk.Frame(
            self.root
        )

        footer.pack(
            fill="x",
            side="bottom"
        )

        self.status_label = tk.Label(
            footer,
            text="Select a project folder",
            anchor="w",
            font=(
                "Segoe UI",
                12,
                "bold"
            ),
            bg="#f0f0f0"
        )

        self.status_label.pack(
            fill="x",
            padx=10,
            pady=5
        )

    def select_folder(self):

        folder = filedialog.askdirectory()

        if not folder:
            return

        self.project_folder = Path(folder)

        self.folder_label.config(
            text=str(
                self.project_folder
            )
        )

        self.refresh_project()

    def file_exists(
        self,
        filename
    ):

        return (
            self.project_folder /
            filename
        ).exists()

    def set_status_label(
        self,
        widget,
        exists
    ):

        if exists:

            widget.config(
                text=f"✅ {widget.cget('text').split(' ',1)[-1]}"
            )

        else:

            widget.config(
                text=f"❌ {widget.cget('text').split(' ',1)[-1]}"
            )

    def get_images(self):

        files = []

        for path in self.project_folder.iterdir():

            if (
                path.is_file()
                and
                path.suffix.lower()
                in IMAGE_EXTENSIONS
            ):

                files.append(
                    path.name
                )

        return sorted(files)

    def load_labels(self):

        file = (
            self.project_folder /
            "labels.json"
        )

        if not file.exists():
            return {}

        try:

            with open(
                file,
                "r"
            ) as f:

                return json.load(f)

        except Exception:

            return {}

    def refresh_project(self):

        if not self.project_folder:
            return

        labels_exists = self.file_exists(
            "labels.json"
        )

        order_exists = self.file_exists(
            "label_order.json"
        )

        plan_exists = self.file_exists(
            "page_plan.json"
        )

        report_exists = self.file_exists(
            "Prototype_Report.xlsx"
        )

        self.set_status_label(
            self.labels_status,
            labels_exists
        )

        self.set_status_label(
            self.order_status,
            order_exists
        )

        self.set_status_label(
            self.plan_status,
            plan_exists
        )

        self.set_status_label(
            self.report_status,
            report_exists
        )

        images = set(
            self.get_images()
        )

        labels = self.load_labels()

        labeled = set(
            labels.keys()
        )

        unlabeled = sorted(
            images - labeled
        )

        orphaned = sorted(
            labeled - images
        )

        self.total_images_var.set(
            str(len(images))
        )

        self.labeled_images_var.set(
            str(
                len(images)
                - len(unlabeled)
            )
        )

        self.unlabeled_images_var.set(
            str(len(unlabeled))
        )

        self.orphaned_var.set(
            str(len(orphaned))
        )

        self.unlabeled_list.delete(
            0,
            tk.END
        )

        self.orphaned_list.delete(
            0,
            tk.END
        )

        for item in unlabeled:

            self.unlabeled_list.insert(
                tk.END,
                item
            )

        for item in orphaned:

            self.orphaned_list.insert(
                tk.END,
                item
            )

        if orphaned:

            self.status_label.config(
                text=(
                    f"❌ EXPORT BLOCKED - "
                    f"{len(orphaned)} orphaned labels found"
                ),
                fg="red"
            )

        elif unlabeled:

            self.status_label.config(
                text=(
                    f"⚠ ACTION REQUIRED - "
                    f"{len(unlabeled)} images need labeling"
                ),
                fg="orange"
            )

        elif (
            labels_exists
            and order_exists
            and plan_exists
        ):

            self.status_label.config(
                text="✅ READY TO EXPORT",
                fg="green"
            )

        else:

            self.status_label.config(
                text="⚠ PROJECT INCOMPLETE",
                fg="orange"
            )


root = tk.Tk()

PictureReportGUI(root)

root.mainloop()