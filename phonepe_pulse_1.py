# Importing Libraries
import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

#____________________________________________________________________________________________________

#MySQL connection
connection  = mysql.connector.connect(user='root', 
                                      password='YOUR_PASSWORD', #Enter your password
                                      host='localhost', 
                                      database="phonepe_pulse") #Enter your database name

cursor = connection.cursor()

#Aggregated_transaction
cursor.execute("select * from aggre_transcation;")
table1 = cursor.fetchall()
aggre_transaction = pd.DataFrame(table1,columns = ("State", "Year", "Quarter", 
                                                   "Transaction_Type", "Transaction_Count", "Transaction_Amount"))

#Aggregated_user
cursor.execute("select * from aggre_user")
table2 = cursor.fetchall()
aggre_user = pd.DataFrame(table2,columns = ("State", "Year", "Quarter",
                                            "Brand", "Brand_T_Count", "Brand_T_Percentage"))

#Map_transaction
cursor.execute("select * from map_transaction")
table3 = cursor.fetchall()
map_transaction = pd.DataFrame(table3,columns = ("State", "Year", "Quarter", 
                                                 "District", "District_T_Count", "District_T_Amount"))

#Map_user
cursor.execute("select * from map_user")
table4 = cursor.fetchall()
map_user = pd.DataFrame(table4,columns = ("State", "Year", "Quarter", 
                                          "District", "District_Reg_User", "App_Opens"))

#Top_transaction
cursor.execute("select * from top_transaction")
table5 = cursor.fetchall()
top_transaction = pd.DataFrame(table5,columns = ("State", "Year", "Quarter", 
                                                 "Pincode", "Pincode_T_Count", "Pincode_T_Amount"))

#Top_user
cursor.execute("select * from top_user")
table6 = cursor.fetchall()
top_user = pd.DataFrame(table6, columns = ("State", "Year", "Quarter", 
                                           "Pincode", "Pincode_Reg_User"))

cursor.close()
connection.close()

#_______________________________________Streamlit_Code_______________________________________________________


# page configuration
icon = Image.open(r" #path of your icon")
st.set_page_config(
    page_title="PhonePe Pulse",
    page_icon=icon,
    layout="wide")

st.markdown("# :orange[₹ PhonePe Pulse Analysis (2018-2022)]")


c1,c2,c3,c4 = st.columns([6,1,1.4,1.5])

with c2:
    y = ['2018', '2019', '2020', '2021', '2022', '2023']
    default_y = y.index("2023")
    year = st.selectbox('Year', y, key='year', index = default_y)

with c3:
    q = ['Q1 (Jan-Mar)', 'Q2 (Apr-June)', 'Q3 (July-Sep)','Q4 (Oct-Dec)']
    default_q = q.index("Q1 (Jan-Mar)")
    quarter = st.selectbox('Quarter', q, key='quarter', index=default_q)
    if quarter == 'Q1 (Jan-Mar)': quarter = 1
    elif quarter == 'Q2 (Apr-June)': quarter = 2
    elif quarter == 'Q3 (July-Sep)': quarter = 3
    elif quarter == 'Q4 (Oct-Dec)': quarter = 4
       
with c4:
    Type = ["Transaction", "User"]
    default_i = Type.index("Transaction")
    Type = st.selectbox('Type', Type, key='view',index = default_i)

#_____________________________________________________

#Formats a given number into an Indian-style currency representation in crores.
def format_crore_value(number):
                crore_value = number / 10**7
                crore_rounded = round(crore_value, 0)
                crore_formatted = "{:,.0f}".format(crore_rounded)
                formatted_result = f"₹ {crore_formatted} Cr"
                return formatted_result
            
#_________________________________________Main________________

c1,c2 = st.columns([6,4])

