import re
def count_unique_students(file_obj):
    try:
        students = set()  # Store unique student names

        for line in file_obj:  # Read file line by line
            match = re.search(r"-\s*([A-Z0-9]+)\s*(?=::|Marks|$)", line)
            if match:
                student_name = match.group(1).strip()
                students.add(student_name)

        result = len(students)
        return str(result)  # Return count as a dictionary
    except Exception as e:
        return {"error": str(e)}
