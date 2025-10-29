import os
import shutil


def remove_existing():
    if os.path.exists("./public"):
        shutil.rmtree("./public")


def begin_copy():
    print("Beginning removal of existing public folder...")
    remove_existing()
    print("Checking static...")
    found_items = check_static("./static")
    os.mkdir("./public")
    copy_items(found_items)
    print("Done")


def check_static(current_directory):
    files_list = []
    if os.path.exists(current_directory):
        temp_files_list = os.listdir(current_directory)
        for item in temp_files_list:
            if item:
                if os.path.isfile(os.path.join(current_directory, item)):
                    print(f"Found {item} in {current_directory}")
                    files_list.append(os.path.join(current_directory, item))
                else:
                    print(f"Directoty {item} found in {current_directory}")
                    files_list.extend(
                        check_static(os.path.join(current_directory, item))
                    )
    return files_list


def copy_items(files_to_copy):
    for item in files_to_copy:
        print(f"Currently copying {item}")
        split_item = item.split("/")
        if len(split_item) == 3:
            shutil.copy(item, "./public")
        if len(split_item) == 4:
            new_dest = os.path.join("./public", split_item[2])
            os.mkdir(new_dest)
            shutil.copy(item, new_dest)
