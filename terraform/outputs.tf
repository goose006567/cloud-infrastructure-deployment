output "vpc_id" {
  value = aws_vpc.main.id
}

output "web_public_ip" {
  value = aws_instance.web.public_ip
}

output "app_private_ip" {
  value = aws_instance.app.private_ip
}

output "db_private_ip" {
  value = aws_instance.db.private_ip
}

output "alb_sg_id" {
  value = aws_security_group.alb.id
}

output "assets_bucket" {
  value = aws_s3_bucket.assets.bucket
}

output "cloudfront_domain" {
  value = aws_cloudfront_distribution.assets.domain_name
}
