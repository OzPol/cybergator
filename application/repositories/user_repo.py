from application.databases.psql_db import get_sql_connection, release_connection
from application.models.user_model import User


def get_user_by_username(username: str) -> User | None:
    """Fetch a user from the database using their username and return a User object"""
    conn = get_sql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        return User(id=user[0], username=user[1], password=user[2]) if user else None

    except Exception as e:
        print(f"Database error: {e}")
        return None

    finally:
        cursor.close()
        release_connection(conn)

def create_user(user: User) -> User | dict:
    """Insert a new user into the database and return a User object"""
    conn = get_sql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
            (user.username, user.password),
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        return User(id=user_id, username=user.username, password=user.password)

    except Exception as e:
        conn.rollback()
        return {"error": "Database error"}

    finally:
        cursor.close()
        release_connection(conn)

def delete_user_by_id(user_id: int) -> dict:
    """Delete a user from the database using their ID"""
    conn = get_sql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id,))
        deleted_id = cursor.fetchone()

        if not deleted_id:
            return {"error": "User not found"}

        conn.commit()
        return {"message": f"User with ID {user_id} deleted successfully"}

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}

    finally:
        cursor.close()
        release_connection(conn)
