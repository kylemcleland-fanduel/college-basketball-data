import os


def find_most_recent_export(file_folder, file_prefix):
    matching_files = []
    for root, dirs, files in os.walk(file_folder):
        for name in files:
            if name.startswith(file_prefix):
                matching_files.append(name)

    return os.path.join(file_folder, matching_files[-1])
