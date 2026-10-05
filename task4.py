import os
import shutil
import pyzipper


def zip_fol(folder_path: str, password: str):
    folder_path = os.path.abspath(folder_path.rstrip("/\\"))
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist")
        return

    parent_dir, folder_name = os.path.split(folder_path)
    zip_path = os.path.join(parent_dir, f"{folder_name}.locked.zip")
    print("Locking '{folder_name}'...")

    with pyzipper.AESZipFile(
        zip_path, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zip_file:
        zip_file.setpassword(password.encode("utf-8"))

        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, parent_dir)
                zip_file.write(full_path, arcname=arcname)

    # shutil.rmtree(folder_path) # **Removes the original folder**
    print(f"Locked successfully: {zip_path}")


def unzip_fol(zip_path: str, password: str):
    zip_path = os.path.abspath(zip_path)
    if not os.path.exists(zip_path):
        print(f"File '{zip_path}' does not exist")
        return

    extract_loc = os.path.dirname(zip_path)
    print(f"Unzipping '{os.path.basename(zip_path)}'...")

    try:
        with pyzipper.AESZipFile(zip_path) as zip_file:
            zip_file.setpassword(password.encode("utf-8"))
            zip_file.extractall(extract_loc)

        # os.remove(zip_path) # **Removes the zipped folder**
        print(f"Unzipped successfully to: {extract_loc}")

    except RuntimeError:
        print("An error occured")
    except Exception as e:
        print(f"Failed to unlock: {e}")


def main():
    print("Folder zip program")
    print("Enter 1 to lock\nEnter 2 to unlock")
    a = int(input("Enter your choice: "))

    if a == 1:
        f = input("Enter folder path to zip: ").strip()
        p = input("Enter the password to zip file with: ")
        zip_fol(f, p)

    elif a == 2:
        lf = input("Enter the locked zip file path to unzip: ").strip()
        p = input("Enter password to unzip: ")
        unzip_fol(lf, p)

    else:
        print(f"Invalid input: {a}")


if __name__ == "__main__":
    main()