with c1:
    # Check if Type is Transaction
    if Type == "Transaction":            
        filtered_data = aggre_transaction[(aggre_transaction["Year"] == int(year)) & (aggre_transaction["Quarter"] == int(quarter))]      
        if filtered_data.empty:
            st.write("No data available for the selected Year and Quarter.")
        else:
            data1 = filtered_data.groupby("State")[["Transaction_Count", "Transaction_Amount"]].sum().reset_index()        
            fig = px.choropleth_mapbox(data1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", 
                                featureidkey='properties.ST_NM',
                                locations='State',
                                title= f"PhonePe - Total Amount in Q{quarter} - {year}",
                                color= 'Transaction_Amount', 
                                mapbox_style="carto-positron",
                                center={"lat": 24, "lon": 79},
                                color_continuous_scale = px.colors.diverging.PuOr,
                                color_continuous_midpoint=0, zoom=3.6, width=800, height=800)
            
            fig.update_layout(title={'text': f"PhonePe - Total Amount in Q{quarter} - {year}",'font': {'size': 30}})            
            st.plotly_chart(fig,use_container_width=True)
          
    # Check if Type is User
    if Type == "User":               
        filtered_data = map_user[(map_user["Year"] == int(year)) & (map_user["Quarter"] == int(quarter))]        
        if filtered_data.empty:
            st.write("No data available for the selected Year and Quarter.")
        else:
            data1 = filtered_data.groupby("State")[["District_Reg_User","App_Opens"]].sum().reset_index()
            fig = px.choropleth_mapbox(data1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", 
                                featureidkey='properties.ST_NM',
                                locations='State',
                                title= f"PhonePe - Total User in Q{quarter} - {year}",
                                color= 'District_Reg_User', 
                                mapbox_style="carto-positron",
                                center={"lat": 24, "lon": 79},
                                color_continuous_scale = px.colors.diverging.PuOr,
                                color_continuous_midpoint=0, zoom=3.6, width=800, height=800)

            fig.update_layout(title={'text': f"PhonePe - Total User in Q{quarter} - {year}",'font': {'size': 30}})            
            st.plotly_chart(fig,use_container_width=True)

#____________________________________TRANSACTION_________________________
with c2:    
    # Check if Type is Transaction
    if Type == "Transaction":

        container = st.container(border=True)
        with container: 
            tab1, tab2 = st.tabs(["Details", "Top 10"])
            # Content for the 'Details' tab
            with tab1:                                    
                st.markdown(f'### :green[Transactions]')

                total_transaction_count = aggre_transaction[(aggre_transaction["Year"] == int(year)) & (aggre_transaction["Quarter"] == int(quarter))]['Transaction_Count'].sum()
                tt_count = "{:,}".format(total_transaction_count) #commas for thousands separators

                total_transaction_amount = aggre_transaction[(aggre_transaction["Year"] == int(year)) & (aggre_transaction["Quarter"] == int(quarter))]['Transaction_Amount'].sum()
                tt_amount = format_crore_value(total_transaction_amount)

                avg_transaction = round(total_transaction_amount/total_transaction_count)#Averege transaction value
                avg_form = '₹ {:,}'.format(avg_transaction)

                st.write(f'##### All PhonePe transactions (UPI + Cards + Wallets)')
                st.write(f'##### :red[{tt_count}]')
                st.write('')
                
                col1, col2 = st.columns([6,5])
                with col1:
                    st.write(f'##### Total payment value')
                    st.write(f'##### :red[{tt_amount}]')

                with col2:
                    st.write(f'##### Avg. transaction value')
                    st.write(f'##### :red[{avg_form}]')

                st.write("______")

                st.write(f'### :green[Categories]')
                col1,col2 = st.columns([3,2])
                with col1:
                    # Calculate total payment value for each category
                    total_merchant_payment = aggre_transaction[(aggre_transaction["Year"] == int(year)) &
                                                                (aggre_transaction["Quarter"] == int(quarter)) &
                                                                (aggre_transaction["Transaction_Type"] == "Merchant payments")]['Transaction_Amount'].sum()
                    total_merchant_payment_f = format_crore_value(total_merchant_payment)
                    
                    total_peer_payment = aggre_transaction[(aggre_transaction["Year"] == int(year)) &
                                                                (aggre_transaction["Quarter"] == int(quarter)) &
                                                                (aggre_transaction["Transaction_Type"] == "Peer-to-peer payments")]['Transaction_Amount'].sum()
                    total_peer_payment_f = format_crore_value(total_peer_payment)

                    total_bill_payment = aggre_transaction[(aggre_transaction["Year"] == int(year)) &
                                                                (aggre_transaction["Quarter"] == int(quarter)) &
                                                                (aggre_transaction["Transaction_Type"] == "Recharge & bill payments")]['Transaction_Amount'].sum()
                    total_bill_payment_f = format_crore_value(total_bill_payment)

                    total_financial_services = aggre_transaction[(aggre_transaction["Year"] == int(year)) &
                                                                (aggre_transaction["Quarter"] == int(quarter)) &
                                                                (aggre_transaction["Transaction_Type"] == "Financial Services")]['Transaction_Amount'].sum()
                    total_financial_services_f = format_crore_value(total_financial_services)

                    total_other_payment = aggre_transaction[(aggre_transaction["Year"] == int(year)) &
                                                                (aggre_transaction["Quarter"] == int(quarter)) &
                                                                (aggre_transaction["Transaction_Type"] == "Others")]['Transaction_Amount'].sum()
                    total_other_payment_f = format_crore_value(total_other_payment)

                    # Display category names
                    st.write(f'##### Merchant payments')
                    st.write(f'##### Peer-to-peer payments')
                    st.write(f'##### Recharge & bill payments')
                    st.write(f'##### Financial Services')
                    st.write(f'##### Others')
                # Display total payment values for each category    
                with col2:
                    st.write(f'##### :red[{total_merchant_payment_f}]')
                    st.write(f'##### :red[{total_peer_payment_f}]')
                    st.write(f'##### :red[{total_bill_payment_f}]')
                    st.write(f'##### :red[{total_financial_services_f}]')
                    st.write(f'##### :red[{total_other_payment_f}]')

        # Content for the 'Top 10' tab
        with tab2:            
            select = st.selectbox("", ("State", "District", "Pincode"))
            if select == "State":
                st.markdown(f'### Top 10 {select}')
                # Filter the DataFrame based on the selected year and quarter
                filtered_df = aggre_transaction[(aggre_transaction['Year'] == int(year)) & (aggre_transaction['Quarter'] == int(quarter))]
                transaction_sum = filtered_df.groupby('State')["Transaction_Amount"].sum().reset_index()
                top_10 = transaction_sum.nlargest(10, "Transaction_Amount")
                # Reset the index and set it to start from 1
                top_10.reset_index(drop=True, inplace=True)
                top_10.index += 1                
                # Convert transaction count to crore format if needed
                top_10["Transaction_Amount"] = top_10["Transaction_Amount"].apply(lambda x: format_crore_value(x))
                st.write(top_10)

            if select == "District":
                st.markdown(f'### Top 10 {select}')
                # Filter the DataFrame based on the selected year and quarter
                filtered_df = map_transaction[(map_transaction['Year'] == int(year)) & (map_transaction['Quarter'] == int(quarter))]
                transaction_sum = filtered_df.groupby('District')["District_T_Amount"].sum().reset_index()
                top_10 = transaction_sum.nlargest(10, "District_T_Amount")                
                # Reset the index and set it to start from 1
                top_10.reset_index(drop=True, inplace=True)
                top_10.index += 1                
                # Convert transaction count to crore format if needed
                top_10["District_T_Amount"] = top_10["District_T_Amount"].apply(lambda x: format_crore_value(x))
                top_10 = top_10.rename(columns={"District_T_Amount": "Transaction_Amount"})
                st.write(top_10)            
                            
            if select == "Pincode":       
                st.markdown(f'### Top 10 {select}')
                # Filter the DataFrame based on the selected year and quarter
                filtered_df = top_transaction[(top_transaction['Year'] == int(year)) & (top_transaction['Quarter'] == int(quarter))]
                transaction_sum = filtered_df.groupby('Pincode')["Pincode_T_Amount"].sum().reset_index()
                top_10 = transaction_sum.nlargest(10, "Pincode_T_Amount")
                # Reset the index and set it to start from 1
                top_10.reset_index(drop=True, inplace=True)
                top_10.index += 1              
                # Convert transaction count to crore format if needed
                top_10["Pincode_T_Amount"] = top_10["Pincode_T_Amount"].apply(lambda x: format_crore_value(x))
                top_10 = top_10.rename(columns={"Pincode_T_Amount": "Transaction_Amount"})
                st.write(top_10)

