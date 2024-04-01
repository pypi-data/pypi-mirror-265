import os
import shutil
import pandas as pd
import mysql.connector
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import logging
import io
import csv

class GoogleDriveImporter:
    def __init__(self, file_id, create_fresh=False):
        self.file_id = file_id
        self.create_fresh = create_fresh
        self.logger = logging.getLogger(__name__)

    def get_csv_filename(self):
        try:
            service = build('drive', 'v3')
            file_metadata = service.files().get(fileId=self.file_id, fields="name").execute()
            return file_metadata.get('name')
        except Exception as e:
            self.logger.error(f"Error retrieving file metadata: {e}")
            return None

    def download_csv_from_google_drive(self):
        try:
            service = build('drive', 'v3')
            file_metadata = service.files().get(fileId=self.file_id, fields="mimeType").execute()
            mime_type = file_metadata.get('mimeType')

            if mime_type == 'text/csv':
                request = service.files().get_media(fileId=self.file_id)
                downloaded = io.BytesIO()
                downloader = MediaIoBaseDownload(downloaded, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                downloaded.seek(0)
                return io.TextIOWrapper(downloaded, encoding='utf-8')
            else:
                self.logger.error("The file is not a CSV file.")
                return None
        except Exception as e:
            self.logger.error(f"Error downloading CSV from Google Drive: {e}")
            return None

    def load_csv_to_mysql(self, host, dbname, user, password):
        csv_file = self.download_csv_from_google_drive()
        if not csv_file:
            self.logger.error("CSV file download failed. Aborting import.")
            return False

        filename = self.get_csv_filename()
        if not filename:
            self.logger.error("Failed to retrieve CSV file name. Aborting import.")
            return False

        table_name = filename.replace('.csv', '').replace(' ', '_').lower()

        try:
            conn = mysql.connector.connect(host=host, user=user, password=password, database=dbname)
            with conn.cursor() as cursor:
                if self.create_fresh:
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                    conn.commit()

                header = next(csv.reader(csv_file))
                col_str = ", ".join([f"`{col.strip()}` VARCHAR(255)" for col in header])
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({col_str})"
                cursor.execute(create_table_query)
                conn.commit()

                insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s']*len(header))})"
                for row in csv.reader(csv_file):
                    cursor.execute(insert_query, row)
                    conn.commit()

            self.logger.info("Data imported successfully from Google Drive.")
            return True
        except mysql.connector.Error as e:
            self.logger.error(f"MySQL Error: {e}")
            return False
        finally:
            if conn:
                conn.close()

class LocalCSVImporter:
    def __init__(self, folder_path, host, dbname, user, password, create_fresh=False):
        self.folder_path = folder_path
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.create_fresh = create_fresh
        self.dataset_dir = os.path.join(os.getcwd(), 'datasets')

    def configure_dataset_directory(self, csv_files):
        if not os.path.exists(self.dataset_dir):
            try:
                os.makedirs(self.dataset_dir)
            except Exception as e:
                print(f"Error creating dataset directory: {e}")
                return False

        for csv in csv_files:
            src_file = os.path.join(self.folder_path, csv)
            dst_file = os.path.join(self.dataset_dir, csv)
            try:
                shutil.copy(src_file, dst_file)
                print(f"Copied {csv} to datasets folder")
            except Exception as e:
                print(f"Error copying {csv}: {e}")
                return False

        return True

    def create_df(self, csv_files):
        data_path = os.path.join(os.getcwd(), self.dataset_dir)
        df = {}
        for file in csv_files:
            try:
                file_path = os.path.join(data_path, file)
                df[file] = pd.read_csv(file_path)
            except UnicodeDecodeError:
                file_path = os.path.join(data_path, file)
                df[file] = pd.read_csv(file_path, encoding="ISO-8859-1")
            print(file)
        return df

    def clean_tbl_name(self, filename):
        clean_tbl_name = filename.lower().replace(" ", "").replace("-", "_").replace(r"/", "_").replace("\\", "_").replace("$", "").replace("%", "")
        tbl_name = '{0}'.format(clean_tbl_name.split('.')[0])
        return tbl_name

    def clean_colname(self, dataframe):
        dataframe.columns = [x.lower().replace(" ", "_").replace("-", "_").replace(r"/", "_").replace("\\", "_").replace(".", "_").replace("$", "").replace("%", "") for x in dataframe.columns]
        dataframe.columns = [x if x != 'rank' else 'rank_column' for x in dataframe.columns]
        replacements = {
            'timedelta64[ns]': 'varchar(255)',
            'object': 'varchar(255)',
            'float64': 'float',
            'int64': 'int',
            'datetime64': 'datetime'
        }
        col_str = ", ".join("`{}` {}".format(n, d) for (n, d) in zip(dataframe.columns, dataframe.dtypes.replace(replacements)))
        return col_str, dataframe.columns

    def create_table(self, tbl_name, col_str):
        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.dbname)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS {} ({});".format(tbl_name, col_str))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print("MySQL Error:", e.msg)
            return False

    def drop_table(self, tbl_name):
        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.dbname)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS {};".format(tbl_name))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print("MySQL Error:", e.msg)
            return False

    def insert_into_table(self, tbl_name, dataframe):
        try:
            conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.dbname)
            cursor = conn.cursor()
            dataframe = dataframe.where(pd.notnull(dataframe), -1)
            values = dataframe.values.tolist()
            placeholders = ', '.join(['%s'] * len(dataframe.columns))
            columns_str = ', '.join(['`{}`'.format(col) for col in dataframe.columns])
            insert_query = "INSERT INTO {} ({}) VALUES ({});".format(tbl_name, columns_str, placeholders.replace('?', '%s'))
            cursor.executemany(insert_query, values)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print("MySQL Error:", e.msg)
            return False

    def import_csv_to_mysql(self):
        csv_files = [file for file in os.listdir(self.folder_path) if file.endswith(".csv")]

        if not csv_files:
            print("No CSV files found in the selected folder.")
            return False

        if not self.configure_dataset_directory(csv_files):
            print("Error configuring dataset directory.")
            return False

        df = self.create_df(csv_files)

        for k, v in df.items():
            tbl_name = self.clean_tbl_name(k)
            col_str, _ = self.clean_colname(v)

            if self.create_fresh:
                drop_table_status = self.drop_table(tbl_name)
                if not drop_table_status:
                    print(f"Error dropping table {tbl_name}.")
                    return False

                create_table_status = self.create_table(tbl_name, col_str)
                if not create_table_status:
                    print(f"Error creating table {tbl_name}.")
                    return False

                insert_into_table_status = self.insert_into_table(tbl_name, v)
                if not insert_into_table_status:
                    print(f"Error inserting into table {tbl_name}.")
                    return False
            else:
                create_table_status = self.create_table(tbl_name, col_str)
                if not create_table_status:
                    print(f"Error creating table {tbl_name}.")
                    return False

                insert_into_table_status = self.insert_into_table(tbl_name, v)
                if not insert_into_table_status:
                    print(f"Error inserting into table {tbl_name}.")
                    return False

        return True


