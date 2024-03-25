from flask import Flask, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

app = Flask(__name__)

# Load your CSV data into a Pandas DataFrame
df = pd.read_csv('tadhack_data - Sheet1.csv')

# Define pastel red color
pastel_red = '#FF6961'

@app.route('/')
def index():
    # Plot 1: Sentiment Rate (Bar Chart)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=df['sentiment'].value_counts().index, y=df['sentiment'].value_counts(), color=pastel_red)
    plt.xlabel('sentiment')
    plt.ylabel('Count')
    plt.title('Customer Satifaction Distribution')
    sentiment_rate_img = plot_to_base64()

    # Plot 2: VID (Bar Chart)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=['Total', 'Unknown'], y=[df['VID'].replace('unknown', np.nan).dropna().astype(float).sum(), df['VID'].value_counts()['unknown']], color=pastel_red)
    plt.xlabel('VID')
    plt.ylabel('Count')
    plt.title('VID Distribution')
    vid_img = plot_to_base64()

    # Plot 3: Reason For Calling (Bar Chart)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=df['Reason For Calling'].value_counts().index, y=df['Reason For Calling'].value_counts(), color=pastel_red)
    plt.xlabel('Reason For Calling')
    plt.ylabel('Count')
    plt.title('Reason For Calling Distribution')
    reason_for_calling_img = plot_to_base64()

    # Plot 4: Who (Bar Chart)
    plt.figure(figsize=(8, 6))
    sns.barplot(y=df['Who'].value_counts().index, x=df['Who'].value_counts(), color=pastel_red)
    plt.xlabel('Count')
    plt.ylabel('Who')
    plt.title('Who Distribution')
    who_img = plot_to_base64()

    # Plot 5: Department (Bar Chart)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=df['Department'].value_counts().index, y=df['Department'].value_counts(), color=pastel_red)
    plt.xlabel('Department')
    plt.ylabel('Count')
    plt.title('Department Distribution')
    department_img = plot_to_base64()

    # Plot 6: Date (Line Graph)
    plt.figure(figsize=(8, 6))
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'].value_counts().sort_index().plot(color=pastel_red)
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Call Count Over Time')
    date_img = plot_to_base64()

    return render_template('index.html', 
                           sentiment_rate_img=sentiment_rate_img, 
                           vid_img=vid_img, 
                           reason_for_calling_img=reason_for_calling_img, 
                           who_img=who_img, 
                           department_img=department_img, 
                           date_img=date_img)

def plot_to_base64():
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

if __name__ == '__main__':
    app.run(debug=True)