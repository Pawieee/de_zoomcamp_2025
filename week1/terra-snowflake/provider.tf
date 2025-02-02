
provider "snowflake" {
  username = var.snowflake_username
  password = var.snowflake_password
  account  = var.snowflake_account_name
  region   = var.snowflake_region
}