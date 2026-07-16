import json
from pathlib import Path


class PagePlannerSession:

    IMAGES_PER_SECTION = 4

    def __init__(
        self,
        project_folder
    ):

        self.project_folder = Path(
            project_folder
        )

        self.labels_file = (
            self.project_folder /
            "labels.json"
        )

        self.order_file = (
            self.project_folder /
            "label_order.json"
        )

        self.page_plan_file = (
            self.project_folder /
            "page_plan.json"
        )

        self.labels = (
            self.load_labels()
        )

        self.figure_order = (
            self.load_figure_order()
        )

    # ==================================
    # Loading
    # ==================================

    def load_labels(self):

        if not self.labels_file.exists():
            return {}

        with open(
            self.labels_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def load_figure_order(self):

        if not self.order_file.exists():
            return []

        with open(
            self.order_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    # ==================================
    # Helpers
    # ==================================

    def get_images_for_label(
        self,
        label
    ):

        images = []

        for image_name, data in (
            self.labels.items()
        ):

            if (
                data["label"]
                == label
            ):

                images.append(
                    {
                        "file":
                            image_name,

                        "sequence":
                            data.get(
                                "sequence",
                                0
                            )
                    }
                )

        images.sort(
            key=lambda x:
            x["sequence"]
        )

        return images

    def build_sections(self):

        sections = []

        for item in self.figure_order:

            label = item["label"]

            figure_number = (
                item["figure_number"]
            )

            images = (
                self.get_images_for_label(
                    label
                )
            )

            image_files = [
                image["file"]
                for image in images
            ]

            chunks = []

            for index in range(
                0,
                len(image_files),
                self.IMAGES_PER_SECTION
            ):

                chunks.append(
                    image_files[
                        index:
                        index +
                        self.IMAGES_PER_SECTION
                    ]
                )

            for chunk_index, chunk in (
                enumerate(chunks)
            ):

                sections.append(
                    {
                        "figure_number":
                            figure_number,

                        "label":
                            label,

                        "continuation":
                            chunk_index > 0,

                        "images":
                            chunk
                    }
                )

        return sections

    # ==================================
    # Page Planning
    # ==================================

    def build_pages(self):

        sections = (
            self.build_sections()
        )

        pages = []

        page_number = 1

        index = 0

        while index < len(sections):

            remaining = (
                len(sections)
                - index
            )

            if remaining >= 2:

                page_sections = [
                    sections[index],
                    sections[index + 1]
                ]

                index += 2

            else:

                page_sections = [
                    sections[index]
                ]

                index += 1

            pages.append(
                {
                    "page":
                        page_number,

                    "sections":
                        page_sections
                }
            )

            page_number += 1

        return pages

    # ==================================
    # Save
    # ==================================

    def save(self):

        pages = (
            self.build_pages()
        )

        with open(
            self.page_plan_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                pages,
                f,
                indent=4
            )

        return pages

    # ==================================
    # Summary
    # ==================================

    def summary(self):

        pages = (
            self.build_pages()
        )

        sections = (
            self.build_sections()
        )

        return {
            "page_count":
                len(pages),

            "section_count":
                len(sections),

            "figure_count":
                len(
                    self.figure_order
                ),

            "pages":
                pages
        }