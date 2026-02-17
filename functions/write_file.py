import os

def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))
        valid_target_dir = os.path.commonpath([working_directory_abs, file_path_abs]) == working_directory_abs
        if not valid_target_dir:
            raise Exception(f'Cannot list "{file_path}" as it is outside the permitted working directory')

        if os.path.isdir(file_path_abs):
            raise Exception(f'Cannot write to "{file_path}" as it is a directory')

        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

        with open(file_path_abs, "w") as f:
            f.write(content + "\n")

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        raise Exception("Error: ", e)