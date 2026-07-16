from pathlib import Path
import subprocess
import sys

ROOT_DIR = Path(
    __file__
).resolve().parent.parent


def run_gui_script(
    script_name,
    project_folder
):

    script_path = (
        ROOT_DIR /
        script_name
    )

    if not script_path.exists():

        raise FileNotFoundError(
            f"Script not found:\n{script_path}"
        )

    subprocess.Popen(
        [
            sys.executable,
            str(script_path),
            str(project_folder)
        ],
        cwd=str(ROOT_DIR)
    )


def run_batch_script(
    script_name,
    project_folder
):

    script_path = (
        ROOT_DIR /
        script_name
    )

    if not script_path.exists():

        raise FileNotFoundError(
            f"Script not found:\n{script_path}"
        )

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            str(project_folder)
        ],
        cwd=str(ROOT_DIR),
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(
            f"{script_name} failed."
        )


def run_labeler(project_folder):

    run_gui_script(
        "labeler.py",
        project_folder
    )


def run_review(project_folder):

    run_gui_script(
        "review_labels.py",
        project_folder
    )


def run_order(project_folder):

    run_batch_script(
        "label_order.py",
        project_folder
    )


def run_page_plan(project_folder):

    run_batch_script(
        "page_planner.py",
        project_folder
    )


def run_export(project_folder):

    run_batch_script(
        "export_excel_v4.py",
        project_folder
    )