import json
from pathlib import Path


class LabelOrderSession:

    def __init__(self, project_folder):

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

        self.labels = (
            self.load_labels()
        )

        self.order = (
            self.load_order()
        )

        if not self.order:

            self.build_default_order()

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

    def load_order(self):

        if not self.order_file.exists():

            return []

        try:

            with open(
                self.order_file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return []

    def save(self):

        with open(
            self.order_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.order,
                f,
                indent=4
            )

    # ==================================
    # Build Default Order
    # ==================================

    def build_default_order(self):

        labels = set()

        for item in self.labels.values():

            labels.add(
                item["label"]
            )

        self.order = []

        for index, label in enumerate(
            sorted(labels),
            start=1
        ):

            self.order.append(
                {
                    "figure_number":
                        index,

                    "label":
                        label
                }
            )

        self.save()

    # ==================================
    # Queries
    # ==================================

    def get_order(self):

        return self.order

    def get_labels(self):

        return [
            item["label"]
            for item in self.order
        ]

    def get_figure_count(self):

        return len(
            self.order
        )

    def get_label_images(
        self,
        label
    ):

        result = []

        for image_name, data in (
            self.labels.items()
        ):

            if (
                data["label"]
                == label
            ):

                result.append(
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

        return sorted(
            result,
            key=lambda x:
            x["sequence"]
        )

    # ==================================
    # Ordering
    # ==================================

    def move_up(
        self,
        index
    ):

        if index <= 0:

            return

        self.order[index - 1], self.order[index] = (
            self.order[index],
            self.order[index - 1]
        )

        self.renumber()

    def move_down(
        self,
        index
    ):

        if index >= (
            len(self.order) - 1
        ):

            return

        self.order[index + 1], self.order[index] = (
            self.order[index],
            self.order[index + 1]
        )

        self.renumber()

    def renumber(self):

        for index, item in enumerate(
            self.order,
            start=1
        ):

            item[
                "figure_number"
            ] = index

        self.save()

    # ==================================
    # Label Operations
    # ==================================

    def add_label(
        self,
        label
    ):

        if label in self.get_labels():

            return

        self.order.append(
            {
                "figure_number":
                    len(self.order) + 1,

                "label":
                    label
            }
        )

        self.save()

    def remove_label(
        self,
        label
    ):

        self.order = [

            item

            for item in self.order

            if item["label"] != label

        ]

        self.renumber()

    def rename_label(
        self,
        old_label,
        new_label
    ):

        for item in self.order:

            if (
                item["label"]
                == old_label
            ):

                item["label"] = (
                    new_label
                )

        self.save()

    # ==================================
    # Summary
    # ==================================

    def summary(self):

        return {

            "figure_count":
                len(
                    self.order
                ),

            "labels":
                self.get_labels(),

            "order":
                self.order
        }