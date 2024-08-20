import streamlit as st
import langchain_helper

st.title("Resturant Name Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Indian", "Italian", "Mexican", "Arabic", "American"))

if cuisine:
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)
    st.header(response['restaurant_name'].strip())
    # Display menu items
    menu_items = response['menu_items'].strip()
    if menu_items:
        menu_items_list = [item.strip() for item in menu_items.split(",")]
        st.write("**Menu Items**")
        for item in menu_items_list:
            st.write(f"- {item}")
    else:
        st.write("No menu items available.")
        
        