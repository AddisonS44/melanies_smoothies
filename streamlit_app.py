# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input('Name on smoothie')
if name_on_order:
    st.write(f'Thank you for ordering, {name_on_order}!')

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections = 5)

if ingredients_list:
    if len(ingredients_list) > 5:
        st.write('Too many fruits!')
    else:
        st.write(ingredients_list)
        st.text(ingredients_list) 

        ingredients_string = ''

        for fruit in ingredients_list:
            ingredients_string += fruit + ' '
            st.subheader(fruit + ' Nutrition Information')
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        # st.write(ingredients_string.strip())

        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

        # st.write(my_insert_stmt)
        # st.stop()
        time_to_insert = st.button('Submit Order')
    
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "Apple")
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "Blueberry")
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "Cantalope")
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "Dragonfruit")
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "Elderberry")
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
