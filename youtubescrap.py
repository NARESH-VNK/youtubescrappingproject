import pip
import psycopg2 as psycopg2
import sqlalchemy as sqlalchemy
import streamlit as streamlit

# pip install psycopg2 sqlalchemy
# pip install streamlit
import streamlit as st
import psycopg2
import pymongo
import pandas as pd
from googleapiclient.discovery import build
from sqlalchemy import create_engine
import plotly.express as px



# create a PostgreSQL connection
conn = psycopg2.connect(
    host = 'localhost',
    user = "postgres",
    password ="naresh",
    port =5432,
    database ="youtube"
)
nk = conn.cursor()

# creating connection btwn psycopg2 and postgressql to insert a dataframe
engine = create_engine('postgresql+psycopg2://postgres:naresh@localhost/youtube')


# create a connection btwn python and mongodb using mongoclient
client = pymongo.MongoClient("mongodb://nareshvnk1227:nareshvnk@ac-3ahszuc-shard-00-00.mvcys6r.mongodb.net:27017,ac-3ahszuc-shard-00-01.mvcys6r.mongodb.net:27017,ac-3ahszuc-shard-00-02.mvcys6r.mongodb.net:27017/?ssl=true&replicaSet=atlas-t4xjip-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client['youtube']
col = db['view']




option = st.sidebar.selectbox('MENU',['ABOUT','APPROACH','DATA EXPLORATION','TABLES','CONCLUSION'])

if option =='ABOUT':
    st.title("YOUTUBE SCRAPPING")
    st.subheader("INTRODUCTION")

    st.write("YouTube scraping, also known as web scraping, refers to the process of extracting data from YouTube's web pages programmatically. It involves automatically retrieving the data from YouTube's website to extract information such as video details, channel information, comments, likes, dislikes, and other relevant data.")
    st.markdown("There are several methods you can use to scrape data from YouTube.Some of them are, Web Scraping with Python Libraries, YouTube Data API, Third-Party Tools and Services, Cloud-Based Scraping Services and Selenium .")
    st.subheader("YOUTUBE API")
    st.markdown("The YouTube Data API provides an authorized way to access YouTube's data. By using the API, you can ensure that you are accessing the data within the boundaries defined by YouTube's terms of service and policies.")
    st.write(
        "The major benefit of using an API is accessing and consuming data and services from thousands of independent sources. This means organizations of all sizes can access these functionalities without developing their own specialized applications. Other major benefits to using APIs include: APIs increase business agility.")

    st.subheader("AIM")

    st.write("##### Create a application allows user to access and analyze data from multiple YouTube channels.")

if option == "APPROACH":
    st.subheader("STEP BY STEP APPROACH")
    st.write(" ##### STEP 1: Connect to the YouTube API, we can  use the Google API client library for Python to make requests to the API to retrieve channel and video data, by giving Channel-ID as input.")


    st.markdown("##### STEP 2: After the retrieval of data from the YouTube API, store the required data in mongodb in json format by using MongoClient package.")
    st.write("##### STEP 3: Now migrate the data from mongodb convert into structured format in python.")
    st.write("##### STEP 4: By using Psycopg2 and SQLALchemy package, upload the table data in SQL Database.")
    st.write("##### STEP 5 : Retrieve the data from SQL by querying from python,by using Psycopg2 package.")
    st.write("##### STEP 6: Deploy the scrapping in Streamlit application and we can take insights from the application and analyse the data for our business approach.")


# UCkHdBeQ4DuvBXTahMYZVlMA-kenji explains
if option =='DATA EXPLORATION':
    st.title("DATA EXTRACTION")
    txt = st.text_area('Enter channel ID', '''    ''')                 # enter the input in streamlit
    # extracting data by using cid-channelID
    def channel(cid):
        api_key = 'AIzaSyCWSqX8gXL-2fCzkJx4XKjg6QoWAcn38Iw'  # Replace with your generated API key
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.channels().list(part=["snippet,contentDetails,statistics"], id=cid)
        response = request.execute()

        data = dict(channel_id=response['items'][0]['id'],
                    channel_name=response['items'][0]['snippet']['title'],
                    channel_description=response['items'][0]['snippet']['description'],
                    channel_subscribers=response['items'][0]['statistics']['subscriberCount'],
                    channel_view_count=response['items'][0]['statistics']['viewCount'],
                    channel_video_count=response['items'][0]['statistics']['videoCount'],
                    playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])

        # Retrieve the channel's uploads playlist ID
        channel_response = youtube.channels().list(part="contentDetails", id=cid).execute()
        uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Retrieve all video IDs from the uploads playlist
        videos_id = []
        playlist_items_request = youtube.playlistItems().list(part="contentDetails", playlistId=uploads_playlist_id,
                                                              maxResults=50)
        while playlist_items_request:
            playlist_items_response = playlist_items_request.execute()
            videos_id.extend(item["contentDetails"]["videoId"] for item in playlist_items_response["items"])
            playlist_items_request = youtube.playlistItems().list_next(playlist_items_request, playlist_items_response)

        video_info = {}
        comment = {}
        for k in range(1, len(videos_id) + 1):
            request = youtube.videos().list(part="snippet,contentDetails,statistics", id=videos_id[k - 1])
            response = request.execute()
            comment_request = youtube.commentThreads().list(part="snippet", videoId=videos_id[k - 1], maxResults=2)
            comment_response = comment_request.execute()


            video_id = response['items'][0]['id']
            video_name = response['items'][0]['snippet']['title']
            video_description = response['items'][0]['snippet']['description']
            video_tags = response['items'][0]['snippet'].get('tags', [])
            video_publishedat = response['items'][0]['snippet']['publishedAt']
            video_thumbnail = response['items'][0]['snippet']['thumbnails']['default']['url']
            video_duration = response['items'][0]['contentDetails']['duration']
            video_caption = response['items'][0]['contentDetails']['caption']
            video_viewcount = response['items'][0]['statistics']['viewCount']
            video_likecount = response['items'][0]['statistics']['likeCount']
            video_favouritecount = response['items'][0]['statistics']['favoriteCount']
            video_commentcount = response['items'][0]['statistics']['commentCount']

            for item in range(len(comment_response["items"])):
                comment_text = comment_response["items"][item]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                author = comment_response["items"][item]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                PublishedAt = comment_response["items"][item]['snippet']['topLevelComment']['snippet']['publishedAt']
                Comment_Id = comment_response["items"][item]['id']

            video_info[f'videos_id{k}'] = {'Video_Id': video_id, 'Title': video_name, 'Description': video_description,
                                           'Tags': video_tags, 'Published At': video_publishedat, 'Thumbnail': video_thumbnail,
                                           'Duration': video_duration, 'Caption': video_caption, 'View Count': video_viewcount,
                                           'Like Count': video_likecount, 'Favorite Count': video_favouritecount,
                                           'Comment Count': video_commentcount,
                                           'comment': {"Comment_Id": Comment_Id, "Comments_text": comment_text,
                                                       "Comment_Author": author, "Comment_PublishedAt": PublishedAt}}

        final = [{'CHANNEL_ID': data,
                  'VIDEO_ID': video_info}]
        return(final)





    # final=channel(cid="UCnz-ZXXER4jOvuED5trXfEA")

    if st.button("Extract All Data"):
        final_dict = channel(cid=txt)
        st.write("Extracting Process Completed")
        st.write("Required Data in Dictionary Format",final_dict)
        client = pymongo.MongoClient(
            "mongodb://nareshvnk1227:nareshvnk@ac-3ahszuc-shard-00-00.mvcys6r.mongodb.net:27017,ac-3ahszuc-shard-00-01.mvcys6r.mongodb.net:27017,ac-3ahszuc-shard-00-02.mvcys6r.mongodb.net:27017/?ssl=true&replicaSet=atlas-t4xjip-shard-0&authSource=admin&retryWrites=true&w=majority")
        col.drop()
        db = client['youtube']
        col = db['view']
        col.insert_many(final_dict)
        st.write("loading process completed")

        # creating ad dataframe from mongo db
        df_channel = {'channelname': [],'channelid': [], 'channeldescription': [], 'channelsubscribers': [], 'channelviewcount': [], 'channelvideocount': [], 'playlistid': []}
        db=col.find()
        for i in db:
          id = i.get('CHANNEL_ID')
          df_channel['channelid'].append(id['channel_id'])
          df_channel['channelname'].append(id['channel_name'])
          df_channel['channeldescription'].append(id['channel_description'])
          df_channel['channelsubscribers'].append(id["channel_subscribers"])
          df_channel['channelviewcount'].append(id['channel_view_count'])
          df_channel['channelvideocount'].append(id['channel_video_count'])
          df_channel['playlistid'].append(id['playlist_id'])
        df_channel["channelsubscribers"] = pd.to_numeric(df_channel['channelsubscribers'])
        df_channel["channelviewcount"] = pd.to_numeric(df_channel['channelviewcount'])
        df_channel["channelvideocount"] = pd.to_numeric(df_channel['channelvideocount'])


        channel = pd.DataFrame(df_channel)
        channel.to_sql('channel', engine, if_exists='replace', index=False)         # inserting a dataframe into sql using to.sql() method

        df_video = {"VideoId": [], 'playlistid': [], "VideoName": [], "VideoDescription": [], "VideoTags": [], "VideoPublishedAt" : [], "VideoViewCount": [], "VideoLikeCount": [], "VideoFavouriteCount": [], "VideoCommentCount": [], "VideoDuration": [], "Thumbnail": [], "CaptionStatus": []}
        df_comment = {"CommentId": [], "VideoId": [], "CommentText": [], "CommentAuthor": [], "CommentPublishedAt":[]}

        db = col.find()
        for i in db:                            #getting all data from db
          vid = i.get('VIDEO_ID')

        for k in range(1,len(vid)+1):
          vid1 = vid[f'videos_id{k}']
          df_video["VideoId"].append(vid1['Video_Id'])
          df_video['playlistid'].append(id['playlist_id'])
          df_video['VideoName'].append(vid1['Title'])
          df_video['VideoDescription'].append(vid1['Description'])
          df_video['VideoTags'].append(vid1['Tags'])
          df_video['VideoPublishedAt'].append(vid1['Published At'])
          df_video['VideoViewCount'].append(vid1['View Count'])
          df_video['VideoLikeCount'].append(vid1['Like Count'])
          df_video['VideoFavouriteCount'].append(vid1['Favorite Count'])
          df_video['VideoCommentCount'].append(vid1['Comment Count'])
          df_video['VideoDuration'].append(vid1['Duration'])
          df_video['Thumbnail'].append(vid1['Thumbnail'])
          df_video['CaptionStatus'].append(vid1['Caption'])
          df_comment["CommentId"].append(vid1['comment']['Comment_Id'])
          df_comment["VideoId"].append(vid1['Video_Id'])
          df_comment["CommentAuthor"].append(vid1['comment']['Comment_Author'])
          df_comment["CommentText"].append(vid1['comment']['Comments_text'])
          df_comment["CommentPublishedAt"].append(vid1['comment']['Comment_PublishedAt'])
        df_video["VideoViewCount"] = pd.to_numeric(df_video['VideoViewCount'])
        df_video["VideoLikeCount"] = pd.to_numeric(df_video['VideoLikeCount'])
        df_video["VideoFavouriteCount"] = pd.to_numeric(df_video['VideoFavouriteCount'])
        df_video["VideoCommentCount"] = pd.to_numeric(df_video['VideoCommentCount'])


        videos = pd.DataFrame(df_video)
        videos.to_sql('video',engine, if_exists='replace', index=False)



        comments = pd.DataFrame(df_comment)
        comments.to_sql('comment',engine, if_exists='replace',index=False)
        st.subheader("LIST OF TABLES")
        st.write("### CHANNEL TABLE")
        st.dataframe(channel)
        st.write("### VIDEO TABLE")                                                         #displaying a dataframe in streamlit
        st.dataframe(videos)
        st.write("### COMMENTS TABLE ")
        st.dataframe(comments)


