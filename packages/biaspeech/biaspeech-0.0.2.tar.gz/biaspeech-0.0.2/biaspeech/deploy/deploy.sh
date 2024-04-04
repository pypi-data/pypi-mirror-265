# - --------------------
#!/bin/bash
# Deploy the Bia solution from macosx to raspberry
# Usage: ./deploy.sh
#
# Nicolas Christophe
#
# v1.0 - 2024.02.06 - Creation
# - --------------------

# - ----
# first the python files
# - ----
echo "IP address of the remote machine, ssh to be enabled ? (xxx.xxx.xxx.xxx) : "
read ip

echo -n "Confirm the deployment of the Bia python files to $ip ? (Y/N) : "
read yn

if [ "$yn" = "y" ] || [ "$yn" = "Y" ]; then
    # Inform the user
    echo "Deploy the Bia project files to $ip"

    # Make a copy of the full folder
    scp -r /users/tylerdddd/Documents/Git/Otto/* tylerdddd@$ip:/home/tylerdddd/Bia/       
    echo "Bia python files successfully deployed"

    echo "Bia config file successfully deployed"

elif [ "$yn" = "n" ] || [ "$yn" = "N" ]; then
    echo "Ok, bye! "

else
    echo "Y or N expected, not $yn"

fi

