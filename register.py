
import hashlib
import mysql.connector
import re
# Function to connect to MySQL


def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",  # Change this to your MySQL username
            password="",  # Change this to your MySQL password
            database="mon-shop"  # Change this to your database name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def hash_password(password):
    result = hashlib.md5(password.encode())
    return result.hexdigest()

# Function to register a new user


def register_user(username, password, firstname, lastname, address, contact_number):
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO credentials (username, password, firstname, lastname, address, contact_number) VALUES (%s, %s, %s, %s, %s, %s)",
                           (username, hash_password(password), firstname, lastname, address, contact_number))
            connection.commit()
            print("Registration successful!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

# Function for alphanumeric password


def validate_password(password):

    if re.match(r"^[a-zA-Z0-9\W]{8,13}$", password):
        return True
    else:
        return False


# Function to log in a user
def login_user():

    username = input('Enter your username: ')
    password = input('Enter your password: ')
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM credentials WHERE username = %s AND password = %s",
                           (username, hash_password(password)))
            result = cursor.fetchone()
            if result:
                print("Login Sucessful")
            else:
                cursor.execute(
                    f"Select * From credentials Where username = '{username}'")
                result = cursor.fetchone()
                if result:
                    print("Invalid password")
                    login_user()
                else:
                    print("No account found, Please Register! ")
                    main()
        except Exception as e:
            login_user()
        finally:
            cursor.close()
            connection.close()


def register():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        username = input('Enter your username: ')
        cursor.execute(
            f"Select * From credentials Where username = '{username}'")
        result = cursor.fetchone()
        if result != None:
            raise Exception("This user is already taken")
            exit()
        password = input('Enter your password: ')
        isValid = validate_password(password)
        if not isValid:
            raise Exception("Not valid password")
        firstname = input('Enter your firstname: ')
        lastname = input('Enter your lastname: ')
        address = input('Enter your address: ')
        contact_number = input('Enter your contact_number: ')

        register_user(username, password, firstname,
                      lastname, address, contact_number)
    except Exception as e:
        print(f"{str(e)}, Trying Again...")
        register()


def main():
    print("Select your transaction")
    print("1 Login")
    print("2 Register")
    choice = input("Enter your transaction :")

    if choice == "1":
        login_user()
    elif choice == "2":
        register()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
