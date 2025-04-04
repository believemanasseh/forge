import os
import shutil
import subprocess
import tempfile

from uagents import Context

from src.dataclasses import ViteConfig
from src.utils import create_zip_file, move_zip_file


def scaffold_django(
    ctx: Context,
    project_name: str = "myproject",
) -> str | None:
    """Scaffolds a Django project and returns the path to the zipped project.

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
        ctx.logger.info("requirements.txt created successfully.")

        # Create zip file
        zip_path = create_zip_file(temp_dir, project_name)
        directory = "/tmp"
        final_zip_path = move_zip_file(zip_path, directory, project_name)
        ctx.logger.info(f"Project zipped successfully: {final_zip_path}")

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


def scaffold_vite(ctx: Context, config: ViteConfig) -> str | None:
    """Scaffolds a project using Vite and returns the path to the zipped project.
    Supports various templates/frameworks including React, Vue, Svelte, Preact, Solid, Svelte, Qwik, Lit and Vanilla JavaScript/TypeScript.

    Args:
        ctx (Context): The agent context object
        config (ViteConfig): Configuration object containing project settings
                            including template choice and package manager

    Returns:
        str | None: Path to the zipped project if successful, None otherwise
    """
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Create app using Vite
        em_dashes = "--" if config.package_manager == "npm" else ""
        subprocess.run(
            f"{config.package_manager} create vite@latest {config.project_name} {em_dashes} --template {config.template}",
            shell=True,
            check=True,
            cwd=temp_dir,
        )
        ctx.logger.info("Vite project created successfully.")

        # Create zip file
        zip_path = create_zip_file(temp_dir, config.project_name)
        directory = "/tmp"
        final_zip_path = move_zip_file(zip_path, directory, config.project_name)
        ctx.logger.info(f"Project zipped successfully: {final_zip_path}")

        return final_zip_path

    except subprocess.CalledProcessError as e:
        ctx.logger.error(f"Command failed: {str(e)}")
        return None
    except Exception as e:
        ctx.logger.error(f"Error creating Vite project: {str(e)}")
        return None
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
