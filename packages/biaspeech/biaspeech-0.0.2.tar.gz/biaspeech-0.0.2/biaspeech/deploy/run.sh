#!/bin/bash
# Run the Bia program
# Usage: ./run.sh
#
# Nicolas Christophe
#
# v1.0 - 2024.02.27 - Creation
# - --------------------

# - ----
# run
# - ----

#cd /home/tylerdddd/Bia
python3 -u ./bia > ./data/logs/bia_"$(date +"%Y_%m_%d_%I_%M_%p").log" 2>&1

