import json
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QHBoxLayout,
)

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp"
}


class LabelerWindow(QWidget):

    def __init__(self, image_folder):
        super().__init__()

        self.image_folder = Path(image_folder)

        self.images = sorted([
            f for f in self.image_folder.iterdir()
            if f.is_file()
            and f.suffix.lower() in SUPPORTED_EXTENSIONS
        ])

        self.json_path = self.image_folder / "labels.json"
        self.report_path = self.image_folder / "report_structure.json"

        self.labels = self.load_labels()

        self.current_index = 0
        self.current_pixmap = None

        self.setWindowTitle("Transformer Photo Labeler")

        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_input = QLineEdit()
        self.label_input.setPlaceholderText(
            "Enter new label..."
        )

        self.existing_label_combo = QComboBox()

        self.prev_button = QPushButton(
            "Previous"
        )

        self.next_button = QPushButton(
            "Save New Label"
        )

        self.use_existing_button = QPushButton(
            "Use Existing Label"
        )

        self.refresh_existing_labels()

        layout = QVBoxLayout()

        layout.addWidget(self.progress_label)
        layout.addWidget(self.image_label, stretch=1)

        layout.addWidget(QLabel("New Label"))
        layout.addWidget(self.label_input)

        layout.addWidget(QLabel("Existing Labels"))
        layout.addWidget(self.existing_label_combo)

        buttons = QHBoxLayout()

        buttons.addWidget(self.prev_button)
        buttons.addWidget(self.use_existing_button)
        buttons.addWidget(self.next_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.prev_button.clicked.connect(
            self.previous_image
        )

        self.next_button.clicked.connect(
            self.save_new_label
        )

        self.use_existing_button.clicked.connect(
            self.save_existing_label
        )

        self.label_input.returnPressed.connect(
            self.save_new_label
        )

        QShortcut(
            QKeySequence(Qt.Key.Key_Left),
            self,
            activated=self.previous_image
        )

        QShortcut(
            QKeySequence(Qt.Key.Key_Right),
            self,
            activated=self.next_image
        )

        self.load_image()

    def load_labels(self):

        if self.json_path.exists():

            with open(self.json_path, "r") as f:
                return json.load(f)

        return {}

    def save_labels(self):

        with open(self.json_path, "w") as f:

            json.dump(
                self.labels,
                f,
                indent=4
            )

    def refresh_existing_labels(self):

        labels = sorted(
            {
                item["label"]
                for item in self.labels.values()
            }
        )

        self.existing_label_combo.clear()
        self.existing_label_combo.addItems(labels)

    def update_image_display(self):

        if not self.current_pixmap:
            return

        scaled = self.current_pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(scaled)

    def resizeEvent(self, event):

        self.update_image_display()

        super().resizeEvent(event)

    def load_image(self):

        image_path = self.images[self.current_index]

        self.progress_label.setText(
            f"Image {self.current_index + 1} / {len(self.images)}"
        )

        self.current_pixmap = QPixmap(
            str(image_path)
        )

        self.update_image_display()

        image_name = image_path.name

        if image_name in self.labels:

            self.label_input.setText(
                self.labels[image_name]["label"]
            )

        else:
            self.label_input.clear()

        self.label_input.setFocus()

    def next_image(self):

        if self.current_index < len(self.images) - 1:

            self.current_index += 1
            self.load_image()

    def previous_image(self):

        if self.current_index > 0:

            self.current_index -= 1
            self.load_image()

    def calculate_sequence(self, label):

        sequences = []

        for item in self.labels.values():

            if item["label"] == label:

                sequences.append(
                    item.get("sequence", 0)
                )

        if not sequences:
            return 1

        return max(sequences) + 1

    def save_label(self, label):

        sequence = self.calculate_sequence(label)

        image_name = self.images[
            self.current_index
        ].name

        self.labels[image_name] = {
            "label": label,
            "sequence": sequence
        }

        self.save_labels()

        self.refresh_existing_labels()

        print(
            f"Saved: {image_name} -> {label}_{sequence}"
        )

        if self.current_index < len(self.images) - 1:

            self.current_index += 1
            self.load_image()
        else:
            self.finish()

    def save_new_label(self):

        label = self.label_input.text().strip().title()

        if not label:
            return

        self.save_label(label)

    def save_existing_label(self):

        label = self.existing_label_combo.currentText()

        if not label:
            return

        self.save_label(label)

    def generate_report_structure(self):

        sections = {}

        for image_name, data in self.labels.items():

            label = data["label"]

            sections.setdefault(
                label,
                []
            )

            sections[label].append(
                {
                    "file": image_name,
                    "sequence": data["sequence"]
                }
            )

        with open(
            self.report_path,
            "w"
        ) as f:

            json.dump(
                sections,
                f,
                indent=4
            )

        return sections

    def finish(self):

        sections = self.generate_report_structure()

        print("\n")
        print("=" * 40)
        print("LABELING COMPLETE")
        print("=" * 40)

        for section in sorted(sections):

            count = len(
                sections[section]
            )

            print(
                f"{section}: {count} image(s)"
            )

        print("\nlabels.json")
        print(self.json_path)

        print("\nreport_structure.json")
        print(self.report_path)

        print("=" * 40)

        self.close()


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            r"Usage: python src\labeler.py images"
        )
        sys.exit()

    app = QApplication(sys.argv)

    window = LabelerWindow(sys.argv[1])

    window.showMaximized()

    sys.exit(app.exec())