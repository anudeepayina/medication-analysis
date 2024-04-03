import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Medication Market Analysis",
        page_icon="👋",
    )

    st.title('Indication X Market Analysis')

    ## Load Data
    df = pd.read_csv('data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    # st.write(df)

    ## Metrics generation and rendering
    df_total = df.groupby(['Brand']).agg({"Quantity":"count"}).rename(columns={"Quantity":"Total Sales"}).reset_index()

    df_monthly_total = df.groupby([pd.Grouper(key='Date',freq='M'), 'Brand']).agg({"Quantity":"count"}).rename(columns={"Quantity":"Total Monthly Sales"}).reset_index()

    df_total['Rank'] = df_total['Total Sales'].rank(ascending=False).astype(int)
    # Metrics
    total_sales = df_total.loc[df_total['Brand']=='Brand H'].reset_index()['Total Sales'][0]
    
    current_monthly_sales = df_monthly_total.loc[(df_monthly_total['Brand']=='Brand H') & (df_monthly_total['Date']=='2023-10-31 00:00:00')].reset_index()['Total Monthly Sales'][0]
    prev_monthly_sales = df_monthly_total.loc[(df_monthly_total['Brand']=='Brand H') & (df_monthly_total['Date']=='2023-09-30 00:00:00')].reset_index()['Total Monthly Sales'][0]
    delta = int(current_monthly_sales) - int(prev_monthly_sales)

    overall_mp = df_total.loc[(df_total['Brand']=='Brand H')].reset_index()['Rank'][0]

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label='Total Sales', value=int(total_sales))

    with col2:
        st.metric(label='Current Market Position', value = int(overall_mp))   

    # with col3:


    with col4:
        st.metric(label='Current Monthly Sales',value=int(current_monthly_sales), delta=delta,delta_color="normal")


if __name__ == "__main__":
    run()
