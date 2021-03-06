# Welcome to the NYC Potholes repo!
![Pothole repair times by NYC Community Board, 3/12/2016-3/12/2021](https://github.com/tal-z/NYCPotHoles/blob/master/NYCPotholeMap.png)

## About
This project is inspired a prompt provided at a session from NYC's Open Data Week 2021, called "Civic Hacking for Transit Equity," led by [co:census](https://cocensus.io). Though this prompt was not selected as a challenge during the session, the conversation during the session invigorated me to try the challenge myself, which sought solutions for understanding transit inequities at the roadbed level. 

The prompt also nudged us toward searching for relationships between response time and other demographic data. And though I did not engage in any deeper exploration of demographic trends, this project provides a framework for doing so. Most importantly, a critical step in the project is geocoding each pothole record by community district. This allows for further analysis of pothole data against other demographic indicators available via [NYC's Community Portal](https://www1.nyc.gov/site/planning/community/community-portal.page).


This repo has one module, Potholes.py, that contains a script for generating a choropleth map of average time to repair potholes across NYC. The script can be adjusted to create a map based on different time periods, and also has a few extra options, like adding base layers and feature labels, for styling the map to one's liking.


## Dependencies:
- pandas
- geopandas
- sodapy
- matplotlib
- rtree

###### Optional:
- adjustText
- contextily