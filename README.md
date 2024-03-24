# Purpose
Provide a command line ability to download some, or all, of the public/authorized users files in an AWS S3 bucket as well as all of the XML that lists its contents, whether the key is public or not. Additionally, this now includes a GUI for easier interaction.

# Requirements
Python3 - Thanks to dreamflasher (https://github.com/dreamflasher) for migrating from Python2 to 3!

# Reason
As I was going through, looking for public AWS S3 buckets that contained PII, I realized that I wanted to be able to download the XML and a subset of data to show companies what data they had exposed. I didn't want to do this manually and I wanted to be able to have ALL of the XML (AWS paginates S3 content per 1k keys). The GUI was added to enhance user experience and provide a more intuitive way of interacting with the application.

# Command-line Use
- Just get the XML, downloaded to the working directory under a the subfolder [bucket_name]:  
  - `./download_bucket.py -n [bucket_name] -x`

- Download the whole bucket to a specified location:  
  - `./download_bucket.py -o /home/foo/bar -n [bucket_name] -d`

- Download only where "test" is in the key and get all of the XML:  
  - `./download_bucket.py -n [bucket_name] -d -x -i test`

- Download where "test" is in the key but "exclude me" is not in the key:  
  - `./download_bucket.py -n [bucket_name] -d -i test -e "exclude me"`

- Download everything starting after thisfile.txt on public readable downloads, e.g. if you don't want to paginate through again:  
  - `./download_bucket.py -n [bucket_name] -d --last_key "thisfile.txt"`

- Download using an API key (e.g. for buckets that allow any authenticated user to access it):  
  - `./download_bucket.py -n [bucket_name] -d -ak "AWS_ACCESS_KEY" -sk "AWS_SECRET_KEY"`

# GUI Use
- Run the script and input 1 for public bucket or 2 for authenticated bucket.
- Provide the bucket name, output folder, AWS access key, and AWS secret key in the GUI.
- Click on buttons to select the output folder and start the download process.
  
# Notes
- If a file is private, the download will be the XML saying that file access is denied.
- Some keys are just folder names, these will not be downloaded but the keys within the bucket will (e.g. a key could be "folder/" but there will be keys with content like "folder/file1").
- You can add multiple "-i" or "-e" parameters. Each set of "-i" and "-e" parameters will be OR'd and the "-i" and "-e" parameters are AND'd together. These are case insensitive.

# Additional Notes for GUI
- The GUI allows for a more user-friendly interaction compared to command-line usage.
- It provides input fields and buttons for easy input and selection of parameters.
- Users can navigate through the GUI easily and initiate the download process with a click of a button.
- GUI enhances accessibility and usability, especially for users who are not comfortable with command-line interfaces.
