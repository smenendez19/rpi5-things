sudo apt-get install apt-transport-https
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt update && sudo apt upgrade -y
sudo apt install tailscale
sudo tailscale up


# Docs: https://tailscale.com/learn/how-to-ssh-into-a-raspberry-pi#sign-up-for-a-tailscale-account