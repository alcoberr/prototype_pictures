import tkinter as tk
from tkinter import ttk, messagebox

from core.label_order_session import (
    LabelOrderSession
)


class LabelOrderFrame(ttk.Frame):

    def __init__(
        self,
        parent,
        project_folder,
        on_close=None
    ):

        super().__init__(parent)

        self.parent = parent

        self.session = (
            LabelOrderSession(
                project_folder
            )
        )

        self.on_close = on_close

        self.build_ui()

        self.load_figures()

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
            weight=2
        )

        self.rowconfigure(
            1,
            weight=1
        )

        # --------------------------
        # Header
        # --------------------------

        header = ttk.Frame(self)

        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Label(
            header,
            text="Figure Order",
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

        # --------------------------
        # Figures
        # --------------------------

        figure_frame = ttk.LabelFrame(
            self,
            text="Figures"
        )

        figure_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.figure_list = tk.Listbox(
            figure_frame
        )

        self.figure_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.figure_list.bind(
            "<<ListboxSelect>>",
            self.on_figure_selected
        )

        # --------------------------
        # Images
        # --------------------------

        image_frame = ttk.LabelFrame(
            self,
            text="Images in Figure"
        )

        image_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.image_list = tk.Listbox(
            image_frame
        )

        self.image_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # --------------------------
        # Actions
        # --------------------------

        actions = ttk.LabelFrame(
            self,
            text="Actions"
        )

        actions.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Button(
            actions,
            text="Move Up",
            command=self.move_up
        ).pack(
            side="left",
            padx=10,
            pady=10
        )

        ttk.Button(
            actions,
            text="Move Down",
            command=self.move_down
        ).pack(
            side="left",
            padx=10,
            pady=10
        )

        ttk.Button(
            actions,
            text="Save Order",
            command=self.save_order
        ).pack(
            side="right",
            padx=10,
            pady=10
        )

    # ==================================
    # Helpers
    # ==================================

    def selected_index(self):

        selection = (
            self.figure_list.curselection()
        )

        if not selection:

            return None

        return selection[0]

    def selected_figure(self):

        index = self.selected_index()

        if index is None:

            return None

        figures = (
            self.session.get_order()
        )

        return figures[index]

    # ==================================
    # Loading
    # ==================================

    def load_figures(self):

        self.figure_list.delete(
            0,
            tk.END
        )

        figures = (
            self.session.get_order()
        )

        for item in figures:

            text = (
                f"{item['figure_number']:02d}"
                f" - "
                f"{item['label']}"
            )

            self.figure_list.insert(
                tk.END,
                text
            )

    def on_figure_selected(
        self,
        event=None
    ):

        figure = (
            self.selected_figure()
        )

        if figure is None:

            return

        self.image_list.delete(
            0,
            tk.END
        )

        images = (
            self.session
            .get_label_images(
                figure["label"]
            )
        )

        for image in images:

            self.image_list.insert(
                tk.END,
                image["file"]
            )

    # ==================================
    # Actions
    # ==================================

    def move_up(self):

        index = (
            self.selected_index()
        )

        if index is None:

            return

        self.session.move_up(
            index
        )

        self.load_figures()

        new_index = max(
            0,
            index - 1
        )

        self.figure_list.selection_set(
            new_index
        )

        self.on_figure_selected()

    def move_down(self):

        index = (
            self.selected_index()
        )

        if index is None:

            return

        self.session.move_down(
            index
        )

        self.load_figures()

        new_index = min(
            self.figure_list.size() - 1,
            index + 1
        )

        self.figure_list.selection_set(
            new_index
        )

        self.on_figure_selected()

    def save_order(self):

        self.session.save()

        messagebox.showinfo(
            "Saved",
            "Figure order saved."
        )

    # ==================================
    # Close
    # ==================================

    def close(self):

        if self.on_close:

            self.on_close()