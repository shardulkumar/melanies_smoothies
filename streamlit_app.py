# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# adding name input to the form
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be: {name}".format(name=name_on_order))

# get the session object
cnx = st.connection("snowflake")
session = cnx.session()

# get the data from fruit_options table into a dataframe
df_fruit_options = session \
    .table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS") \
    .select(col("fruit_name"))

# use the dataframe from fruit_options table to feed into the streamlit app
# st.dataframe(data=df_fruit_options, use_container_width=True)

ingredient_list = st.multiselect(
      "Choose up to 5 ingredients:"
    , df_fruit_options
    , max_selections=5
)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

if ingredient_list:    
    ingredients_string = ""
    for ingredient in ingredient_list:
        ingredients_string += ingredient + " "

    # st.text(ingredients_string)

    my_insert_stmt = """
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
