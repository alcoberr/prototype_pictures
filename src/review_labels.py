import json
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QListWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QInputDialog,
    QMessageBox,
    QComboBox,
)


class ReviewLabelsWindow(QWidget):

    def __init__(self, image_folder):
        super().__init__()

        self.image_folder = Path(image_folder)
        self.json_file = self.image_folder / "labels.json"

        with open(self.json_file, "r") as f:
            self.labels = json.load(f)

        self.setWindowTitle("Review Labels")
        self.resize(1400, 900)

        self.label_list = QListWidget()
        self.file_list = QListWidget()

        self.image_preview = QLabel()
        self.image_preview.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.rename_button = QPushButton(
            "Rename Label"
        )

        self.save_button = QPushButton(
            "Save Changes"
        )

        self.move_combo = QComboBox()

        self.move_button = QPushButton(
            "Move Selected Image"
        )

        self.build_layout()

        self.label_list.itemSelectionChanged.connect(
            self.load_files_for_label
        )

        self.file_list.itemSelectionChanged.connect(
            self.show_image_preview
        )

        self.rename_button.clicked.connect(
            self.rename_label
        )

        self.move_button.clicked.connect(
            self.move_selected_image
        )

        self.save_button.clicked.connect(
            self.save_changes
        )

        self.refresh_labels()

    def build_layout(self):

        left_layout = QVBoxLayout()

        left_layout.addWidget(
            QLabel("Labels")
        )
        left_layout.addWidget(
            self.label_list
        )

        middle_layout = QVBoxLayout()

        middle_layout.addWidget(
            QLabel("Files")
        )
        middle_layout.addWidget(
            self.file_list
        )

        right_layout = QVBoxLayout()

        right_layout.addWidget(
            QLabel("Preview")
        )
        right_layout.addWidget(
            self.image_preview
        )

        right_layout.addWidget(
            QLabel("Move To Label")
        )
        right_layout.addWidget(
            self.move_combo
        )
        right_layout.addWidget(
            self.move_button
        )

        right_layout.addWidget(
            self.rename_button
        )

        right_layout.addWidget(
            self.save_button
        )

        main_layout = QHBoxLayout()

        main_layout.addLayout(
            left_layout,
            1
        )

        main_layout.addLayout(
            middle_layout,
            1
        )

        main_layout.addLayout(
            right_layout,
            2
        )

        self.setLayout(main_layout)

    def get_label_counts(self):

        counts = {}

        for item in self.labels.values():

            label = item["label"]

            counts[label] = (
                counts.get(label, 0) + 1
            )

        return counts

    def refresh_labels(self):

        self.label_list.clear()

        counts = self.get_label_counts()

        for label, count in sorted(
            counts.items()
        ):
            self.label_list.addItem(
                f"{label} ({count})"
            )

        self.move_combo.clear()

        for label in sorted(counts.keys()):
            self.move_combo.addItem(label)

    def load_files_for_label(self):

        self.file_list.clear()

        item = self.label_list.currentItem()

        if not item:
            return

        label = item.text().split(" (")[0]

        for filename, data in self.labels.items():

            if data["label"] == label:

                self.file_list.addItem(
                    filename
                )

    def show_image_preview(self):

        item = self.file_list.currentItem()

        if not item:
            return

        image_name = item.text()

        image_path = (
            self.image_folder / image_name
        )

        if not image_path.exists():
            return

        pixmap = QPixmap(str(image_path))

        self.image_preview.setPixmap(
            pixmap.scaled(
                800,
                600,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    def rename_label(self):

        item = self.label_list.currentItem()

        if not item:
            return

        old_label = item.text().split(" (")[0]

        new_label, ok = QInputDialog.getText(
            self,
            "Rename Label",
            f"Rename '{old_label}' to:"
        )

        if not ok or not new_label:
            return

        new_label = (
            new_label.strip().title()
        )

        for value in self.labels.values():

            if value["label"] == old_label:

                value["label"] = new_label

        self.refresh_labels()

    def move_selected_image(self):

        file_item = self.file_list.currentItem()

        if not file_item:
            return

        filename = file_item.text()

        target_label = (
            self.move_combo.currentText()
        )

        self.labels[filename]["label"] = target_label

        self.load_files_for_label()

        self.refresh_labels()

    def save_changes(self):

        with open(self.json_file, "w") as f:

            json.dump(
                self.labels,
                f,
                indent=4
            )

        QMessageBox.information(
            self,
            "Saved",
            "Changes saved successfully."
        )


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            r"Usage: python src\review_labels.py images"
        )

        sys.exit()

    app = QApplication(sys.argv)

    window = ReviewLabelsWindow(
        sys.argv[1]
    )

    window.showMaximized()

    sys.exit(app.exec())