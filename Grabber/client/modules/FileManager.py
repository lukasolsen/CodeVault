import os
import shutil


def find_everyfile_extension(extension, source_path, target_path):
    for root, _, files in os.walk(source_path):
        for file in files:
            if file.endswith(extension):
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_path, file)

                # Create the "Grabbed Files" directory if it doesn't exist
                grabbed_folder = os.path.join(target_path, "Grabbed Files")
                os.makedirs(grabbed_folder, exist_ok=True)

                # Copy the file to the target directory
                try:
                    shutil.copy(source_file_path, os.path.join(
                        grabbed_folder, file))
                except:
                    pass
