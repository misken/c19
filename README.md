# Resources for COVID-19 hospital impact modelling

This repo is just a place store some notes and code related to c19
hospital impact modeling. Some of the work is based on the amazing CHIME
project done by the folks at [UPenn's Predictive Healthcare group](http://predictivehealthcare.pennmedicine.org/) and
the [CodeForPhilly CHIME project](https://codeforphilly.org/projects/chime). 

## CHIME project

* [Online hospital impact simulator](https://penn-chime.phl.io/)
* [https://github.com/CodeForPhilly/chime](https://github.com/CodeForPhilly/chime)
* [CHIME docs](https://code-for-philly.gitbook.io/chime/)
* [Announcing CHIME blog post](http://predictivehealthcare.pennmedicine.org/2020/03/14/accouncing-chime.html)

## Some stuff I created that's in this repo

### Capacity driven census and admission adjustments to chime model

Woke up in the middle of the night and an idea came to me for adjusting census and admission sduring **early stages** of virus spread to deal with census at time 0 problem. Thought about it, couldn't sleep and figured I'd get my rough ideas down in writing.

Basic idea is that underlying epidemic has its dynamics that will play out almost independent of resources. But for capacity constrained resources it seems like there are three phases during the early growth stage of the virus. Let's just use hospital beds as the example resource.

#### growth phase - haven't hit capacity yet and epidemic in exponential growth phase

In this phase, we have the "zero census" problem with the underlying model. But if we are in growth phase, should be easy to just solve for t* < t0 in the basic exponential growth equation to "reconstruct" the admission history and use that along with LOS to compute census for the period [t*, t0] and thus have a better estimate of starting census at t0 as well as decent approximation of the mix of how far along those patients are in there stay to better model them leaving - as opposed to assuming all patients at t0 just started there stay, which causes a weird census spike at start of model projections.

A complication is that the virus grew at intrinsic growth rate for a while and then
when social distancing started, grew at implied growth rate.

Hacked around in Excel so I could see what I was doing and this appears to make some sense for this phase. Talking
it through with a few colleagues and then Pythonizing it.

See 'model' sheet in [explore_census_adj.xlsx](https://github.com/misken/c19/blob/master/explore_census_adj.xlsx).

#### flat phase - at capacity

I'm guessing we are going to hit capacity constraints well before epidemic passes inflection point
in the standard logistic model of its exponential spread and then eventual slowing growth.

At this stage, no matter how many admits predicting by underlying SIR model, we have our max admission rate, A* and max census C*. We will stay in this state until the underlying SIR model has admission rate A < A*. So, resource use is flat.

#### decay phase

When A < A*, the underlying growth rate in the epidemic must be slowing and now, we can use A to compute census in normal way.

I'm going to try to hack a procedure together uses standard outputs from the current chime model to implement these ideas. If things look good, we can float our approach to the chime team for that thoughts and potential adoption. It would likely require user to input guesstimate of capacity for each resource being modelled.


### run_sim_chime_scenario.py

We adapted the CLI application in the CHIME project (https://github.com/CodeForPhilly/chime).

- added scenario and output_path parameters (separate from main Parameters object)
- added ability to use an input file, command line args, or DEFAULTS to instantiate model
- added ability to import this and call sim_chime() function from external apps so that we can run tons of scenarios over ranges of input parameters
- output is a dictionary of the standard CHIME dataframes as well as dictionaries
containing parameter and variable values.
- also writes out csvs of the dataframes and json for the dictionaries

https://github.com/misken/c19/blob/master/mychime/run_sim_chime_scenario.py

### Cheat sheets for installing CHIME locally

The docs for CHIME are great. I created this to help folks with limited
exposure to this kind of stuff get CHIME installed in either Windows or Linux.
The hospital based analysts we are trying to help with this work are all on Windows. 

https://github.com/misken/c19/tree/master/mychime/docs

### Jupyter notebook version of early CHIME model

**NOTE: This was based on a very early version of the CHIME model. Nevertheless,
the comments might still be useful to someone trying to understand the basic
logic of the model.**

I've added tons of code comments and other descriptive text throughout the notebook to help others understand exactly how this works and how we might adapt it for our use.

https://github.com/misken/c19/blob/master/chime_earlyversion_annotated.ipynb

### Jupyter notebook for downloading COVID-19 time series data

Downloads latest time series data from https://github.com/CSSEGISandData/COVID-19.

- does a bunch of data wrangling to create global as well as US datasets (at county and state level) that are amenable to analysis
- all dataframes are created both in semi-wide and long forms. The semi-wide forms have been date melted but contain separate columns for confirmed, deaths, and recovered. The long forms are measure melted in addition to date melted.
- csvs explorted to path of your choosing
- basic line plot at bottom for demo.

https://github.com/misken/c19/blob/master/get_c19_data_alpha.ipynb

## Johns Hopkins projects

* [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)
    - do git pull to get updated data including daily and time series (csv)
    - for US can get data both at state and county level 
    - [Dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
    - links to Lancet article and many data sources
* [CSSE dept at JHU](https://systems.jhu.edu/)

## Articles, blog posts, vids

* [A War Footing: Surfing the Curve](https://medium.com/swlh/a-war-footing-surfing-the-curve-f5ffe6134e37)
* [The Flaw of Averages in Flattening the Curve](https://www.probabilitymanagement.org/blog/2020/3/19/the-flaw-of-averages-in-flattening-the-curve)
* [A combination of coronavirus and the flaw of averages can drive you nuts](https://www.probabilitymanagement.org/blog/2020/1/30/a-combination-of-coronavirus-and-the-flaw-of-averages-can-drive-you-nuts)

## Kaggle data, kernels, challenges

* https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset
* https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks
...

## Other Covid19 data and simulators

* https://alhill.shinyapps.io/COVID19seir/
* https://metasd.com/2020/03/interactive-coronavirus-models/
* https://metasd.com/2020/03/community-coronavirus-model-bozeman/
* https://forio.com/app/jeroen_struben/corona-virus-covid19-seir-simulator/index.html#introduction.html
* http://covidsim.eu/


## PySD

Simulating SD models in Python - https://pysd.readthedocs.io/en/master/

Can read Vensim .mdl files. They are just text files.



