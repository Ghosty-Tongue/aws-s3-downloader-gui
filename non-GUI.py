import os
import configparser
from module.download_bucket_public import download_bucket_public
from module.download_bucket_auth import download_bucket_auth
from download_bucket_obj import Bucket
from requests.exceptions import ChunkedEncodingError, ConnectionError, RequestException
import tqdm
import joblib
import boto

class S3Downloader:
    def __init__(self):
        self.load_config()

    def load_config(self):
        self.config_file = "config.ini"
        self.config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            self.last_output_folder = self.config.get("Settings", "LastOutputFolder")
        else:
            self.last_output_folder = ""
            self.save_config()

    def save_config(self):
        self.config["Settings"] = {"LastOutputFolder": self.last_output_folder}
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def download_public_bucket(self):
        bucket_name = input("Enter the name of the public bucket: ")
        url = input("Enter the URL of the public bucket: ")
        output_folder = input("Enter the output folder path: ")
        self.last_output_folder = output_folder

        bucket = Bucket(
            bucket_name=bucket_name,
            url=url,
            download=True,
            download_include=[],
            download_exclude=[],
            get_xml=False,
            output_folder=output_folder,
            aws_access_key=None,
            aws_secret_key=None,
            quiet=False,
            last_key=None
        )

        last_key = None
        while True:
            try:
                bucket.last_key = last_key
                last_key = download_bucket_public(bucket)
                if last_key is None:
                    break  # Download complete
            except (ChunkedEncodingError, ConnectionError, RequestException) as e:
                print(f"An error occurred while downloading. Error: {str(e)}. Retrying...")
                continue

        print("Public bucket download complete.")
        self.save_config()

    def download_authenticated_bucket(self):
        bucket_name = input("Enter the name of the authenticated bucket: ")
        url = input("Enter the URL of the authenticated bucket: ")
        access_key = input("Enter your access key: ")
        secret_key = input("Enter your secret key: ")
        output_folder = input("Enter the output folder path: ")
        self.last_output_folder = output_folder

        if not access_key or not secret_key:
            print("Please enter access key and secret key.")
            return

        bucket = Bucket(
            bucket_name=bucket_name,
            url=url,
            download=True,
            download_include=[],
            download_exclude=[],
            get_xml=False,
            output_folder=output_folder,
            aws_access_key=access_key,
            aws_secret_key=secret_key,
            quiet=False,
            last_key=None
        )

        last_key = None
        while True:
            try:
                bucket.last_key = last_key
                last_key = download_bucket_auth(bucket)
                if last_key is None:
                    break  # Download complete
            except (ChunkedEncodingError, ConnectionError, RequestException) as e:
                print(f"An error occurred while downloading. Error: {str(e)}. Retrying...")
                continue

        print("Authenticated bucket download complete.")
        self.save_config()

if __name__ == "__main__":
    downloader = S3Downloader()
    bucket_type = input("Enter 'public' for a public bucket or 'authenticated' for an authenticated bucket: ")
    if bucket_type.lower() == "public":
        downloader.download_public_bucket()
    elif bucket_type.lower() == "authenticated":
        downloader.download_authenticated_bucket()
    else:
        print("Invalid input. Please enter 'public' or 'authenticated'.")
