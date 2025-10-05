import streamlit as st
import pandas as pd
import requests

API_BASE = "http://localhost:8000"
USER_ID = 1  

st.set_page_config(page_title="Kaggle Dataset Search", layout="wide")
st.title("📊 Kaggle Dataset Search App")

# --- Tabs ---
tab_search, tab_collections = st.tabs(["🔍 Search Datasets", "📁 My Collections"])

# --- Load user's current collections upfront ---
def get_user_collections(user_id):
    try:
        resp = requests.get(f"{API_BASE}/datasets/{user_id}")
        resp.raise_for_status()
        datasets = resp.json()
        seen_refs = set()
        collections = []
        for ds in datasets:
            ref = ds.get("dataset_ref")
            if ref not in seen_refs:
                seen_refs.add(ref)
                collections.append(ds)
        return collections
    except requests.exceptions.RequestException:
        return []

user_collections = get_user_collections(USER_ID)
user_refs = {ds.get("dataset_ref") for ds in user_collections}

# --- TAB 1: SEARCH ---
with tab_search:
    if "search_results" not in st.session_state:
        st.session_state.search_results = None

    query = st.text_input("Enter search query:")

    if st.button("Search"):
        if not query.strip():
            st.warning("Please enter a search query!")
        else:
            try:
                resp = requests.get(f"{API_BASE}/search", params={"query": query})
                resp.raise_for_status()
                data = resp.json()

                if not data:
                    st.info("No results found.")
                    st.session_state.search_results = None
                else:
                    df = pd.DataFrame(data)
                    st.session_state.search_results = df
                    st.success(f"Found {len(df)} results")

            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")

    if st.session_state.search_results is not None:
        df = st.session_state.search_results
        for i, row in df.iterrows():
            ref = row['ref']
            url = f"https://www.kaggle.com/datasets/{ref}"

            with st.container():
                st.markdown(f"### {row['title']}")
                st.markdown(f"[🔗 View on Kaggle]({url})")

                if ref in user_refs:
                    st.info("✅ Already in your collection")
                else:
                    if st.button(f"Add to Collection", key=f"add_{i}"):
                        try:
                            # Import dataset (Mongo + Embedding)
                            import_resp = requests.post(
                                f"{API_BASE}/datasets/import",
                                params={"dataset_ref": ref, "user_id": USER_ID}
                            )
                            import_resp.raise_for_status()
                            import_result = import_resp.json()

                            # Create record in Postgres
                            payload = {
                                "dataset_ref": ref,
                                "collection_name": f"user_{USER_ID}_datasets"
                            }
                            pg_resp = requests.post(
                                f"{API_BASE}/datasets/{USER_ID}",
                                json=payload
                            )
                            pg_resp.raise_for_status()
                            pg_result = pg_resp.json()

                            st.success(
                                f"✅ Added `{ref}` to your collection "
                                f"(Inserted {import_result.get('inserted',0)} rows)"
                            )
                            user_refs.add(ref)

                        except requests.exceptions.RequestException as e:
                            st.error(f"Error adding dataset: {e}")

# --- TAB 2: COLLECTIONS ---
with tab_collections:
    st.subheader("📁 My Collections")

    if not user_collections:
        st.info("You have no datasets yet.")
    else:
        for ds in user_collections:
            ref = ds.get("dataset_ref")
            url = f"https://www.kaggle.com/datasets/{ref}"
            with st.expander(ref):
                st.markdown(f"- **Collection:** {ds.get('collection_name', 'N/A')}")
                st.markdown(f"- **View on Kaggle:** [🔗 Link]({url})")
