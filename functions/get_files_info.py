import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not os.path.isdir(target_dir):
            raise Exception(f'Error: "{directory}" is not a directory')

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        result = []

        for name in os.listdir(target_dir):
            path = os.path.join(target_dir, name)
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)

            result.append(f"{name} : file_size={file_size}, is_dir={is_dir}")

        return "\n".join(result)
    except Exception as e:
        raise Exception(f"Error: {e}")
