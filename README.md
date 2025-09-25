# 🏀 BasketBall Game Prediction Pipeline

An end-to-end machine learning pipeline for predicting Basketball game outcomes. This modular system handles everything from data extraction and model training to deploying a serverless prediction API and maintaining an up-to-date database of game results.

## 📁 Project Architecture
f
This project is organized into three separate branches, each representing a distinct module of the pipeline.

| Branch | Purpose | Key Technologies |
| :--- | :--- | :--- |
| [**`BasketBallNotebook`**](https://github.com/EagleAI-Research/BasketBall/BasketBallNotebook) | Data Science & Modeling | Python, Pandas, Scikit-learn, Jupyter |
| [**`BasketBallLambda`**](https://github.com/EagleAI-Research/BasketBall/BasketBallLambda) | Prediction API | AWS Lambda, Python, API Gateway |
| [**`BasketBallRDS`**](https://github.com/EagleAI-Research/BasketBall/BasketBallRDS) | Data Warehousing & Automation | AWS RDS, AWS Lambda, Python |

---

## 🧪 1. BasketBallNotebook (Data & Modeling)

This branch contains the core data science workflow for the project.

### Purpose
The goal of this module is to acquire raw Basketball data, explore it, engineer features, and train a predictive machine learning model.

### Contents
*   **Data Acquisition:** Scripts for scraping/ingesting data from sources like the Basketball API or stats.nba.com.
*   **Exploratory Data Analysis (EDA):** Jupyter notebooks for comprehensive data cleaning, visualization, and statistical analysis.
*   **Feature Engineering:** The process of creating predictive features from raw data.
*   **Model Training & Validation:** Building, training, and evaluating machine learning models to predict game outcomes.
*   **Output:** Serialized trained models (e.g., `.pkl` files) and cleaned CSV datasets for use in the other branches.

---

## ⚡ 2. BasketBallLambda (Prediction API)

This branch contains the code for serving model predictions in a production-like environment.

### Purpose
To create a serverless, scalable endpoint that can be called by a backend application to get predictions for ongoing and future games.

### Contents
*   **AWS Lambda Function:** The core function package written in Python.
*   **Model Loading:** Code to load the serialized model trained in the `BasketBallNBANotebook` branch.
*   **Preprocessing Logic:** Functions to preprocess incoming game data in real-time, ensuring it matches the pipeline used during training.
*   **Prediction Handler:** The main function that receives input, preprocesses it, runs the model, and returns a prediction.
*   **Integration:** Designed to be triggered via HTTP requests through AWS API Gateway.
---
## 🗄️ 3. BasketBallRDS (Data Warehousing)

This branch handles the automation for maintaining a persistent and historical record of game data.
### Purpose
To ensure the database is continuously updated with the latest game results, which is crucial for model re-training and historical analysis.

### Contents
*   **Automation Scripts:** Python scripts designed to run on a daily schedule (e.g., via a cron job on AWS EventBridge/Lambda).
*   **Data Fetching:** Code to fetch completed game statistics from the previous day.
*   **Data Preprocessing:** Cleans and structures the new data to match the database schema.
*   **Database Operations:** Executes `INSERT` and `UPDATE` operations on a MySQL/PostgreSQL database hosted on AWS RDS.
*   **Output:** A reliably updated database that serves as the single source of truth for all historical game data.

---

## 🚀 Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/EagleAI-Research/BasketBall.git
    ```

2.  **Explore a Module:** Check out the specific branch you are interested in.
    ```bash
    git checkout BasketBallNotebook
    ```
    *Repeat for `BasketBallLambda` and `BasketBallRDS`.*

3.  Each branch has its own detailed setup instructions and requirements. Please refer to the `README.md` file within each branch for specific steps.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
