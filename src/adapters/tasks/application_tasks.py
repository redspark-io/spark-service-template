import logging
import os

from aiofiles import open
from github import InputGitTreeElement
from jinja2 import Template

from src.infrastructure.configs import settings
from src.utils.github import create_github_repo

logger = logging.getLogger("uvicorn")
files_in_memory = {}


async def _replace_attrs(file_content, attrs):
    template = Template(file_content)
    return template.render(attrs)


async def _create_github_tree_from_local(repo, template_path, attrs):
    tree = []
    for root, _, files in os.walk(template_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            git_file_path = os.path.relpath(file_path, template_path)
            logger.info(f"Creating blob: {git_file_path}")
            async with open(file_path, "r") as file:
                file_content = await file.read()
                final_file_content = await _replace_attrs(file_content, attrs)
                blob = repo.create_git_blob(
                    content=final_file_content, encoding="utf-8"
                )
                tree.append(
                    InputGitTreeElement(
                        path=git_file_path,
                        mode="100644",
                        type="blob",
                        sha=blob.sha,
                    )
                )
    return tree


async def _create_github_tree_from_external_repo(
    external_repo,
    repo,
    attrs,
    path="",
):
    tree = []
    contents = external_repo.get_contents(path)
    for content_file in contents:
        if content_file.type == "dir":
            list_tree = await _create_github_tree_from_external_repo(
                external_repo, repo, attrs, content_file.path
            )
            tree.extend(list_tree)
        else:
            git_file_path = os.path.relpath(content_file.path, "skeleton")
            logger.info(f"Creating blob: {git_file_path}")
            file_content = content_file.decoded_content.decode("utf-8")
            final_file_content = await _replace_attrs(file_content, attrs)
            blob = repo.create_git_blob(content=final_file_content, encoding="utf-8")
            tree.append(
                InputGitTreeElement(
                    path=git_file_path,
                    mode="100644",
                    type="blob",
                    sha=blob.sha,
                )
            )
    return tree


async def task_building(
    application_id: str,
    template_identifier: str,
    repo_access_token: str,
    repo_org: str,
    properties: dict,
):
    logger.info("Starting task to build application")
    try:
        # await ApplicationService.update_application(
        #     {"status": "building"}, {"_id": ObjectId(application_id)}, db
        # )

        logger.info("Creating github repository")
        repo = await create_github_repo(
            repo_access_token,
            properties["identifier"],
            repo_org,
        )

        # await ApplicationService.update_application(
        #     {"repo_full_name": repo.full_name}, {"_id": ObjectId(application_id)}, db
        # )

        logger.info("Creating github webhook")
        events = ["workflow_job"]
        config = {
            "url": f"{settings.HOST_URL}/api/v1/applications/{application_id}/pipeline-webhook",
            "content_type": "json",
        }
        repo.create_hook("web", config, events, active=True)

        logger.info("Creating github secrets")
        repo.create_secret("REGISTRY_PASSWORD", settings.REGISTRY_PASSWORD)
        repo.create_secret("AZURE_CREDENTIALS", settings.AZURE_CREDENTIALS)

        logger.info("Creating github blob from local")
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        template_path = os.path.join(
            root_path, "demo_templates", template_identifier, "skeleton"
        )

        if not os.path.exists(template_path):
            raise Exception("Template not found with path {0}".format(template_path))

        tree = await _create_github_tree_from_local(repo, template_path, properties)

        logger.info("Creating github tree")

        new_tree = repo.create_git_tree(
            tree=tree, base_tree=repo.get_git_tree(sha="main")
        )

        logger.info("Creating initial commit")

        first_commit = repo.create_git_commit(
            message="Create skeleton from template",
            tree=repo.get_git_tree(sha=new_tree.sha),
            parents=[repo.get_git_commit(repo.get_branch("main").commit.sha)],
        )

        logger.info("Pushing to github")

        main_ref = repo.get_git_ref(ref="heads/main")
        main_ref.edit(sha=first_commit.sha)

        logger.info("Application built successfully")
        # await ApplicationService.update_application(
        #     {"status": "waiting_workflow"}, {"_id": ObjectId(application_id)}, db
        # )

    except Exception as e:
        # await ApplicationService.update_application(
        #     {"status": "failed"}, {"_id": ObjectId(application_id)}, db
        # )

        logger.error(f"Error: {e}")

        raise e
