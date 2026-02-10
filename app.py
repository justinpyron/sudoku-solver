import streamlit as st

st.set_page_config(
    page_title="Sudoku Solver",
    page_icon="🧩",
    layout="centered",
)

# --- Header ---
st.title("Sudoku Solver")
st.caption("Snap a photo. Get the solution.")

# --- Image uploader ---
uploaded_file = st.file_uploader(
    "Upload a puzzle screenshot",
    type=["png", "jpg", "jpeg"],
)

if uploaded_file is not None:
    st.image(uploaded_file, use_container_width=True)
