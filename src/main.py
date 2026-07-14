from pathlib import Path
import sys

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp"
}


def load_images(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    images = []

    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append(file)

    return sorted(images)


def main():

    if len(sys.argv) < 2:
        print("Usage:")
        print(r"python src\main.py <image_folder>")
        return

    image_folder = sys.argv[1]

    images = load_images(image_folder)

    print(f"\nFound {len(images)} image(s).\n")

    for image in images:
        print(image.name)


if __name__ == "__main__":
    main()