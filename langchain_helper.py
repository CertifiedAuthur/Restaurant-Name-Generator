from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(temperature=0.7)

def generate_restaurant_name_and_items(cuisine):
    llm = OpenAI(temperature=0.7)

    prompt_template_name = PromptTemplate(
        input_variables = ['cuisine'],
        template = "Suggest a fancy name for a restaurant that serves {cuisine} food. Provide the name without quotes."
    )

    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    llm = OpenAI(temperature=0.7)

    prompt_template_items = PromptTemplate(
        input_variables = ['restaurant_name'],
        template = "Suggest some menu items for {restaurant_name}."
    )

    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")
    
    chain = SequentialChain(
    chains = [name_chain, food_items_chain],
    input_variables = ['cuisine'],
    output_variables = ['restaurant_name', 'menu_items']
    )
    response = chain({'cuisine': 'cuisine'})
    
    return response

if __name__ == "__main__":
    print(generate_restaurant_name_and_items("italian"))