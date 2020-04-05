# Quick intro to conda envs for chime

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

Create a folder somewhere to store your conda "recipes" and put
the [datasci.yml] file in it. Open it in a text editor and you'll
quickly see what it is and is going to do.

### Fire up an Anaconda prompt and navigate to your recipes folder

###  Now we will create a conda environment from that recipe

    conda env create -f datasci.yml 
    
###  Activate your new environment

    conda activate datasci
    
    # See what packages are installed (it's a bunch)
    conda list
    
###  Now we'll create another env called chime by cloning datasci

I usually get back into the base conda env

	# Back to base
    conda deactivate
    
    conda create --name chime --clone datasci
    
    conda activate chime
    
###  Now navigate to your chime repo directory and let's install it

    pip install .
    
    # Confirm penn_chime installed
    conda list
    
### Use penn_chime in multiple ways

You can run their cli app by just being in whatever directory you
want to be working in and then

	# See their help text
    penn_chime -h
    
    # Run using a config file - easiest
    penn_chime --file yourconfigfile.cfg
    

You can also [use my sim_chime_scenario_runner.py script](https://github.com/misken/c19/blob/master/mychime/scenario_runner/using_sim_chime_scenario_runner.ipynb).

You can use Jupyter notebooks and do imports of my script and/or imports of penn_chime modules.
My script obviously imports such modules.
