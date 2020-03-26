# Resources for COVID-19 hospital impact modelling

This repo is just a place store some notes and code related to c19
hospital impact modeling. Much of the work is based on the amazing CHIME
project which has 

## Some stuff I created that's in this repo

* [get_c19_data_alpha.ipynb](https://github.com/misken/c19/blob/master/get_c19_data_alpha.ipynb)
    - downloads lates time series data from https://github.com/CSSEGISandData/COVID-19
    - does a bunch of data wrangling to create global as well as US datasets (at county and state level) that are amenable to analysis
    - all dataframes are created both in semi-wide and long forms. The semi-wide forms have been date melted but contain separate columns for confirmed, deaths, and recovered. The long forms are measure melted in addition to date melted.
    - csvs explorted to path of your choosing
    - basic line plot at bottom for demo.

## CHIME project

* [Online hospital impact simulator](https://penn-chime.phl.io/)
* [https://github.com/CodeForPhilly/chime](https://github.com/CodeForPhilly/chime)
* [CHIME docs](https://code-for-philly.gitbook.io/chime/)
* [Announcing CHIME blog post](http://predictivehealthcare.pennmedicine.org/2020/03/14/accouncing-chime.html)

## Johns Hopkins projects

* [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)
    - do git pull to get updated data including daily and time series (csv)
    - for US can get data both at state and county level 
    - [Dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
    - links to Lancet article and many data sources
* [CSSE dept at JHU](https://systems.jhu.edu/)

## Articles, blog posts, vids

* https://medium.com/swlh/a-war-footing-surfing-the-curve-f5ffe6134e37
* https://www.probabilitymanagement.org/blog/2020/3/19/the-flaw-of-averages-in-flattening-the-curve

* https://www.probabilitymanagement.org/blog/2020/1/30/a-combination-of-coronavirus-and-the-flaw-of-averages-can-drive-you-nuts

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

Following thread on INFORMS forum email list on 3/22/2020

----- START -----
Multiple folks from the System Dynamics (SD) community have built models. Tom Fiddaman also made a video

Tom Fiddaman's model/video
metasd.com/2020/03/community-coronavirus-model-bozeman

Jeroen Struben's model
forio.com/app/jeroen_struben/...

Tom Fiddaman's review of Struben's model
metasd.com/2020/03/interactive-coronavirus-models

Tom Fiddaman's review of Jack Homer's COVID-19 model
metasd.com/2020/03/model-covid-19-us


Bob Eberlein's model

exchange.iseesystems.com/public/isee/covid-19-simulator/...
https://exchange.iseesystems.com/models/player/isee/covid-19-model


Bob Eberlein will be presenting his work this Friday, March 27th 2-3PM ET in a Worcester Polytechnic Institute (WPI) System Dynamics Collective Learning Meeting (CLM). I am waiting on details from him about the presentation. Please follow/join WPI SD for more info 

twitter.com/WPISDclub

www.linkedin.com/groups/1916314

Below is a link to sign up to be on the WPI System Dynamics Club mailing list:

eepurl.com/dzmA4j


Wish you and yours health and happiness!

Sincerely,
Christine Tang
WPI System Dynamics Social Media Manager
Interdisciplinary PhD Student in System Dynamics
Forgot to share the System Dynamics Society's page on COVID-19 with INFORMS folks...and I should share the INFORMS page on COVID-19 with SD folks
https://www.systemdynamics.org/covid-19

----- END -----


## PySD

Can read Vensim .mdl files. They are just text files.



