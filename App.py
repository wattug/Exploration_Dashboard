import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load data
data = pd.read_csv("IdentifikasiIzinMCU.csv")

# Page Layout
st.set_page_config(page_title="Wilayah Dashboard", layout="wide")

# Title and Description
st.title("Identifikasi dan Perizinan Meliau")
st.write("Perkembangan TP selama proses eksplorasi.")

# Mobile-Friendly Design: Toggle between Tabs
tab1, tab2, tab3 = st.tabs(["Semua Data", "Data per Spasi", "Peta & Data"])

with tab1:
    st.write("## Diagram Seluruh Data")
    st.write("Bagian ini menjelaskan perkembangan proses Identifkasi dan Perizinan di setiap spasi di setiap prospek.")

    # Create Grouped Bar Chart for All Spasi
    st.write("### Diagram Batang Keseluruhan Data")
    pivot_all_spasi = data.pivot_table(index='Wilayah', columns='Status', values='Spasi', aggfunc='count', fill_value=0)

    fig_all_spasi = go.Figure()
    for status in pivot_all_spasi.columns:
        fig_all_spasi.add_trace(go.Bar(
            x=pivot_all_spasi.index,
            y=pivot_all_spasi[status],
            name=status,
            text=pivot_all_spasi[status],  # Display values on bars
            textposition='auto',  # Position text outside the bars
        ))

    fig_all_spasi.update_layout(
        barmode='group',  # Grouped bars
        xaxis_title="Prospek",
        yaxis_title="Jumlah Titik",
        template="plotly_dark",
        height=350,
        margin=dict(l=40, r=100, t=50, b=100),
        autosize=True,
    )
    
    st.plotly_chart(fig_all_spasi, use_container_width=True)

with tab2:
    st.write("## Diagram Batang Terpisah Setiap Spasi")
    unique_spasi = data['Spasi'].unique()

    for spasi_value in unique_spasi:
        st.write(f"### Diagram Batang Spasi: {spasi_value}")
        
        spasi_data = data[data['Spasi'] == spasi_value]
        pivot_spasi = spasi_data.pivot_table(index='Wilayah', columns='Status', values='Spasi', aggfunc='count', fill_value=0)

        fig_spasi = go.Figure()
        for status in pivot_spasi.columns:
            fig_spasi.add_trace(go.Bar(
                x=pivot_spasi.index,
                y=pivot_spasi[status],
                name=status,
                text=pivot_spasi[status],  # Display values on bars
                textposition='auto',  # Position text inside the bars
            ))

        fig_spasi.update_layout(
            barmode='group',  # group bars
            xaxis_title="Prospek",
            yaxis_title="Jumlah Titik",
            template="plotly_dark",
            height=350,
            margin=dict(l=40, r=100, t=50, b=100),
            autosize=True,
        )

        st.plotly_chart(fig_spasi, use_container_width=True)

with tab3:
    st.write("## Peta & Data")


    st.write("Peta Titik per Status:")

    # Ensure that the 'X' and 'Y' columns exist in your data and contain latitude and longitude values
    # For the map, we assume 'X' is longitude and 'Y' is latitude
    map_fig = px.scatter_mapbox(data, lat='Y', lon='X', color='Status', 
                                title="Map: Points Colored by Status", 
                                hover_data=['Wilayah', 'Spasi', 'Status'])

    # Set the Mapbox style
    map_fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=10, mapbox_center={"lat": data['Y'].mean(), "lon": data['X'].mean()})

    # Display the map
    st.plotly_chart(map_fig, use_container_width=True)    # Show the original data matrix in a collapsible section

    with st.expander("Tampilkan Data"):
        st.dataframe(data)

# Final Optimizations:
st.write("\n\n")
st.write("## Summary")
st.write("Dashboard ini digunakan untuk kegiatan pengawasan harian proses Identifikasi dan Perizinan sepanjang kegiatan eksplorasi berlangsung.")