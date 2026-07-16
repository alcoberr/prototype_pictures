import json
from pathlib import Path


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp"
}


def get_image_files(project_folder):

    project_folder = Path(project_folder)

    images = []

    for file in project_folder.iterdir():

        if (
            file.is_file()
            and file.suffix.lower() in IMAGE_EXTENSIONS
        ):
            images.append(
                file.name
            )

    return sorted(images)


def load_json(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return None


def get_labels(project_folder):

    project_folder = Path(project_folder)

    labels_file = (
        project_folder /
        "labels.json"
    )

    if not labels_file.exists():
        return {}

    data = load_json(
        labels_file
    )

    if isinstance(data, dict):
        return data

    return {}


def get_label_order(project_folder):

    project_folder = Path(project_folder)

    order_file = (
        project_folder /
        "label_order.json"
    )

    if not order_file.exists():
        return None

    return load_json(
        order_file
    )


def get_page_plan(project_folder):

    project_folder = Path(project_folder)

    page_plan_file = (
        project_folder /
        "page_plan.json"
    )

    if not page_plan_file.exists():
        return None

    return load_json(
        page_plan_file
    )


def validate_project(project_folder):

    project_folder = Path(
        project_folder
    )

    image_files = set(
        get_image_files(
            project_folder
        )
    )

    labels = get_labels(
        project_folder
    )

    labeled_files = set(
        labels.keys()
    )

    unlabeled = sorted(
        image_files -
        labeled_files
    )

    orphaned = sorted(
        labeled_files -
        image_files
    )

    labels_exists = (
        project_folder /
        "labels.json"
    ).exists()

    order_exists = (
        project_folder /
        "label_order.json"
    ).exists()

    page_plan_exists = (
        project_folder /
        "page_plan.json"
    ).exists()

    report_exists = (
        project_folder /
        "Prototype_Report.xlsx"
    ).exists()

    ready_to_export = (
        labels_exists
        and order_exists
        and page_plan_exists
        and len(unlabeled) == 0
        and len(orphaned) == 0
    )

    if orphaned:

        status = "ERROR"

        message = (
            f"{len(orphaned)} "
            f"orphaned label(s) found"
        )

    elif unlabeled:

        status = "WARNING"

        message = (
            f"{len(unlabeled)} "
            f"unlabeled image(s)"
        )

    elif ready_to_export:

        status = "READY"

        message = (
            "Ready to export"
        )

    else:

        status = "INCOMPLETE"

        message = (
            "Project incomplete"
        )

    result = {

        "project_folder":
            str(project_folder),

        "files": {

            "labels_exists":
                labels_exists,

            "label_order_exists":
                order_exists,

            "page_plan_exists":
                page_plan_exists,

            "report_exists":
                report_exists,
        },

        "images": {

            "total":
                len(image_files),

            "labeled":
                len(image_files)
                - len(unlabeled),

            "unlabeled":
                len(unlabeled),

            "orphaned":
                len(orphaned),
        },

        "unlabeled_files":
            unlabeled,

        "orphaned_files":
            orphaned,

        "labels":
            labels,

        "ready_to_export":
            ready_to_export,

        "status":
            status,

        "message":
            message,
    }

    return result


if __name__ == "__main__":

    folder = input(
        "Project Folder: "
    )

    result = validate_project(
        folder
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )