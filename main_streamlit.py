import streamlit as st
import pandas as pd
import base64

def format_csv(df1,df_tp):
    # Perform some action to format the CSV file
    # For example, sort the dataframe by a specific column
    df1['*ContactName'] = df_tp['Customer Name']
    df1['EmailAddress'] = df_tp['Primary Contact EmailID']
    df1['POAddressLine1'] = df_tp['Billing Address']
    df1['POCity'] = df_tp['Billing City']
    df1['POCountry'] = df_tp['Billing Country']
    df1['*InvoiceNumber'] = df_tp['Invoice Number']
    df1['Reference'] = df_tp['CF.TGM #']
    df1['*InvoiceDate'] = df_tp['Invoice Date']
    df1['*DueDate'] = df_tp['Expected Payment Date']
    df1['Total'] = df_tp['Total']
    df1['*Description'] = df_tp['Item Desc']
    df1['*Quantity'] = df_tp['Quantity']
    df1['*UnitAmount'] = df_tp['Item Price']
    df1['Discount'] = df_tp['Discount']
    df1['*AccountCode'] = df_tp['Account Code']
    df1['*TaxType'] = df_tp['Item Tax Type']
    df1['TaxAmount'] = 0
    df1['Currency'] = df_tp['Currency Code']

    return df1

def download_csv(df):
    # Create a downloadable link for the formatted CSV
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="formatted.csv">Download Formatted CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

def main():

    st.title("CSV Formatter")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    uploaded_template = st.file_uploader("Upload CSV template file", type="csv")

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

if __name__ == '__main__':
    main()