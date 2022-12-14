import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("Happy Restaurant")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + choice)
  # take json version of response and normalize
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  # display on screen
  return fruityvice_normalized
  

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
  
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list;")
    return my_cur.fetchall()

# snowflake

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into fruit_load_list values('{new_fruit}')")
    return 'Thanks for adding ' + new_fruit
  
streamlit.header("Fruit load list contains:")
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
if streamlit.button("Get Fruit Load List"):
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like add?','jackfruit')
if streamlit.button("Add a fruit to the list"):
  info = insert_row_snowflake(add_my_fruit)
  streamlit.text(info)
my_cnx.close()
  

