terraform {
  backend "kubernetes" {
    secret_suffix = "state"
  }

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.1"
    }
  }
}

provider "kubernetes" {
  config_path = var.kubeconfig
}

locals {
  base_name = "pandocode"
  selectors = {
    "app.kubernetes.io/name"     = "pandocode"
    "app.kubernetes.io/instance" = "pandocode"
  }
}
