import pymysql

# Set the database credentials
host = 'database-1.cpyjslxy8wep.eu-north-1.rds.amazonaws.com'
port = 3306
user = 'admin'
password = 'Rellai23!'
database = 'mysql'

# Connect to the database
connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

# Create a cursor object
cursor = connection.cursor()

# Execute a SQL query
cursor.execute("CREATE TABLE client (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, phone VARCHAR(20) NOT NULL, address VARCHAR(255) NOT NULL, city VARCHAR(255) NOT NULL, state VARCHAR(255) NOT NULL, zip VARCHAR(10) NOT NULL);")

# Fetch the results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the cursor and connection
cursor.close()
connection.close()

