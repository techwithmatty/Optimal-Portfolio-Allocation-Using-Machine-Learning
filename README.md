# Optimal Portfolio Allocation Using Machine Learning

## SUMMARY 

This project combines unsupervised and supervised Machine Learning techniques with Financial Theory and Statistics, to build a diversified stock portfolio using stocks from the S&P500 Index.

## FILES 

Data:
- S&P_500_End_of_Year_2020_Fundamental_FINAL.xlsx

Software/Deliverables:
- Constructing a Diversified Stock Portfolio using Machine Learning Techniques - FULL VERSION.ipynb 
- Classification Models - EVALUATION.ipynb
- Clustering Algorithms - EVALUATION.ipynb
- main.py

## SPEC

Runs on macOS Big Sur (Version 11.1) and Windows 10 (or later)
- Possible Backwards Compatibility

## RUNNING REQUIREMENTS

This project requires you to have the following tools installed:
- Python v3 (https://www.python.org/downloads/)
- Anaconda (https://www.anaconda.com/products/distribution)
- A Python IDE of your choice

After installing anaconda, install streamlit: 
- streamlit (https://docs.streamlit.io/library/get-started/installation)

The following python libraries should be installed:
- yfinance 0.1.70 or later (https://pypi.org/project/yfinance/)
- PyPortfolioOpt (https://pyportfolioopt.readthedocs.io/en/latest/)
- cvxpy (https://www.cvxpy.org/install/)
- arch (https://pypi.org/project/arch/)
- matplotlib (https://pypi.org/project/matplotlib/)
- sklearn (https://pypi.org/project/scikit-learn/)
- numpy (https://pypi.org/project/numpy/)
- pandas (https://pypi.org/project/pandas/)
- plotly (https://plotly.com/python/getting-started/)

You should be able to install most, if not all the above libraries using 'pip install (LIBRARY_NAME)'

## INSTRUCTIONS FOR FILES:

Constructing a Diversified Stock Portfolio using Machine Learning Techniques - FULL VERSION.ipynb 
- Contains the main investigation carried out in this priject

1. Save the 'S&P_500_End_of_Year_2020_Fundamental_FINAL.xlsx' file in a location of your choice
2. Go to the second block of code where the pandas reads the excel file into a DataFrame and change the line of code so the filepath is directed to the location where you saved the excel file.
3. Run the code


Clustering Algorithms - EVALUATION.ipynb
- Contains the evaluation of the clusering algorithms

1. Save the 'S&P_500_End_of_Year_2020_Fundamental_FINAL.xlsx' file in a location of your choice
2. Go to the second block of code where the pandas reads the excel file into a DataFrame and change the line of code so the filepath is directed to the location where you saved the excel file.
3. Run the code

Classification Models - EVALUATION.ipynb
- Contains the evaluation of the classification models

main.py
- Contains the user interface which demonstrates the practical use of our investigation
- It simulates the 2021 trading year (from 04/01/2021 to 31/12/2021)
- The data is from yfinance
- The stocks determined from the 'Constructing a Diversified Stock Portfolio using Machine Learning Techniques - FULL VERSION.ipynb' have been used in this application

1. Set up streamlit 
2. Open terminal and change the directory to the location where you downloaded 'main.py'
3. Run 'streamlit run main.py'
4. Input an initial amount on the sidebar (this has to be a minimum of 100 dollars)
5. Select allocation strategy
5. Click on the 'Generate Portfolio' button
6. You should see the current date, current porfolio value, profit/loss (which is initially N/A) and a pie chart of the initial allocation.
7. Click the 'Rebalance Portfolio' button and see the changes on the pie chart of the current holdings and scroll down to see a graph of the portfolio history.
8. Click the 'Rebalance Portfolio' another 12 times to simulate through the whole year.
9. Clear the cache before re-running the program.


