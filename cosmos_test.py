import os
import time
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

# Load environment variables
load_dotenv()

ENDPOINT = os.getenv("COSMOS_ENDPOINT")
KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = os.getenv("COSMOS_DATABASE")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Connect to Cosmos DB
client = CosmosClient(
    ENDPOINT,
    credential=KEY,
    consistency_level="Eventual"
)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)


# Admin login
def admin_login():
    print("\n===== ADMIN LOGIN =====")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("\nLogin successful!")
        return True

    print("\nInvalid username or password!")
    return False


# View students
def view_students():
    students = list(container.query_items(
        query="SELECT * FROM c",
        enable_cross_partition_query=True
    ))

    print("\n===== STUDENT RECORDS =====")

    if not students:
        print("No student records found.")
        return

    for student in students:
        print(
            f"ID: {student['id']} | "
            f"Student ID: {student['studentId']} | "
            f"Name: {student['name']} | "
            f"Course: {student['course']} | "
            f"Marks: {student['marks']}"
        )


# Add student
def add_student():
    print("\n===== ADD STUDENT =====")

    student_id = input("Enter student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    existing = list(container.query_items(
        query="SELECT * FROM c WHERE c.studentId = @sid",
        parameters=[{"name": "@sid", "value": student_id}],
        enable_cross_partition_query=True
    ))

    if existing:
        print("Student ID already exists.")
        return

    name = input("Enter name: ").strip()
    course = input("Enter course: ").strip()

    try:
        marks = float(input("Enter marks: "))
        if not 0 <= marks <= 100:
            print("Marks must be between 0 and 100.")
            return
    except ValueError:
        print("Please enter valid marks.")
        return

    student = {
        "id": f"student{student_id}",
        "studentId": student_id,
        "name": name,
        "course": course,
        "marks": marks
    }

    container.create_item(body=student)
    print("Student added successfully!")


# Find student by studentId
def find_student(student_id):
    results = list(container.query_items(
        query="SELECT * FROM c WHERE c.studentId = @sid",
        parameters=[{"name": "@sid", "value": student_id}],
        enable_cross_partition_query=True
    ))
    return results[0] if results else None


# Update student
def update_student():
    print("\n===== UPDATE STUDENT =====")
    student_id = input("Enter student ID to update: ").strip()

    student = find_student(student_id)

    if not student:
        print("Student not found.")
        return

    name = input(f"Enter new name [{student['name']}]: ").strip()
    course = input(f"Enter new course [{student['course']}]: ").strip()
    marks_input = input(f"Enter new marks [{student['marks']}]: ").strip()

    if name:
        student["name"] = name

    if course:
        student["course"] = course

    if marks_input:
        try:
            marks = float(marks_input)
            if not 0 <= marks <= 100:
                print("Marks must be between 0 and 100.")
                return
            student["marks"] = marks
        except ValueError:
            print("Please enter valid marks.")
            return

    container.replace_item(
        item=student["id"],
        body=student
    )

    print("Student updated successfully!")


# Delete student
def delete_student():
    print("\n===== DELETE STUDENT =====")
    student_id = input("Enter student ID to delete: ").strip()

    student = find_student(student_id)

    if not student:
        print("Student not found.")
        return

    confirm = input(
        f"Delete {student['name']}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        container.delete_item(
            item=student["id"],
            partition_key=student["studentId"]
        )
        print("Student deleted successfully!")
    else:
        print("Deletion cancelled.")


# Consistency read-time test
def consistency_test():
    print("\n===== READ TIME TEST =====")

    times = []

    for i in range(10):
        start = time.perf_counter()

        students = list(container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        ))

        end = time.perf_counter()
        elapsed = (end - start) * 1000
        times.append(elapsed)

        print(f"Test {i + 1}: {elapsed:.2f} ms")

    average = sum(times) / len(times)

    print("\nConsistency level: Account default")
    print("Total students:", len(students))
    print(f"Average read time: {average:.2f} ms")


# Admin dashboard
def admin_dashboard():
    while True:
        print("\n===== ADMIN DASHBOARD =====")
        print("1. View Students")
        print("2. Add Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Consistency Read-Time Test")
        print("6. Logout")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                view_students()
            elif choice == "2":
                add_student()
            elif choice == "3":
                update_student()
            elif choice == "4":
                delete_student()
            elif choice == "5":
                consistency_test()
            elif choice == "6":
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print("Operation failed:", e)


# Main program
if __name__ == "__main__":
    if not all([
        ENDPOINT, KEY, DATABASE_NAME, CONTAINER_NAME,
        ADMIN_USERNAME, ADMIN_PASSWORD
    ]):
        raise ValueError("Missing configuration in .env file")

    print("Connected to Azure Cosmos DB!")

    if admin_login():
        admin_dashboard()