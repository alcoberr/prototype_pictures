import json
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QListWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QMessageBox,
)


class LabelOrderWindow(QWidget):

    def __init__(self, image_folder):
        super().__init__()

        self.image_folder = Path(image_folder)

        self.labels_file = (
            self.image_folder / "labels.json"
        )

        self.order_file = (
            self.image_folder / "label_order.json"
        )

        with open(self.labels_file, "r") as f:
            self.labels = json.load(f)

        self.setWindowTitle(
            "Report Builder"
        )

        self.resize(600, 700)

        self.instructions = QLabel(
            "Drag labels to set the report order."
        )

        self.label_list = QListWidget()

        self.label_list.setDragEnabled(True)
        self.label_list.setAcceptDrops(True)
        self.label_list.setDragDropMode(
            QListWidget.DragDropMode.InternalMove
        )
        self.label_list.setDefaultDropAction(
            Qt.DropAction.MoveAction
        )

        self.save_button = QPushButton(
            "Save Order"
        )

        layout = QVBoxLayout()

        layout.addWidget(self.instructions)
        layout.addWidget(self.label_list)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.save_button.clicked.connect(
            self.save_order
        )

        self.load_labels()

    def load_labels(self):

        unique_labels = sorted(
            {
                value["label"]
                for value in self.labels.values()
            }
        )

        if self.order_file.exists():

            with open(
                self.order_file,
                "r"
            ) as f:

                saved = json.load(f)

            ordered_labels = saved.get(
                "label_order",
                []
            )

            remaining_labels = [
                label
                for label in unique_labels
                if label not in ordered_labels
            ]

            unique_labels = (
                ordered_labels + remaining_labels
            )

        self.label_list.clear()

        for label in unique_labels:

            self.label_list.addItem(label)

    def save_order(self):

        labels = []

        for i in range(
            self.label_list.count()
        ):

            labels.append(
                self.label_list.item(i).text()
            )

        with open(
            self.order_file,
            "w"
        ) as f:

            json.dump(
                {
                    "label_order": labels
                },
                f,
                indent=4
            )

        QMessageBox.information(
            self,
            "Saved",
            "Report order saved successfully."
        )


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            r"Usage: python src\label_order.py images"
        )

        sys.exit()

    app = QApplication(sys.argv)

    window = LabelOrderWindow(
        sys.argv[1]
    )

    window.show()

    sys.exit(app.exec())