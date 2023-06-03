
# YOUTUBE SCRAPPING

YouTube scraping, also known as web scraping, refers to the process of extracting data from YouTube's web pages programmatically. It involves automatically retrieving the data from YouTube's website to extract information such as video details, channel information, comments, likes, dislikes, and other relevant data.
From this extraction we can get required information from the visual representations.


## Installation

Install my-project with npm

```bash
    import streamlit as st
    import psycopg2
    import pymongo
    import pandas as pd
    from googleapiclient.discovery import build
    from sqlalchemy import create_engine
    import plotly.express as px
```
    
## CONNECTIONS

For this project wee need to connect different Databases and packages through python.

* Use pakages Psycopg2 - Python to SQL connection

- Use Package Pymongo - Python to MongoDB connection

- Use plotly packages for visualization

- Streamlit app is  for deploying our outcomes. 

## Deployment

To deploy this project qw use streamlit to run 

```bash
  youtubescrap.py 
```


## WORKFLOW

STEP 1 : Generate a api key credentials by signing up into an gmail account.This gives us secured data scrapping for us. 

        - Connect to the YouTube API, we can use the Google API client library for Python to make requests to the API to retrieve channel and video data, by giving Channel-ID as input.

        - Cleaning the data before inserting into mongoDB. 
        

STEP 2 : After the retrieval of data from the YouTube API, store the required data in mongodb in json format by using MongoClient package.

        - Create database and Collections to store the data that we scrapped. 

STEP 3 : Now migrate the data from mongodb convert into structured format in python.

        - Pandas package is used to  convert the unstructed data format into table format that gices us to read the data efficiently.

STEP 4 : By using Psycopg2 and SQLALchemy package, upload the table data in SQL Database.

        - Upload the created DataFrame into SQL as  different tables assigning its own parameters.

STEP 5 : Retrieve the data from SQL by querying from python,by using Psycopg2 package.

        - Using execute command query the data from python in SQL. 

STEP 6 : Visualize the extrated data into graphs inorder to a clear idea of the datas so that we can implements into our needs based on our conditions.

        - Using plotly packages represent the data into graphs.

STEP 7 : Deploy the scrapping in Streamlit application and we can take insights from the application and analyse the data for our business approach.

        - Create a interface for users to extract the data by themselves.


## APPLICATION 

This project will be helpful in the following areas:

- Video Analytics: Extracting data related to video performance, such as views, likes, dislikes, comments.

- Channel Analytics: Gathering information about a YouTube channel, including subscriber count, total views, growth rate.

- Trend Analysis: Extracting data on trending videos, popular topics, and viral content to understand the current trends.

- Content Research: Collecting data on videos related to specific topics or keywords..

- Competitive Analysis: Extracting data on competitor channels, their video performance and subscriber growth.

- User Sentiment Analysis: Analyzing comments, likes, dislikes, and engagement patterns to value the audience sentiment and feedback .



- Advertising and Sponsorship : Extracting data on channels or videos with high engagement and relevant audience to identify potential advertising or sponsorship opportunities.




## Lessons Learned

I have a learnt alot,like connecting databases with python, deploying in streamlit app, querying the required data from SQl to python.


## 🛠 Languages And Databases 
Python, SQL, MongoDB,Data Visualization Tools...


## Demo

Insert gif or link to demo


## 🚀 About Me


🧠 I'm currently learning Datascience and MachineLearning

👯‍♀️ I'm looking forward to move on into Datascience career.
## Results

- Here, we can retrieve all the relevant data like Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of all video using Google API by giving Youtube channel Id as input.

- We can interpret the extrated data from youtube and take required insights for our requirements.

- By scrapping and gaining the data from Youtube, we can apply those relevant datas and insights for our business approach.