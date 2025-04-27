import os
import shutil
import subprocess
import tempfile

from uagents import Context

from src.config import get_config
from src.dataclasses import ViteConfig
from src.utils import create_zip_file, move_zip_file, upload_to_s3

config = get_config()


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

        project_name = project_name.replace(" ", "-")

        # Create virtual environment
        venv_path = os.path.join(temp_dir, "venv")
        subprocess.run(
            f"python3 -m venv {venv_path}",
            shell=True,
            check=True,
            env={"PATH": f"{os.environ['PATH']}:/usr/bin"},
        )

        # Get path to pip and python in virtual environment
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")

        # Install Django
        subprocess.run(
            f"{pip_path} install django", shell=True, check=True, cwd=temp_dir
        )
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

        s3_url = upload_to_s3(
            ctx, final_zip_path, "forge-projects", f"projects/{project_name}.zip"
        )
        if not s3_url:
            return None

        ctx.logger.info(f"Project uploaded successfully: {s3_url}")
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
            ctx.logger.info(f"Cleaned up temp direcotry: {temp_dir}")

        # Clean up zip file
        if final_zip_path and os.path.exists(final_zip_path):
            os.remove(final_zip_path)
            ctx.logger.info(f"Cleaned up zip file: {final_zip_path}")

    return s3_url


def scaffold_vite(ctx: Context, vite_config: ViteConfig) -> str | None:
    """Scaffolds a project using Vite and returns the path to the zipped project.
    Supports various templates/frameworks including React, Vue, Svelte, Preact, Solid, Svelte, Qwik, Lit and Vanilla JavaScript/TypeScript.

    Args:
        ctx (Context): The agent context object
        vite_config (ViteConfig): Configuration object containing project settings
                            including template choice and package manager

    Returns:
        str | None: Path to the zipped project if successful, None otherwise
    """
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        project_name = vite_config.project_name.replace(" ", "-")

        # Create app using Vite
        em_dashes = "--" if vite_config.package_manager == "npm" else ""
        subprocess.run(
            f"{vite_config.package_manager} create vite{'@latest' if vite_config.package_manager == 'npm' else ''} {project_name} {em_dashes} --template {vite_config.template}",
            shell=True,
            check=True,
            cwd=temp_dir,
            env={
                "PATH": f"{os.environ['PATH']}:{config.NODE_PATH}:/usr/local/bin:/usr/bin",
            },
        )
        ctx.logger.info("Vite project created successfully.")

        # Create zip file
        zip_path = create_zip_file(temp_dir, vite_config.project_name)
        directory = "/tmp"
        final_zip_path = move_zip_file(zip_path, directory, vite_config.project_name)
        ctx.logger.info(f"Project zipped successfully: {final_zip_path}")

        s3_url = upload_to_s3(
            ctx,
            final_zip_path,
            "forge-projects",
            f"projects/{vite_config.project_name}.zip",
        )
        if not s3_url:
            return None

        ctx.logger.info(f"Project uploaded successfully: {s3_url}")
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
            ctx.logger.info(f"Cleaned up temp direcotry: {temp_dir}")

        # Clean up zip file
        if final_zip_path and os.path.exists(final_zip_path):
            os.remove(final_zip_path)
            ctx.logger.info(f"Cleaned up zip file: {final_zip_path}")

    return s3_url


def scaffold_laravel(ctx: Context, project_name: str = "myproject") -> str | None:
    """Scaffolds a Laravel project with Composer and returns the path to the zipped project.

    Args:
        ctx (Context): The agent context object
        project_name (str, optional): Name of the PHP project. Defaults to "myproject"

    Returns:
        str | None: Path to the zipped project if successful, None otherwise
    """
    try:
        temp_dir = tempfile.mkdtemp()

        project_name = project_name.replace(" ", "-")

        # Set environment variables for Composer
        env = os.environ.copy()
        env.update(
            {
                "HOME": config.HOME_PATH,
                "PATH": f"{env['PATH']}:/usr/local/bin:/usr/bin",
            }
        )

        # Create project using Composer
        subprocess.run(
            f"composer create-project --prefer-dist laravel/laravel {project_name}",
            shell=True,
            check=True,
            cwd=temp_dir,
            env=env,
        )
        ctx.logger.info("Laravel project created successfully.")

        # Create zip file
        zip_path = create_zip_file(temp_dir, project_name)
        directory = "/tmp"
        final_zip_path = move_zip_file(zip_path, directory, project_name)
        ctx.logger.info(f"Project zipped successfully: {final_zip_path}")

        s3_url = upload_to_s3(
            ctx, final_zip_path, "forge-projects", f"projects/{project_name}.zip"
        )
        if not s3_url:
            return None

        ctx.logger.info(f"Project uploaded successfully: {s3_url}")
    except Exception as e:
        ctx.logger.error(f"Error creating Laravel project: {str(e)}")
        return None
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            ctx.logger.info(f"Cleaned up temp direcotry: {temp_dir}")

        # Clean up zip file
        if final_zip_path and os.path.exists(final_zip_path):
            os.remove(final_zip_path)
            ctx.logger.info(f"Cleaned up zip file: {final_zip_path}")

    return s3_url


def scaffold_rails(ctx: Context, project_name: str = "myproject") -> str | None:
    """Scaffolds a Ruby on Rails project and returns the path to the zipped project.

    Args:
        ctx (Context): The agent context object
        project_name (str, optional): Name of the Rails project. Defaults to "myproject"

    Returns:
        str | None: Path to the zipped project if successful, None otherwise
    """
    try:
        temp_dir = tempfile.mkdtemp()

        project_name = project_name.replace(" ", "-")

        env = os.environ.copy()
        env.update(
            {
                "GEM_HOME": config.GEM_HOME,
                "GEM_PATH": config.GEM_PATH,
                "PATH": f"{env['PATH']}:{config.RUBY_PATH}",
            }
        )

        # Create Rails project
        subprocess.run(
            f"rails new {project_name}", shell=True, check=True, cwd=temp_dir, env=env
        )
        ctx.logger.info("Rails project created successfully.")

        # Create zip file
        zip_path = create_zip_file(temp_dir, project_name)
        directory = "/tmp"
        final_zip_path = move_zip_file(zip_path, directory, project_name)
        ctx.logger.info(f"Project zipped successfully: {final_zip_path}")

        s3_url = upload_to_s3(
            ctx, final_zip_path, "forge-projects", f"projects/{project_name}.zip"
        )
        if not s3_url:
            return None

        ctx.logger.info(f"Project uploaded successfully: {s3_url}")
    except Exception as e:
        ctx.logger.error(f"Error creating Rails project: {str(e)}")
        return None
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            ctx.logger.info(f"Cleaned up temp direcotry: {temp_dir}")

        # Clean up zip file
        if final_zip_path and os.path.exists(final_zip_path):
            os.remove(final_zip_path)
            ctx.logger.info(f"Cleaned up zip file: {final_zip_path}")

    return s3_url
