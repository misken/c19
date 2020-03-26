Getting chime running locally for development
=============================================

Writing this not knowing people level of comfort/familiarity with Anaconda Python distro,
using virtual conda environments, running things from shells. So, if you know all
this, it will be really easy.

Clone or download the source from its GitHub site at https://github.com/pennsignals/chime
into directory of your choosing. If you do a `git clone https://github.com/CodeForPhilly/chime.git`
you'll end up with a new directory called chime. That's the working directory. If
instead, you just download the zip file from GitHub, you'll get a file named
`chime-master.zip`. After you extract it, that folder will be the working directory. It
will be called chime-master but you can obviously change it.

Instructions for getting the app running locally so that you can modify code are at: [https://codeforphilly.github.io/chime/contributing/app-dev.html](https://codeforphilly.github.io/chime/contributing/app-dev.html)

I'm just walking through the instructions as I'm getting this running on my machine.

I'm using Anaconda Python distro and I use conda for package management. I'm using
Ubuntu but all of this stuff is cross-platform.

* Open an Anaconda prompt (on Windows) or a terminal shell in Linux/Mac.
* Navigate to the `chime` diectory.
* Now, following the instructions above, we'll create a new conda virtual environment, install Streamlit and launch the app locally.

Type these commands in your terminal.

    conda env create -f environment.yml
    conda activate chime
    pip install streamlit
    streamlit run src/app.py
    
A few notes about the above. 

* On Windows you do `conda activate chime` even though the instructions say use `source activate chime`. The former works on both Linux and Windows, the latter doesn't work on Windows.
* The `environment.yml` file is a YAML file that has the "recipe" for creating the necessary conda virtual env needed by Streamlit.
* After the last command that actually launches the app, your terminal window will show you to URLs. Just copy the network URL and paste into a new browser tab.
* Voila, the app is running. 
* The terminal window is running the necessary services. Just leave it open while you are playing with the app.
* Use CTRL+C within the terminal to kill the app.

