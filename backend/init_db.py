import mysql.connector
from mysql.connector import Error


def init_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='26210'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS yudada CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("Database yudada created/verified")

            cursor.execute("USE yudada")

            # Drop all tables in reverse dependency order
            tables = [
                "export_files", "quality_scores", "review_issues", "shots",
                "beats", "scenes", "scripts", "story_events", "locations",
                "relationships", "characters", "chapters", "source_documents",
                "tasks", "projects",
            ]
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print("Old tables dropped")

            cursor.close()
            connection.close()
            print("Database initialized successfully")

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    init_database()
