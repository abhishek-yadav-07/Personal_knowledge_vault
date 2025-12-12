import os

FILE_NAME = "notes.txt"


# ------------ LOAD NOTES ------------
def load_notes():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return []

    # Split notes safely even if formatting isn't perfect
    raw_notes = [n.strip() for n in content.split("---") if n.strip()]

    notes = []
    for n in raw_notes:
        lines = n.split("\n")

        # Extract title
        if not lines[0].startswith("TITLE: "):
            continue  # skip malformed notes

        title = lines[0].replace("TITLE: ", "").strip()

        # Find "CONTENT:" line
        try:
            content_index = lines.index("CONTENT:")
        except ValueError:
            continue

        # Join all remaining lines as content
        data = "\n".join(lines[content_index + 1:]).strip()

        notes.append({"title": title, "content": data})

    return notes


# ------------ SAVE NOTES ------------
def save_notes(notes):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for note in notes:
            f.write(f"TITLE: {note['title']}\n")
            f.write("CONTENT:\n")
            f.write(f"{note['content']}\n")
            f.write("---\n")  # always end with separator


# ------------ CREATE NOTE ------------
def create_note():
    print("\n--- Create New Note ---")
    title = input("Enter note title: ").strip()

    print("Enter content (type END on a new line to finish):")
    content_lines = []
    while True:
        line = input()
        if line == "END":
            break
        content_lines.append(line)

    notes = load_notes()
    notes.append({"title": title, "content": "\n".join(content_lines)})
    save_notes(notes)
    print("Note saved!\n")


# ------------ VIEW NOTES ------------
def view_notes():
    notes = load_notes()

    if not notes:
        print("\nNo notes found.\n")
        return

    print("\n--- All Notes ---")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['title']}")

    choice = input("\nEnter note number to view (0 to cancel): ")

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(notes):
        print("Cancelled.\n")
        return

    note = notes[int(choice) - 1]
    print(f"\n--- {note['title']} ---")
    print(note["content"])
    print()


# ------------ SEARCH NOTES ------------
def search_notes():
    keyword = input("Enter keyword to search: ").lower().strip()
    notes = load_notes()

    results = [
        n for n in notes
        if keyword in n["title"].lower() or keyword in n["content"].lower()
    ]

    if not results:
        print("No matching notes found.\n")
        return

    print("\n--- Search Results ---")
    for note in results:
        print(f"- {note['title']}")
    print()


# ------------ EDIT NOTE ------------
def edit_note():
    notes = load_notes()

    if not notes:
        print("No notes to edit.\n")
        return

    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['title']}")

    choice = input("\nEnter note number to edit: ")

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(notes):
        print("Invalid choice.\n")
        return

    note = notes[int(choice) - 1]

    print("\nCurrent content:")
    print(note["content"])

    print("\nEnter new content (type END to finish):")
    new_lines = []
    while True:
        line = input()
        if line == "END":
            break
        new_lines.append(line)

    note["content"] = "\n".join(new_lines)
    save_notes(notes)
    print("Note updated!\n")


# ------------ DELETE NOTE ------------
def delete_note():
    notes = load_notes()

    if not notes:
        print("No notes to delete.\n")
        return

    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['title']}")

    choice = input("\nEnter note number to delete: ")

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(notes):
        print("Invalid choice.\n")
        return

    deleted = notes.pop(int(choice) - 1)
    save_notes(notes)
    print(f"Deleted: {deleted['title']}\n")


# ------------ MAIN MENU ------------
def main():
    while True:
        print("==========================")
        print("  Personal Knowledge Vault")
        print("==========================")
        print("1. Create Note")
        print("2. View Notes")
        print("3. Search Notes")
        print("4. Edit Note")
        print("5. Delete Note")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            search_notes()
        elif choice == "4":
            edit_note()
        elif choice == "5":
            delete_note()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()
