import streamlit
import pandas as pd
import requests
from urllib.error import URLError
import snowflake.connector

def get_fruityvice_data(fruit):
  return pd.json_normalize(requests.get("https://fruityvice.com/api/fruit/" + fruit).json())

def get_fruit_load_list(my_cnx):
  with my_cnx.cursor() as cur:
    cur.execute('select * from fruit_load_list;')
    return cur.fetchall()
  
def insert_row(my_cnx, fruit):
  with my_cnx.cursor() as cur:
    cur.execute('insert into fruit_load_list VALUES (%s);', fruit)
    return ("Thanks for adding %s", fruit)

streamlit.title('My parents new healthy diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
fruit_list = fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
selected_fruits = streamlit.multiselect("Pick some fruits:", list(fruit_list.index), ['Avocado', 'Strawberries'])

# Display the table on the page.
streamlit.dataframe(fruit_list.loc[selected_fruits])

streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Select a fruit')
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()

if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.dataframe(get_fruit_load_list(my_cnx))

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.text(insert_row(add_my_fruit, my_cnx))
