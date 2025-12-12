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

    raw_notes = [n.strip() for n in content.split("---") if n.strip()]
    notes = []

    for n in raw_notes:
        lines = n.split("\n")

        # Must start with TITLE
        if not lines[0].startswith("TITLE: "):
            continue

        title = lines[0].replace("TITLE: ", "").strip()

        # TAGS line
        try:
            tags_line = next(l for l in lines if l.startswith("TAGS:"))
            tags = tags_line.replace("TAGS:", "").strip()
        except StopIteration:
            tags = ""

        # CONTENT starts after "CONTENT:"
        try:
            content_index = lines.index("CONTENT:")
        except ValueError:
            continue

        content_data = "\n".join(lines[content_index + 1:]).strip()

        notes.append({
            "title": title,
            "tags": tags,
            "content": content_data
        })

    return notes


# ------------ SAVE NOTES ------------
def save_notes(notes):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for note in notes:
            f.write(f"TITLE: {note['title']}\n")
            f.write(f"TAGS: {note['tags']}\n")
            f.write("CONTENT:\n")
            f.write(f"{note['content']}\n")
            f.write("---\n")


# ------------ CREATE NOTE ------------
def create_note():
    print("\n--- Create New Note ---")
    title = input("Enter note title: ").strip()
    tags = input("Enter tags (comma separated): ").strip()

    print("Enter content (type END on a new line to finish):")
    content_lines = []
    while True:
        line = input()
        if line == "END":
            break
        content_lines.append(line)

    notes = load_notes()
    notes.append({
        "title": title,
        "tags": tags,
        "content": "\n".join(content_lines)
    })

    save_notes(notes)
    print("Note saved!\n")


# ------------ VIEW NOTES ------------
def view_notes():
    notes = load_notes()

    if not notes:
        print("\nNo notes found.\n")
        return

    print("\n--- All Notes ---")
    for i, n in enumerate(notes, 1):
        print(f"{i}. {n['title']}  (Tags: {n['tags']})")

    choice = input("\nEnter note number to view (0 to cancel): ")

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(notes):
        print("Cancelled.\n")
        return

    note = notes[int(choice) - 1]
    print(f"\n--- {note['title']} ---")
    print(f"Tags: {note['tags']}")
    print("\n" + note["content"] + "\n")


# ------------ SEARCH NOTES ------------
def search_notes():
    keyword = input("Enter keyword to search: ").lower().strip()
    notes = load_notes()

    results = [
        n for n in notes
        if keyword in n["title"].lower()
        or keyword in n["content"].lower()
        or keyword in n["tags"].lower()
    ]

    if not results:
        print("No matching notes found.\n")
        return

    print("\n--- Search Results ---")
    for note in results:
        print(f"- {note['title']}  (Tags: {note['tags']})")
    print()


# ------------ EDIT NOTE ------------
def edit_note():
    notes = load_notes()

    if not notes:
        print("No notes to edit.\n")
        return

    for i, n in enumerate(notes, 1):
        print(f"{i}. {n['title']} (Tags: {n['tags']})")

    choice = input("\nEnter note number to edit: ")

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(notes):
        print("Invalid choice.\n")
        return

    note = notes[int(choice) - 1]

    print("\nCurrent title:", note["title"])
    new_title = input("New title (press Enter to keep same): ").strip()
    if new_title:
        note["title"] = new_title

    print("\nCurrent tags:", note["tags"])
    new_tags = input("New tags (comma separated, Enter to keep same): ").strip()
    if new_tags:
        note["tags"] = new_tags

    print("\nCurrent content:")
    print(note["content"])

    print("\nEnter new content (type END to finish, Enter to keep same):")
    first_input = input()

    if first_input != "":
        content_lines = []
        if first_input != "END":
            content_lines.append(first_input)
        while first_input != "END":
            line = input()
            if line == "END":
                break
            content_lines.append(line)
        note["content"] = "\n".join(content_lines)

    save_notes(notes)
    print("Note updated!\n")


# ------------ DELETE NOTE ------------
def delete_note():
    notes = load_notes()

    if not notes:
        print("No notes to delete.\n")
        return

    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['title']} (Tags: {note['tags']})")

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
