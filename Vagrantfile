Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  config.vm.provision "shell", privileged: false, inline: <<-SHELL

    # Install pyenv prerequisites
    sudo apt-get update; sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

    # Install pyenv
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

    # Pyenv environment variables
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile

    # Pyenv initialisation
    echo 'eval "$(pyenv init --path)"' >> ~/.profile
    source ${HOME}/.profile

    # Python 3.9.1 installation
    pyenv install 3.9.1
    pyenv global 3.9.1

    # Install poetry
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    source ${HOME}/.profile
    
  SHELL

  # Redirect traffic from pport 5000 on host to guest
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # Setup and launch TODO app
  $script = <<-SCRIPT
    vagrant ssh
    cd /vagrant
    poetry install
    nohup poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
  SCRIPT

  config.trigger.after :up do |trigger|
		trigger.name = "Launching App"
		trigger.info = "Running the TODO app setup script"
		trigger.run_remote = {privileged: false, inline: $script}
	end
end
