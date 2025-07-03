import os
import sqlite3

def delete_all_data():
    try:
        # Connect to the database
        conn = sqlite3.connect('faces.db')
        cursor = conn.cursor()

        # Delete all records from the 'persons' table
        cursor.execute("DELETE FROM persons")

        # Commit the changes
        conn.commit()

        # Remove all images from the 'registered_faces' directory
        registered_faces_dir = "registered_faces"
        if os.path.exists(registered_faces_dir):
            for file_name in os.listdir(registered_faces_dir):
                file_path = os.path.join(registered_faces_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        # Close the database connection
        conn.close()

        print("[SUCCESS] All data deleted: IDs, names, crimes, and photos removed.")

    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")

# Run the function to delete all data
delete_all_data()
