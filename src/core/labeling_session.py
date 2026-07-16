import json
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp"
}


class LabelingSession:

    def __init__(self, image_folder):

        self.image_folder = Path(
            image_folder
        )

        self.images = sorted(
            [
                f
                for f in self.image_folder.iterdir()
                if (
                    f.is_file()
                    and
                    f.suffix.lower()
                    in SUPPORTED_EXTENSIONS
                )
            ]
        )

        self.labels_path = (
            self.image_folder /
            "labels.json"
        )

        self.report_path = (
            self.image_folder /
            "report_structure.json"
        )

        self.labels = (
            self.load_labels()
        )

        self.current_index = 0

    # ===================================
    # Files
    # ===================================

    def load_labels(self):

        if not self.labels_path.exists():

            return {}

        try:

            with open(
                self.labels_path,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return {}

    def save_labels(self):

        with open(
            self.labels_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.labels,
                f,
                indent=4
            )

    # ===================================
    # Navigation
    # ===================================

    def current_image(self):

        if not self.images:

            return None

        return self.images[
            self.current_index
        ]

    def current_image_name(self):

        image = self.current_image()

        if image is None:

            return None

        return image.name

    def current_label(self):

        image_name = (
            self.current_image_name()
        )

        if image_name is None:

            return ""

        if image_name not in self.labels:

            return ""

        return self.labels[
            image_name
        ]["label"]

    def next_image(self):

        if (
            self.current_index
            < len(self.images) - 1
        ):

            self.current_index += 1

        return self.current_image()

    def previous_image(self):

        if self.current_index > 0:

            self.current_index -= 1

        return self.current_image()

    def goto_image(
        self,
        index
    ):

        if not self.images:

            return None

        index = max(
            0,
            min(
                index,
                len(self.images) - 1
            )
        )

        self.current_index = index

        return self.current_image()

    # ===================================
    # Labels
    # ===================================

    def get_existing_labels(self):

        labels = set()

        for item in self.labels.values():

            labels.add(
                item["label"]
            )

        return sorted(labels)

    def calculate_sequence(
        self,
        label
    ):

        sequences = []

        for item in self.labels.values():

            if item["label"] == label:

                sequences.append(
                    item.get(
                        "sequence",
                        0
                    )
                )

        if not sequences:

            return 1

        return (
            max(sequences)
            + 1
        )

    def save_label(
        self,
        label
    ):

        label = label.strip()

        if not label:

            return

        image_name = (
            self.current_image_name()
        )

        if image_name is None:

            return

        sequence = (
            self.calculate_sequence(
                label
            )
        )

        self.labels[
            image_name
        ] = {
            "label": label,
            "sequence": sequence
        }

        self.save_labels()

    # ===================================
    # Status
    # ===================================

    def image_count(self):

        return len(
            self.images
        )

    def labeled_count(self):

        return len(
            self.labels
        )

    def unlabeled_count(self):

        return (
            self.image_count()
            - self.labeled_count()
        )

    def progress_text(self):

        if not self.images:

            return "No Images"

        return (
            f"Image "
            f"{self.current_index + 1}"
            f" / "
            f"{len(self.images)}"
        )

    def is_complete(self):

        return (
            self.image_count()
            > 0
            and
            self.unlabeled_count()
            == 0
        )

    # ===================================
    # Report Structure
    # ===================================

    def generate_report_structure(self):

        sections = {}

        for image_name, data in (
            self.labels.items()
        ):

            label = (
                data["label"]
            )

            sections.setdefault(
                label,
                []
            )

            sections[
                label
            ].append(
                {
                    "file":
                        image_name,

                    "sequence":
                        data[
                            "sequence"
                        ]
                }
            )

        for label in sections:

            sections[label] = sorted(
                sections[label],
                key=lambda x:
                x["sequence"]
            )

        with open(
            self.report_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                sections,
                f,
                indent=4
            )

        return sections

    # ===================================
    # Summary
    # ===================================

    def summary(self):

        return {
            "folder":
                str(
                    self.image_folder
                ),

            "total_images":
                self.image_count(),

            "labeled_images":
                self.labeled_count(),

            "unlabeled_images":
                self.unlabeled_count(),

            "existing_labels":
                self.get_existing_labels(),

            "complete":
                self.is_complete(),
        }