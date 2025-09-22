import streamlit as st


st.title("Goodnature")

pg = st.navigation([
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/trend.py", title="Trends"),
    st.Page("pages/heatmap.py", title="Heat Map"),
    st.Page("pages/heatmap2.py", title="Territorial Heat Map"),
    st.Page("pages/scatter_plots.py", title="Scatter Plots"),
    st.Page("pages/journals.py", title="Journals")])
st.set_page_config(page_title="Goodnature - Data Analysis", page_icon=":material/home:")
pg.run()