#____________________________________USER_________________________

    # Check if Type is "User"
    if Type == "User":
            container = st.container(border=True)
            with container:
                tab1, tab2 = st.tabs(["User", "Top 10"])
                # Content for the User tab
                with tab1:
                    # user
                    total_appopen_count = map_user[(map_user["Year"] == int(year)) & (map_user["Quarter"] == int(quarter))]['District_Reg_User'].sum()
                    tao_count = "{:,}".format(total_appopen_count) #commas for thousands separators
                    st.write(f'##### Registered PhonePe users in Q{quarter}-{year}')
                    st.write(f'##### :red[{tao_count}]')
                    st.write('')

                    # app opened
                    total_appopen_count = map_user[(map_user["Year"] == int(year)) & (map_user["Quarter"] == int(quarter))]['App_Opens'].sum()
                    tao_count = "{:,}".format(total_appopen_count) #commas for thousands separators
                    st.write(f'##### PhonePe app opens in Q{quarter}-{year}')
                    st.write(f'##### :red[{tao_count}]')
                    st.write('')
                    
                # Content for the Top 10 tab
                with tab2:
                    # Select box to choose display type (State, District, Pincode)
                    select = st.selectbox("", ("State", "District", "Pincode"))
                    if select == "State":
                        st.markdown(f'### Top 10 {select}')
                        filtered_df = map_user[(map_user['Year'] == int(year)) & (map_user['Quarter'] == int(quarter))]
                        transaction_sum = filtered_df.groupby('State')["District_Reg_User"].sum().reset_index()
                        top_10 = transaction_sum.nlargest(10, "District_Reg_User")
                        top_10.reset_index(drop=True, inplace=True)
                        top_10.index += 1 # Reset the index and set it to start from 1
                        top_10 = top_10.rename(columns={"District_Reg_User": "Registered User"})
                        st.write(top_10)

                    if select == "District":
                        st.markdown(f'### Top 10 {select}')
                        filtered_df = map_user[(map_user['Year'] == int(year)) & (map_user['Quarter'] == int(quarter))]
                        transaction_sum = filtered_df.groupby('District')["District_Reg_User"].sum().reset_index()
                        top_10 = transaction_sum.nlargest(10, "District_Reg_User")
                        top_10.reset_index(drop=True, inplace=True)
                        top_10.index += 1 # Reset the index and set it to start from 1
                        top_10 = top_10.rename(columns={"District_Reg_User": "Registered User"})
                        st.write(top_10)

                    if select == "Pincode":
                        st.markdown(f'### Top 10 {select}')
                        filtered_df = top_user[(top_user['Year'] == int(year)) & (top_user['Quarter'] == int(quarter))]
                        transaction_sum = filtered_df.groupby('Pincode')["Pincode_Reg_User"].sum().reset_index()
                        top_10 = transaction_sum.nlargest(10, "Pincode_Reg_User")
                        top_10.reset_index(drop=True, inplace=True)
                        top_10.index += 1 # Reset the index and set it to start from 1
                        top_10 = top_10.rename(columns={"Pincode_Reg_User": "Registered User"})
                        st.write(top_10)
                        
