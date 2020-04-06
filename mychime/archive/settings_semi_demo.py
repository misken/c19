#!/usr/bin/env python

"""These are just example settings values based on counties in SE Michigan."""

from .defaults import Constants, Regions, RateLos

wayne = 1778396
oakland = 1248141
macomb = 867502
genesee = 414657
washtenaw = 326058
saintclair = 158313
monroe = 153436
lapeer = 79723

DEFAULTS = Constants(
    # EDIT YOUR DEFAULTS HERE
    region=Regions(
        wayne=wayne,
        oakland=oakland,
        macomb=macomb,
        genesee=genesee,
        washtenaw=washtenaw,
        saintclair=saintclair,
        monroe=monroe,
        lapeer=lapeer,
    ),
    current_hospitalized=200,
    doubling_time=4,
    known_infected=1000,
    n_days=60,
    market_share=0.25,
    relative_contact_rate=0.3,
    hospitalized=RateLos(0.025, 7),
    icu=RateLos(0.0075, 9),
    ventilated=RateLos(0.005, 10),
)
