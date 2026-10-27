output "vpc_id" {
  description = "VPC that holds the test instance."
  value       = aws_vpc.main.id
}

output "public_ip" {
  description = "Elastic IP of the instance."
  value       = aws_eip.main.public_ip
}

output "ssh_user" {
  description = "Linux user for SSH."
  value       = var.admin_username
}

output "pem_file" {
  description = "Private key written next to this Terraform config. Keep it out of git."
  value       = local_sensitive_file.pem.filename
}

output "ssh_command" {
  description = "SSH into the instance."
  value       = "ssh -i ${var.name}.pem ${var.admin_username}@${aws_eip.main.public_ip}"
}

output "app_url" {
  description = "HTTP URL for the on-prem host once it listens on 0.0.0.0:8080."
  value       = "http://${aws_eip.main.public_ip}:8080"
}