if option =="TABLES":
    st.title("INSIGHTS")
    query = ('select channelname from channel')
    nk.execute(query)
    x= nk.fetchall()
    st.write(f'### Channel Name - {x[0][0]}')
    options=['Names of all videos','Total Number of Videos','Top 10 Most Viewed Video','Total No Of Comments On Each Video','Highest Number Of Likes','Total Number Of Likes And Dislikes on Each Video','Total No Of Views','Duration Of All Videos','Highest No Of Comments']
    select_query = st.selectbox('CHOOSE ANY TABLE',options)
    if select_query=='Names of all videos':
        query = ('select "VideoName" from video')
        nk.execute(query)
        x = nk.fetchall()
        a = pd.DataFrame(x, columns=['VideoName'])
        st.dataframe(a)
    if select_query == 'Total Number of Videos':
        query = ('select channelvideocount from channel')
        nk.execute(query)
        x = nk.fetchall()
        a = pd.DataFrame(x, columns=['TotalVideoCount'])
        st.dataframe(a)
    if select_query == 'Top 10 Most Viewed Video':
        query = ('select "VideoName","VideoViewCount" from video order by "VideoViewCount" DESC limit 10')
        nk.execute(query)
        x = nk.fetchall()
        a = pd.DataFrame(x, columns=['VideoName','VideoViewCount'])
        st.dataframe(a)
        fig = px.bar(a, y='VideoName', x="VideoViewCount", title=f' Top 10 Most Viewed Video',
                     color="VideoViewCount", hover_data=['VideoName','VideoViewCount'])
        fig.update_traces(texttemplate='%{x}', textposition='outside', textfont=dict(size=20))
        fig.update_layout(width=900, height=900)
        st.plotly_chart(fig)
    if select_query == 'Total No Of Comments On Each Video':
        query = ('select "VideoName","VideoCommentCount" from video order by "VideoCommentCount" DESC ')
        nk.execute(query)
        x = nk.fetchall()
        a = pd.DataFrame(x, columns=['VideoName', 'VideoCommentCount'])
        st.dataframe(a)
        fig = px.bar(a, y='VideoName', x="VideoCommentCount", title=f' Top 10 Most Viewed Video',
                     color="VideoCommentCount", hover_data=['VideoName', 'VideoCommentCount'])
        fig.update_traces(texttemplate='%{x}', textposition='outside', textfont=dict(size=20))
        fig.update_layout(width=900, height=900)
        st.plotly_chart(fig)

    if select_query == 'Highest Number Of Likes':
        query = ('select "VideoName","VideoLikeCount" from video order by "VideoLikeCount" DESC limit 10')
        nk.execute(query)
        x = nk.fetchall()
        a = pd.DataFrame(x, columns=['VideoName', 'VideoLikeCount'])
        st.dataframe(a)
        fig = px.bar(a, y='VideoName', x="VideoLikeCount", title=f' Top 10 Most Viewed Video',
                     color="VideoLikeCount", hover_data=['VideoName', 'VideoLikeCount'])
        fig.update_traces(texttemplate='%{x}', textposition='outside', textfont=dict(size=20))
        fig.update_layout(width=900, height=900)
        st.plotly_chart(fig)

    if select_query == 'Total Number Of Likes And Dislikes on Each Video':
        query = ('select "VideoName","VideoLikeCount" from video order by "VideoLikeCount" DESC')
        nk.execute(query)
        x = nk.fetchall()
        a = pd.DataFrame(x, columns=['VideoName', 'VideoLikeCount'])
        st.dataframe(a)
    if select_query == 'Total No Of Views':
        query = ('select "channelviewcount" from channel;')
        nk.execute(query)
        x = nk.fetchall()
        a = pd.DataFrame(x, columns=['ChannelViewCount'])
        st.dataframe(a)
    if select_query == 'Duration Of All Videos':
        query = ('select "VideoName","VideoDuration" from video')
        nk.execute(query)
        x = nk.fetchall()
        a = pd.DataFrame(x,columns=['VideoName', 'VideoDuration'])
        st.dataframe(a)
    if select_query == 'Highest No Of Comments':
        query = ('select "VideoName","VideoCommentCount" from video order by "VideoCommentCount" DESC limit 1')
        nk.execute(query)
        x = nk.fetchall()
        a = pd.DataFrame(x, columns=['VideoName', 'VideoCommentCount'])
        st.dataframe(a)


if option =="CONCLUSION":
    st.header("OUTCOMES OF THIS PROJECT")
    st.subheader("NEED")
    st.write(" Extracting data from YouTube satisfies  various needs . Some of the requirements are,")
    st.write("1. Video Analytics -  Extracting data related to video performance, such as views, likes, dislikes, comments, engagement rates, and demographics of the viewers")
    st.write("2. Channel Analytics - Gathering information about a YouTube channel, including subscriber count, total views, growth rate, audience demographics, and engagement metrics.")
    st.write("3. Trend Analysis - Extracting data on trending videos, popular topics, and viral content to understand the current trends and user preferences on YouTube.")

    st.subheader("RESULTS")

    st.write("This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a MongoDB database, migrates it to a SQL data warehouse, and enables users to search for channel details and join tables to view data in the Streamlit app.")
    st.markdown("##### Here, we can  retrieve all the relevant data like Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of all  video using Google API by giving Youtube channel Id as input.")
    st.write("#### By scrapping and gaining the data from Youtube, we can apply those relevant datas and insights  for our business approach")