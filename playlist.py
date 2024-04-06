import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from streamlit_gsheets import GSheetsConnection

csv_path = 'Playlistเพลง.csv'
df = pd.read_csv(csv_path)

import base64

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "BG.png"
        
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover;
        }}
        .stTextInput>div>div>div>label {{
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_hack('BG.jpg')


def upload_csv_to_google_sheet(csv_path, sheet_url, sheet_name):
    # Define the scope and credentials for Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('rbc12-419515-c3e9b5d05d48.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet and the specific worksheet
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_path)

    # Convert the DataFrame to a list of lists, which is the format expected by gspread
    data = df.values.tolist()

    # Update the worksheet with the data, starting from the first cell
    worksheet.update('A1', [df.columns.values.tolist()] + data)  # Include the header row



def create_orders_dataframe(sheet_url, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('rbc12-419515-c3e9b5d05d48.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)
    values = worksheet.get_all_values()
    df = pd.DataFrame(values[1:-1], columns=values[0])
    return df

sheet_url = "https://docs.google.com/spreadsheets/d/1Ss6rifwUQxeyGjKbgBJmpFbb4upg8R6OHbR1-e_C4OI/edit?usp=sharing"
sheet_name = "Orders"

orders = create_orders_dataframe(sheet_url, sheet_name)

with st.expander("queue ⤵"):
    st.write("song")
    st.dataframe(orders[:5])



house = st.text_input("House Name")
name = st.text_input("Name")
song = st.text_input("Song Name")
submit = st.button("Add")

if submit and name and house and song:
    # Add the new data to the DataFrame
    new_data = {'name':name,'house': house, 'song': song}
    df = df.append(new_data, ignore_index=True)
    
    # Step 3: Write the updated DataFrame back to the same CSV file
    df.to_csv(csv_path, index=False)
    
    st.success("Data added successfully!")
else:
    st.warning("Please fill in all the fields")

# Display the DataFrame
# st.write(df)

csv_path = 'Playlistเพลง.csv'
sheet_url = 'https://docs.google.com/spreadsheets/d/1Ss6rifwUQxeyGjKbgBJmpFbb4upg8R6OHbR1-e_C4OI/edit?usp=sharing'
sheet_name = 'Orders'
upload_csv_to_google_sheet(csv_path, sheet_url, sheet_name)
