# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }
  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "rg" {
  name     = "myTFResourceGroup"
  location = "japaneast"
}

# Create a storage account (Blob Storage)
resource "azurerm_storage_account" "blob_storage" {
  name                     = "dezoomcampstorageacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "BlobStorage"

  # Optional: Enable HTTPS traffic only
  enable_https_traffic_only = true

  # Optional: Set access tier to Hot (default is Hot)
  access_tier = "Hot"
}

# Create a storage container within the Blob Storage account
resource "azurerm_storage_container" "blob_container" {
  name                  = "blob-container"
  storage_account_name  = azurerm_storage_account.blob_storage.name
  container_access_type = "private"
}