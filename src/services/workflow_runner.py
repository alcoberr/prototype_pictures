from pathlib import Path
import subprocess
import sys


ROOT_DIR = Path(
    __file__
).resolve().parent.parent


def run_python_script(script_name):

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
            str(script_path)
        ],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(
            result.stderr
        )

    return result.stdout


def run_labeler():

    return run_python_script(
        "labeler.py"
    )


def run_review():

    return run_python_script(
        "review_labels.py"
    )


def run_order():

    return run_python_script(
        "label_order.py"
    )


def run_page_plan():

    return run_python_script(
        "page_planner.py"
    )


def run_export():

    return run_python_script(
        "export_excel_v4.py"
    )


def run_full_pipeline():

    logs = []

    logs.append(
        run_labeler()
    )

    logs.append(
        run_review()
    )

    logs.append(
        run_order()
    )

    logs.append(
        run_page_plan()
    )

    logs.append(
        run_export()
    )

    return "\n".join(logs)