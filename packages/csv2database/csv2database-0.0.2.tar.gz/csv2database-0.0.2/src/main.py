import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\import_csv_to_mysql\beginest-service-account-key.json"
from csv_to_mysql_importer.csv_import import LocalCSVImporter, GoogleDriveImporter

def main():

    # Call the import_csv_to_mysql function for local CSV files
    local_folder_path = r"D:\MY Datasets"  # Use raw string for Windows file paths
    success_local = LocalCSVImporter(local_folder_path, "localhost", "my_database", "root", "Arfaan@123456", create_fresh=False).import_csv_to_mysql()
    if success_local:
        print("Local CSV files imported successfully.")
    else:
        print("Error importing local CSV files.")

    # Call the load_csv_to_mysql function for Google Drive file
    google_drive_file_id = "1RvpZBm6vWZE9V4V8TWwM26IZsdWnzOyg"
    success_google_drive = GoogleDriveImporter(google_drive_file_id,create_fresh=False).load_csv_to_mysql("localhost", "my_database", "root", "Arfaan@123456")
    if success_google_drive:
        print("Google Drive CSV file imported successfully.")
    else:
        print("Error importing Google Drive CSV file.")

if __name__ == "__main__":
    main()
