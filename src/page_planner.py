import json
from pathlib import Path

IMAGE_FOLDER = "images"


def load_labels(folder):

    with open(
        Path(folder) / "labels.json",
        "r"
    ) as f:
        return json.load(f)


def load_order(folder):

    with open(
        Path(folder) / "label_order.json",
        "r"
    ) as f:
        data = json.load(f)

    return data["label_order"]


def group_images(labels):

    grouped = {}

    for filename, data in labels.items():

        label = data["label"]

        if label not in grouped:
            grouped[label] = []

        grouped[label].append(
            filename
        )

    for files in grouped.values():
        files.sort()

    return grouped


def build_figures(order, grouped):

    figures = []

    figure_number = 1

    for label in order:

        images = grouped.get(
            label,
            []
        )

        if not images:
            continue

        figures.append(
            {
                "figure_number":
                figure_number,

                "label":
                label,

                "images":
                images
            }
        )

        figure_number += 1

    return figures


def build_pages(figures):

    pages = []

    page_number = 1

    current_page = []

    remaining_slots = 4

    for figure in figures:

        images = figure["images"]

        index = 0

        continuation = False

        while index < len(images):

            if remaining_slots == 0:

                pages.append(
                    {
                        "page":
                        page_number,

                        "sections":
                        current_page
                    }
                )

                page_number += 1

                current_page = []

                remaining_slots = 4

            images_to_take = min(
                remaining_slots,
                len(images) - index
            )

            section_images = (
                images[
                    index:index + images_to_take
                ]
            )

            section = {
                "figure_number":
                figure["figure_number"],

                "label":
                figure["label"],

                "continuation":
                continuation,

                "images":
                section_images,

                "image_count":
                len(section_images)
            }

            current_page.append(
                section
            )

            index += images_to_take

            remaining_slots -= images_to_take

            continuation = True

    if current_page:

        pages.append(
            {
                "page":
                page_number,

                "sections":
                current_page
            }
        )

    return pages


def save_plan(folder, pages):

    output_file = (
        Path(folder)
        / "page_plan.json"
    )

    with open(
        output_file,
        "w"
    ) as f:

        json.dump(
            pages,
            f,
            indent=4
        )

    return output_file


def print_plan(pages):

    print()
    print("=" * 60)
    print("PAGE PLAN")
    print("=" * 60)

    for page in pages:

        print()
        print(
            f"Page {page['page']}"
        )

        for section in page["sections"]:

            title = (
                f"  FIGURE "
                f"{section['figure_number']:02d}: "
                f"{section['label']}"
            )

            if section["continuation"]:
                title += " (CONT.)"

            print(title)

            print(
                f"      Images: "
                f"{section['image_count']}"
            )

            for image in section["images"]:

                print(
                    f"          {image}"
                )


def main():

    labels = load_labels(
        IMAGE_FOLDER
    )

    order = load_order(
        IMAGE_FOLDER
    )

    grouped = group_images(
        labels
    )

    figures = build_figures(
        order,
        grouped
    )

    pages = build_pages(
        figures
    )

    output = save_plan(
        IMAGE_FOLDER,
        pages
    )

    print_plan(
        pages
    )

    print()
    print(
        f"Saved: {output}"
    )
    print()


if __name__ == "__main__":
    main()