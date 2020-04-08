#!/bin/bash
cd ${C19_HOME}
cd ./chime
# impossible to activate conda chime environment from shell script
#conda activate chime
if [ "$CONDA_PREFIX" == "/home/$USER/anaconda3/envs/chime" ]
then
  git fetch upstream
  git checkout develop
  git merge upstream/develop
  pip install . -q
else
  echo 'need to activate conda chime environment'
fi
cd ${C19_HOME}

