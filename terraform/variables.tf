variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "az" {
  default = "us-east-1a"
}

variable "ami" {
  description = "Amazon Linux 2 id (us-east-1) - replace with your region's id before apply"
  default     = "ami-0c02fb55956c7d316"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "bucket_name" {
  description = "Globally unique S3 bucket name"
  default     = "devops-projects-static-assets"
}

variable "mock_endpoint" {
  description = "Point the AWS provider at a local moto server (e.g. http://127.0.0.1:5000). Empty = real AWS."
  default     = ""
}
