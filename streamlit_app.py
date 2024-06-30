# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd


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
    .select(col("fruit_name"), col("search_on"))

pd_df = df_fruit_options.to_pandas()
st.dataframe(pd_df)
# st.stop()

ingredient_list = st.multiselect(
      "Choose up to 5 ingredients:"
    , df_fruit_options
    , max_selections=5
)

if ingredient_list:    
    ingredients_string = ""
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + " "

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)

    my_insert_stmt = """
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
