import streamlit as st
import pandas as pd
import base64

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

def download_csv(df):
    # Create a downloadable link for the formatted CSV
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="formatted.csv">Download Formatted CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)
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
         unsafe_allow_html=True)
def main():
    page_bg_img = '''
    <style>
    body {
    background-image: url("https://images.hellomagazine.com/horizon/landscape/47a19dab71aa-gettyimages-1255875965.jpg");
    background-size: cover;
    }
    </style>
    '''

st.markdown(page_bg_img, unsafe_allow_html=True)
    set_bg_hack_url()
    st.title("CSV Formatter for MR. Slawekdeppppppppppp")

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