st.write("__________") # Add horizontal line to separate sections

#___________________________________________________State_Wise_Analysis____________________________________________________________________

# Display a markdown heading for State-Wise Analysis
st.markdown("## :blue[State-Wise Analysis]")
st.write("")

c1, c2, c3, c4, c5 = st.columns([2,1,1,1,2])
# Column 1: Select a State
with c1:
    name = ['Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
       'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
       'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
       'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
       'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
       'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
       'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
       'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
       'Uttarakhand', 'West Bengal']    
    state1 = st.selectbox('Select a State', name, key='state1')
# Column 2: Select a Chart Type    
with c2:
    chart_type = ['Bar','Line','Area','Pie']
    chart1 = st.selectbox('Select a Chart Type', chart_type, key='chart')
# Column 3: Select a Year    
with c3:
    y1 = ['2018', '2019', '2020','2021','2022','2023']
    default_y = y1.index("2023")
    year1 = st.selectbox('Select a Year', y1, key='year1', index = default_y)
# Column 4: Select a Quarter
with c4:
    q1 = ['Q1 (Jan-Mar)', 'Q2 (Apr-June)', 'Q3 (July-Sep)','Q4 (Oct-Dec)']
    default_q = q1.index("Q1 (Jan-Mar)")
    quarter1 = st.selectbox('Select a Quarter', q1, key='quarter1', index=default_q)
    if quarter1 == 'Q1 (Jan-Mar)': quarter1 = 1
    elif quarter1 == 'Q2 (Apr-June)': quarter1 = 2
    elif quarter1 == 'Q3 (July-Sep)': quarter1 = 3
    elif quarter1 == 'Q4 (Oct-Dec)': quarter1 = 4
# Column 5: Select a Type (Transactions or Users)
with c5:
    t1 = ["Transactions", "Users"]
    Type1 = st.selectbox("Select a Type", t1, key='Type1')
    
#______________________________def_for_Transactions________________________________

def bar_chart(df, state1, year1, quarter1):

    filtered_df = df[(df['State'] == state1) &
                     (df['Year'] == int(year1)) &
                     (df['Quarter'] == int(quarter1))]
  
    if filtered_df.empty:
        st.warning("No data available for the selected parameters.")
        return

    df1 = filtered_df.groupby("District")[["District_T_Count", "District_T_Amount"]].sum() 
    df1_sorted = df1.sort_values(by="District", ascending = True)

    fig_bar_1 = px.bar(df1_sorted, x="District_T_Count", y=df1_sorted.index, orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width=700,
                        title=f"{state1.upper()} - TRANSACTION COUNT", height=500)

    fig_bar_2 = px.bar(df1_sorted, x="District_T_Amount", y=df1_sorted.index, orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width=700,
                        title=f"{state1.upper()} - TRANSACTION AMOUNT", height=500)

    fig_bar_1.update_layout(yaxis_title="District")
    fig_bar_2.update_layout(yaxis_title="District")
    
    c1, c2 = st.columns(2)
    with c1:
        fig_bar_1.update_traces(textposition='inside')
        st.plotly_chart(fig_bar_1, use_container_width=True) 
    with c2:
        fig_bar_2.update_traces(textposition='inside')
        st.plotly_chart(fig_bar_2, use_container_width=True)
      
    st.write(df1_sorted)

