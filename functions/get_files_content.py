import os
from config import CHARACTER_LIMIT

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))
        valid_target_dir = os.path.commonpath([working_directory_abs, file_path_abs]) == working_directory_abs
        if not valid_target_dir:
            raise Exception(f'Cannot list "{file_path_abs}" as it is outside the permitted working directory')

        if not os.path.isfile(file_path_abs):
            raise Exception(f'File not found or is not a regular file: "{file_path_abs}"')

        with open(file_path_abs, "r") as f:
            file_content = f.read(CHARACTER_LIMIT)

            if f.read(1):
                file_content += f'[...File "{file_path_abs}" truncated at {CHARACTER_LIMIT} characters]'

            return file_content
    except Exception as e:
        raise Exception(f"Error: {e}")

