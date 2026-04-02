# ============================================================
# Assignment - Part 1: Python Basics & Control Flow
# Theme     : Student Grade Tracker
# Author    : [Krina Desai]
# Date      : March 2026
# ============================================================
# This program manages student data, computes results, and
# provides a summary report using core Python concepts like
# loops, conditionals, string methods, and f-strings.
# ============================================================


# ============================================================
# TASK 1 — Data Parsing & Profile Cleaning
# ============================================================
# Raw data often comes from forms or spreadsheets with messy
# formatting — extra spaces, wrong casing, wrong data types.
# Here we clean each student record before using it.

raw_students = [
    {"name": "  ayesha SHARMA  ", "roll": "101", "marks_str": "88, 72, 95, 60, 78"},
    {"name": "ROHIT verma",       "roll": "102", "marks_str": "55, 68, 49, 72, 61"},
    {"name": "  Priya Nair  ",    "roll": "103", "marks_str": "91, 85, 88, 94, 79"},
    {"name": "karan MEHTA",       "roll": "104", "marks_str": "40, 55, 38, 62, 50"},
    {"name": " Sneha pillai ",    "roll": "105", "marks_str": "75, 80, 70, 68, 85"},
]

# Store cleaned records so we can reuse them in Tasks 2 and 3
cleaned_students = []

print("=" * 40)
print("       TASK 1 — Profile Cleaning")
print("=" * 40)

for student in raw_students:

    # Step 1: Remove leading/trailing spaces, then apply Title Case
    # .strip() removes whitespace from both ends of the string
    # .title() capitalises the first letter of every word
    clean_name = student["name"].strip().title()

    # Step 2: Convert roll from string "101" → integer 101
    # We use int() because roll numbers should be numeric, not text
    clean_roll = int(student["roll"])

    # Step 3: Split "88, 72, 95" on ", " to get ["88","72","95"],
    # then convert each element to int using a list comprehension
    clean_marks = [int(m) for m in student["marks_str"].split(", ")]

    # Build a clean dictionary for this student
    cleaned = {
        "name":  clean_name,
        "roll":  clean_roll,
        "marks": clean_marks,
    }
    cleaned_students.append(cleaned)

    # Step 4: Validate — every word in the name must be alphabetic only.
    # .split() breaks the name into individual words.
    # all() returns True only if every word passes .isalpha()
    all_words_alpha = all(word.isalpha() for word in clean_name.split())
    validity = "✓ Valid name" if all_words_alpha else "✗ Invalid name"

    # Step 5: Print a formatted profile card using f-strings
    print(f"\n{validity}")
    print("=" * 32)
    print(f"Student : {clean_name}")
    print(f"Roll No : {clean_roll}")
    print(f"Marks   : {clean_marks}")
    print("=" * 32)

# Step 6: Find the student with roll number 103 and print name variations
# We loop through cleaned_students and check the roll field
for s in cleaned_students:
    if s["roll"] == 103:
        # .upper() converts every character to uppercase
        # .lower() converts every character to lowercase
        print(f"\nRoll 103 — ALL CAPS  : {s['name'].upper()}")
        print(f"Roll 103 — lowercase : {s['name'].lower()}")
        break   # No need to keep looping once we found the match


# ============================================================
# TASK 2 — Marks Analysis Using Loops & Conditionals
# ============================================================
# We analyse a single student's marks across subjects,
# then let the user add new subjects through a while loop.

student_name = "Ayesha Sharma"
subjects     = ["Math", "Physics", "CS", "English", "Chemistry"]
marks        = [88, 72, 95, 60, 78]

print("\n" + "=" * 40)
print("       TASK 2 — Marks Analysis")
print("=" * 40)

# --- Grade scheme using a for loop ---
# We pair each subject with its marks using zip(), which lets us
# iterate over two lists at the same time without needing an index.
print(f"\nGrade Report for {student_name}:\n")
print(f"{'Subject':<12} | {'Marks':>5} | Grade")
print("-" * 30)

for subject, mark in zip(subjects, marks):
    # Assign grade based on mark range using if-elif-else ladder
    if mark >= 90:
        grade = "A+"
    elif mark >= 80:
        grade = "A"
    elif mark >= 70:
        grade = "B"
    elif mark >= 60:
        grade = "C"
    else:
        grade = "F"

    # :<12 means left-align in 12 characters; :>5 means right-align in 5
    print(f"{subject:<12} | {mark:>5} | {grade}")

# --- Summary statistics ---
# sum() adds all values; len() counts elements; max/min work on lists
total   = sum(marks)
average = round(total / len(marks), 2)   # round to 2 decimal places

# zip(subjects, marks) lets us find the subject name alongside its mark
highest_subject = subjects[marks.index(max(marks))]
lowest_subject  = subjects[marks.index(min(marks))]

print(f"\nTotal Marks   : {total}")
print(f"Average Marks : {average}")
print(f"Highest       : {highest_subject} ({max(marks)})")
print(f"Lowest        : {lowest_subject} ({min(marks)})")

# --- While loop: simulated marks-entry system ---
# We keep looping until the user types "done".
# We handle invalid inputs so the program never crashes.
print("\n--- Add New Subjects (type 'done' to stop) ---")