#---------------------

def line_chart(df, state1, year1, quarter1):

    filtered_df = df[(df['State'] == state1) &
                     (df['Year'] == int(year1)) &
                     (df['Quarter'] == int(quarter1))]
    if filtered_df.empty:
        st.warning("No data available for the selected parameters.")
        return
    
    df1 = filtered_df.groupby("District")[["District_T_Count", "District_T_Amount"]].sum()
    df1_sorted = df1.sort_values(by='District', ascending=True)
    
    fig_line_1 = px.line(df1_sorted, x=df1_sorted.index, y="District_T_Count", 
                         color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                         width=700, title=f"{state1.upper()} - TRANSACTION COUNT", height=500)

    fig_line_2 = px.line(df1_sorted, x=df1_sorted.index, y="District_T_Amount", 
                         color_discrete_sequence=px.colors.sequential.Greens_r, 
                         width=700, title=f"{state1.upper()} - TRANSACTION AMOUNT", height=500)

    fig_line_1.update_layout(xaxis_title="District")
    fig_line_2.update_layout(xaxis_title="District")
    fig_line_1.update_xaxes(tickangle=-90, tickmode='linear')
    fig_line_2.update_xaxes(tickangle=-90, tickmode='linear')
    
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_line_1, use_container_width=True) 
    with c2:
        st.plotly_chart(fig_line_2, use_container_width=True)

    st.write(df1_sorted)

#-------------

def area_chart(df, state1, year1, quarter1):

    filtered_df = df[(df['State'] == state1) &
                     (df['Year'] == int(year1)) &
                     (df['Quarter'] == int(quarter1))]
    if filtered_df.empty:
        st.warning("No data available for the selected parameters.")
        return

    df1 = filtered_df.groupby("District")[["District_T_Count", "District_T_Amount"]].sum()
    df1_sorted = df1.sort_values(by='District', ascending=True)
    
    fig_area_1 = px.area(df1_sorted, x=df1_sorted.index, y="District_T_Count", 
                         color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                         width=700, title=f"{state1.upper()} - TRANSACTION COUNT", height=500)
    
    fig_area_2 = px.area(df1_sorted, x=df1_sorted.index, y="District_T_Amount", 
                         color_discrete_sequence=px.colors.sequential.Greens_r, 
                         width=700, title=f"{state1.upper()} - TRANSACTION AMOUNT", height=500)

    fig_area_1.update_layout(xaxis_title="District")
    fig_area_2.update_layout(xaxis_title="District")
    fig_area_1.update_xaxes(tickangle=-90, tickmode='linear')
    fig_area_2.update_xaxes(tickangle=-90, tickmode='linear')
    
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_area_1, use_container_width=True) 
    with c2:
        st.plotly_chart(fig_area_2, use_container_width=True)

    st.write(df1_sorted)

#-------------


def pie_chart(df, state1, year1, quarter1):

    filtered_df = df[(df['State'] == state1) &
                     (df['Year'] == int(year1)) &
                     (df['Quarter'] == int(quarter1))]
    if filtered_df.empty:
        st.warning("No data available for the selected parameters.") #px.colors.sequential.Viridis
        return

    df1 = filtered_df.groupby("District")[["District_T_Count", "District_T_Amount"]].sum()
    df1_sorted = df1.sort_values(by='District', ascending=True)
    
    fig_pie_1 = px.pie(df1_sorted, names=df1_sorted.index, values="District_T_Count", hole=.3,color_discrete_sequence=px.colors.cyclical.Phase)
    fig_pie_1.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='black', width=2)))

    fig_pie_2 = px.pie(df1_sorted, names=df1_sorted.index, values="District_T_Amount", hole=.3,color_discrete_sequence=px.colors.cyclical.Phase)    
    fig_pie_2.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='black', width=2)))

    fig_pie_1.update_layout(title_text=f"{state1.upper()} - TRANSACTION COUNT", width=350, height=450)
    fig_pie_2.update_layout(title_text=f"{state1.upper()} - TRANSACTION AMOUNT", width=350, height=450)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_pie_1, use_container_width=True) 
    with c2:
        st.plotly_chart(fig_pie_2, use_container_width=True)

    st.write(df1_sorted)

