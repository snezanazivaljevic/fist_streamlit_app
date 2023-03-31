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
#import requests 

def get_fruityvice_data(this_fruit_choice):
 
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # Takes json format and formalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    #streamlit.text(fruityvice_response.json())
    return fruityvice_normalized

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select the fruit to get information")
    else:     
        #streamtlit.write('The user entered ', fruit_choice)   
        back_from_function=get_fruityvice_data(fruit_choice)
        # put output as table
        streamlit.dataframe(back_from_function)
        
except URLError as e:
      streamlit.error()

#streamlit.stop()

#import snowflake.connector

streamlit.text("The fruit load list contains ")
#Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()
#add a botton to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row=get_fruit_load_list()
  streamlit.dataframe(my_data_row)





add_my_fruit = streamlit.text_input('What fruit would you like ito add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
