import pandas as pd
import streamlit as st
import plotly.express as px

dataset=pd.read_excel('Book1.xlsx')

st.set_page_config(page_title='🏪Sales',layout='wide')

st.sidebar.header('🔍Filter BY:')

category=st.sidebar.multiselect('Filter By Category:',
                                options=dataset['Region'].unique(),
                                default=dataset['Region'].unique())

selection_query=dataset.query(
     "Region== @category"
)

st.title('Superstore Dataset🛍️')



total_profit=round((selection_query['Profit'].sum()/1000),2)
avg_sales=round((selection_query['Sales'].mean()),2)




first_column,second_column=st.columns(2)



st.markdown('---')

profit_by_category=(selection_query.groupby(by=['Region']).sum()[['Profit']])

profit_by_category_barchart=px.bar(profit_by_category,
                                x="Profit",
                                y=profit_by_category.index,
                                title='Profit by Region 📊',
                                color_discrete_sequence=['#17f50c'],
                                )
profit_by_category_barchart.update_layout(plot_bgcolor = 'rgba(0,0,0,0)',xaxis=(dict(showgrid=False)))
    

avg_sales_by_category=(selection_query.groupby(by=['Region']).mean()[['Sales']])

avg_sales_by_category_piechart=px.pie(avg_sales_by_category, 
                                      names= avg_sales_by_category.index, 
                                      values= 'Sales', 
                                      title='Average Sales % By Region', 
                                      hole=.3, 
                                      color=avg_sales_by_category.index, 
                                      color_discrete_sequence=['red', 'yellow', 'green', 'blue', 'pink', 'yellow'])




left_column,right_column=st.columns(2)
left_column.plotly_chart(profit_by_category_barchart,use_container_width=True)
right_column.plotly_chart(avg_sales_by_category_piechart,use_container_width=True)

hide="""
       <style>
       #MainMenu {visibility:hidden;}
       footer {visibility:hidden;}
       header {visibility:hidden}
       </style>
    """
st.markdown(hide,unsafe_allow_html=True)

left_column, right_column = st.columns(2)



highest_profit_region = selection_query.groupby(by=['Region']).sum()[['Profit']].idxmax()[0]
highest_profit = round(selection_query.groupby(by=['Region']).sum()[['Profit']].max()[0],2)

highest_sales_region = selection_query.groupby(by=['Region']).mean()[['Sales']].idxmax()[0]
highest_sales = round(selection_query.groupby(by=['Region']).mean()[['Sales']].max()[0],2)

with first_column:
    st.markdown('## Highest Profit Region:')
    st.subheader(highest_profit_region)
    st.markdown('### Profit:')
    st.subheader(f'{highest_profit} $')

with second_column:
    st.markdown('## Highest Average Sales Region:')
    st.subheader(highest_sales_region)
    st.markdown('### Sales:')
    st.subheader(f'{highest_sales} $')
