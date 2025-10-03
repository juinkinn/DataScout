import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Kaggle Dataset Search", layout="wide")
st.title("Kaggle Dataset Search App")

query = st.text_input("Enter search query:")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search query!")
    else:
        try:
            response = requests.get("http://localhost:8000/search", params={"query": query})
            response.raise_for_status()
            
            data = response.json()
            if not data:
                st.info("No results found.")
            else:
                df = pd.DataFrame(data)
                st.success(f"Found {len(df)} results")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download results as CSV",
                    data=csv,
                    file_name="kaggle_search_results.csv",
                    mime="text/csv"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from API: {e}")
