# CLAUDE.md

## Project Overview

Picture Report Generator is a Tkinter desktop application used to create engineering photo reports in Excel.

The report consists of:

- Photos
- Figure numbers
- Labels
- Page planning
- Excel export

Generated from:

```text
Template.xlsx
```

using:

```python
openpyxl
```

---

# Original Architecture

Originally the application worked directly against:

```text
Network Drive
```

Example:

```text
\\m020diseng1\...
```

Problems:

- Slow labeling
- Slow page planning
- Slow export
- GUI freezes

---

# Workspace Architecture Migration

The application was redesigned.

New workflow:

```text
Source Folder
        ↓
Copy To Local Workspace
        ↓
Work Locally
        ↓
Sync Back
```

Workspace:

```python
Path.home() / "PictureReportWorkspace"
```

Benefits:

- Faster image loading
- Faster UI
- Less network latency

---

# Resume Feature

Problem:

Local workspace caused loss of resume capability.

Solution:

Copy existing project files:

```text
labels.json
report_structure.json
label_order.json
page_plan.json
Prototype_Report.xlsx
```

from source folder into workspace at load time.

Sync files back to source folder:

```python
sync_workspace_to_project()
```

when:

- Dashboard opens
- Application closes
- Report generates

---

# Enter Key Enhancement

Requested feature:

Pressing Enter should save label.

Implementation:

```python
self.label_entry.bind(
    "<Return>",
    self.on_enter
)
```

Methods:

```python
def on_enter(self, event=None):
    self.save_label()
```

---

# Image Count Bug

Observed:

6 photos present.

Only 4 appeared.

Root cause investigation:

Page planner was generating sections larger than report layout supported.

Design clarified:

```text
2 images per section
2 sections per page
```

Page planner updated:

```python
IMAGES_PER_SECTION = 2
```

instead of:

```python
IMAGES_PER_SECTION = 4
```

---

# Loading Screen Enhancement

Issue:

Application froze while:

- opening folder
- generating report

Solution:

Worker threads.

Implemented:

```python
threading.Thread(...)
```

Folder loading:

```python
_load_folder()
```

Report generation:

```python
_generate_report()
```

UI:

```python
show_loading()
hide_loading()
```

using:

```python
tk.Toplevel
ttk.Progressbar
```

Result:

Responsive UI during long operations.

---

# PyInstaller Build

Working command:

```cmd
pyinstaller --onedir --windowed --name PictureReportGenerator --add-data "src\docs;docs" --add-data "src\ralph.png;." src\main_gui.py
```

Important discovery:

Template folder located in:

```text
src/docs
```

not:

```text
docs
```

---

# Template Resource Handling

Implemented:

```python
resource_path()
```

using:

```python
sys._MEIPASS
```

for EXE compatibility.

Used for:

```python
Template.xlsx
ralph.png
```

---

# Pillow Compatibility Issue

Observed:

```text
AttributeError:
Image.Resampling
```

Environment:

```text
Python 3.8
```

Fix:

```python
Image.LANCZOS
```

instead of:

```python
Image.Resampling.LANCZOS
```

---

# Template Graphics Investigation

Original template contained:

```text
image1.jpeg
image2.emf
```

inside:

```text
xl/media
```

EMF was replaced with PNG.

New contents:

```text
image1.jpeg
image2.png
```

---

# MPO Export Failure Investigation

Observed:

```text
KeyError: '.mpo'
```

during:

```python
wb.save()
```

Investigation steps:

1. Verified source folder had no MPO files.
2. Verified report images were JPG.
3. Printed every image inserted into workbook.
4. Printed workbook image references.

Discovery:

Workbook images reported:

```text
PATH: /xl/media/image1.mpo
FORMAT: mpo
```

for report images despite filenames ending in:

```text
.jpg
```

Example:

```text
IMG_8306.jpg
FORMAT: mpo
```

Root Cause:

OpenPyXL/Pillow image objects were being assigned MPO format internally.

Not caused by source filenames.

Not caused by source folder contents.

Not caused by page planner.

Occurs during:

```python
wb.save()
```

inside:

```python
openpyxl.packaging.manifest
```

---

# Current Recommended MPO Fix

Inside:

```python
add_image()
```

after:

```python
img = Image(str(image_path))
```

force:

```python
img.format = "jpeg"
```

Alternative stronger fix:

```python
Pillow open
→ convert RGB
→ save temp JPG
→ insert temp JPG
```

before OpenPyXL image creation.

---

# Current Project Status

Working:

✅ Folder selection

✅ Local workspace

✅ Resume functionality

✅ Labeling

✅ Enter key save

✅ Review labels

✅ Figure order

✅ Page planner

✅ Loading screens

✅ Threaded operations

✅ EXE build configuration

✅ Template PNG migration

Outstanding issue:

❌ MPO format detected during workbook save.

Next recommended fix:

```python
img.format = "jpeg"
```

or convert images through Pillow before OpenPyXL insertion.