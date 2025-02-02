terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.76"
    }
  }
}

resource "snowflake_warehouse" "demo" {
  name = "demo_warehouse"
  warehouse_size = "X-Small"
  auto_suspend   = 60
}