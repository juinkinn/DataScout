import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Kaggle Dataset Search", layout="wide")
st.title("Kaggle Dataset Search App")

if "search_results" not in st.session_state:
    st.session_state.search_results = None

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
                st.session_state.search_results = df  
                st.success(f"Found {len(df)} results")

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from API: {e}")

if st.session_state.search_results is not None:
    df = st.session_state.search_results

    for i, row in df.iterrows():
        with st.container():
            st.write(f"**{row['title']}** ({row['ref']})")
            
            st.markdown(f"[🔗 Kaggle link]({row['url']})")

            if st.button(f"Download {row['ref']}", key=f"dl_{i}"):
                try:
                    dl_response = requests.post(
                        "http://localhost:8000/datasets/download",
                        params={
                            "dataset_ref": row["ref"],
                            "collection_name": "kaggle_datasets",
                            "user_id": "test_user"
                        }
                    )
                    dl_response.raise_for_status()
                    result = dl_response.json()
                    st.success(f"✅ Downloaded {row['ref']} - Inserted {result.get('inserted',0)} rows")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error downloading dataset: {e}")


    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name="kaggle_search_results.csv",
        mime="text/csv"
    )
