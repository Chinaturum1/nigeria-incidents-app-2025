import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import altair as alt
import re



def load_data():
    # using pandas to load the dataset
    df = pd.read_csv("incidents.csv")
    #add new columns
    incident_list = []
    location_list = []
    for value in df['Title'].astype(str):
        #list comprehension
        parts = [p.strip() for p in re.split(r'[,\.\-]\s*',value )if p.strip()]

        if len(parts)>1:
            incident_list.append(parts[0])
            location_list.append(parts[-1])
        else:
            incident_list.append(parts[0])
            location_list.append(None)
    df["Incident"] = incident_list
    df["Location"] = location_list
    # more cleaning ops
    # convert dates
    df["Year"] = df['End date'].str.split("-",n=1,expand=True)[0]
    return df

def main():
    df = load_data()
    # using pandas to load the dataset
    st.title("Nigeria Incidents App 2025")
    
    # data preview
    st.write(df.head(5))

    # filters 
    # create filters 
    filters = {
        "Incident" : df["Incident"].unique(),
        "Location" : df["Location"].unique(),
        "Year" : df["Year"].unique()
    }
    # user selection 
    selected_filters = {}

    # generate multi-select widgets dynamically
    for key, options in filters.items():
        selected_filters[key]=st.sidebar.multiselect(key,options)
          
    # parse the filtered content into the dataframe
    df = df.copy()

    # apply filtered selection to the data 

    for key, selected_values in selected_filters.items():
        if selected_values:
            df = df[df[key].isin(selected_values)]

   # metrics
    st.subheader("Summary Section")

    # calculations
    no_of_incidents = df.shape[0]
    no_of_deaths = df["Number of deaths"].sum()

    # columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric("No of Incidents", no_of_incidents)

    with col2:
          st.metric("No of Deaths", no_of_deaths)
  
    # metric
    st.subheader("Incidents Value Counts")
    temp1 = df.Incident.value_counts().reset_index()
    st.dataframe(temp1)
    # st.write(temp1)
    # st.bar_chart(temp1[:10])

    # altair plotting library
    # bar chart
    # data for bar chart top 10
    temp1 = temp1.nlargest(10, 'count')
    
    chart1 = alt.Chart(temp1).mark_bar().encode(
        x=alt.X('count:Q', title="Incident Count"),
        y=alt.Y('Incident:N'),
    ).properties(height=300)

    # display the chart
    st.altair_chart(chart1)

if __name__ == "__main__":
    main()