new_subjects_added = 0   # Counter for how many valid subjects were added

while True:
    # Ask for subject name first
    sub_input = input("Enter subject name (or 'done' to stop): ").strip()

    if sub_input.lower() == "done":
        # User wants to exit — break out of the while loop
        break

    # Now ask for the marks for this subject
    marks_input = input(f"Enter marks for {sub_input} (0-100): ").strip()

    # --- Input validation ---
    try:
        # Try converting to float first to allow decimals like 85.5
        new_mark = float(marks_input)

        if 0 <= new_mark <= 100:
            # Valid mark — add to our lists
            subjects.append(sub_input)
            marks.append(new_mark)
            new_subjects_added += 1
            print(f"  ✓ Added: {sub_input} = {new_mark}")
        else:
            # Number exists but is out of the 0–100 range
            print("  ⚠ Warning: Marks must be between 0 and 100. Entry skipped.")

    except ValueError:
        # Input is not a number at all (e.g. user typed "abc")
        print("  ⚠ Warning: Invalid input — please enter a numeric value. Entry skipped.")

# After the loop: print summary of new entries and updated average
print(f"\nNew subjects added : {new_subjects_added}")
updated_avg = round(sum(marks) / len(marks), 2)
print(f"Updated average    : {updated_avg}")


# ============================================================
# TASK 3 — Class Performance Summary
# ============================================================
# We compute averages and pass/fail status for a whole class,
# then print a formatted report table, top student, and stats.

class_data = [
    ("Ayesha Sharma",  [88, 72, 95, 60, 78]),
    ("Rohit Verma",    [55, 68, 49, 72, 61]),
    ("Priya Nair",     [91, 85, 88, 94, 79]),
    ("Karan Mehta",    [40, 55, 38, 62, 50]),
    ("Sneha Pillai",   [75, 80, 70, 68, 85]),
]

print("\n" + "=" * 40)
print("     TASK 3 — Class Performance")
print("=" * 40)

# Table header — :<17 means left-align in 17 chars, :^7 means centred in 7
print(f"\n{'Name':<17} | {'Average':^7} | Status")
print("-" * 40)

passed_count = 0
failed_count = 0
all_averages = []   # We'll use this to compute the class average later
topper_name  = ""
topper_avg   = 0

for name, m_list in class_data:
    # Calculate average for this student, rounded to 2 decimal places
    avg = round(sum(m_list) / len(m_list), 2)
    all_averages.append(avg)

    # Pass if average >= 60, otherwise Fail
    status = "Pass" if avg >= 60 else "Fail"

    # Count passes and fails for the summary below
    if status == "Pass":
        passed_count += 1
    else:
        failed_count += 1

    # Track the class topper (student with highest average)
    if avg > topper_avg:
        topper_avg  = avg
        topper_name = name

    # Print this student's row — :>7.2f means right-align, 2 decimal places
    print(f"{name:<17} | {avg:>7.2f}  | {status}")

# --- Post-table summary ---
class_avg = round(sum(all_averages) / len(all_averages), 2)

print(f"\nStudents Passed : {passed_count}")
print(f"Students Failed : {failed_count}")
print(f"Class Topper    : {topper_name} ({topper_avg})")
print(f"Class Average   : {class_avg}")


# ============================================================
# TASK 4 — String Manipulation Utility
# ============================================================
# We apply a series of string operations on a student's essay.
# Each step builds on the previous clean version.

essay = "  python is a versatile language. it supports object oriented, functional, and procedural programming. python is widely used in data science and machine learning.  "

print("\n" + "=" * 40)
print("   TASK 4 — String Manipulation")
print("=" * 40)

# Step 1: Strip leading/trailing whitespace.
# We store this as clean_essay and use it for ALL steps below.
clean_essay = essay.strip()
print(f"\nStep 1 — Stripped:\n{clean_essay}\n")

# Step 2: Title Case — capitalises first letter of every word.
# We apply this to clean_essay (not the original messy version).
title_essay = clean_essay.title()
print(f"Step 2 — Title Case:\n{title_essay}\n")

# Step 3: Count how many times "python" appears.
# clean_essay is already lowercase after strip(), so we can count directly
# without needing .lower() again.
python_count = clean_essay.count("python")
print(f"Step 3 — 'python' appears {python_count} time(s)\n")

# Step 4: Replace every "python" with "Python 🐍".
# Since clean_essay is lowercase, .replace("python", ...) catches all of them.
replaced_essay = clean_essay.replace("python", "Python 🐍")
print(f"Step 4 — After replacement:\n{replaced_essay}\n")

# Step 5: Split into sentences by splitting on ". " (period + space).
# This gives us a list of individual sentences.
sentences = clean_essay.split(". ")
print(f"Step 5 — Sentence list:\n{sentences}\n")

# Step 6: Print each sentence numbered, with a period at the end if missing.
# We use enumerate(start=1) so numbering begins at 1 instead of 0.
print("Step 6 — Numbered sentences:")
for i, sentence in enumerate(sentences, start=1):
    # Check if the sentence already ends with "." — if not, add one
    if not sentence.endswith("."):
        sentence += "."
    print(f"{i}. {sentence}")

# ============================================================
# End of Assignment — Part 1
# ============================================================
