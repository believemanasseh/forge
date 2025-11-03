import os
import shutil
import subprocess
import tempfile

from uagents import Context

from src.config import get_config
from src.dataclasses import ComposerConfig, ViteConfig
from src.utils import create_zip_file, move_zip_file, upload_to_s3

config = get_config()


def scaffold_django(ctx: Context, project_name: str = "myproject") -> str:
    """Scaffolds a Django project and returns the path to the zipped project.

    Args:
        ctx (Context): The agent context object.
        project_name (str, optional): Name of the Django project. Defaults to "myproject".

    Returns:
        str: Path to the zipped project.

    Raises:
        OSError: If the /tmp directory does not exist or if the move operation fails.
        subprocess.CalledProcessError: If the command to create the Django project fails.
        Exception: If any error occurs during the project creation or zipping process.
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

        # Create Django project
        subprocess.run(
            f"{python_path} -m django startproject {project_name}",
            shell=True,
            check=True,
            cwd=temp_dir,
        )

        # Create requirements.txt
        subprocess.run(
            f"{pip_path} freeze > requirements.txt",
            shell=True,
            check=True,
            cwd=temp_dir,
        )
        ctx.logger.info("requirements.txt created successfully.")

        # Create zip file
        zip_path = create_zip_file(ctx, temp_dir, project_name)
        directory = "/tmp"
        final_zip_path = move_zip_file(ctx, zip_path, directory, project_name)
        ctx.logger.info(f"Project zipped successfully: {final_zip_path}")

        s3_url = upload_to_s3(ctx, final_zip_path, project_name)
        ctx.logger.info(f"Project uploaded successfully: {s3_url}")
    except OSError as e:
        ctx.logger.error(f"Filesystem operation failed: {str(e)}")
        raise
    except subprocess.CalledProcessError as e:
        ctx.logger.error(f"Subprocess command failed: {str(e)}")
        raise
    except Exception as e:
        ctx.logger.error(f"Error creating Django project: {str(e)}")
        raise
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
        ctx (Context): The agent context object.
        vite_config (ViteConfig): Configuration object containing project settings
                            including template choice and package manager.

    Returns:
        str: Path to the zipped project

    Raises:
        OSError: If the /tmp directory does not exist or if the move operation fails.
        subprocess.CalledProcessError: If the command to create the Vite project fails.
        Exception: If any error occurs during the project creation or zipping process.
    """
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        project_name = vite_config.project_name.replace(" ", "-")

        # Create app using Vite
        em_dashes = "--" if vite_config.package_manager == "npm" else ""
        subprocess.run(
            f"no '' | {vite_config.package_manager} create vite{'@latest' if vite_config.package_manager == 'npm' else ''} {project_name} {em_dashes} --template {vite_config.template} --no-rolldown",
            shell=True,
            check=True,
            cwd=temp_dir,
            env={
                "PATH": f"{os.environ['PATH']}:{config.NODE_PATH}:/usr/local/bin:/usr/bin",
            },
        )
        ctx.logger.info("Vite project created successfully.")

        # Create zip file
        zip_path = create_zip_file(ctx, temp_dir, vite_config.project_name)
        directory = "/tmp"
        final_zip_path = move_zip_file(
            ctx, zip_path, directory, vite_config.project_name
        )
        ctx.logger.info(f"Project zipped successfully: {final_zip_path}")

        s3_url = upload_to_s3(ctx, final_zip_path, vite_config.project_name)
        ctx.logger.info(f"Project uploaded successfully: {s3_url}")
    except OSError as e:
        ctx.logger.error(f"Filesystem operation failed: {str(e)}")
        raise
    except subprocess.CalledProcessError as e:
        ctx.logger.error(f"Subprocess command failed: {str(e)}")
        raise
    except Exception as e:
        ctx.logger.error(f"Error creating Vite project: {str(e)}")
        raise
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


