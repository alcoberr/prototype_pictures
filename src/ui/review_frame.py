import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

from core.review_session import ReviewSession


class ReviewFrame(ttk.Frame):

    def __init__(
        self,
        parent,
        project_folder,
        on_close=None
    ):

        super().__init__(parent)

        self.session = ReviewSession(
            project_folder
        )

        self.on_close = on_close

        self.current_photo = None

        self.build_ui()

        self.load_labels()

    # ==================================
    # UI
    # ==================================

    def build_ui(self):

        self.columnconfigure(
            0,
            weight=1
        )

        self.columnconfigure(
            1,
            weight=1
        )

        self.columnconfigure(
            2,
            weight=2
        )

        self.rowconfigure(
            1,
            weight=1
        )

        # Header

        header = ttk.Frame(self)

        header.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Label(
            header,
            text="Review Labels",
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).pack(
            side="left"
        )

        ttk.Button(
            header,
            text="Back",
            command=self.close
        ).pack(
            side="right"
        )

        # ==========================
        # Labels
        # ==========================

        labels_frame = ttk.LabelFrame(
            self,
            text="Labels"
        )

        labels_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.label_list = tk.Listbox(
            labels_frame
        )

        self.label_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.label_list.bind(
            "<<ListboxSelect>>",
            self.on_label_selected
        )

        # ==========================
        # Images
        # ==========================

        images_frame = ttk.LabelFrame(
            self,
            text="Images"
        )

        images_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.image_list = tk.Listbox(
            images_frame
        )

        self.image_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.image_list.bind(
            "<<ListboxSelect>>",
            self.on_image_selected
        )

        # ==========================
        # Preview
        # ==========================

        preview_frame = ttk.LabelFrame(
            self,
            text="Preview"
        )

        preview_frame.grid(
            row=1,
            column=2,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.preview_label = ttk.Label(
            preview_frame
        )

        self.preview_label.pack(
            fill="both",
            expand=True
        )

        # ==========================
        # Actions
        # ==========================

        action_frame = ttk.LabelFrame(
            self,
            text="Actions"
        )

        action_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Label(
            action_frame,
            text="Rename Label:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.rename_var = tk.StringVar()

        self.rename_entry = ttk.Entry(
            action_frame,
            textvariable=self.rename_var,
            width=30
        )

        self.rename_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Button(
            action_frame,
            text="Rename",
            command=self.rename_label
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        ttk.Label(
            action_frame,
            text="Merge Into:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.merge_combo = ttk.Combobox(
            action_frame,
            width=28
        )

        self.merge_combo.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Button(
            action_frame,
            text="Merge",
            command=self.merge_label
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

        ttk.Button(
            action_frame,
            text="Delete Label",
            command=self.delete_label
        ).grid(
            row=2,
            column=0,
            columnspan=3,
            pady=10
        )

    # ==================================
    # Helpers
    # ==================================

    def selected_label(self):

        selection = (
            self.label_list.curselection()
        )

        if not selection:
            return None

        text = self.label_list.get(
            selection[0]
        )

        return text.split(
            " ("
        )[0]

    # ==================================
    # Load Labels
    # ==================================

    def load_labels(self):

        self.label_list.delete(
            0,
            tk.END
        )

        counts = (
            self.session.get_label_counts()
        )

        for label, count in (
            counts.items()
        ):

            self.label_list.insert(
                tk.END,
                f"{label} ({count})"
            )

        self.merge_combo["values"] = (
            self.session.get_labels()
        )

    # ==================================
    # Label Selected
    # ==================================

    def on_label_selected(
        self,
        event=None
    ):

        label = (
            self.selected_label()
        )

        if not label:
            return

        self.image_list.delete(
            0,
            tk.END
        )

        self.rename_var.set(
            label
        )

        images = (
            self.session
            .get_images_for_label(
                label
            )
        )

        for item in images:

            self.image_list.insert(
                tk.END,
                item["file"]
            )

        if self.image_list.size() > 0:

            self.image_list.selection_set(
                0
            )

            self.on_image_selected()

    # ==================================
    # Image Preview
    # ==================================

    def on_image_selected(
        self,
        event=None
    ):

        selection = (
            self.image_list.curselection()
        )

        if not selection:
            return

        image_name = (
            self.image_list.get(
                selection[0]
            )
        )

        image_path = (
            self.session.image_folder
            / image_name
        )

        if not image_path.exists():
            return

        try:

            image = Image.open(
                image_path
            )

            image.thumbnail(
                (
                    900,
                    700
                )
            )

            self.current_photo = (
                ImageTk.PhotoImage(
                    image
                )
            )

            self.preview_label.configure(
                image=self.current_photo,
                text=""
            )

        except Exception as ex:

            self.preview_label.configure(
                image="",
                text=str(ex)
            )

    # ==================================
    # Actions
    # ==================================

    def rename_label(self):

        old_label = (
            self.selected_label()
        )

        new_label = (
            self.rename_var
            .get()
            .strip()
        )

        if not old_label:
            return

        if not new_label:
            return

        self.session.rename_label(
            old_label,
            new_label
        )

        self.load_labels()

    def merge_label(self):

        source = (
            self.selected_label()
        )

        target = (
            self.merge_combo
            .get()
            .strip()
        )

        if not source:
            return

        if not target:
            return

        if source == target:

            messagebox.showwarning(
                "Merge",
                "Choose a different target label."
            )

            return

        self.session.merge_labels(
            source,
            target
        )

        self.load_labels()

    def delete_label(self):

        label = (
            self.selected_label()
        )

        if not label:
            return

        if not messagebox.askyesno(
            "Delete Label",
            (
                f"Delete label:\n\n"
                f"{label}\n\n"
                f"This removes all assignments."
            )
        ):
            return

        self.session.delete_label(
            label
        )

        self.image_list.delete(
            0,
            tk.END
        )

        self.preview_label.configure(
            image="",
            text=""
        )

        self.load_labels()

    # ==================================
    # Close
    # ==================================

    def close(self):

        if self.on_close:

            self.on_close()