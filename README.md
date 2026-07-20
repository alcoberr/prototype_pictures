# Picture Report Generator

## Overview

Picture Report Generator is a Python/Tkinter desktop application used to generate engineering photo reports from a folder of images.

The workflow allows a user to:

1. Select a source folder of pictures.
2. Label photos.
3. Review and edit labels.
4. Order figures.
5. Plan report pages.
6. Generate an Excel report using a template.

The application was designed to work efficiently on large network folders by copying project files into a local workspace before processing.

---

# Project Structure

```text
prototype_pictures/
│
├── src/
│   ├── main_gui.py
│   ├── jayjay.py
│   ├── core/
│   ├── ui/
│   ├── docs/
│   │   └── Template.xlsx
│   └── ralph.png
│
├── tests/
├── sample_images/
├── requirements.txt
├── myenv/
└── PictureReportGenerator.spec
```

---

# Environment Setup

## Create Virtual Environment

```bash
python -m venv myenv
```

Activate:

Windows CMD:

```cmd
myenv\Scripts\activate
```

PowerShell:

```powershell
.\myenv\Scripts\Activate.ps1
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

If rebuilding from scratch:

```bash
pip install pillow
pip install openpyxl
pip install pyinstaller
```

---

# Running the Application

From project root:

```bash
python src/main_gui.py
```

---

# How the Application Works

## Folder Selection

User clicks:

```text
Browse Folder
```

The application:

1. Copies images to:

```text
C:\Users\<user>\PictureReportWorkspace
```

2. Copies project JSON files if they already exist:

```text
labels.json
report_structure.json
label_order.json
page_plan.json
Prototype_Report.xlsx
```

This allows projects to be resumed later.

---

## Label Photos

User assigns labels to images.

Example:

```text
Transformer
Switch
Cabinet
```

Labels are stored in:

```text
labels.json
```

Enter key can be used to save labels.

---

## Review Labels

Allows:

- Label editing
- Label cleanup
- Label verification

---

## Order Figures

Controls:

```text
Figure 01
Figure 02
Figure 03
```

Ordering.

Saved to:

```text
label_order.json
```

---

## Page Planner

Creates page layout instructions.

Saved to:

```text
page_plan.json
```

Rules:

- 2 images per section
- 2 sections per page

---

## Generate Report

User clicks:

```text
Generate Report
```

The application:

1. Loads Template.xlsx
2. Inserts report images
3. Creates report pages
4. Saves:

```text
Prototype_Report.xlsx
```

---

# Workspace Architecture

The application works from a local cache.

```text
Network Folder
        ↓
Copy To Workspace
        ↓
Edit Locally
        ↓
Sync Back To Source Folder
```

Workspace location:

```text
C:\Users\<user>\PictureReportWorkspace
```

Advantages:

- Faster performance
- Reduced network lag
- Safer report generation

---

# Building EXE

## Clean Build

```cmd
rmdir /s /q build
rmdir /s /q dist
del PictureReportGenerator.spec
```

---

## Build

```cmd
pyinstaller --onedir --windowed --name PictureReportGenerator --add-data "src\docs;docs" --add-data "src\ralph.png;." src\main_gui.py
```

---

## EXE Output

```text
dist/
└── PictureReportGenerator/
    ├── PictureReportGenerator.exe
    ├── docs/
    └── ...
```

Launch:

```text
dist\PictureReportGenerator\PictureReportGenerator.exe
```

---

# Common Issues

## Ralph Logo Error

Replace:

```python
Image.Resampling.LANCZOS
```

with:

```python
Image.LANCZOS
```

Older Pillow versions do not support `Resampling`.

---

## MPO Export Error

Symptoms:

```text
KeyError: '.mpo'
```

during:

```python
wb.save(...)
```

Cause:

OpenPyXL detected workbook images using MPO format.

Workaround:

```python
img.format = "jpeg"
```

after creating OpenPyXL images.

Future fix:

Convert all source images to JPEG before report insertion.

---

## Template.xlsx Issues

OpenPyXL may fail on:

```text
EMF
WMF
```

embedded images.

Preferred formats:

```text
PNG
JPEG
```

---

# Git Workflow

Commit:

```bash
git add .
git commit -m "Description"
```

Push:

```bash
git push
```

---

# Author

Ralphael Alcober
Engineering Aide Temporary