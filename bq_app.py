import streamlit as st
import json, requests, pandas as pd


def page_setup():
    st.header("Select your criteria to view ETFs.")


def call_cloud_function(function_url, query):
    """
    Calls a Google Cloud Function with a specified query.

    Args:
        function_url (str): The URL of the deployed Cloud Function.
        query (str): The BigQuery query to execute.

    Returns:
        dict: The JSON response from the Cloud Function, or None if an error occurred.
    """
    try:
        # Construct the JSON payload
        payload = {'query': query}

        # Set the headers for the request
        headers = {'Content-Type': 'application/json'}

        # Make the POST request to the Cloud Function
        response = requests.post(function_url, data=json.dumps(payload), headers=headers)

        # Raise an exception for bad status codes
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        # Parse the JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error calling Cloud Function: {e}")
        return None  # Indicate an error occurred



def main():
    selection = st.selectbox("Which criteria do you want of filter on?",
                             ("Company Name", "1-Year Return", "Sector"), index=None)
    if selection == "Company Name":
        cname = st.radio("Select one of the options:",["SPDR", "Vanguard", "iShares"], index=None)
        if cname == "SPDR":
            query = (
                    "SELECT * FROM `your-table` "  
                    "WHERE company = 'SPDR'"
                    )
        elif cname == "Vanguard":
            query = (
                    "SELECT * FROM `your-table` "  
                    "WHERE company = 'Vanguard'"
                    )
        elif cname == "iShares":
            query = (
                    "SELECT * FROM `your-table` "  
                    "WHERE company = 'iShares'"
                    )
        if not cname: st.stop()
        results = call_cloud_function(FUNCTION_URL, query)
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            print("Failed to call Cloud Function.")
                
    elif selection == "1-Year Return":
        return_choice = st.radio("Select one of the options:",["<0%", ">5%", ">12%"], index=None)
    elif selection == "Sector":
        st.write("oiweafds")


if __name__ == '__main__':
    page_setup()
    FUNCTION_URL = "" #plug in your function url
    main()
