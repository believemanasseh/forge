import os
import shutil


def create_zip_file(temp_dir: str, project_name: str) -> str:
    """Creates a zip file of the project.

    Args:
        temp_dir (str): The temporary directory containing the project files.
        project_name (str): The name of the project to be zipped.

    Returns:
        str: The path to the created zip file.
    """
    os.path.join(temp_dir, f"{project_name}.zip")
    return shutil.make_archive(
        os.path.join(temp_dir, project_name), "zip", temp_dir, project_name
    )


def move_zip_file(zip_path: str, directory: str, project_name: str) -> str:
    """Moves the zip file to the specified directory.

    Args:
        zip_path (str): The path to the zip file.
        project_name (str): The name of the project.

    Returns:
        str: The path to the moved zip file in the /tmp directory.

    Raises:
        OSError: If the /tmp directory does not exist or if the move operation fails.
    """
    # Move zip file to /tmp directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    final_zip_path = os.path.join(directory, f"{project_name}.zip")
    shutil.move(zip_path, final_zip_path)
    return final_zip_path
