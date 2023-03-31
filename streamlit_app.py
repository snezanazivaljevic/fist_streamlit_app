import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#import streamlit
streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega3 & Bluberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie ')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruit_selected]

streamlit.dataframe(fruits_to_show)
streamlit.header('Fruityvice Fruit Advice')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please selec the fruit to get information")
    else:
        #streamtlit.write('The user entered ', fruit_choice)
        #import requests
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        #streamlit.text(fruityvice_response.json())
        # Takes json format and formalize it
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        # put output as table
        streamlit.dataframe(fruityvice_normalized)

except URLError as e:
      streamlit.error()

streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains ")
streamlit.dataframe(my_data_row)
add_my_fruit = streamlit.text_input('What fruit would you like ito add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