#__________________________________________def_for_Users_______________________________


def bar_chart1(df, state1, year1, quarter1):

    filtered_df = df[(df['State'] == state1) &
                     (df['Year'] == int(year1)) &
                     (df['Quarter'] == int(quarter1))]
    if filtered_df.empty:
        st.warning("No data available for the selected parameters.")
        return

    df2 = filtered_df.groupby("District")[["District_Reg_User", "App_Opens"]].sum()        
    df2_sorted = df2.sort_values(by='District', ascending = True)

    fig_bar_1 = px.bar(df2_sorted, x="District_Reg_User", y=df2_sorted.index, orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width=700,
                        title=f"{state1.upper()} - REGISTERED USER", height=500)

    fig_bar_2 = px.bar(df2_sorted, x="App_Opens", y=df2_sorted.index, orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width=700,
                        title=f"{state1.upper()} - APP OPENED", height=500)

    fig_bar_1.update_layout(yaxis_title="Districts")
    fig_bar_2.update_layout(yaxis_title="Districts")
    
    c1, c2 = st.columns(2)
    with c1:
        fig_bar_1.update_traces(textposition='inside')
        st.plotly_chart(fig_bar_1, use_container_width=True) 
    with c2:
        fig_bar_2.update_traces(textposition='inside')
        st.plotly_chart(fig_bar_2, use_container_width=True)

    st.write(df2_sorted)
        
#-------------

def line_chart1(df, state1, year1, quarter1):
    filtered_df = df[(df['State'] == state1) &
                     (df['Year'] == int(year1)) &
                     (df['Quarter'] == int(quarter1))] 
    if filtered_df.empty:
        st.warning("No data available for the selected parameters.")
        return
    df2 = filtered_df.groupby("District")[["District_Reg_User", "App_Opens"]].sum()  
    df2_sorted = df2.sort_values(by='District', ascending=True)
    
    fig_line_1 = px.line(df2_sorted, x=df2_sorted.index, y="District_Reg_User", 
                         color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                         width=700, title=f"{state1.upper()} - REGISTERED USER", height=500)

    fig_line_2 = px.line(df2_sorted, x=df2_sorted.index, y="App_Opens", 
                         color_discrete_sequence=px.colors.sequential.Greens_r, 
                         width=700, title=f"{state1.upper()} - APP OPENED", height=500)

    fig_line_1.update_layout(xaxis_title="Districts")
    fig_line_2.update_layout(xaxis_title="Districts")
    fig_line_1.update_xaxes(tickangle=-90, tickmode='linear')
    fig_line_2.update_xaxes(tickangle=-90, tickmode='linear')
    
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_line_1, use_container_width=True) 
    with c2:
        st.plotly_chart(fig_line_2, use_container_width=True)

    st.write(df2_sorted)


#-------------

def area_chart1(df, state1, year1, quarter1):

    filtered_df = df[(df['State'] == state1) &
                     (df['Year'] == int(year1)) &
                     (df['Quarter'] == int(quarter1))]
    if filtered_df.empty:
        st.warning("No data available for the selected parameters.")
        return
    df2 = filtered_df.groupby("District")[["District_Reg_User", "App_Opens"]].sum()
    df2_sorted = df2.sort_values(by='District', ascending=True)
    
    fig_area_1 = px.area(df2_sorted, x=df2_sorted.index, y="District_Reg_User", 
                         color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                         width=700, title=f"{state1.upper()} - REGISTERED USER", height=500)

    fig_area_2 = px.area(df2_sorted, x=df2_sorted.index, y="App_Opens", 
                         color_discrete_sequence=px.colors.sequential.Greens_r, 
                         width=700, title=f"{state1.upper()} - APP OPENED", height=500)

    fig_area_1.update_layout(xaxis_title="Districts")
    fig_area_2.update_layout(xaxis_title="Districts")
    fig_area_1.update_xaxes(tickangle=-90, tickmode='linear')
    fig_area_2.update_xaxes(tickangle=-90, tickmode='linear')

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_area_1, use_container_width=True)
    with c2:
        st.plotly_chart(fig_area_2, use_container_width=True)

    st.write(df2_sorted)

#-------------

