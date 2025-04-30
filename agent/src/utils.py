import os
import shutil

import boto3
from botocore.exceptions import ClientError
from uagents import Context


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
    try:
        # Move zip file to /tmp directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        final_zip_path = os.path.join(directory, f"{project_name}.zip")
        shutil.move(zip_path, final_zip_path)
        return final_zip_path
    except OSError as e:
        raise OSError(f"Failed to move zip file: {e}") from e


def upload_to_s3(ctx: Context, file_path: str, object_name: str) -> str | None:
    """Upload a file to an S3 bucket and return the public URL.

    Args:
        ctx (Context): The agent context object
        file_path (str): File to upload
        object_name (str): S3 object name.

    Returns:
        str | None: Public URL of the uploaded file if successful, None otherwise

    Raises:
        ClientError: If the upload fails
    """
    session = boto3.Session()
    s3_client = session.client(service_name="s3")

    try:
        bucket = "forge-projects"
        s3_client.upload_file(
            file_path, bucket, object_name, ExtraArgs={"ACL": "public-read"}
        )
        url = f"https://{bucket}.s3.amazonaws.com/projects/{object_name}.zip"
        ctx.logger.info(f"{url} uploaded to S3")
        return url
    except ClientError as e:
        ctx.logger.info(f"Error uploading to S3: {e}")
        return None
