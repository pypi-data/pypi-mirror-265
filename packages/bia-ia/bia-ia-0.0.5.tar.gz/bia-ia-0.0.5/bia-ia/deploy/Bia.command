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

cd /Users/tylerdddd/Documents/Git/Otto
python3 -u ./main.py > ./data/logs/bia_"$(date +"%Y_%m_%d_%I_%M_%p").log" 2>&1

