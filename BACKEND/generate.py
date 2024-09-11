import mysql.connector
from datetime import datetime, timedelta
import random

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cms"
)

cursor = mydb.cursor()

# List of employee IDs
employee_ids = [50, 55, 56]

# Number of days to backtrack
num_days = 20

# Function to insert raw data into the 'rawdata' table
def insert_raw_data(employee_id, date, log_time):
    query = "INSERT INTO rawdata (employee_id, date, log_time) VALUES (%s, %s, %s)"
    cursor.execute(query, (employee_id, date, log_time))
    mydb.commit()

# Function to generate a random log time (between 8:00 AM and 6:00 PM)
def generate_random_log_time():
    # Random hour between 8 and 18 (8 AM to 6 PM)
    hour = random.randint(8, 18)
    # Random minute and second
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.strptime(f"{hour}:{minute}:{second}", '%H:%M:%S').time()

# Add raw data for the last 20 days
current_date = datetime.now().date()

for day in range(num_days):
    # Get the date for the past days
    date = current_date - timedelta(days=day)

    for employee_id in employee_ids:
        # Generate random log time for the employee
        log_time = generate_random_log_time()

        # Insert the log entry
        print(f"Inserting log data for Employee {employee_id} on {date} at {log_time}")
        insert_raw_data(employee_id, date, log_time)

print("Raw data inserted for all employees for the last 20 days.")

cursor.close()
mydb.close()
