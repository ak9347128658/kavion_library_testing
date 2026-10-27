data "aws_availability_zones" "available" {
  state = "available"

  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }

  filter {
    name   = "zone-type"
    values = ["availability-zone"]
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

resource "aws_vpc" "main" {
  cidr_block           = "10.20.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name    = "${var.name}-vpc"
    purpose = "onprem-example-function-test"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name    = "${var.name}-igw"
    purpose = "onprem-example-function-test"
  }
}

resource "aws_subnet" "main" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.20.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = false

  tags = {
    Name    = "${var.name}-subnet"
    purpose = "onprem-example-function-test"
  }
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name    = "${var.name}-rt"
    purpose = "onprem-example-function-test"
  }
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

resource "aws_security_group" "main" {
  name        = "${var.name}-sg"
  description = "Allow all inbound and outbound traffic."
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "allow_all"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "allow_all"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.name}-sg"
    purpose = "onprem-example-function-test"
  }
}

resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_sensitive_file" "pem" {
  content         = tls_private_key.ssh.private_key_pem
  filename        = "${path.module}/${var.name}.pem"
  file_permission = "0600"
}

resource "aws_key_pair" "main" {
  key_name   = "${var.name}-key"
  public_key = tls_private_key.ssh.public_key_openssh

  tags = {
    Name    = "${var.name}-key"
    purpose = "onprem-example-function-test"
  }
}

resource "aws_instance" "main" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.main.id
  vpc_security_group_ids      = [aws_security_group.main.id]
  key_name                    = aws_key_pair.main.key_name
  associate_public_ip_address = false

  root_block_device {
    volume_size = var.root_volume_size_gb
    volume_type = "gp3"
  }

  tags = {
    Name    = "${var.name}-vm"
    purpose = "onprem-example-function-test"
  }

  depends_on = [aws_route_table_association.main]
}

resource "aws_eip" "main" {
  domain = "vpc"

  tags = {
    Name    = "${var.name}-eip"
    purpose = "onprem-example-function-test"
  }
}

resource "aws_eip_association" "main" {
  instance_id   = aws_instance.main.id
  allocation_id = aws_eip.main.id
}
