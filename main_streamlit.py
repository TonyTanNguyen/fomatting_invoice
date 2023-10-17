import streamlit as st
import pandas as pd
import base64
import datetime
import re
import io
import numpy as np
import time
import os
def download_file(sql_file):
    return st.download_button(
        label="DOWNLOAD!",
        data=sql_file,
        file_name=sql_file.name.replace('.sql','_replaced.sql'),
        mime="text/plain"
        )
def format_csv(df1,df_tp):
    # Perform some action to format the CSV file
    # For example, sort the dataframe by a specific column
    cols = df1.columns
    if 'Customer Name' in cols:
        df_tp['*ContactName'] = df1['Customer Name']
    else:
        st.write(f'Missing Customer Name')
    if not 'PO Number' in cols:
    #     df_tp['InventoryItemCode'] = df1['PO Number']
    # else:
        st.write(f'Missing PO Number')
    if 'Primary Contact EmailID' in cols:
        df_tp['EmailAddress'] = df1['Primary Contact EmailID']
    else:
        st.write(f'Missing Primary Contact EmailID')
        
    if 'Customer Name' in cols:
        df_tp['Billing Address'] = df1['Billing Address']
    else:
        st.write(f'Missing Billing Address')
    if 'Billing City' in cols:
        df_tp['POCity'] = df1['Billing City']
    else:
        st.write(f'Missing Billing City')
    if 'Billing Country' in cols:
        df_tp['POCountry'] = df1['Billing Country']
    else:
        st.write(f'Missing Billing Country')
    if 'Invoice Number' in cols:
        # df_tp['*InvoiceNumber'] = df1.apply(lambda x: '# ' + x['Invoice Number'] if '#' not in x['Invoice Number'] else x['Invoice Number'], axis=1)
        df_tp['*InvoiceNumber'] = df1['Invoice Number']
    else:
        st.write(f'Missing Invoice Number')
    if 'CF.TGM #' in cols:
        df_tp['Reference'] = df1['CF.TGM #']
    else:
        st.write(f'Missing Reference')
    if 'Invoice Date' in cols:
        
        df_tp['*InvoiceDate'] = df1['Invoice Date']
    else:
        st.write(f'Missing Invoice Date')
    if 'Expected Payment Date' in cols:
        df_tp['*DueDate'] = df1['Expected Payment Date']
    else:
        st.write(f'Missing Expected Payment Date')
    if 'Total' in cols:
        df_tp['Total'] = df1['Total']
    else:
        st.write(f'Missing Total')
    if 'Item Desc' in cols:
        # df_tp['*Description'] = df1['Item Desc']
        df_tp['*Description'] = df1.apply(lambda x: x['Item Desc'] + '\nPurchase Order: ' + str(x['PO Number']) if x['PO Number'] not in ['',np.nan] else x['Item Desc'],axis=1)
        # df_tp['*Description'] = df1['Item Desc'] + '\nPurchase Order: ' + df1['PO Number']
    else:
        st.write(f'Missing Item Desc')
    if 'Quantity' in cols:
        df_tp['*Quantity'] = df1['Quantity']
    else:
        st.write(f'Missing Quantity')
    if 'Item Price' in cols:
        df_tp['*UnitAmount'] = df1['Item Price']
    else:
        st.write(f'Missing Item Price')
    if 'Discount' in cols:
        df_tp['Discount'] = df1['Discount']
    else:
        st.write(f'Missing Discount')
    if 'Account Code' in cols:
        df_tp['*AccountCode'] = df1['Account Code']
    else:
        st.write(f'Missing Account Code')
    if 'Item Tax Type' in cols:
        df_tp['*TaxType'] = df1['Item Tax Type']
    else:
        st.write(f'Missing Item Tax Type')
    df_tp['TaxAmount'] = 0
    if 'Currency Code' in cols:
        df_tp['Currency'] = df1['Currency Code']
    else:
        st.write(f'Missing Currency Code')
    # indexes = df_tp[df_tp['*InvoiceNumber'].duplicated()].index
    # count=0
    # for i in indexes:
    #     new_text = str(df_tp['*InvoiceNumber'][i])+ '-'+ str(count)
    #     df_tp.at[i,'*InvoiceNumber'] = new_text
    #     count+=1
    
    return df_tp
