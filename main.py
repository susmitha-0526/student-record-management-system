"""Student Record Management System
Covers: functions, parameters, return values, lambda, list comprehensions,
file handling (JSON + CSV), and exception handling (try-except-finally).
"""

import csv
import json
import os

JSON_FILE = "students.json"
CSV_FILE = "students.csv"
FIELDS = ["id", "name", "age", "course", "marks"]


# ---------- File handling ----------
def load_students(filename=JSON_FILE):
    """Load students from a JSON file. Returns [] if file is missing/corrupt."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: data file is corrupted. Starting with an empty list.")
        return []


def save_students(students, filename=JSON_FILE):
    """Save students to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(students, f, indent=4)
    except OSError as e:
        print(f"Could not save data: {e}")


def export_to_csv(students, filename=CSV_FILE):
    """Export all records to a CSV file."""
    try:
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(students)
        print(f"Exported {len(students)} records to {filename}")
    except OSError as e:
        print(f"Export failed: {e}")


def import_from_csv(filename=CSV_FILE):
    """Read students from a CSV file (converting numeric fields)."""
    students = []
    try:
        with open(filename, "r", newline="") as f:
            for row in csv.DictReader(f):
                row["id"] = int(row["id"])
                row["age"] = int(row["age"])
                row["marks"] = float(row["marks"])
                students.append(row)
    except FileNotFoundError:
        print(f"{filename} not found.")
    except (ValueError, KeyError):
        print("CSV file has invalid or missing data.")
    return students


# ---------- Input helpers (exception handling) ----------
def get_number(prompt, cast=int, minimum=None, maximum=None):
    """Keep asking until the user enters a valid number."""
    while True:
        try:
            value = cast(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            print("Invalid input, please try again.")


def next_id(students):
    return max((s["id"] for s in students), default=0) + 1


# ---------- CRUD ----------
def add_student(students):
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    student = {
        "id": next_id(students),
        "name": name,
        "age": get_number("Age: ", int, 1, 100),
        "course": input("Course: ").strip(),
        "marks": get_number("Marks (0-100): ", float, 0, 100),
    }
    students.append(student)
    save_students(students)
    print(f"Added student with ID {student['id']}.")


def display_students(students):
    if not students:
        print("No records found.")
        return
    print(f"\n{'ID':<5}{'Name':<20}{'Age':<6}{'Course':<15}{'Marks':<6}")
    print("-" * 52)
    for s in students:
        print(f"{s['id']:<5}{s['name']:<20}{s['age']:<6}{s['course']:<15}{s['marks']:<6}")


def find_student(students, student_id):
    return next((s for s in students if s["id"] == student_id), None)


def search_students(students):
    keyword = input("Search by name: ").strip().lower()
    # list comprehension
    results = [s for s in students if keyword in s["name"].lower()]
    display_students(results)


def update_student(students):
    student = find_student(students, get_number("Student ID to update: "))
    if student is None:
        print("Student not found.")
        return
    print("Press Enter to keep the current value.")
    student["name"] = input(f"Name [{student['name']}]: ").strip() or student["name"]
    age = input(f"Age [{student['age']}]: ").strip()
    if age:
        try:
            student["age"] = int(age)
        except ValueError:
            print("Invalid age, keeping old value.")
    student["course"] = input(f"Course [{student['course']}]: ").strip() or student["course"]
    marks = input(f"Marks [{student['marks']}]: ").strip()
    if marks:
        try:
            student["marks"] = float(marks)
        except ValueError:
            print("Invalid marks, keeping old value.")
    save_students(students)
    print("Record updated.")


def delete_student(students):
    student = find_student(students, get_number("Student ID to delete: "))
    if student is None:
        print("Student not found.")
        return
    students.remove(student)
    save_students(students)
    print("Record deleted.")


# ---------- Lambda / list comprehension extras ----------
def show_toppers(students):
    # lambda used as a sort key
    ranked = sorted(students, key=lambda s: s["marks"], reverse=True)[:3]
    print("\nTop 3 students:")
    display_students(ranked)


def show_average(students):
    if not students:
        print("No records found.")
        return
    avg = sum([s["marks"] for s in students]) / len(students)
    print(f"Class average: {avg:.2f}")


# ---------- Main menu ----------
def main():
    students = load_students()
    menu = """
=== Student Record Management System ===
1. Add student
2. View all students
3. Search by name
4. Update student
5. Delete student
6. Show top 3 students
7. Show class average
8. Export to CSV
9. Exit
"""
    try:
        while True:
            print(menu)
            choice = input("Choose an option: ").strip()
            if choice == "1":
                add_student(students)
            elif choice == "2":
                display_students(students)
            elif choice == "3":
                search_students(students)
            elif choice == "4":
                update_student(students)
            elif choice == "5":
                delete_student(students)
            elif choice == "6":
                show_toppers(students)
            elif choice == "7":
                show_average(students)
            elif choice == "8":
                export_to_csv(students)
            elif choice == "9":
                break
            else:
                print("Invalid choice.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        save_students(students)
        print("Data saved. Goodbye!")


if __name__ == "__main__":
    main()
