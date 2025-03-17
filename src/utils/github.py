import requests
from github import Github

GITHUB_BASE_URL = "https://api.github.com"


async def _post_github_request(url, token, data):
    return requests.post(
        url,
        json=data,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
        },
    )


async def _get_github_request(url, token):
    return requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
        },
    )


async def post_github_workflow_dispatche(
    repo_full_name, token, workflow_id, ref, inputs
):
    return await _post_github_request(
        f"{GITHUB_BASE_URL}/repos/{repo_full_name}/actions/workflows/{workflow_id}/dispatches",
        token,
        {"ref": ref, "inputs": inputs},
    )


async def get_github_workflow_logs(repo_full_name, run_id, token):
    return await _get_github_request(
        f"{GITHUB_BASE_URL}/repos/{repo_full_name}/actions/runs/{run_id}/logs", token
    )


async def getting_github_repo(repo_name, token=None):
    g = Github(token if token else None)
    return g.get_repo(repo_name)


async def create_github_repo(token, name, org=None):
    g = Github(token if token else None)
    if org:
        github = g.get_organization(org)
    else:
        github = g.get_user()

    repo = github.create_repo(name, auto_init=True, private=True)

    return repo