def pie_chart1(df, state1, year1, quarter1):

    filtered_df = df[(df['State'] == state1) &
                     (df['Year'] == int(year1)) &
                     (df['Quarter'] == int(quarter1))]

    if filtered_df.empty:
        st.warning("No data available for the selected parameters.")
        return
    df2 = filtered_df.groupby("District")[["District_Reg_User", "App_Opens"]].sum()
    df2_sorted = df2.sort_values(by='District', ascending=True)

    fig_pie_1 = px.pie(df2_sorted, names=df2_sorted.index, values="District_Reg_User", hole=.3,color_discrete_sequence=px.colors.cyclical.mygbm)
    fig_pie_1.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='black', width=2)))

    fig_pie_2 = px.pie(df2_sorted, names=df2_sorted.index, values="App_Opens", hole=.3,color_discrete_sequence=px.colors.cyclical.mygbm)    
    fig_pie_2.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='black', width=2)))

    fig_pie_1.update_layout(title_text=f"{state1.upper()} - REGISTERED USER", width=350, height=450)
    fig_pie_2.update_layout(title_text=f"{state1.upper()} - APP OPENED", width=350, height=450)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_pie_1, use_container_width=True) 
    with c2:
        st.plotly_chart(fig_pie_2, use_container_width=True)

    st.write(df2_sorted)


#________________________def_for_Others______________________

def aggre_transaction_type(state1):
    # Filter the DataFrame for the selected state
    df_state = aggre_transaction[aggre_transaction["State"] == state1]
    # Check if filtered data is empty
    if df_state.empty:
        st.warning("No data available for the selected parameters.")
        return
    df_state.reset_index(drop=True, inplace=True)
    
    data = df_state.groupby("Transaction_Type")[["Transaction_Count", "Transaction_Amount"]].sum()
    data.reset_index(inplace=True)

    fig_bar_1 = px.bar(data, x="Transaction_Count", y="Transaction_Type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Cividis, width=700, height=500,
                        title=f"{state1.upper()} - TRANSACTION TYPES AND TRANSACTION COUNT (2018-2023)")
    fig_bar_1.update_layout(title_font_size=14)

    fig_bar_2 = px.bar(data, x="Transaction_Amount", y="Transaction_Type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Jet, width=700, height=500,
                        title=f"{state1.upper()} - TRANSACTION TYPES AND TRANSACTION AMOUNT (2018-2023)")
    fig_bar_2.update_layout(title_font_size=14)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_bar_1, use_container_width=True)
    with c2:
        st.plotly_chart(fig_bar_2, use_container_width=True)

#----------------------

def aggre_user_plot(year1):
    # Filter data for the selected year
    data= aggre_user[aggre_user["Year"] == int(year1)]
    # Check if filtered data is empty
    if data.empty:
        st.warning("No data available related to brands !")
        return
    data.reset_index(drop= True, inplace= True)
    data= pd.DataFrame(data.groupby("Brand")["Brand_T_Count"].sum())
    data.reset_index(inplace= True)

    fig_bar = px.bar(data, x="Brand",y="Brand_T_Count", title=f"{year} - BRANDS AND TRANSACTION COUNT (2018-2023)",
                    width=1000,color_discrete_sequence=px.colors.sequential.Jet)
 
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with c2:
        st.write(data)

#___________________________Call_the_def_for_chart1_____________________


if chart1 == "Bar":
    if Type1 == "Transactions":
        bar_chart(map_transaction, state1, year1, quarter1)
        aggre_transaction_type(state1)
    if Type1 == "Users":
        bar_chart1(map_user, state1, year1, quarter1)
        aggre_user_plot(year1)

if chart1 == "Line":
    if Type1 == "Transactions":
        line_chart(map_transaction, state1, year1, quarter1)        
    if Type1 == "Users":
        line_chart1(map_user, state1, year1, quarter1)

if chart1 == "Area":
    if Type1 == "Transactions":
        area_chart(map_transaction, state1, year1, quarter1)       
    if Type1 == "Users":
        area_chart1(map_user, state1, year1, quarter1)

if chart1 == "Pie":
    if Type1 == "Transactions":
        pie_chart(map_transaction, state1, year1, quarter1)
    if Type1 == "Users":
        pie_chart1(map_user, state1, year1, quarter1)

st.write("__________") # Add horizontal line to separate sections


#______________________________________def_for_analysis______________________________

