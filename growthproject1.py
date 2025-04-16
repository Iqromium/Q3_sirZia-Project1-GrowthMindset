import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Project 1 - Iqra's Artist Finder",
    page_icon="🎨",
    layout='wide'
)

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E90FF;
        color: #FFD700;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & description
st.title("🎨 IQRA's Artist Finder 🕵️🔍 - Iqra Kalim")
st.write("Peek into a variety of artists and their inspired work. Available in CSV & Excel formats here.")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your list of artists (CSV or Excel):",
    type=["csv", "xlsx"],
    accept_multiple_files=False
)

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

    try:
        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
    except Exception as e:
        st.error(f"Error reading file: {e}")
    else:
        st.subheader("🎭 Preview of Artists Data")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🧹 Data Cleaning Options")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Remove Duplicates"):
                df.drop_duplicates(inplace=True)
                st.success("Duplicates removed!")

        with col2:
            if st.button("Fill Missing Numeric Values"):
                numeric_cols = df.select_dtypes(include=['int', 'float']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("Missing numeric values filled!")

        # Display selected columns
        st.subheader("🎯 Artists That Inspire Us Most")
        selected_columns = st.multiselect("Select columns to display", df.columns.tolist(), default=df.columns.tolist())
        st.dataframe(df[selected_columns])

        # Visualization
        st.subheader("📊 Graphical Representation of Artists")
        if st.checkbox("Show bar chart"):
            numeric_df = df.select_dtypes(include='number')
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.warning("No numeric data available for chart.")

        # File Conversion
        st.subheader("📤 Convert and Download File")

        conversion_type = st.radio("Choose format to convert to:", ["CSV", "Excel"])

        if st.button("Convert & Download"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                mime_type = "text/csv"
                new_filename = uploaded_file.name.replace(file_ext, ".csv")
            else:
                df.to_excel(buffer, index=False)
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_filename = uploaded_file.name.replace(file_ext, ".xlsx")

            buffer.seek(0)

            st.download_button(
                label=f"Download as {conversion_type}",
                data=buffer,
                file_name=new_filename,
                mime=mime_type
            )

        st.success("🎉 Artist Finder is ready for you!")
