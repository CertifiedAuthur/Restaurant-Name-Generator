import streamlit as st
import openai
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Variable to store the API key
api_key = None

# Function to set the OpenAI API key
def set_api_key(key):
    global api_key
    api_key = key
    openai.api_key = api_key

# Function to check if the API key is set
def is_api_key_set():
    return api_key is not None

# Function to generate restaurant name and menu items
def generate_restaurant_name_and_items(cuisine):
    if not is_api_key_set():
        raise ValueError("API key not set. Please provide an API key.")
    
    try:
        llm = OpenAI(openai_api_key=api_key, temperature=0.7)
    except Exception as e:
        st.error(f"Failed to initialize OpenAI: {e}")
        return None

    # Prompt template for generating restaurant name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="Suggest a fancy name for a restaurant that serves {cuisine} food. Provide the name without quotes."
    )

    # Chain to generate restaurant name
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    # Prompt template for generating menu items
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some menu items for {restaurant_name}."
    )

    # Chain to generate menu items
    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")

    # Sequential chain to link name and menu items generation
    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']
    )

    # Execute the chain with the given cuisine
    response = chain({'cuisine': cuisine})
    
    return response

# Streamlit app
st.title("Restaurant Name Generator")

# Sidebar input for OpenAI API key
api_key_input = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Button to set the API key
if st.sidebar.button("Set API Key"):
    set_api_key(api_key_input)
    st.sidebar.success("API Key set successfully!")

# Check if API key is provided and set
if is_api_key_set():
    # Cuisine selection
    cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Indian", "Italian", "Mexican", "Arabic", "American"))

    if cuisine:
        # Generate restaurant name and menu items
        response = generate_restaurant_name_and_items(cuisine)
        
        if response:
            st.header(response['restaurant_name'].strip())
            menu_items = response['menu_items'].strip().split(",")
            st.write("**Menu Items**")
            
            for item in menu_items:
                st.write("-", item)
else:
    st.warning("Please enter your OpenAI API Key to use the application.")
