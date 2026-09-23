provider "aws" {
  region = var.region

  # Offline/dev: skip the STS credential validation round-trip.
  # Remove these two lines when using real AWS credentials.
  skip_credentials_validation = true
  skip_requesting_account_id  = true

  # When mock_endpoint is set (e.g. http://127.0.0.1:5000), all AWS calls are
  # redirected to the local moto server so we can apply offline.
  dynamic "endpoints" {
    for_each = var.mock_endpoint != "" ? [1] : []

    content {
      sts        = var.mock_endpoint
      ec2        = var.mock_endpoint
      s3         = var.mock_endpoint
      cloudfront = var.mock_endpoint
    }
  }
}
