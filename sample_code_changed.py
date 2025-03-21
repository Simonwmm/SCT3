import os
import pymysql
import subprocess
from urllib.request import urlopen

# ⚠️ Hardcoded credentials (easily detected)
db_config = {
    'host': 'mydatabase.com',
    'user': 'admin',
    'password': 'secret123'  # Hardcoded password
}

def get_user_input():
    user_input = input('Enter your name: ')  # ⚠️ User input with no validation
    return user_input

def send_email(to, subject, body):
    # ⚠️ Direct execution of system commands, command injection risk
    command = f'echo {body} | mail -s "{subject}" {to}'
    subprocess.Popen(command, shell=True)  # ⚠️ Using `shell=True`, makes vulnerability more obvious

def get_data():
    # ⚠️ Insecure API (HTTP, not encrypted)
    url = 'http://insecure-api.com/get-data?user=' + get_user_input()  # ⚠️ User input directly concatenated, SSRF vulnerability
    data = urlopen(url).read().decode()
    return data

def save_to_db(data):
    # ⚠️ SQL injection risk (string concatenation)
    query = "INSERT INTO mytable (column1, column2) VALUES ('" + data + "', 'Another Value')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)  # ⚠️ SQL Injection
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
