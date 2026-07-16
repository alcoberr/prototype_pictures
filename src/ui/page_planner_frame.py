import json
import tkinter as tk
from tkinter import ttk, messagebox

from core.page_planner_session import (
    PagePlannerSession
)


class PagePlannerFrame(ttk.Frame):

    def __init__(
        self,
        parent,
        project_folder,
        on_close=None
    ):

        super().__init__(parent)

        self.parent = parent

        self.session = (
            PagePlannerSession(
                project_folder
            )
        )

        self.on_close = on_close

        self.pages = (
            self.session.build_pages()
        )

        self.build_ui()

        self.load_pages()

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

        # ----------------------
        # Header
        # ----------------------

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
            text="Page Planner",
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

        # ----------------------
        # Pages
        # ----------------------

        page_frame = ttk.LabelFrame(
            self,
            text="Pages"
        )

        page_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.page_list = tk.Listbox(
            page_frame
        )

        self.page_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.page_list.bind(
            "<<ListboxSelect>>",
            self.on_page_selected
        )

        # ----------------------
        # Details
        # ----------------------

        detail_frame = ttk.LabelFrame(
            self,
            text="Page Details"
        )

        detail_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.detail_text = tk.Text(
            detail_frame,
            wrap="word"
        )

        self.detail_text.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ----------------------
        # Summary
        # ----------------------

        summary_frame = ttk.LabelFrame(
            self,
            text="Summary"
        )

        summary_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=5
        )

        self.summary_label = ttk.Label(
            summary_frame,
            text=""
        )

        self.summary_label.pack(
            anchor="w",
            padx=10,
            pady=10
        )

        # ----------------------
        # Buttons
        # ----------------------

        button_frame = ttk.Frame(
            self
        )

        button_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Button(
            button_frame,
            text="Regenerate Preview",
            command=self.regenerate
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Save Page Plan",
            command=self.save_plan
        ).pack(
            side="right",
            padx=5
        )

    # ==================================
    # Data Loading
    # ==================================

    def load_pages(self):

        self.page_list.delete(
            0,
            tk.END
        )

        self.pages = (
            self.session.build_pages()
        )

        for page in self.pages:

            section_count = len(
                page["sections"]
            )

            self.page_list.insert(
                tk.END,
                f"Page {page['page']} "
                f"({section_count} section(s))"
            )

        summary = (
            self.session.summary()
        )

        self.summary_label.config(
            text=(
                f"Figures: "
                f"{summary['figure_count']}    "
                f"Sections: "
                f"{summary['section_count']}    "
                f"Pages: "
                f"{summary['page_count']}"
            )
        )

    # ==================================
    # Detail Viewer
    # ==================================

    def on_page_selected(
        self,
        event=None
    ):

        selection = (
            self.page_list.curselection()
        )

        if not selection:
            return

        page = self.pages[
            selection[0]
        ]

        self.detail_text.delete(
            "1.0",
            tk.END
        )

        lines = []

        lines.append(
            f"PAGE {page['page']}"
        )

        lines.append("")
        lines.append(
            "=" * 40
        )
        lines.append("")

        for section in (
            page["sections"]
        ):

            title = (
                f"Figure "
                f"{section['figure_number']:02d}"
                f" - "
                f"{section['label']}"
            )

            if section.get(
                "continuation",
                False
            ):
                title += " (CONT.)"

            lines.append(title)
            lines.append("")

            for image in (
                section["images"]
            ):

                lines.append(
                    f"    {image}"
                )

            lines.append("")
            lines.append(
                "-" * 30
            )
            lines.append("")

        self.detail_text.insert(
            "1.0",
            "\n".join(lines)
        )

    # ==================================
    # Actions
    # ==================================

    def regenerate(self):

        self.pages = (
            self.session.build_pages()
        )

        self.load_pages()

        messagebox.showinfo(
            "Updated",
            "Page preview regenerated."
        )

    def save_plan(self):

        pages = (
            self.session.save()
        )

        messagebox.showinfo(
            "Saved",
            (
                f"Saved "
                f"{len(pages)} page(s)"
            )
        )

    # ==================================
    # Close
    # ==================================

    def close(self):

        if self.on_close:

            self.on_close()