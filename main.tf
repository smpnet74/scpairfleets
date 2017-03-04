# Configure the AWS Provider
provider "aws" {
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
    region = "${var.setregion}"
}

//SECURITY GROUP
resource "aws_security_group" "os_all_producers" {

  name = "os_consumer"
  vpc_id = "${var.vpcid}"
  description = "Security group to allow all sources to intercommunicate and to talk out"

  ingress {
    from_port = "0"
    to_port = "0"
    protocol = "-1"
    self = true
    cidr_blocks = ["73.210.192.27/32"]
  }

    egress {
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    name = "os_all_producers"
  }
}

//USER CREATION
resource "aws_key_pair" "deployer" {
  key_name = "deployer-key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6BzZ5+IKdp7yNBbHMZGcghRVNkEEsTJW3MmjTeCxmJhnnCBd0z8d3+CPeiOyfC4IIlR5Ykm0UxEH2uhCjgmR9V8oJitcZTlqdIidrFRZdUwPfH3uvfggCdlUchS5tb6T04QkVQnghaohx/GgmLzJWN6mcGVpOhgN17q+LFyTR3Y3B4I1MbvvVcmDxjJPunIvDY4YqSUAFlHePZ2ACoIo/4M1ZRDKxLSDuLss/ELHTgZ0Ayxu/A3oYfuBYiYxCfubXZFDwsHTrwxvVITyRY7OqfPB4cRwAd5fhhhOJ4asuNt8t5AHOzSJOQ6ChgnrfU6PtAplb5hcjFaC5dumhkRqL ubuntu@ubuntu-yakkety"
}


//INSTANTIATION EC2
resource "aws_instance" "os_master" {
    key_name = "deployer-key"
    ami = "${var.aminumber}"
    instance_type = "${var.master_instsize}"
    subnet_id = "${var.subnet}"
    key_name = "deployer-key"
    count = "${var.master_count}"
    user_data = "${data.template_file.os_master_userdata.rendered}"
    vpc_security_group_ids = ["${aws_security_group.os_all_producers.id}"]
    tags {
        Name = "os-master-${count.index}"
    }
    root_block_device {
      delete_on_termination = true
    }
    ebs_block_device {
      device_name = "/dev/sdg"
      volume_size = 10
      volume_type = "gp2"
      delete_on_termination = true
    }
}

data "template_file" "os_master_userdata" {
    template = "${file("./master.tpl")}"
}
