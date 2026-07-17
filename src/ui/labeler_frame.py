from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

from core.labeling_session import (
    LabelingSession
)


class LabelerFrame(ttk.Frame):

    def __init__(
        self,
        parent,
        project_folder,
        on_close=None
    ):

        super().__init__(parent)

        self.parent = parent

        self.project_folder = Path(
            project_folder
        )

        self.on_close = on_close

        self.session = LabelingSession(
            self.project_folder
        )

        self.current_photo = None

        self.build_ui()

        self.load_current_image()

    # ==================================
    # UI
    # ==================================
    def on_enter(
        self,
        event=None
    ):
        self.save_label()

    def build_ui(self):

        self.columnconfigure(
            0,
            weight=1
        )

        self.rowconfigure(
            1,
            weight=1
        )

        header = ttk.Frame(self)

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        self.progress_label = ttk.Label(
            header,
            text=""
        )

        self.progress_label.pack(
            side="left"
        )

        ttk.Button(
            header,
            text="Back",
            command=self.close
        ).pack(
            side="right"
        )

        self.image_label = ttk.Label(
            self
        )

        self.image_label.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        bottom = ttk.Frame(self)

        bottom.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Label(
            bottom,
            text="Label:"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.label_var = tk.StringVar()

        self.label_entry = ttk.Entry(
            bottom,
            textvariable=self.label_var,
            width=40
        )

        self.label_entry.bind(
            "<Return>",
            self.on_enter
        )

        self.label_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Button(
            bottom,
            text="Save Label",
            command=self.save_label
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        ttk.Label(
            bottom,
            text="Existing Labels:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(10, 0)
        )

        self.label_combo = ttk.Combobox(
            bottom,
            width=35
        )

        self.label_combo.grid(
            row=1,
            column=1,
            padx=5,
            pady=(10, 0)
        )

        ttk.Button(
            bottom,
            text="Use Existing",
            command=self.use_existing
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=(10, 0)
        )

        nav = ttk.Frame(bottom)

        nav.grid(
            row=2,
            column=0,
            columnspan=3,
            pady=15
        )

        ttk.Button(
            nav,
            text="Previous",
            command=self.previous_image
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            nav,
            text="Next",
            command=self.next_image
        ).pack(
            side="left",
            padx=5
        )

    # ==================================
    # Image Loading
    # ==================================

    def load_current_image(self):

        image_path = (
            self.session.current_image()
        )

        if image_path is None:

            self.progress_label.config(
                text="No Images"
            )

            return

        self.progress_label.config(
            text=self.session.progress_text()
        )

        try:

            image = Image.open(
                image_path
            )

            image.thumbnail(
                (
                    1200,
                    900
                )
            )

            self.current_photo = (
                ImageTk.PhotoImage(
                    image
                )
            )

            self.image_label.config(
                image=self.current_photo
            )

        except Exception as ex:

            self.image_label.config(
                text=str(ex)
            )

        current_label = (
            self.session.current_label()
        )

        self.label_var.set(
            current_label
        )

        self.refresh_existing_labels()

        self.label_entry.focus_set()

        self.label_entry.selection_range(
            0,
            tk.END
        )

    # ==================================
    # Labels
    # ==================================

    def refresh_existing_labels(self):

        self.label_combo["values"] = (
            self.session.get_existing_labels()
        )

    def save_label(self):

        label = (
            self.label_var.get()
            .strip()
            .title()
        )

        if not label:

            return

        self.session.save_label(
            label
        )

        self.refresh_existing_labels()

        if (
            self.session.current_index
            <
            self.session.image_count() - 1
        ):

            self.session.next_image()

            self.load_current_image()

        else:

            self.finish()

    def use_existing(self):

        label = (
            self.label_combo.get()
            .strip()
        )

        if not label:

            return

        self.label_var.set(
            label
        )

        self.save_label()

    # ==================================
    # Navigation
    # ==================================

    def previous_image(self):

        self.session.previous_image()

        self.load_current_image()

    def next_image(self):

        self.session.next_image()

        self.load_current_image()

    # ==================================
    # Finish
    # ==================================

    def finish(self):

        self.session.generate_report_structure()

        messagebox.showinfo(
            "Complete",
            "Labeling completed."
        )

        self.close()

    def close(self):

        if self.on_close:

            self.on_close()