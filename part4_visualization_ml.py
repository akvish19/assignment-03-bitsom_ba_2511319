import pandas as pd
df = pd.read_csv("students.csv")
print(df.head())
print("Shape:", df.shape)
print("Columns:", df.columns)
print("\nData Types:\n", df.dtypes)

print(df.describe())

print(df['passed'].value_counts())

subject_cols = ['math', 'science', 'english', 'history', 'pe']

# Average for passing students
passing_avg = df[df['passed'] == 1][subject_cols].mean()
print("Average for Passing Students:\n", passing_avg)

# Average for failing students
failing_avg = df[df['passed'] == 0][subject_cols].mean()
print("\nAverage for Failing Students:\n", failing_avg)

# Create a temporary average column
df['temp_avg'] = df[subject_cols].mean(axis=1)

# Find the student (row) with the maximum average
top_student = df.loc[df['temp_avg'].idxmax()]

print("Student with highest overall average:")
print(top_student)

# student with the highest overall average across all 5 subjects
df['overall_average'] = df[['math', 'science', 'english', 'history', 'pe']].mean(axis=1)