def plot_states(aggre_transaction, order, n):
    
    data_state = aggre_transaction[["State", "Transaction_Amount"]]
    data_state_a1 = data_state.groupby("State")["Transaction_Amount"].sum().sort_values(ascending=False)
    
    # Selecting top or low states based on the parameter order
    if order == "Top":
        data_state_a2 = data_state_a1.head(n).reset_index()
    elif order == "Bottom":
        data_state_a2 = data_state_a1.tail(n).reset_index()

    data_state_a2.index += 1

    # Plotting bar chart
    fig = px.bar(data_state_a2, x="State", y="Transaction_Amount", 
                 title=f"{order} {n} State and Transaction Amount", 
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    fig.update_traces(textposition='inside')
    fig.update_xaxes(tickangle=-90, tickmode='linear')

    # Creating Streamlit layout
    c1, c2, c3 = st.columns([5,1,5])
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        st.write(data_state_a2)

#-----------------------------

def plot_district(map_transaction, order, n):
    
    data_district = map_transaction[["District", "District_T_Amount"]]
    data_district_a1 = data_district.groupby("District")["District_T_Amount"].sum().sort_values(ascending=False)
    
    # Selecting top or low states based on the parameter order
    if order == "Top":
        data_district_a2 = data_district_a1.head(n).reset_index()
    elif order == "Bottom":
        data_district_a2 = data_district_a1.tail(n).reset_index()

    data_district_a2.index += 1

    # Plotting bar chart
    fig = px.bar(data_district_a2, x="District", y="District_T_Amount", 
                 title=f"{order} {n} District and Transaction Amount", 
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    fig.update_traces(textposition='inside')
    fig.update_xaxes(tickangle=-90, tickmode='linear')

    # Creating Streamlit layout
    c1, c2, c3 = st.columns([5,1,5])
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        st.write(data_district_a2)

#----------------------------


def plot_pincode(top_transaction, order, n):
    data_pincode = top_transaction[["Pincode", "Pincode_T_Amount"]]
    data_pincode_a1 = data_pincode.groupby("Pincode")["Pincode_T_Amount"].sum().sort_values(ascending=False)
    
    # Selecting top or bottom pin codes based on the parameter order
    if order == "Top":
        data_pincode_a2 = data_pincode_a1.head(n).reset_index()
    elif order == "Bottom":
        data_pincode_a2 = data_pincode_a1.tail(n).reset_index()

    data_pincode_a2.index += 1

    # Plotting pie chart
    fig = px.pie(data_pincode_a2, names="Pincode", values="Pincode_T_Amount", 
                 title=f"{order} {n} Pincode and Transaction Amount", 
                 hole=0.5, width=1000,
                 color_discrete_sequence=px.colors.sequential.Magenta_r)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    # Creating Streamlit layout
    c1, c2, c3 = st.columns([5,1,5])
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        st.write(data_pincode_a2)

#----------------------------

def plot_brand(aggre_user, order, n):
    
    data_brand = aggre_user[["Brand", "Brand_T_Count"]]
    data_brand_a1 = data_brand.groupby("Brand")["Brand_T_Count"].sum().sort_values(ascending=False)
    
    # Selecting top or low states based on the parameter order
    if order == "Top":
        data_brand_a2 = data_brand_a1.head(n).reset_index()
    elif order == "Bottom":
        data_brand_a2 = data_brand_a1.tail(n).reset_index()

    data_brand_a2.index += 1

    # Plotting bar chart
    fig = px.bar(data_brand_a2, x="Brand", y="Brand_T_Count", 
                 title=f"{order} {n} Brand and Transaction Amount", 
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    fig.update_traces(textposition='inside')
    fig.update_xaxes(tickangle=-90, tickmode='linear')

    # Creating Streamlit layout
    c1, c2, c3 = st.columns([5,1,5])
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        st.write(data_brand_a2)
      

#______________________________________________call_the_def_for_Analysis________________________


st.markdown("## :blue[Analysis Using Graphs]")
st.write("")

select = st.selectbox('Select a Question',("Top 10 States (according to total amount)", "Bottom 10 States (according to total amount)",
                                           "Top 10 Districts (according to total amount)", "Bottom 10 Districts (according to total amount)",
                                           "Top 10 Pincodes (according to total amount)", "Bottom 10 Pincodes (according to total amount)",
                                           "Top 5 Brands (according to total amount)", "Botttom 5 Brands (according to total amount)"))
                                           
if select == "Top 10 States (according to total amount)":
    plot_states(aggre_transaction, "Top", 10)

if select == "Bottom 10 States (according to total amount)":
    plot_states(aggre_transaction, "Bottom", 10)    
#-----------
if select == "Top 10 Districts (according to total amount)":
    plot_district(map_transaction, "Top", 10)

if select == "Bottom 10 Districts (according to total amount)":
    plot_district(map_transaction, "Bottom", 10)    
#-----------
if select == "Top 10 Pincodes (according to total amount)":
    plot_pincode(top_transaction, "Top", 10)

if select == "Bottom 10 Pincodes (according to total amount)":
    plot_pincode(top_transaction, "Bottom", 10)   
#-----------
if select == "Top 5 Brands (according to total amount)":
    plot_brand(aggre_user, "Top", 5)

if select == "Botttom 5 Brands (according to total amount)":
    plot_brand(aggre_user, "Bottom", 5)




