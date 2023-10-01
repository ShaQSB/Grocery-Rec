import streamlit as st
import pandas as pd
import pickle
import random
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import pathlib as Path


st.set_page_config(page_title="Grocery Recommendation System", page_icon="🍎")


st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    .chatbot-nav {
        background-color: #007BFF;
        padding: 10px;
        border-radius: 10px;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    .chatbot-nav a {
        text-decoration: none;
        color: white;
        font-weight: bold;
        margin: 0 10px;
        padding: 5px 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .chatbot-nav a:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

df1 = pickle.load(open('Grocery1.pkl', 'rb'))
similarity = pickle.load(open('similarityUpdated.pkl', 'rb'))

def home():
    st.title("Grocery List")
    st.header("Featured Products")

    df1_shuffled = df1.sample(frac=1, random_state=42)

    items_per_row = 3
    max_items_to_display = 50

    num_rows = max_items_to_display // items_per_row

    for row in range(num_rows):
        row_layout = st.columns(items_per_row)

        for col in range(items_per_row):
            index = row * items_per_row + col

            if index < max_items_to_display:
                product_info = {
                    "Image_Url": df1_shuffled['Image_Url'].iloc[index],
                    "ProductName": df1_shuffled['ProductName'].iloc[index],
                    "Brand": df1_shuffled['Brand'].iloc[index],
                    "Price": df1_shuffled['Price'].iloc[index],
                    "Category": df1_shuffled['Category'].iloc[index]
                }

                product_card = f"""
                <div style="background-color: white; border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; display: flex; flex-direction: column; align-items: flex-start;">
                    <img src="{product_info['Image_Url']}" style="max-width: 100%; height: auto;">
                    <h4 style="text-align: left;">{product_info['ProductName']}</h4>
                    <p>Brand: {product_info['Brand']}</p>
                    <p>Price: {product_info['Price']}</p>
                    <p>Category: {product_info['Category']}</p>
                   
                </div>
                """

                row_layout[col].write(product_card, unsafe_allow_html=True)

def product_search():
    st.title("Product Search")
    select_value = st.text_input('Search for a Product')
    search_button = st.button('Search')

    if search_button:

        def recommended(Product):

            if Product in df1['ProductName'].values:
                index = df1[df1['ProductName'] == Product].index[0]
                distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
                recom = []
                recpic = []
                for i in distance[0:10]:
                    recpic.append(df1.iloc[i[0]].Image_Url)
                    recom.append(df1.iloc[i[0]].ProductName)

                return recom, recpic
            else:
                return []

        rec_names, rec_images = recommended(select_value)

        if rec_names:
            st.write("Recommended Products:")

            items_per_row = 3

            num_rows = len(rec_names) // items_per_row + (len(rec_names) % items_per_row > 0)

            for row in range(num_rows):
                row_layout = st.columns(items_per_row)

                for col in range(items_per_row):
                    index = row * items_per_row + col

                    if index < len(rec_names):
                        product_card = f"""
                        <div style="background-color: white; border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; display: flex; flex-direction: column; align-items: flex-start;">
                            <img src="{rec_images[index]}" style="max-width: 100%; height: auto;">
                            <h4 style="text-align: left;">{rec_names[index]}</h4>
                            <p>Brand: {df1[df1['ProductName'] == rec_names[index]]['Brand'].values[0]}</p>
                            <p>Price: {df1[df1['ProductName'] == rec_names[index]]['Price'].values[0]}</p>
                            <p>Category: {df1[df1['ProductName'] == rec_names[index]]['Category'].values[0]}</p>
                            
                        </div>
                        """

                        row_layout[col].write(product_card, unsafe_allow_html=True)
        else:
            st.write("Product not found.")

def contact():
    st.title("Contact")
    st.image("https://img.freepik.com/free-photo/hot-line-contact-us-call-center-search-interface_53876-124009.jpg", caption="Contact us for any inquiries or support.")
    st.write("You can reach us at:")
    st.write("Email: contact@example.com")
    st.write("Phone: +91 99999 99999")
    st.write("Address: 123 Main Street, City, Country")

def about():
    st.title("About")
    st.image("https://img.freepik.com/free-vector/contact-us-concept-landing-page_52683-12860.jpg?w=2000")
    st.write("Learn more about our Grocery Recommendation System.")
    st.write("Our Grocery Recommendation System is designed to help you discover and find the best grocery products available in the market. Whether you're looking for your favorite brands or exploring new options, our system can provide you with personalized recommendations based on your preferences.")
    st.write("Feel free to explore our app, search for products, and discover exciting grocery items that match your taste and needs.")



with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Product Search',"Contact","About"],
        icons=['','house', 'search','telephone-forward','file-person'], menu_icon=" ", default_index=0)
    selected

#navigation = st.sidebar.radio(" ", ["Home 🏠", "Product Search 🔍", "Contact 📞", "About ℹ️"])

if selected == "Home":
    home()
elif selected == "Product Search":
    product_search()
elif selected == "Contact":
    contact()
elif selected == "About":
    about()

