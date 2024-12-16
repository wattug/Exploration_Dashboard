import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load data
data = pd.read_csv("IdentifikasiIzinMCU.csv")
data2 = pd.read_csv("dataTerpasangTersampling.csv")

# Page Layout
st.set_page_config(page_title="Dashboard Eksplorasi", layout="wide")

# Title and Description
st.title("Dashboard Eksplorasi Bauksit Meliau")
st.write("Perkembangan TP selama proses eksplorasi.")

# Mobile-Friendly Design: Toggle between Tabs
tab1, tab2, tab3 = st.tabs(["Seluruh Data", "Data per Spasi", "Peta & Data"])

with tab1:
    st.write("## Seluruh Data")
    st.write("Bagian ini menjelaskan perkembangan proses Identifkasi, Perizinan, Preukur Terpasang, dan Sampling  di setiap spasi di setiap prospek.")
    
    # Pivot Table for Identifikasi dan Perizinan
    pivot_all_spasi = data.pivot_table(index='Wilayah', columns='Status', values='Spasi', aggfunc='count', fill_value=0)

    # Display Matrix Representation
    st.write("### Matriks Identifikasi dan Perizinan")
    st.dataframe(pivot_all_spasi)

    # Pivot Table for Preukur Terpasang dan Sampling
    pivot_all_spasi2 = data2.pivot_table(index='Daerah', columns='Status', values='SPASI', aggfunc='count', fill_value=0)

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
            text=pivot_all_spasi[status],  # Display values on bars
            textposition='auto',  # Position text is auto 
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

    # Grouped Bar Chart for All Spasi
    st.write("### Diagram Batang Preukur Terpasang dan Tersampling")
    fig_all_spasi = go.Figure()
    for status in pivot_all_spasi2.columns:
        fig_all_spasi.add_trace(go.Bar(
            x=pivot_all_spasi2.index,
            y=pivot_all_spasi2[status],
            name=status,
            text=pivot_all_spasi2[status],  # Display values on bars
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
    st.write("## Data setiap Spasi")
    st.write("### Matriks Identifikasi dan Perizinan")
    
    unique_spasi = data['Spasi'].unique()
    
    for spasi_value in unique_spasi:
        spasi_data = data[data['Spasi'] == spasi_value]

        # Pivot Table for the Current Spasi
        pivot_spasi = spasi_data.pivot_table(index='Wilayah', columns='Status', values='Spasi', aggfunc='count', fill_value=0)
        
        # Display Matrix for Each Spasi
        st.write(f"### Matriks Spasi {spasi_value}")
        st.dataframe(pivot_spasi)

    st.write("### Matriks Preukur Terpasang dan Tersampling")
    
    for SPASI_value in unique_spasi:
        SPASI_data = data2[data2['SPASI'] == SPASI_value]

        # Pivot Table for the Current SPASI
        pivot_SPASI = SPASI_data.pivot_table(index='Daerah', columns='Status', values='SPASI', aggfunc='count', fill_value=0)
        
        # Display Matrix for Each SPASI
        st.write(f"### Matriks untuk spasi: {SPASI_value}")
        st.dataframe(pivot_SPASI)

    st.write("### Diagram Identifikasi dan Perizinan")
    
    for i, spasi_value in enumerate(unique_spasi):
        spasi_data = data[data['Spasi'] == spasi_value]

        # Pivot Table for the Current Spasi
        pivot_spasi = spasi_data.pivot_table(index='Wilayah', columns='Status', values='Spasi', aggfunc='count', fill_value=0)
        # Bar Chart for Each Spasi
        st.write(f"### Diagram Spasi {spasi_value}")
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
            barmode='group',
            xaxis_title="Prospek",
            yaxis_title="Jumlah Titik",
            template="plotly_dark",
            height=350,
            margin=dict(l=40, r=100, t=50, b=100),
            autosize=True,
        )
        st.plotly_chart(fig_spasi, use_container_width=True, key=f"fig_spasi_{i}")

    st.write("### Diagram Preukur Terpasang dan Tersampling")
    
    for i, SPASI_value in enumerate(unique_spasi):
        SPASI_data = data2[data2['SPASI'] == SPASI_value]

        # Pivot Table for the Current SPASI
        pivot_SPASI = SPASI_data.pivot_table(index='Daerah', columns='Status', values='SPASI', aggfunc='count', fill_value=0)
        # Bar Chart for Each SPASI
        st.write(f"### Diagram spasi {SPASI_value}")
        fig_SPASI = go.Figure()
        for status in pivot_SPASI.columns:
            fig_SPASI.add_trace(go.Bar(
                x=pivot_SPASI.index,
                y=pivot_SPASI[status],
                name=status,
                text=pivot_SPASI[status],  # Display values on bars
                textposition='auto',  # Position text inside the bars
            ))

        fig_SPASI.update_layout(
            barmode='group',
            xaxis_title="Prospek",
            yaxis_title="Jumlah Titik",
            template="plotly_dark",
            height=350,
            margin=dict(l=40, r=100, t=50, b=100),
            autosize=True,
        )
        st.plotly_chart(fig_SPASI, use_container_width=True, key=f"fig_SPASI_{i}")

with tab3:
    st.write("## Peta & Data")

    # Scatter map for `data`
    map_fig_data = px.scatter_mapbox(
        data, lat='Y', lon='X', color='Status', 
        title="Peta Progress Identifikasi dan Terizin",
        hover_data=['Wilayah', 'Spasi', 'Status']
    )

    # Scatter map for `data2`
    map_fig_data2 = px.scatter_mapbox(
        data2, lat='latitude', lon='longitude', color='Status', 
        title="Peta Progress Presurvey Terukur dan Tersampling",
        hover_data=['Daerah', 'SPASI', 'Status']
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

    # Expandable sections for both datasets
    with st.expander("Data Identifikasi dan Perizinan"):
        st.dataframe(data)

    with st.expander("Data Preukur Terpasang dan Tersampling"):
        st.dataframe(data2)

# Final Optimizations
st.write("## Summary")
st.write("Dashboard ini digunakan untuk kegiatan pengawasan harian proses Identifikasi dan Perizinan sepanjang kegiatan eksplorasi berlangsung.")
