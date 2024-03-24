import os
import tkinter as tk
from tkinter import filedialog, messagebox
import configparser
from module.download_bucket_public import download_bucket_public
from module.download_bucket_auth import download_bucket_auth
from download_bucket_obj import Bucket

class S3DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AWS S3 Downloader")
        
        self.load_config()
        self.create_main_gui()

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

    def create_main_gui(self):
        self.clear_gui()
        
        self.bucket_type_var = tk.IntVar()
        tk.Label(self.root, text="Select bucket type:").pack()

        tk.Radiobutton(self.root, text="Public Bucket", variable=self.bucket_type_var, value=1).pack(anchor=tk.W)
        tk.Radiobutton(self.root, text="Authenticated Bucket", variable=self.bucket_type_var, value=2).pack(anchor=tk.W)

        tk.Button(self.root, text="Select", command=self.select_bucket_type).pack()

    def select_bucket_type(self):
        bucket_type = self.bucket_type_var.get()
        if bucket_type == 1:  # Public bucket
            self.create_public_bucket_gui()
        elif bucket_type == 2:  # Authenticated bucket
            self.create_authenticated_bucket_gui()

    def create_public_bucket_gui(self):
        self.clear_gui()

        self.bucket_name_var = tk.StringVar()
        self.output_folder_var = tk.StringVar(value=self.last_output_folder)
        self.url_var = tk.StringVar()

        tk.Label(self.root, text="Bucket Name:").pack()
        tk.Entry(self.root, textvariable=self.bucket_name_var).pack()

        tk.Label(self.root, text="Bucket URL:").pack()
        tk.Entry(self.root, textvariable=self.url_var).pack()

        tk.Label(self.root, text="Output Folder:").pack()
        output_folder_frame = tk.Frame(self.root)
        output_folder_frame.pack()
        tk.Entry(output_folder_frame, textvariable=self.output_folder_var).pack(side=tk.LEFT)
        tk.Button(output_folder_frame, text="...", command=self.select_output_folder).pack(side=tk.LEFT)

        tk.Button(self.root, text="Download", command=self.download_public_bucket).pack()

    def create_authenticated_bucket_gui(self):
        self.clear_gui()

        self.bucket_name_var = tk.StringVar()
        self.output_folder_var = tk.StringVar(value=self.last_output_folder)
        self.url_var = tk.StringVar()
        self.access_key_var = tk.StringVar()
        self.secret_key_var = tk.StringVar()

        tk.Label(self.root, text="Bucket Name:").pack()
        tk.Entry(self.root, textvariable=self.bucket_name_var).pack()

        tk.Label(self.root, text="Bucket URL:").pack()
        tk.Entry(self.root, textvariable=self.url_var).pack()

        tk.Label(self.root, text="Access Key:").pack()
        tk.Entry(self.root, textvariable=self.access_key_var).pack()

        tk.Label(self.root, text="Secret Key:").pack()
        tk.Entry(self.root, textvariable=self.secret_key_var).pack()

        tk.Label(self.root, text="Output Folder:").pack()
        output_folder_frame = tk.Frame(self.root)
        output_folder_frame.pack()
        tk.Entry(output_folder_frame, textvariable=self.output_folder_var).pack(side=tk.LEFT)
        tk.Button(output_folder_frame, text="...", command=self.select_output_folder).pack(side=tk.LEFT)

        tk.Button(self.root, text="Download", command=self.download_authenticated_bucket).pack()

    def download_public_bucket(self):
        bucket_name = self.bucket_name_var.get()
        url = self.url_var.get()
        output_folder = self.output_folder_var.get()
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
        download_bucket_public(bucket)
        messagebox.showinfo("Download Complete", "Public bucket download complete.")
        self.save_config()

    def download_authenticated_bucket(self):
        bucket_name = self.bucket_name_var.get()
        url = self.url_var.get()
        access_key = self.access_key_var.get()
        secret_key = self.secret_key_var.get()
        output_folder = self.output_folder_var.get()
        self.last_output_folder = output_folder

        if not access_key or not secret_key:
            messagebox.showerror("Error", "Please enter access key and secret key.")
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
       
    def clear_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_var.set(folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = S3DownloaderApp(root)
    root.mainloop()
