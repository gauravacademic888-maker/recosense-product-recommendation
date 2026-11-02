# RecoSense – AI Product Recommendation & Customer Preference System

Project: BCA Vth Semester
Technology Stack: Python, Flask, Pandas, Scikit-learn, HTML, CSS, and Machine Learning

## 1. How to Run the Project on Windows

Follow these steps to run the RecoSense project on your Windows laptop.

Step 1: Install Python

* Install Python 3.10 or above from the official Python website.
* During installation, make sure to select the "Add Python to PATH" checkbox.

Step 2: Open the Project Folder

* Place the complete project folder on your Desktop.
* Open the project folder.
* Click on the address bar, type cmd, and press Enter.
* This will open Command Prompt directly inside the project directory.

Step 3: Install Required Libraries

Run the following command:

pip install -r requirements.txt

This command installs all the Python libraries required to run the project. An internet connection is required for this step. It needs to be performed only once.

Step 4: Generate Sample Data (Optional)

If you want to generate new sample datasets, execute:

python generate_data.py

The project already contains sample CSV datasets inside the data/ folder, so you can skip this step.

Step 5: Start the Application

Run the following command:

python app.py

Step 6: Open the Website

Open your web browser and visit:

http://127.0.0.1:5000

The RecoSense application will now be running locally on your laptop.

Note: Once the required libraries are installed, the project does not require an internet connection during the demonstration.

## 2. Project File Structure and Their Functions

The project contains the following main files and directories:

1. generate_data.py
   Generates sample product, customer, and purchase datasets.

2. recommender.py
   Implements the complete machine learning recommendation system, including Content-Based Filtering, Collaborative Filtering, Hybrid Recommendation, RFM Segmentation, and model evaluation.

3. app.py
   Runs the Flask web application and manages the dashboard, customer profiles, product targeting, and JSON API.

4. templates/
   Contains HTML templates used to design and display the website pages.

5. data/
   Stores three CSV datasets containing product, customer, and purchase information.

6. requirements.txt
   Contains the list of Python libraries required to run the project.

## 3. Machine Learning Algorithms and Working (For Viva)

RecoSense uses multiple machine learning techniques to understand customer preferences and generate personalized product recommendations.

### 3.1 Content-Based Filtering

* This technique recommends products based on their features and descriptions.
* Product names, categories, and descriptions are converted into numerical representations using TF-IDF (Term Frequency–Inverse Document Frequency).
* Cosine Similarity is then used to calculate the similarity between products.
* Products with similar features are recommended to customers.

Example: If a customer purchases a smartphone, the system may recommend similar smartphones or related electronic accessories.

### 3.2 Collaborative Filtering

* This technique recommends products based on the purchasing behaviour of different customers.
* It identifies relationships between products purchased by the same customers.
* An item-item similarity matrix is generated using Cosine Similarity.
* Products frequently purchased by similar customer groups can be recommended to other customers.

Example: If customers who purchased Product A also purchased Product B, the system may recommend Product B to customers interested in Product A.

### 3.3 Hybrid Recommendation System

* The Hybrid Recommendation System combines Content-Based Filtering and Collaborative Filtering.
* It uses both product information and customer purchasing behaviour to generate recommendations.
* In this project, both recommendation techniques contribute 50% each to the final recommendation score.
* The weighting factor, called alpha, can be adjusted in recommender.py.

Formula:

Hybrid Score = (0.5 × Content-Based Score) + (0.5 × Collaborative Score)

This approach combines the advantages of both recommendation techniques.

### 3.4 Customer Segmentation Using RFM Analysis

The project uses RFM Analysis (Recency, Frequency, and Monetary) to understand customer purchasing behaviour.

The three RFM parameters are:

* Recency: How recently a customer made a purchase.
* Frequency: How frequently a customer makes purchases.
* Monetary: How much money a customer has spent.

After calculating these values, the system applies the K-Means Clustering Algorithm with four clusters.

Customers are divided into four segments:

1. High-Value Customers
2. Loyal Customers
3. Regular Customers
4. At-Risk Customers

This segmentation helps businesses understand their customers and plan targeted marketing campaigns.

### 3.5 Model Evaluation and Accuracy Testing

* The system evaluates its recommendation performance using a testing technique called Hit Rate@5.
* For each customer, the most recent purchase is temporarily hidden.
* The recommendation system generates five recommendations based on the remaining purchase history.
* The system checks whether the hidden product appears among those five recommendations.
* The results are displayed in the accuracy evaluation table on the dashboard.

