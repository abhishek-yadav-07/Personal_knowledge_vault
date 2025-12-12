import os

FILE_NAME = "notes.txt"

def load_notes():
    if not os.path.exists(FILE_NAME):
        return []

    notes = []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return []

    raw_notes = content.split("\n---\n")

    for n in raw_notes:
        lines = n.split("\n")
        title = lines[0].replace("TITLE: ", "")
        content_index = lines.index("CONTENT:")
        data = "\n".join(lines[content_index + 1:])
        notes.append({"title": title, "content": data})

    return notes


def save_notes(notes):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for note in notes:
            f.write(f"TITLE: {note['title']}\n")
            f.write("CONTENT:\n")
            f.write(f"{note['content']}\n")
            f.write("---\n")


def create_note():
    title = input("Enter note title: ")
    content = []
    print("Enter note content (type 'END' on a new line to stop):")

    while True:
        line = input()
        if line == "END":
            break
        content.append(line)

    notes = load_notes()
    notes.append({"title": title, "content": "\n".join(content)})
    save_notes(notes)
    print("Note saved!\n")


def view_notes():
    notes = load_notes()

    if not notes:
        print("No notes found.\n")
        return

    print("\nAll Notes:")
    for i, n in enumerate(notes):
        print(f"{i+1}. {n['title']}")
    print()

    choice = int(input("Enter note number to view (0 to cancel): "))
    if choice == 0:
        return

    note = notes[choice - 1]
    print("\n====", note['title'], "====")
    print(note['content'])
    print()


def search_notes():
    keyword = input("Enter search keyword: ").lower()
    notes = load_notes()

    results = [n for n in notes if keyword in n['title'].lower() or keyword in n['content'].lower()]

    if not results:
        print("No matching notes found.\n")
        return

    print("\nSearch Results:")
    for n in results:
        print("- " + n['title'])
    print()


def edit_note():
    notes = load_notes()

    for i, n in enumerate(notes):
        print(f"{i+1}. {n['title']}")

    choice = int(input("Enter note number to edit: "))
    note = notes[choice - 1]

    print("Current content:")
    print(note['content'])

    print("\nEnter new content (type 'END' to finish):")
    content = []
    while True:
        line = input()
        if line == "END":
            break
        content.append(line)

    note['content'] = "\n".join(content)
    save_notes(notes)
    print("Note updated!\n")


def delete_note():
    notes = load_notes()

    for i, n in enumerate(notes):
        print(f"{i+1}. {n['title']}")

    choice = int(input("Enter note number to delete: "))

    removed = notes.pop(choice - 1)
    save_notes(notes)
    print(f"Deleted note: {removed['title']}\n")


def main():
    while True:
        print("==========================")
        print("  Personal Knowledge Vault")
        print("==========================")
        print("1. Create Note")
        print("2. View All Notes")
        print("3. Search Notes")
        print("4. Edit Note")
        print("5. Delete Note")
        print("6. Exit")

        choice = input("Enter your choice: ")

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
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