def scaffold_composer(ctx: Context, composer_config: ComposerConfig) -> str:
    """Scaffolds various PHP projects using Composer and returns the path to the zipped project.

    Args:
        ctx (Context): The agent context object.
        composer_config (ComposerConfig): Configuration object for the PHP project.

    Returns:
        str: Path to the zipped project.

    Raises:
        OSError: If the /tmp directory does not exist or if the move operation fails.
        subprocess.CalledProcessError: If the command to create the Composer project fails.
        Exception: If any error occurs during the project creation or zipping process.
    """
    try:
        temp_dir = tempfile.mkdtemp()

        project_name = composer_config.project_name.replace(" ", "-")

        # Set environment variables for Composer
        env = os.environ.copy()
        env.update(
            {
                "HOME": config.HOME_PATH,
                "PATH": f"{env['PATH']}:/usr/local/bin:/usr/bin",
            }
        )

        # Create commands for different project types
        create_commands = {
            "laravel": f"composer create-project --prefer-dist laravel/laravel {project_name}",
            "symfony": f"composer create-project symfony/skeleton {project_name}",
            "drupal": f"composer create-project drupal/recommended-project {project_name}",
            "wordpress": f"composer create-project roots/bedrock {project_name}",
            "cakephp": f"composer create-project --prefer-dist cakephp/app {project_name}",
            "phpbb": f"composer create-project phpbb/phpbb {project_name}",
            "magento": f"composer create-project --repository-url=https://repo.magento.com/ magento/project-community-edition {project_name}",
            "joomla": f"composer create-project joomla/joomla-cms {project_name}",
            "octobercms": f"composer create-project october/october {project_name}",
            "silverstripe": f"composer create-project silverstripe/installer {project_name}",
        }

        # Create project using Composer
        subprocess.run(
            create_commands[composer_config.template],
            shell=True,
            check=True,
            cwd=temp_dir,
            env=env,
        )
        ctx.logger.info(
            f"{composer_config.template.capitalize()} project created successfully."
        )

        # Create zip file
        zip_path = create_zip_file(ctx, temp_dir, project_name)
        directory = "/tmp"
        final_zip_path = move_zip_file(ctx, zip_path, directory, project_name)
        ctx.logger.info(f"Project zipped successfully: {final_zip_path}")

        s3_url = upload_to_s3(ctx, final_zip_path, project_name)
        ctx.logger.info(f"Project uploaded successfully: {s3_url}")
    except OSError as e:
        ctx.logger.error(f"Filesystem operation failed: {str(e)}")
        raise
    except subprocess.CalledProcessError as e:
        ctx.logger.error(f"Subprocess command failed: {str(e)}")
        raise
    except Exception as e:
        ctx.logger.error(f"Error creating PHP project: {str(e)}")
        raise
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


def scaffold_rails(ctx: Context, project_name: str = "myproject") -> str:
    """Scaffolds a Ruby on Rails project and returns the path to the zipped project.

    Args:
        ctx (Context): The agent context object.
        project_name (str, optional): Name of the Rails project. Defaults to "myproject".

    Returns:
        str: Path to the zipped project.

    Raises:
        OSError: If the /tmp directory does not exist or if the move operation fails.
        subprocess.CalledProcessError: If the command to create the Rails project fails.
        Exception: If any error occurs during the project creation or zipping process.
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
        zip_path = create_zip_file(ctx, temp_dir, project_name)
        directory = "/tmp"
        final_zip_path = move_zip_file(ctx, zip_path, directory, project_name)
        ctx.logger.info(f"Project zipped successfully: {final_zip_path}")

        s3_url = upload_to_s3(ctx, final_zip_path, project_name)
        ctx.logger.info(f"Project uploaded successfully: {s3_url}")
    except OSError as e:
        ctx.logger.error(f"Filesystem operation failed: {str(e)}")
        raise
    except subprocess.CalledProcessError as e:
        ctx.logger.error(f"Subprocess command failed: {str(e)}")
        raise
    except Exception as e:
        ctx.logger.error(f"Error creating Rails project: {str(e)}")
        raise
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
