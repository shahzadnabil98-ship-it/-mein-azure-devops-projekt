resource "aws_instance" "nutrition_api" {

  ami           = "ami-0e872aee57663ae2d"
  instance_type = "t3.micro"

  tags = {
    Name = "nutrition-api"
  }
}