terraform {
  backend "s3" {
    bucket       = "terraform-github-oidc-drift-demo"
    key          = "oidc-setup/terraform.tfstate"
    region       = "eu-west-2"
    use_lockfile = true
    encrypt      = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
}