def format_csv_contact(df_old,df_new):

    df_new['*ContactName'] = df_old['Contact Name']
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
    df_new = df_new.drop_duplicates(subset='*ContactName',keep="first")
    return df_new

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
             background: url("https://vcdn1-giaitri.vnecdn.net/2023/05/18/deppcannes-1684376950-16843769-7808-2139-1684377768.jpg?w=500&h=300&q=100&dpr=2&fit=crop&s=LLzHRXv7WX6Rw8c-5je0Lg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
def main():
    # set_bg_hack_url()
    st.image('https://vcdn1-giaitri.vnecdn.net/2023/05/18/deppcannes-1684376950-16843769-7808-2139-1684377768.jpg?w=500&h=300&q=100&dpr=2&fit=crop&s=LLzHRXv7WX6Rw8c-5je0Lg',caption="THANK YOU FOR YOUR SERVICE MR TAN")
    

    tab1,tab2,tab3,tab4 = st.tabs(["CSV Formatter - Invoices","CSV Formatter - Contacts","Excel Date Formatter","DB Replacer"])
    with tab1:
        st.title("CSV Format - Invoicessssssss")
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
                st.dataframe(formatted_df)

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
                st.dataframe(formatted_df2)

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
    with tab4:
        st.title("DB Replacer")
        # Upload CSV file
        sql_file = st.file_uploader("Upload DB file", type="sql")
        uploaded_excel = st.file_uploader("Upload excel data", type="xlsx")
    
        if uploaded_excel is not None:
            try:
                excel  = pd.read_excel(uploaded_excel,header=0,sheet_name='Sheet1')
            except:
                st.write('Please put data into sheet name "Sheet1" and try again.')
        if sql_file is not None:
            # with open(sql_file,'r') as file:
            sql_str = sql_file.read().decode('utf-8')
                # Format button
            if st.button("Format"):
                progress_text = "Replacing is in progress. Please wait."
                my_bar = st.progress(0.0, text=progress_text)
                start_time = time.time()
                new_excel = pd.melt(excel,id_vars = 'Alias',var_name='Find',value_name='Replace')
                new_excel['Alias'] = new_excel['Alias'].str.lower().str.replace('(','').str.replace(')','').str.replace(' ','-')
                new_excel = new_excel.sort_values("Alias")
                df = new_excel.copy()
                df = df.reset_index(drop=True)
                df_report = df.copy()
                df_report['Status'] = ''
                status_text = st.empty()
                for index, row in df.iterrows():
                    time.sleep(0.05)
                    my_bar.progress((index+1)/len(df), text=progress_text)
                    
                    find = str(row['Find']).strip()
                    replace = str(row['Replace']).replace('percent','%').strip()
                    replace = replace.replace("'",r"\'").replace("\n","").replace("\r","")
            #         replace = replace.replace("'",r"\'").replace("/",r"\/").replace("/",r"\/").replace("\n","").replace("\r","")
                    if find == 'abc,def' and not replace  == '-':
                        replace = f'{int(replace):,}'
                    dump = find.replace('$','\$').replace('(','\(').replace(')','\)').replace('\\', r'\\').replace('\/', r'/')
                    alias = row['Alias'].strip()
                    # if index%100==0:
                    status_text.write(f'{index}/{len(df)}')
            #         for i in range(2):
                    result = re.subn(fr"(?<={alias}).+{dump}(?=[^a-zA-Z])",lambda x: x.group().replace(find,replace),sql_str)
                    if not result[1]==0:
                        
                        sql_str = result[0]
                        df_report.at[index,'Status'] = 'Sucess'
                    else:
                        df_report.at[index,'Status'] = 'Counld not find'
                time.sleep(1)
                my_bar.empty()
                st.write("--- %s minutes ---" % ((time.time() - start_time)/60))
                with open(os.path.join("/tmp", sql_file.name), "w") as f:
                    f.write(sql_str)
                # sql_file.write(sql_str)
                # Download formatted CSV button
                download_file(sql_file)
                display_missing_df = df_report[df_report['Status']=='Counld not find']
                st.write(f'Report: {len(display_missing_df)} Could not find')
                st.dataframe(display_missing_df)
                st.write('Download Report:')
                download_excel(df_report)
if __name__ == '__main__':
    main()
