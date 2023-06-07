import streamlit
import pandas as pd
import requests

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
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.dataframe(pd.json_normalize(fruityvice_response.json()))


