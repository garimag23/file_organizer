# Smart File Organizer 📁

A Python-based file organization tool that automatically sorts files into categories based on their file extensions.

## Features

* 📂 Automatically organizes files into categories
* 🖼️ Supports Images
* 📄 Supports Documents
* 🎵 Supports Music
* 🎬 Supports Videos
* 📊 Supports Presentations
* 💻 Supports Code files
* 📦 Places unknown file types into `Others`
* 🔍 Preview changes before moving files
* 🔢 Handles duplicate filenames
* ↩️ Supports undoing the last organization operation
* 💾 Saves operation history using JSON
* ⚠️ Handles common file and permission errors

## Categories

| File Type                       | Folder        |
| ------------------------------- | ------------- |
| `.jpg`, `.jpeg`, `.png`, `.gif` | Images        |
| `.pdf`, `.docx`, `.txt`         | Documents     |
| `.mp3`, `.wav`                  | Music         |
| `.mp4`, `.mkv`                  | Videos        |
| `.pptx`, `.ppt`                 | Presentations |
| `.py`, `.cpp`, `.c`, `.java`    | Code          |
| Other extensions                | Others        |

## How to Run

Make sure Python is installed, then run:

```bash
python organizer.py
```

The program will provide a menu to:

1. Organize a folder
2. Undo the last operation
3. Exit

## Technologies Used

* Python
* OS / filesystem handling
* JSON
* Git & GitHub

