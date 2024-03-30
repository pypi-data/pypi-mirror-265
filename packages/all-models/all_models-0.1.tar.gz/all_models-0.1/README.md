# Machine Learning Models for Regression and Classification Tasks

This repository contains a collection of machine learning models implemented using various algorithms and evaluated on test datasets. 

## Introduction

In this repository, we have implemented a variety of machine learning models for both regression and classification tasks. Each model is trained on a given dataset and evaluated using appropriate evaluation metrics. The main purpose of this repository is to provide a comprehensive comparison of different machine learning algorithms and their performance on various datasets.

## List of Models

### Regression Models
- XGBoost Regressor
- XGBoost Random Forest Regressor
- Gradient Boosting Regressor
- Random Forest Regressor
- AdaBoost Regressor
- Bagging Regressor
- Extra Trees Regressor
- Linear Regression
- Ridge Regression
- Lasso Regression
- Elastic Net
- Bayesian Ridge
- Huber Regressor
- Lars
- Lasso Lars
- Lasso Lars IC
- Orthogonal Matching Pursuit
- Passive Aggressive Regressor
- RANSAC Regressor
- SGD Regressor
- Theil-Sen Regressor
- Support Vector Regressor (SVR)
- Linear Support Vector Regressor (LinearSVR)
- K-Nearest Neighbors Regressor (KNeighborsRegressor)
- Radius Neighbors Regressor (RadiusNeighborsRegressor)
- Multi-layer Perceptron Regressor (MLPRegressor)

### Classification Models
- XGBoost Classifier
- XGBoost Random Forest Classifier
- Gradient Boosting Classifier
- Random Forest Classifier
- AdaBoost Classifier
- Bagging Classifier
- Extra Trees Classifier
- Logistic Regression
- Perceptron
- Ridge Classifier
- SGD Classifier
- Decision Tree Classifier
- Extra Tree Classifier
- K-Nearest Neighbors Classifier (KNeighborsClassifier)
- Radius Neighbors Classifier (RadiusNeighborsClassifier)
- Multi-layer Perceptron Classifier (MLPClassifier)
- Bernoulli Restricted Boltzmann Machine (BernoulliRBM)

## Evaluation Metrics

For regression tasks, the following evaluation metrics are used:
- Mean Squared Error (MSE)
- Mean Absolute Error (MAE)
- R2 Score

For classification tasks, the following evaluation metrics are used:
- Accuracy
- F1 Score
- Precision
- Recall
- ROC AUC Score

## How to Use

Each model is implemented as a separate function that takes training and test data as input and prints the evaluation metrics. Users can import the required models and call the corresponding function with their data to evaluate the model performance.

## Requirements

The code in this repository requires the following Python libraries:
- xgboost
- scikit-learn
- numpy
- pandas

You can install these libraries using pip:
```bash
pip install xgboost scikit-learn numpy pandas
```