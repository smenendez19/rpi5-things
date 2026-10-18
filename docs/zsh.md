# Instalacion de zsh y oh-my-zsh

        sudo apt install zsh
        chsh -s /bin/zsh
        sh c "$(wget -qO- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
        git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
        git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

En el archivo $HOME/.zshrc

- Deshabilitar autoupdate de omz
- Agregar gitfast, zsh-autosuggestions y zsh-syntax-highlighting en plugins
- Habilitar UTF-8
- Cambiar el theme a *agnoster* (o alguno preferido)
