locals {
  github_repositories = [
    "seunayolu/terraform-github-oidc-drift-demo",
    "seunayolu/terraform-files"
  ]
  github_repo_conditions = [
    for repo in local.github_repositories : "repo:${repo}:*"
  ]
}