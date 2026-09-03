import os
import shutil
import json


file_categories = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",

    ".pdf": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",

    ".mp3": "Music",
    ".wav": "Music",

    ".mp4": "Videos",
    ".mkv": "Videos",

    ".pptx": "Presentations",
    ".ppt": "Presentations",

    ".py": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".java": "Code"
}


def create_plan(folder):

    plan = []
    planned_destinations = set()

    files = os.listdir(folder)

    for file in files:

        # Skip folders
        if not os.path.isfile(os.path.join(folder, file)):
            continue

        # Skip the organizer itself
        if file == "organizer.py":
            continue

        # Get filename and extension
        name, extension = os.path.splitext(file)
        extension = extension.lower()

        # Determine category
        if extension in file_categories:
            category = file_categories[extension]
        else:
            category = "Others"

        # Destination folder
        destination_folder = os.path.join(
            folder,
            category
        )

        # Source and destination paths
        source = os.path.join(
            folder,
            file
        )

        destination = os.path.join(
            destination_folder,
            file
        )

        # Handle duplicate filenames
        counter = 0

        while (
            os.path.exists(destination)
            or destination in planned_destinations
        ):

            counter += 1

            new_name = f"{name}_{counter}{extension}"

            destination = os.path.join(
                destination_folder,
                new_name
            )

        # Reserve destination
        planned_destinations.add(destination)

        # Add operation to plan
        plan.append(
            (source, destination)
        )

    return plan


def execute_plan(plan):

    results = {
        "moved": [],
        "failed": []
    }

    for source, destination in plan:

        try:

            # Create destination folder
            destination_folder = os.path.dirname(
                destination
            )

            os.makedirs(
                destination_folder,
                exist_ok=True
            )

            # Move file
            shutil.move(
                source,
                destination
            )

            # Record successful move
            results["moved"].append(
                (source, destination)
            )

        except FileNotFoundError:

            results["failed"].append(
                (
                    source,
                    destination,
                    "File not found"
                )
            )

        except PermissionError:

            results["failed"].append(
                (
                    source,
                    destination,
                    "Permission denied"
                )
            )

        except OSError as error:

            results["failed"].append(
                (
                    source,
                    destination,
                    str(error)
                )
            )

    return results


def print_report(results):

    print("\n✓ SUCCESSFUL")

    if results["moved"]:

        for source, destination in results["moved"]:

            print(
                f"  {source} → {destination}"
            )

    else:

        print("  No files were moved.")

    if results["failed"]:

        print("\n✗ FAILED")

        for source, destination, reason in results["failed"]:

            print(
                f"  {source} → {destination}"
            )

            print(
                f"    Reason: {reason}"
            )

    print(
        f"\nMoved: {len(results['moved'])}"
    )

    print(
        f"Failed: {len(results['failed'])}"
    )


def save_history(results, folder):

    history_file = os.path.join(
        folder,
        "history.json"
    )

    history = []

    # Load existing history
    if os.path.exists(history_file):

        try:

            with open(
                history_file,
                "r"
            ) as file:

                history = json.load(file)

        except (
            json.JSONDecodeError,
            OSError
        ):

            history = []

    # Create new operation
    operation = {
        "moved": results["moved"],
        "failed": results["failed"]
    }

    history.append(operation)

    # Save history
    with open(
        history_file,
        "w"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


def undo_operation(folder):

    history_file = os.path.join(
        folder,
        "history.json"
    )

    # Check whether history exists
    if not os.path.exists(history_file):

        print("\nNo history found.")
        return

    # Load history
    try:

        with open(
            history_file,
            "r"
        ) as file:

            history = json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        print("\nCould not read history.")
        return

    # Check whether history is empty
    if not history:

        print("\nNothing to undo.")
        return

    # Get latest operation
    operation = history[-1]

    moved = operation.get(
        "moved",
        []
    )

    if not moved:

        print("\nNothing to undo.")
        return

    remaining = []

    print("\nUndoing last operation...")

    # Undo in reverse order
    for source, destination in reversed(moved):

        try:

            if not os.path.exists(destination):

                print(
                    f"Could not find: {destination}"
                )

                remaining.append(
                    [source, destination]
                )

                continue

            # Move file back
            shutil.move(
                destination,
                source
            )

            print(
                f"  {destination} → {source}"
            )

        except PermissionError:

            print(
                f"Permission denied: {destination}"
            )

            remaining.append(
                [source, destination]
            )

        except OSError as error:

            print(
                f"Failed: {destination}"
            )

            print(
                f"Reason: {error}"
            )

            remaining.append(
                [source, destination]
            )

    # Update history
    if remaining:

        operation["moved"] = list(
            reversed(remaining)
        )

    else:

        # Everything was successfully undone
        history.pop()

    # Save updated history
    try:

        with open(
            history_file,
            "w"
        ) as file:

            json.dump(
                history,
                file,
                indent=4
            )

    except OSError:

        print(
            "\nWarning: Could not update history file."
        )

    # Report undo results
    restored = (
        len(moved) -
        len(remaining)
    )

    print("\nUndo complete.")
    print(f"Restored: {restored}")
    print(f"Still pending: {len(remaining)}")


def main():

    print("\n================================")
    print("      SMART FILE ORGANIZER")
    print("================================")

    while True:

        print("\n1. Organize folder")
        print("2. Undo last operation")
        print("3. Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        # ORGANIZE
        if choice == "1":

            folder = input(
                "\nEnter folder path: "
            ).strip()

            if not os.path.isdir(folder):

                print(
                    "\nInvalid folder path."
                )

                continue

            # Create plan
            plan = create_plan(folder)

            # Empty folder
            if not plan:

                print(
                    "\nNo files found to organize."
                )

                continue

            # Preview
            print("\nPlanned changes:")

            for source, destination in plan:

                print(
                    f"  {source} → {destination}"
                )

            # Confirmation
            answer = input(
                "\nExecute these changes? (y/n): "
            ).strip().lower()

            if answer != "y":

                print(
                    "\nNo files were moved."
                )

                continue

            # Execute
            results = execute_plan(plan)

            # Report
            print_report(results)

            # Save history
            if results["moved"]:

                save_history(
                    results,
                    folder
                )

                print(
                    "\nOperation saved to history."
                )

        # UNDO
        elif choice == "2":

            folder = input(
                "\nEnter folder path: "
            ).strip()

            if not os.path.isdir(folder):

                print(
                    "\nInvalid folder path."
                )

                continue

            undo_operation(folder)

        # EXIT
        elif choice == "3":

            print(
                "\nGoodbye! 👋"
            )

            break

        # INVALID CHOICE
        else:

            print(
                "\nInvalid choice. "
                "Please select 1, 2, or 3."
            )


if __name__ == "__main__":
    main()
