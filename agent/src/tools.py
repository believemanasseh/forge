import os
import shutil
import subprocess
import tempfile

from uagents import Context


def scaffold_django(
    ctx: Context,
    project_name: str = "myproject",
) -> str | None:
    """
    Scaffolds a Django project and returns the path to the zipped project.

    Args:
        ctx (Context): The agent context object
        project_name (str, optional): Name of the Django project. Defaults to "myproject"

    Returns:
        str | None: Path to the zipped project if successful, None otherwise
    """
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Create virtual environment
        venv_path = os.path.join(temp_dir, "venv")
        subprocess.run(f"python3 -m venv {venv_path}", shell=True, check=True)

        # Get path to pip and python in virtual environment
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")

        # Install Django
        subprocess.run(f"{pip_path} install django", shell=True, check=True)
        ctx.logger.info("Django installed successfully.")

        project_path = os.path.join(temp_dir, project_name)
        if os.path.exists(project_path):
            ctx.logger.error(
                f"Project '{project_name}' already exists at {project_path}"
            )
            return None

        # Create Django project
        try:
            os.chdir(temp_dir)
            subprocess.run(
                f"{python_path} -m django startproject {project_name}",
                shell=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr:
                ctx.logger.error(f"Project '{project_name}' already exists")
            else:
                ctx.logger.error(f"Failed to create project: {e.stderr}")
            return None

        # Create requirements.txt
        subprocess.run(f"{pip_path} freeze > requirements.txt", shell=True, check=True)

        # Create zip file
        zip_path = os.path.join(temp_dir, f"{project_name}.zip")
        shutil.make_archive(
            os.path.join(temp_dir, project_name), "zip", temp_dir, project_name
        )

        # Move zip file to /tmp directory
        if not os.path.exists("/tmp"):
            os.makedirs("/tmp")
        final_zip_path = os.path.join("/tmp", f"{project_name}.zip")
        shutil.move(zip_path, final_zip_path)

        return final_zip_path

    except subprocess.CalledProcessError as e:
        ctx.logger.error(f"Command failed: {str(e)}")
        return None
    except Exception as e:
        ctx.logger.error(f"Error creating Django project: {str(e)}")
        return None
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def scaffold_react():
    # TODO: Implement React scaffolding
    pass


def scaffold_vue():
    # TODO: Implement Vue scaffolding
    pass
