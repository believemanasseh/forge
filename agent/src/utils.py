import os
import shutil

import boto3
from botocore.exceptions import ClientError
from uagents import Context


def create_zip_file(ctx: Context, temp_dir: str, project_name: str) -> str:
    """Creates a zip file of the project.

    Args:
        ctx (Context): The agent context object.
        temp_dir (str): The temporary directory containing the project files.
        project_name (str): The name of the project to be zipped.

    Returns:
        str: The path to the created zip file.

    Raises:
        OSError: If the zip file creation fails.
    """
    try:
        os.path.join(temp_dir, f"{project_name}.zip")
        return shutil.make_archive(
            os.path.join(temp_dir, project_name), "zip", temp_dir, project_name
        )
    except OSError as e:
        ctx.logger.error(f"Failed to create zip file: {e}")
        raise


def move_zip_file(
    ctx: Context, zip_path: str, directory: str, project_name: str
) -> str:
    """Moves the zip file to the specified directory.

    Args:
        ctx (Context): The agent context object.
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
        ctx.logger.error(f"Failed to move zip file: {e}")
        raise


def upload_to_s3(ctx: Context, file_path: str, file_name: str) -> str:
    """Upload a file to an S3 bucket and return the public URL.

    Args:
        ctx (Context): The agent context object.
        file_path (str): File to upload.
        file_name (str): S3 object file name.

    Returns:
        str: Public URL of the uploaded file if successful.

    Raises:
        ClientError: If the upload fails.
    """
    session = boto3.Session()
    s3_client = session.client(service_name="s3")

    try:
        bucket = "forge-projects"
        object_name = f"projects/{file_name}.zip"
        s3_client.upload_file(
            file_path, bucket, object_name, ExtraArgs={"ACL": "public-read"}
        )
        url = f"https://{bucket}.s3.amazonaws.com/{object_name}"
        ctx.logger.info(f"{url} uploaded to S3")
        return url
    except ClientError as e:
        ctx.logger.error(f"Error uploading to S3: {e}")
        raise
