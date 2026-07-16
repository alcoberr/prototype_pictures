import json
from pathlib import Path


class ReviewSession:

    def __init__(self, image_folder):

        self.image_folder = Path(
            image_folder
        )

        self.labels_file = (
            self.image_folder /
            "labels.json"
        )

        self.labels = (
            self.load_labels()
        )

    # ==================================
    # File Operations
    # ==================================

    def load_labels(self):

        if not self.labels_file.exists():

            return {}

        try:

            with open(
                self.labels_file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return {}

    def save(self):

        with open(
            self.labels_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.labels,
                f,
                indent=4
            )

    # ==================================
    # Queries
    # ==================================

    def get_image_names(self):

        return sorted(
            self.labels.keys()
        )

    def get_labels(self):

        labels = set()

        for item in self.labels.values():

            labels.add(
                item["label"]
            )

        return sorted(
            labels
        )

    def get_images_for_label(
        self,
        label
    ):

        images = []

        for image_name, data in (
            self.labels.items()
        ):

            if data["label"] == label:

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

        return sorted(
            images,
            key=lambda x:
            x["sequence"]
        )

    def get_label_counts(self):

        result = {}

        for item in self.labels.values():

            label = item["label"]

            result.setdefault(
                label,
                0
            )

            result[label] += 1

        return dict(
            sorted(
                result.items()
            )
        )

    # ==================================
    # Image Operations
    # ==================================

    def assign_label(
        self,
        image_name,
        label
    ):

        if image_name not in self.labels:

            self.labels[
                image_name
            ] = {}

        self.labels[
            image_name
        ]["label"] = label

        if (
            "sequence"
            not in
            self.labels[
                image_name
            ]
        ):

            self.labels[
                image_name
            ]["sequence"] = 1

        self.save()

    def remove_image(
        self,
        image_name
    ):

        if image_name in self.labels:

            del self.labels[
                image_name
            ]

            self.save()

    # ==================================
    # Label Operations
    # ==================================

    def rename_label(
        self,
        old_label,
        new_label
    ):

        if (
            not old_label
            or
            not new_label
        ):

            return

        for item in (
            self.labels.values()
        ):

            if (
                item["label"]
                == old_label
            ):

                item["label"] = (
                    new_label
                )

        self.save()

    def merge_labels(
        self,
        source_label,
        target_label
    ):

        for item in (
            self.labels.values()
        ):

            if (
                item["label"]
                == source_label
            ):

                item["label"] = (
                    target_label
                )

        self.save()

    def delete_label(
        self,
        label
    ):

        remove_keys = []

        for image_name, data in (
            self.labels.items()
        ):

            if (
                data["label"]
                == label
            ):

                remove_keys.append(
                    image_name
                )

        for image_name in remove_keys:

            del self.labels[
                image_name
            ]

        self.save()

    # ==================================
    # Sequence Operations
    # ==================================

    def renumber_label(
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
                    image_name
                )

        images.sort()

        for index, image_name in (
            enumerate(
                images,
                start=1
            )
        ):

            self.labels[
                image_name
            ][
                "sequence"
            ] = index

        self.save()

    # ==================================
    # Summary
    # ==================================

    def summary(self):

        counts = (
            self.get_label_counts()
        )

        return {

            "total_images":
                len(
                    self.labels
                ),

            "labels":
                counts,

            "total_labels":
                len(
                    counts
                )
        }