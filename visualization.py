import streamlit as st
import plotly.express as px
import pandas as pd

def plot_prediction_proba(proba_df):
    """Plot the probability distribution of predicted sleep disorders"""
    # Ensure probabilities are in percentage format
    proba_df['Probability'] = proba_df['Probability'].round(2)  # Round to 2 decimal places
    proba_df['Probability_Label'] = proba_df['Probability'].astype(str) + '%'

    # Create a bar chart with Plotly
    fig = px.bar(
        proba_df,
        x='Disorder',
        y='Probability',
        text='Probability_Label',  # Use the percentage label for display
        title='Prediction Probability Distribution',
        color='Disorder',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=400
    )

    # Customize the layout to avoid label overlap
    fig.update_traces(
        textposition='auto',  # Automatically adjust text position to avoid overlap
        textfont=dict(size=14, color='black')
    )
    fig.update_layout(
        xaxis_title="Sleep Disorder",
        yaxis_title="Probability (%)",
        yaxis=dict(range=[0, 100], tickformat=".0f"),  # Ensure y-axis is in percentage scale
        plot_bgcolor='rgba(240, 240, 240, 0.9)',  # Light background for readability
        paper_bgcolor='rgba(240, 240, 240, 0.9)',
        font=dict(size=12),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_sleep_patterns(sleep_df):
    """Plot sleep patterns based on advanced sleep log data"""
    # Example: Plot average sleep duration and quality over time
    sleep_df['Date'] = pd.to_datetime(sleep_df['Date'])
    fig = px.line(
        sleep_df,
        x='Date',
        y=['Sleep Duration', 'Quality of Sleep'],
        title='Sleep Patterns Over Time',
        labels={'value': 'Value', 'variable': 'Metric'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Value",
        height=400,
        plot_bgcolor='rgba(240, 240, 240, 0.9)',
        paper_bgcolor='rgba(240, 240, 240, 0.9)'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_prediction_distribution(logs_df):
    """Plot distribution of predictions from logs"""
    fig = px.histogram(
        logs_df,
        x='prediction',
        title='Distribution of Sleep Disorder Predictions',
        color='prediction',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        xaxis_title="Predicted Disorder",
        yaxis_title="Count",
        height=400,
        plot_bgcolor='rgba(240, 240, 240, 0.9)',
        paper_bgcolor='rgba(240, 240, 240, 0.9)'
    )
    st.plotly_chart(fig, use_container_width=True)