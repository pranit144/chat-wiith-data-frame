from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import BytesIO
import base64

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    # Default dataset_info when no file is uploaded
    dataset_info = {
        "Number of Rows": 0,
        "Number of Columns": 0,
        "Columns": [],
        "Numerical Summary": '',
        "Categorical Summary": '',
        "Missing Values": {}
    }
    return render_template('index.html', dataset_info=dataset_info)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return redirect(url_for('visualize', file_name=file.filename))


@app.route('/visualize/<file_name>')
def visualize(file_name):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    df = pd.read_csv(file_path)

    dataset_info = {
        "Number of Rows": df.shape[0],
        "Number of Columns": df.shape[1],
        "Columns": list(df.columns),
        "Numerical Summary": df.describe(include=[float, int]).to_html(),
        "Categorical Summary": df.describe(include=[object, 'category']).to_html(),
        "Missing Values": df.isnull().sum().to_dict()
    }

    plot_images = []
    insights = []

    # Line Plot: Overall Trend
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='Year', y='Number_of_Students', ax=ax).set_title('Overall Trend')
    overall_trend = df.groupby('Year')['Number_of_Students'].sum()
    insights.append(f"Overall Trend: The highest number of students was in {overall_trend.idxmax()} with {overall_trend.max()} students.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Line Plot: Trend by Branch
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='Year', y='Number_of_Students', hue='Branch', ax=ax).set_title('Trend by Branch')
    insights.append("Trend by Branch: This graph shows how student counts varied across branches over the years.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Bar Plot: Students by Branch
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df, x='Branch', y='Number_of_Students', ax=ax).set_title('Students by Branch')
    branch_totals = df.groupby('Branch')['Number_of_Students'].sum()
    insights.append(f"Students by Branch: The branch with the most students is {branch_totals.idxmax()} with {branch_totals.max()} students.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Bar Plot: Students by Category
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df, x='Category', y='Number_of_Students', ax=ax).set_title('Students by Category')
    category_totals = df.groupby('Category')['Number_of_Students'].sum()
    insights.append(f"Students by Category: The category with the most students is {category_totals.idxmax()} with {category_totals.max()} students.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Stacked Bar Plot: Students by Year and Gender
    fig, ax = plt.subplots(figsize=(12, 6))
    stacked = df.pivot_table(index='Year', columns='Gender', values='Number_of_Students', aggfunc='sum')
    stacked.plot(kind='bar', stacked=True, ax=ax, title='Students by Year and Gender')
    insights.append("Students by Year and Gender: This stacked bar plot shows the distribution of students by gender over the years.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Pie Chart: Proportion by Branch
    fig, ax = plt.subplots(figsize=(12, 6))
    df.groupby('Branch')['Number_of_Students'].sum().plot(kind='pie', ax=ax, autopct='%1.1f%%').set_title('Proportion by Branch')
    insights.append("Proportion by Branch: This pie chart shows the percentage of students in each branch.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Box Plot: Students by Branch
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x='Branch', y='Number_of_Students', ax=ax).set_title('Boxplot by Branch')
    insights.append("Boxplot by Branch: This boxplot highlights the variation in student counts across branches.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Heatmap: Correlation
    fig, ax = plt.subplots(figsize=(12, 6))
    correlation = df.select_dtypes(include=['float64', 'int64']).corr()
    sns.heatmap(correlation, annot=True, ax=ax).set_title('Correlation Heatmap')
    insights.append("Correlation Heatmap: This heatmap shows correlations between numerical variables.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Violin Plot: Students by Gender
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.violinplot(data=df, x='Gender', y='Number_of_Students', ax=ax).set_title('Violin Plot by Gender')
    insights.append("Violin Plot by Gender: This violin plot shows the distribution of student counts by gender.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Area Chart: Cumulative Students by Year
    fig, ax = plt.subplots(figsize=(12, 6))
    df.groupby('Year')['Number_of_Students'].sum().plot(kind='area', ax=ax).set_title('Cumulative Students by Year')
    insights.append("Cumulative Students by Year: This area chart shows the cumulative student counts by year.")
    img_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
    plt.close(fig)

    # Treemap: Students by Branch
    try:
        import squarify
        fig, ax = plt.subplots(figsize=(12, 6))
        branch_totals = df.groupby('Branch')['Number_of_Students'].sum()
        squarify.plot(sizes=branch_totals, label=branch_totals.index, ax=ax, alpha=0.8)
        ax.set_title('Treemap of Branches')
        ax.axis('off')
        insights.append("Treemap of Branches: This treemap provides a hierarchical view of student counts by branch.")
        img_stream = BytesIO()
        plt.tight_layout()
        plt.savefig(img_stream, format='png')
        img_stream.seek(0)
        plot_images.append(base64.b64encode(img_stream.getvalue()).decode('utf-8'))
        plt.close(fig)
    except ImportError:
        insights.append("Treemap not generated: 'squarify' package is not installed.")

    return render_template('index.html', plot_images=plot_images, dataset_info=dataset_info, insights=insights)


if __name__ == '__main__':
    app.run(debug=True)
