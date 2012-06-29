#!/bin/sh

INDEX_URL="{{ index_url }}"

set_pip_env () {
    echo "Adding global pip enviornment variable to /etc/profile"
    sudo sh -c "echo '
# Localshop index server
export PIP_INDEX_URL=$INDEX_URL
' >> /etc/profile"
}

write_pipconf () {
    echo "Writing pip.conf file to ~/.pip/pip.conf"
    mkdir ~/.pip
    echo "[global]
index-url = $INDEX_URL
" > ~/.pip/pip.conf
}

write_pydistutils () {
    echo "Writing .pydistutils.cfg file to ~/.pydistutils.cfg"
    echo "[easy_install]
index_url = $INDEX_URL
" > ~/.pydistutils.cfg
}

write_buildoutconf () {
    echo "Writing buildout.cfg file to ~/.buildout/default.cfg"
    mkdir ~/.buildout
    echo "[buildout]
index = $INDEX_URL
" > ~/.buildout/default.cfg
}

# Add global environment variable for pip
echo "Do you want to install a global pip environemnt variable?"
select yn in Yes No; do
    case $yn in
        Yes ) set_pip_env; break;;
        No ) break;;
    esac
done

# Add pip.conf file for good measure
if [ -e ~/.pip/pip.conf ]; then
    echo "pip.conf exists. Do you want to overwrite it?"
    select yn in Yes No; do
        case $yn in
            Yes ) write_pipconf; break;;
            No ) break;;
        esac
    done
else
    write_pipconf
fi

# Add .pydistutils.cfg
if [ -e ~/.pydistutils.cfg ]; then
    echo ".pydistutils.cfg exists. Do you want to overwrite it?"
    select yn in Yes No; do
        case $yn in
            Yes ) write_pydistutils; break;;
            No ) break;;
        esac
    done
else
    write_pydistutils
fi

# Add buildout.conf
if [ -e ~/.buildout/default.cfg ]; then
    echo ".buildout/default.cfg exists. Do you want to overwrite it?"
    select yn in Yes No; do
        case $yn in
            Yes ) write_buildoutconf; break;;
            No ) break;;
        esac
    done
else
    write_buildoutconf
fi

echo "Done."
