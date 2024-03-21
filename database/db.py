import psycopg2
import json

# Replace these variables with your actual database credentials
database_name = "course"
user = "admin"
password = "password"
host = "localhost"  # Change this if your database is on a different host
port = "5432"       # Default PostgreSQL port

# Path to your JSON file
json_file_path = "cleaned_courses.json"

def create_table(cursor):
    # Define the table structure as per your requirements
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS course_list (
            id INT,
            name TEXT,
            description TEXT,
            prereqs INTEGER[],
            misc TEXT
        );
    '''
    cursor.execute(create_table_query)

def insert_data_from_json(cursor):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Assuming each entry in the JSON file has 'name' and 'age' fields
    insert_query = '''
        INSERT INTO course_list (id, name, description, prereqs, misc) VALUES (%s, %s, %s, %s, %s);
    '''

    for entry in data:
        id = entry['id']
        name = entry['name']
        description = entry['desc']
        prereqs = entry.get('prereqs', [])  
        misc = entry['misc']
        cursor.execute(insert_query, (id, name, description, prereqs, misc))

def main():
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(
        database=database_name,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Create the table (if not exists)

    # Insert data from the JSON file into the table
    insert_data_from_json(cursor)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection when done
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()