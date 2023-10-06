import streamlit as st
import pandas as pd
import base64
import datetime
import re
import io

def format_csv(df1,df_tp):
    # Perform some action to format the CSV file
    # For example, sort the dataframe by a specific column
    df_tp['*ContactName'] = df1['Customer Name']
    df_tp['EmailAddress'] = df1['Primary Contact EmailID']
    df_tp['POAddressLine1'] = df1['Billing Address']
    df_tp['POCity'] = df1['Billing City']
    df_tp['POCountry'] = df1['Billing Country']
    df_tp['*InvoiceNumber'] = df1['Invoice Number']
    df_tp['Reference'] = df1['CF.TGM #']
    df_tp['*InvoiceDate'] = df1['Invoice Date']
    df_tp['*DueDate'] = df1['Expected Payment Date']
    df_tp['Total'] = df1['Total']
    df_tp['*Description'] = df1['Item Desc']
    df_tp['*Quantity'] = df1['Quantity']
    df_tp['*UnitAmount'] = df1['Item Price']
    df_tp['Discount'] = df1['Discount']
    df_tp['*AccountCode'] = df1['Account Code']
    df_tp['*TaxType'] = df1['Item Tax Type']
    df_tp['TaxAmount'] = 0
    df_tp['Currency'] = df1['Currency Code']

    return df_tp
def format_csv_contact(df_old,df_new):

    
    df_new['EmailAddress'] = df_old['EmailID']
    df_new['FirstName'] = df_old['First Name']
    df_new['LastName'] = df_old['Last Name']
    df_new['POAttentionTo'] = df_old['Billing Attention']
    df_new['POAddressLine1'] = df_old['Billing Address']
    df_new['POAddressLine2'] = df_old['Billing Street2']
    df_new['POCity'] = df_old['Billing City']
    df_new['POPostalCode'] = df_old['Billing Code']
    df_new['POCountry'] = df_old['Billing Country']
    df_new['PhoneNumber'] = df_old['Billing Phone']
    df_new['FaxNumber'] = df_old['Billing Fax']
    df_new['MobileNumber'] = df_old['MobilePhone']
    df_new['SkypeName'] = df_old['Skype Identity']
    df_new['TaxNumber'] = df_old['Tax Percentage']

    return df_tp

def format_excel(df):
    deal_created_count = 0
    deal_closed_count = 0
    for i in df.columns:
        my_series = df[i].dropna().to_list()
        if len(my_series)>0 and re.search('\d\d\d\d-\d\d-\d\d',str(my_series[0])) is not None:
            
            df[i] = pd.to_datetime(df[i],format='%Y/%m/%d',errors='coerce',yearfirst=True)
            if i == 'Deal - Deal created':
                deal_created_count+=1
                df['Created_month'] = df[i].astype('datetime64[ns]').dt.strftime('%m/%Y')
                df['Created_quater'] =  df[i].astype('datetime64[ns]').dt.to_period('Q').dt.strftime('Q%q/%y')

            elif i == 'Deal - Deal closed on':
                deal_closed_count+=1
                df['Closed_month'] = df[i].astype('datetime64[ns]').dt.strftime('%m/%Y')
                df['Closed_quater'] = df[i].astype('datetime64[ns]').dt.to_period('Q').dt.strftime('Q%q/%y')

            df[i] = pd.to_datetime(df[i], format='%Y/%m/%d',errors='ignore').dt.date
    if deal_created_count==0:
        st.write("Couldn't find the column 'Deal - Deal created'")
    elif deal_closed_count==0:
        st.write("Couldn't find the column 'Deal - Deal closed on'")
    return df

def download_csv(df):
    # Create a downloadable link for the formatted CSV
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="formatted.csv">Download Formatted CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

def download_excel(dataframe):
 # Convert the pandas DataFrame to an Excel file
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, mode='xlsx', engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False)
    excel_file.seek(0)
    
    # Set the file name and type
    file_name = 'data_formatted.xlsx'
    file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    # Create a button to download the file
    download_button_str = f"Click here to download {file_name}!"
    download_button = st.download_button(label=download_button_str, data=excel_file, file_name=file_name, mime=file_type)
    
    # Display the button
    st.write(download_button)

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://1159025897.rsc.cdn77.org/data/images/full/82178/johnny-depp.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
def main():
    # set_bg_hack_url()
    st.image('https://1159025897.rsc.cdn77.org/data/images/full/82178/johnny-depp.jpg',caption="I hadn't known Tan has been on my back over 1 year, so I was spending my life on those things manually.")
    

    tab1,tab2,tab3 = st.tabs(["CSV Formatter - Invoices","CSV Formatter - Contacts","Excel Date Formatter"])
    with tab1:
        st.title("CSV Format - Invoices")
        # Upload CSV file
        uploaded_file = st.file_uploader("Upload CSV - invoice file", type="csv")
        uploaded_template = st.file_uploader("Upload CSV template - invoice file", type="csv")

        if uploaded_template is not None:
            template_df  = pd.read_csv(uploaded_template,header=0)
        if uploaded_file is not None:
            df_file = pd.read_csv(uploaded_file,header=0)
            # Format button
            if st.button("Format"):
                formatted_df = format_csv(df_file,template_df)

                # Display the formatted dataframe
                st.write(formatted_df)

                # Download formatted CSV button
                download_csv(formatted_df)
    with tab2:
        st.title("CSV Formatter - Contacts")
        # Upload CSV file
        uploaded_file2 = st.file_uploader("Upload CSV file - contact", type="csv")
        uploaded_template2 = st.file_uploader("Upload CSV template - contact file", type="csv")

        if uploaded_template2 is not None:
            template_df2  = pd.read_csv(uploaded_template2,header=0)
        if uploaded_file2 is not None:
            df_file2 = pd.read_csv(uploaded_file2,header=0)
            # Format button
            if st.button("Format"):
                formatted_df2 = format_csv_contact(df_file2,template_df2)

                # Display the formatted dataframe
                st.write(formatted_df2)

                # Download formatted CSV button
                download_csv(formatted_df2)
    with tab3:
        st.title("Excel Date Formatter")
        uploaded_file1 = st.file_uploader("Upload Excel file", type="xlsx")
        if uploaded_file1 is not None:
            uploaded_file1_df  = pd.read_excel(uploaded_file1,header=0)
            if st.button("Format"):
                formatted_df1 = format_excel(uploaded_file1_df)

                # Display the formatted dataframe
                st.write(formatted_df1)

                # Download formatted CSV button
                download_excel(formatted_df1)
if __name__ == '__main__':
    main()
