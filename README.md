# odoo-docker-compose

Using odoo16 image from docker hub  

Changed for my odoo environment on docker based on  
https://github.com/minhng92/odoo-14-docker-compose

Added some development tools.  

# Usase

```
$ docker-compose up
```

# After connected from VSCode using devcontainer function

## Use ssh key on Windows
Activate ssh-agent on windows.  
```
ssh-add -l
```
Confirm ssh connection to GitHub in the container.  
```
ssh -T git@github.com
```

## Settings for git
```
git config --global core.editor "code --wait"
git config --global core.autocrlf input
git config --global --unset core.sshCommand
git config --global core.sshCommand /usr/bin/ssh
git config --global user.name "[YOUR NAME]"
git config --global user.email "[YOUR EMAIL]"

```