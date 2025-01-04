# app.py
import streamlit as st
from st_keyup import st_keyup
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Page Layout
st.set_page_config(page_title="Dashboard Eksplorasi", layout="wide")

# Title and Description
st.title("Dashboard Eksplorasi Bauksit Meliau")
st.write("Perkembangan TP selama proses eksplorasi.")

# Mobile-Friendly Design: Toggle between Tabs
tab1, tab2, tab3 = st.tabs(["Matriks Data", "Tabel Data", "Peta"])

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Load data
data = conn.read(worksheet=0)
data2 = conn.read(worksheet=945353715)
with tab1:
    st.write("## Matriks Data")
    st.write("Bagian ini menjelaskan perkembangan proses Identifkasi, Perizinan, Preukur Terpasang, dan Sampling di setiap spasi di setiap prospek.")
    
    # Pivot Table for Identifikasi dan Perizinan with Total column and Total row
    pivot_all_spasi = data.pivot_table(index='Wilayah', columns='Status', values='Spasi', aggfunc='count', fill_value=0)
    pivot_all_spasi = pivot_all_spasi.assign(Total=pivot_all_spasi.sum(axis=1))
    pivot_all_spasi.loc['Total'] = pivot_all_spasi.sum(axis=0)

    # Display Matrix Representation
    st.write("### Matriks Identifikasi dan Perizinan")
    st.dataframe(pivot_all_spasi)

    # Pivot Table for Preukur Terpasang dan Sampling with Total column and Total row
    pivot_all_spasi2 = data2.pivot_table(index='Daerah', columns='Status', values='SPASI', aggfunc='count', fill_value=0)
    pivot_all_spasi2 = pivot_all_spasi2.assign(Total=pivot_all_spasi2.sum(axis=1))
    pivot_all_spasi2.loc['Total'] = pivot_all_spasi2.sum(axis=0)

    # Display Matrix Representation
    st.write("### Matriks Preukur dan Sampling")
    st.dataframe(pivot_all_spasi2)

    # Grouped Bar Chart for All Spasi
    st.write("### Diagram Batang Identifikasi dan Perizinan")
    fig_all_spasi = go.Figure()
    for status in pivot_all_spasi.columns:
        fig_all_spasi.add_trace(go.Bar(
            x=pivot_all_spasi.index,
            y=pivot_all_spasi[status],
            name=status,
            text=pivot_all_spasi[status],
            textposition='auto',
        ))

    fig_all_spasi.update_layout(
        barmode='group',
        xaxis_title="Prospek",
        yaxis_title="Jumlah Titik",
        template="plotly_dark",
        height=350,
        margin=dict(l=40, r=100, t=50, b=100),
        autosize=True,
    )
    st.plotly_chart(fig_all_spasi, use_container_width=True)

    # Grouped Bar Chart for All Spasi
    st.write("### Diagram Batang Preukur Terpasang dan Tersampling")
    fig_all_spasi2 = go.Figure()
    for status in pivot_all_spasi2.columns:
        fig_all_spasi2.add_trace(go.Bar(
            x=pivot_all_spasi2.index,
            y=pivot_all_spasi2[status],
            name=status,
            text=pivot_all_spasi2[status],
            textposition='auto',
        ))

    fig_all_spasi2.update_layout(
        barmode='group',
        xaxis_title="Prospek",
        yaxis_title="Jumlah Titik",
        template="plotly_dark",
        height=350,
        margin=dict(l=40, r=100, t=50, b=100),
        autosize=True,
    )
    st.plotly_chart(fig_all_spasi2, use_container_width=True)

    st.write("## Matriks Data setiap Spasi")
    st.write("### Matriks Identifikasi dan Perizinan")
    
    unique_spasi = data['Spasi'].unique()
    
    for spasi_value in unique_spasi:
        spasi_data = data[data['Spasi'] == spasi_value]

        # Pivot Table for the Current Spasi with Total
        pivot_spasi = spasi_data.pivot_table(index='Wilayah', columns='Status', values='Spasi', aggfunc='count', fill_value=0)
        pivot_spasi = pivot_spasi.assign(Total=pivot_spasi.sum(axis=1))
        pivot_spasi.loc['Total'] = pivot_spasi.sum(axis=0)

        # Display Matrix for Each Spasi
        st.write(f"### Matriks Spasi {spasi_value}")
        st.dataframe(pivot_spasi)

    st.write("### Matriks Preukur Terpasang dan Tersampling")
    
    for SPASI_value in unique_spasi:
        SPASI_data = data2[data2['SPASI'] == SPASI_value]

        # Pivot Table for the Current SPASI with Total
        pivot_SPASI = SPASI_data.pivot_table(index='Daerah', columns='Status', values='SPASI', aggfunc='count', fill_value=0)
        pivot_SPASI = pivot_SPASI.assign(Total=pivot_SPASI.sum(axis=1))
        pivot_SPASI.loc['Total'] = pivot_SPASI.sum(axis=0)

        # Display Matrix for Each SPASI
        st.write(f"### Matriks spasi {SPASI_value}")
        st.dataframe(pivot_SPASI)

with tab2:
    st.write("## Tabel Data")

    # Expandable sections for both datasets
    with st.expander("Data Identifikasi dan Perizinan"):
        name = st_keyup("Search Bar Identifikasi dan Perizinan", key="unique_key_1")

        if name:
            filtered = data[data.apply(lambda row: row.astype(str).str.lower().str.contains(name.lower(), na=False).any(), axis=1)]
        else:
            filtered = data
        
        st.write(len(filtered), "data ditemukan")
        st.write(filtered)

    with st.expander("Data Preukur Terpasang dan Tersampling"):
        name = st_keyup("Search Bar Terpasang dan Tersampling", key="unique_key_2")

        if name:
            filtered = data2[data2.apply(lambda row: row.astype(str).str.lower().str.contains(name.lower(), na=False).any(), axis=1)]
        else:
            filtered = data2
        
        st.write(len(filtered), "data ditemukan")
        st.write(filtered)

with tab3:
    st.write("## Peta")

    # Scatter map for `data`
    map_fig_data = px.scatter_mapbox(
        data, lat='Y', lon='X', color='Status', 
        title="Peta Progress Identifikasi dan Terizin",
        hover_data=['Wilayah', 'Spasi', 'Status', 'Name']
    )

    # Scatter map for `data2`
    map_fig_data2 = px.scatter_mapbox(
        data2, lat='latitude', lon='longitude', color='Status', 
        title="Peta Progress Presurvey Terukur dan Tersampling",
        hover_data=['Daerah', 'SPASI', 'Status', 'Pemilik Lahan']
    )

    # Update layouts for both maps
    map_fig_data.update_layout(
        mapbox_style="open-street-map", 
        mapbox_zoom=10, 
        mapbox_center={"lat": data['Y'].mean(), "lon": data['X'].mean()}
    )
    map_fig_data2.update_layout(
        mapbox_style="open-street-map", 
        mapbox_zoom=10, 
        mapbox_center={"lat": data2['latitude'].mean(), "lon": data2['longitude'].mean()}
    )

    # Display maps
    st.plotly_chart(map_fig_data, use_container_width=True)
    st.plotly_chart(map_fig_data2, use_container_width=True)

# Final Optimizations
st.write("## Summary")
st.write("Dashboard ini digunakan untuk kegiatan pengawasan harian proses Identifikasi dan Perizinan sepanjang kegiatan eksplorasi berlangsung.")
