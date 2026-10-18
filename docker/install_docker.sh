# Instalacion de docker y asignacion al groupmod

sudo apt-get update && apt-get upgrade -y
sudo apt-get autoremove -y
sudo curl -fsSL https://get.docker.com/ -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ${USER}
sudo reboot