Hit Rate@5 measures how frequently the actual purchased product appears within the top five recommendations.

### 3.6 Cold Start Problem

The Cold Start Problem occurs when the system does not have sufficient purchase history for a new customer.

To handle this problem:

* The system identifies customers with no previous purchase history.
* Instead of generating personalized recommendations, it displays popular products.
* This allows new customers to receive recommendations even without previous purchasing data.

## 4. Project Demonstration Flow (5-Minute Demo)

Follow this sequence while presenting the project to your faculty members.

Step 1: Dashboard
Show total customers, products, purchases, customer segments, and recommendation evaluation results.

Step 2: Customer Recommendations
Click on the High-Value Customer segment, select a customer, and open the View Recommendations page.

Step 3: Explainable Recommendations
Explain the "Because you bought..." section to demonstrate how the system generates relevant recommendations.

Step 4: Product Targeting
Open the Product Targeting section, select a product, and demonstrate which customers are suitable for receiving its recommendations.

Step 5: JSON API
Open the recommendation API endpoint in the browser and demonstrate how external applications can access recommendation results.

API Demonstration Example:

http://127.0.0.1:5000/api/recommend/5

This API returns recommendation results in JSON format for the selected customer.

It demonstrates how other websites or business applications can integrate the recommendation functionality into their platforms.

## 5. How to Use Real Business Data

RecoSense allows businesses to replace the existing sample datasets with their own customer, product, and purchase information.

To use real business data:

1. Open the data/ folder.
2. Replace the existing three CSV files with your own datasets.
3. Make sure the new datasets follow the same column structure.
4. Restart the Flask application.

The required CSV formats are explained below.

### 5.1 products.csv

Contains product-related information.

Required columns:

* product_id: Unique product identification number.
* name: Product name.
* category: Product category.
* price: Product price.
* description: Product description.

### 5.2 customers.csv

Contains customer-related information.

Required columns:

* customer_id: Unique customer identification number.
* name: Customer name.
* city: Customer's city.

### 5.3 purchases.csv

Contains customer purchase history.

Required columns:

* customer_id: Customer identification number.
* product_id: Purchased product identification number.
* date: Purchase date in YYYY-MM-DD format.
* quantity: Number of units purchased.

After replacing the datasets, restart the application using:

python app.py

The system will use the updated datasets to generate recommendations and customer segments.

## 6. Common Errors and Their Solutions

The following are some common errors that may occur while running the project.

1. Error: 'python' is not recognized

Solution: Install Python again and ensure that the Add Python to PATH option is selected.

2. Error: pip command is not working

Solution: Use the following command instead:

python -m pip install -r requirements.txt

3. Error: Port already in use

Solution: Change the application port from 5000 to 5001 in the app.py file.

4. Error: Missing CSV file

Solution: Check whether all three CSV files are available inside the data/ folder.

5. Error: Module not found

Solution: Install the missing Python library using pip.

Changing the Application Port:

If port 5000 is already being used by another application, update the last line of app.py:

app.run(port=5001)

Then run the application again and open:

http://127.0.0.1:5001

## 7. Project Summary

RecoSense is an AI-powered product recommendation and customer preference analysis system developed using Python, Flask, Pandas, and Scikit-learn.

The system combines Content-Based Filtering, Collaborative Filtering, Hybrid Recommendation Techniques, and RFM-based Customer Segmentation to understand customer purchasing behaviour and generate personalized product recommendations.

It also provides a web-based dashboard, product targeting functionality, recommendation evaluation, and API integration.

The primary objective of RecoSense is to help businesses understand customer preferences, improve product discovery, create targeted marketing strategies, and enhance the overall customer shopping experience.

## 8. Project Details

Project Name: RecoSense – AI Product Recommendation & Customer Preference System

Academic Program: Bachelor of Computer Applications (BCA)

Semester: Vth Semester

Programming Language: Python

Web Framework: Flask

Machine Learning Library: Scikit-learn

Data Processing Library: Pandas

Frontend Technologies: HTML and CSS

Project Category: Artificial Intelligence and Machine Learning

Project Objective: To develop an intelligent product recommendation system that analyses customer preferences and purchasing behaviour to provide personalized product suggestions and support business decision-making.
