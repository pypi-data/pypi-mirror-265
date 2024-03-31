import os
import requests
import platform
import shutil







def init(path): #path of your folder where you want to use(with username) like C:/Users/{your username}/(OneDrive/Desktop/{your folder name}/) or /home/{your username}/(Desktop/app/)
    user = get_username()
    if platform.system() == 'Windows':
        source_dir = f"C:/Users/{user}/zxpm/packages"
        destination_dir = f"{path}/packages/"
    elif platform.system() in ['Linux', 'Darwin']:  # Linux or Mac
        source_dir = f"/home/{user}/zxpm/packages"
        destination_dir = f"{path}"
    
    if os.path.exists(destination_dir):
        return None
    else:
        try:
            os.makedirs(destination_dir)
            print(f"Created directory: {destination_dir}")
        except OSError as e:
            print(f"Error creating directory: {destination_dir}")
            print(e)


    # Get a list of all .py files in the source directory
    py_files = [file for file in os.listdir(source_dir) if file.endswith('.py')]

    # Copy or move each .py file to the destination directory
    for file in py_files:
        source_file_path = os.path.join(source_dir, file)
        destination_file_path = os.path.join(destination_dir, file)
        shutil.copy(source_file_path, destination_file_path)  # or shutil.move() for moving











































































































































def get_username():
    if platform.system() == 'Windows':
        return os.getenv('USERNAME')
    else:
        return os.getenv('USER')

def download_package(url, package_name, version, output_dir):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        filename = f"{package_name}-{version}.zip"
        file_path = os.path.join(output_dir, filename)

        if os.path.exists(file_path):
            overwrite = input(f"The file '{filename}' already exists. Do you want to overwrite it? (y/n): ")
            if overwrite.lower() != 'y':
                print("Download aborted by user.")
                return False, None

        os.makedirs(output_dir, exist_ok=True)

        with open(file_path, 'wb') as file:
            total_length = response.headers.get('content-length')
            if total_length is None:
                file.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    file.write(data)
                    done = int(50 * dl / total_length)
                    print(f"\rDownloading [{done*'='}{(50-done)*' '}] {dl}/{total_length} bytes", end='', flush=True)

        print(f"\nPackage {package_name}-{version} downloaded successfully to {file_path}")
        return True, file_path

    except Exception as e:
        print(f"\nFailed to download package: {e}")
        return False, None

def main():
    print("\033[1m--- ZHRXXgroup Package Downloader ---\033[0m")
    url = input("Enter the URL of the package to download: ")
    package_name = input("Enter the name of the package: ")
    version = input("Enter the version of the package: ")

    username = get_username()
    if platform.system() == 'Windows':
        output_dir = f"C:/Users/{username}/zxpm/packages"
    elif platform.system() in ['Linux', 'Darwin']:  # Linux or Mac
        output_dir = f"/home/{username}/zxpm/packages"
    else:
        print("Unsupported operating system.")
        return

    # Check if the directory exists before creating it
    if os.path.exists(output_dir):
        print(f"Directory already exists: {output_dir}")
    else:
        try:
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        except OSError as e:
            print(f"Error creating directory: {output_dir}")
            print(e)

    success, file_path = download_package(url, package_name, version, output_dir)
    if success:
        print("Download completed successfully!")
    else:
        print("Download failed. Please check the error messages.")

if __name__ == "__main__":
    main()
