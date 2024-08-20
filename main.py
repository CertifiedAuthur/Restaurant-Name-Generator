import streamlit as st
import langchain_helper

# Streamlit app
st.title("Restaurant Name Generator")

# Sidebar input for OpenAI API key
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Button to set API key
if st.sidebar.button("Enter"):
    if api_key:
        # Set the OpenAI API key
        langchain_helper.set_api_key(api_key)
        st.success("API Key set successfully!")
    else:
        st.warning("Please enter your OpenAI API Key.")

# Only show cuisine options if the API key has been set
if api_key and langchain_helper.is_api_key_set():
    # Cuisine selection
    cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Indian", "Italian", "Mexican", "Arabic", "American"))

    if cuisine:
        # Generate restaurant name and menu items
        response = langchain_helper.generate_restaurant_name_and_items(cuisine)
        
        st.header(response['restaurant_name'].strip())
        menu_items = response['menu_items'].strip().split(",")
        st.write("**Menu Items**")
        
        for item in menu_items:
            st.write("-", item)
else:
    st.warning("Please enter and set your OpenAI API Key to use the application.")
