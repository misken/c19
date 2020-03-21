# Resource collection for COVID-19 hospital impact modelling

## Some stuff I created that's in this repo

* [get_c19_data_alpha.ipynb](https://github.com/misken/c19/blob/master/get_c19_data_alpha.ipynb)
    - downloads lates time series data from https://github.com/CSSEGISandData/COVID-19
    - does a bunch of data wrangling to create global as well as US datasets (at county and state level) that are amenable to analysis
    - all dataframes are created both in semi-wide and long forms. The semi-wide forms have been date melted but contain separate columns for confirmed, deaths, and recovered. The long forms are measure melted in addition to date melted.
    - csvs explorted to path of your choosing
    - basic line plot at bottom for demo.

## CHIME project

* [Online hospital impact simulator](https://penn-chime.phl.io/)
* [https://github.com/pennsignals/chime](https://github.com/pennsignals/chime)
* [Announcing CHIME blog post](http://predictivehealthcare.pennmedicine.org/2020/03/14/accouncing-chime.html)

## Johns Hopkins projects

* [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)
    - do git pull to get updated data including daily and time series (csv)
    - for US can get data both at state and county level 
    - [Dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
    - links to Lancet article and many data sources
* [CSSE dept at JHU](https://systems.jhu.edu/)

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

Can read Vensim .mdl files. They are just text files.



