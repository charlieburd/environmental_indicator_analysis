# -*- coding: utf-8 -*-
"""ML_Yahoo_Fianance_Stock.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dNliobNkKXJ0mmZILVuzS4qxnEvpKzhp

# **FINAL PROJECT** - Columbia Engineering 2021

**Crypto Crystal Ball**

by Emmanuel Martinez, George Quintanilla and Charlie Burd.

### **Using nbinteract CLI Usage as #nbi:hide_in to hide our Python Code**

# **PART #1**

First, let's install all dependencies to have our Software up to date and with all tools that we need.
"""

!pip install nbinteract

!pip install pandas

!pip install pandas-datareader

!pip install plotly

!pip install datetime

!pip install numpy

!pip install yfinance

!pip install sklearn

"""## **Import ipywidgets to interact Jupyter Notebook over HTML**

### Key Feature is "Yahoo! Finance" to downloading histrocial market data.
"""

import ipywidgets as widgets

import pandas as pd 
from pandas_datareader import data 
import plotly.graph_objects as go 
import plotly.express as px # Plotly Dark Templates
import yfinance as yf # Key Import
from datetime import date 
from dateutil.relativedelta import relativedelta 
import numpy as np 
from sklearn.linear_model import LinearRegression # Machine Leraning (Linear Model)
from sklearn.model_selection import train_test_split # Machine Leraning (Train and Tool Model)

"""Below the Bash Colors in Python from **python_bash_font** GitHub"""

class color:
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   PURPLE = '\033[95m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   END = '\033[0m'

"""## **CORE CODE:**

As Machine Learning, our SVR (SVM) Model predicts from Yahoo Finance Librery Stock Historcal source.

From Pandas, "pandas_datareader" we're using "data" library, It's important because help during the process imported every time the END USER Ineraction.
"""

from pandas_datareader import data


# Date Vars Definicion (YYY-MM-DD)
start_date = '2020-01-01'
end_date = '2020-01-15'


# WHILE-TRUE as END USER Inputs for DataFrame interaction with Yahoo Finance.
# From PANDAS, DATAREADER to get our Final Data interaction.
while True:
    try:
        symbol = input('Enter a valid Stock Tricker Symbol: ')
        # We're using the "symbol" as Stock ticker, then "yahoo" for Yahoo Finance historial data, and last, "start_date" and "end_date" as Date manual input search criteria. 
        df = data.DataReader(symbol, 'yahoo', start_date, end_date)
        break
    # As en error respond: (Example: An invalid Stock Symbol) our END USER gerts the below to submit a valid ticker. 
    except(KeyError, OSError):
        print(color.RED + color.DARKCYAN + f'> {symbol} is not a valid Stock Symbol. Please submit a valid Stock Symbol, Example: BAC for Bank of America' + color.END) 




# Make a User Menu
print(color.BOLD + color.UNDERLINE + color.DARKCYAN + '\n> Please select from below an option to Analyzing your Stock Ticker Data:' + color.END)
choice = True
while choice:
    print(f'''\n SELECT FROM THE BELOW YOUR ANALYSIS OPTION: \n
    1 - Machine Learning 15 days Prediction (SVR Model) from Your Stock "{symbol}" Tricker.
    2 - Machine Learning 30 days Prediction (SVR Model) from Your Stock "{symbol}" Tricker.
    3 - Price Date Range Chart (YYY-MM-DD) from your Stock "{symbol}" Tricker.
    4 - Price Comparison from your Stock "{symbol}" Tricker with another Tricker.
    5 - Your Stock "{symbol}" Tricker 180 Past-Days Analysis.

    Q - Quit and Restart the Process using different Symbol or Stock Tricker.
    ''')
    choice = (input('''\nPlease select a Numeric Option (Example: For the Second Option type "1" and or "Q" to Quit.): '''))
    
    
    
    
    
    
    # ALL CONDITIONS (1 to 5 including Q option)
    
    # OPTION 1: Machine Learning 15 days Prediction from Your Stock "{symbol}" Tricker.
    if choice == '1' or choice == 'A' or choice == 'a':
        
        today = date.today()
        today = today.strftime('%Y-%m-%d')

        df = data.DataReader(symbol, 'yahoo', '2000-01-01', 'today')

        df = df[['Adj Close']]

        # N as Variable for 15 days
        n = 15


        df['Prediction'] = df[['Adj Close']].shift(-n)
        

        # Creating Independent DataSet "X"
        X = df.drop(['Prediction'],1)

        X = np.array(X)

        X = X[:-n]

        # Create the Dependent "Y" DataSet
        Y = df['Prediction']

        Y = np.array(Y)

        # Remove the last "n" rows
        Y = Y[:-n]

        # Split the data into 80% train data and 20 % test data
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)

        # Create Linear Regression Model
        lr = LinearRegression()
        # Train the model
        lr.fit(x_train, y_train)

        # We want the last 30 rows  
        forecast = np.array(df.drop(['Prediction'],1))[-n:]


        # Print the predictions for the next "n" days
        lr_prediction = lr.predict(forecast)

  
        predictions = pd.DataFrame(lr_prediction, columns = ['Prediction'])
        # "predictions" has 1 column with the predicted values

        df = df.reset_index()

        # From "Date" we need the to get the last value
        d = df['Date'].iloc[-1]
        d = d + relativedelta(days =+ 1)

        # Now we make a list with the respective daterange for our prediction, 15 days after that. 
        datelist = pd.date_range(d, periods = 15).tolist()

        # We add the variable to our Dataframe "predictions"
        predictions['Date'] = datelist
        
        # Save the date of today 3 months older
        trhee_months = date.today() - relativedelta(months=+3)
        trhee_months = trhee_months.strftime('%Y-%m-%d')

        # Get the data for plotting
        df = data.DataReader(symbol, 'yahoo', trhee_months, today)
        df = df.reset_index()

        # Plotting the chart
        fig = go.Figure()
        # Add the data from the first stock
        fig.add_trace(go.Scatter(
                        x=df.Date,
                        y=df['Adj Close'],
                        name=f'{symbol} stock',
                        line_color='dodgerblue',
                        opacity=0.9))
        
        # Add the data from the predictions
        fig.add_trace(go.Scatter(
                        x=predictions.Date,
                        y=predictions['Prediction'],
                        name=f'ML Prediction',
                        line=dict(color='green', dash = 'dot'),
                        opacity=0.9))
    
        fig.update_layout(title=f'Historical {symbol} Quote Stock Value - With 15 Days Prediction',
                                    yaxis_title='Closing Day Price Value in USD',
                                    template='plotly_dark',
                                    xaxis_tickfont_size=14,
                                    yaxis_tickfont_size=14)
        
        fig.show()


   
    
    
    # OPTION 2: Machine Learning 30 days Prediction from Your Stock "{symbol}" Tricker.
    # Same model as above, but using 4 Months data for 30 precition price. 

    elif choice == '2' or choice == 'B' or choice == 'b':
        
        # Get the date of today
        today = date.today()
        # Change the format
        today = today.strftime('%Y-%m-%d')

        df = data.DataReader(symbol, 'yahoo', '2000-01-01', 'today')

        df = df[['Adj Close']]

        # N as Variable for 30 days
        n = 30

        # Create another column "Prediction" shifted "n" units up
        df['Prediction'] = df[['Adj Close']].shift(-n)
        
        X = df.drop(['Prediction'],1)
        X = np.array(X)
        X = X[:-n]


        Y = df['Prediction']
        Y = np.array(Y)
        Y = Y[:-n]

        # Split the data into 80% train data and 20 % test data
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)


        lr = LinearRegression()

        lr.fit(x_train, y_train)
 
        forecast = np.array(df.drop(['Prediction'],1))[-n:]

        lr_prediction = lr.predict(forecast)


        predictions = pd.DataFrame(lr_prediction, columns = ['Prediction'])

        df = df.reset_index()

        d = df['Date'].iloc[-1]
        d = d + relativedelta(days =+ 1)


        datelist = pd.date_range(d, periods = 30).tolist()

        predictions['Date'] = datelist

        

        four_months = date.today() - relativedelta(months=+4)
        four_months = four_months.strftime('%Y-%m-%d')


        df = data.DataReader(symbol, 'yahoo', four_months, today)
        df = df.reset_index()


        fig = go.Figure()

        fig.add_trace(go.Scatter(
                        x=df.Date,
                        y=df['Adj Close'],
                        name=f'{symbol} stock',
                        line_color='dodgerblue',
                        opacity=0.9))
        

        fig.add_trace(go.Scatter(
                        x=predictions.Date,
                        y=predictions['Prediction'],
                        name=f'ML Prediction',
                        line=dict(color='green', dash = 'dot'),
                        opacity=0.9))
    
        fig.update_layout(title=f'Historical {symbol} Quote Stock Value - With 30 Days Prediction',
                                    yaxis_title='Closing Day Price Value in USD',
                                    template='plotly_dark',
                                    xaxis_tickfont_size=14,
                                    yaxis_tickfont_size=14)
        
        fig.show()





    # OPTION 3: Price Date Range Chart from Date Selected. 

    elif choice == '3' or choice == 'C' or choice == 'c':
    
        start_date = input('\nSubmit you Starting Date Analysis (With YYYY-MM-DD Format): ')
        end_date = input('Submit you Ending Date Analysis (With YYYY-MM-DD Format): ')
    
        df = data.DataReader(symbol, 'yahoo', start_date, end_date)
    
        df = df.reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.Date,
                                 y=df['Adj Close'],
                                 line_color='dodgerblue'))
        
        fig.update_layout(title=f'{symbol} Stock Price from {start_date} to {end_date}',
                                    yaxis_title='Closing Day Price Value in USD',
                                    template='plotly_dark',
                                    xaxis_tickfont_size=14,
                                    yaxis_tickfont_size=14)

        fig.show()
     
    
    



    # OPTION 4: Price Comparison from your Stock Tricker.
    elif choice == '4' or choice == 'D' or choice == 'd':
        start_date = input('\nSubmit you Starting Date Analysis (With YYYY-MM-DD Format): ')
        end_date = input('Submit you Ending Date Analysis (With YYYY-MM-DD Format): ')
    
        df = data.DataReader(symbol, 'yahoo', start_date, end_date)
        df = df.reset_index()
        
        while True:
            try:
                symbol_2 = input(f'\nWith which stock would you like to compare {symbol} stock? \nPlease enter a valid Stock Symbol: ')
                df_2 = data.DataReader(symbol_2, 'yahoo', start_date, end_date)
                df_2 = df_2.reset_index()
                break
            except(KeyError, OSError):
                print(color.BOLD + color.UNDERLINE + f'> {symbol_2} is not a valid stock symbol. Please try again...' + color.END)

                
        fig = go.Figure()

        fig.add_trace(go.Scatter(
                    x=df.Date,
                    y=df['Adj Close'],
                    name=f'{symbol} Stock',
                    line_color='dodgerblue',
                    opacity=0.9))
        
        fig.add_trace(go.Scatter(
                    x=df_2.Date,
                    y=df_2['Adj Close'],
                    name=f'{symbol_2} Stock',
                    line_color='dimgray',
                    opacity=0.9))
    
    
        fig.update_layout(title=f'Price Comparison of {symbol} Stock and {symbol_2} Stock from {start_date} to {end_date}', 
                                    yaxis_title='Closing Day Price Value in USD',
                                    template='plotly_dark',
                                    xaxis_tickfont_size=14,
                                    yaxis_tickfont_size=14)
        
        fig.show()
    

        
   
    
    
    # Option 5: Your Stock Tricker 180 Past-Days Analysis.
    elif choice == '5' or choice == 'E' or choice == 'e':

        try:
            # Save the date of today in the variable "today"
            today = date.today()
            # We convert the type of the variable in the format %Y-%m-%d
            today = today.strftime('%Y-%m-%d')
            # Save the date of today 6 months ago, by subtracting 6 months from the date of today
            six_months = date.today() - relativedelta(months=+6)
            six_months = six_months.strftime('%Y-%m-%d')
        
            df2 = yf.Ticker(symbol)
            # Save the Analyst Recommendations in "rec"
            rec = df2.recommendations
            # The DataFrame "rec" has 4 columns: "Firm", "To Grade", "From Grade" and "Action"
            # The index is the date ("DatetimeIndex")
    
            # Now we select only those columns which have the index(date) from "six months" to "today"
            rec = rec.loc[six_months:today,]
        
            # Unfortunately in some cases no data is available, so that the DataFrame is empty. Then the user gets the following message
            if rec.empty:
                print(color.BOLD + color.UNDERLINE + "\n> Unfortunately, there are no recommendations by analysts provided for your chosen stock!" + color.END)
                    
                    
            else:    
                # Replace the index with simple sequential numbers and save the old index ("DatetimeIndex") as a variable "Date"
                rec = rec.reset_index()
    
                # For our analysis we don't need the variables/columns "Firm", "From Grade" and "Action", therefore we delete them
                rec.drop(['Firm', 'From Grade', 'Action'], axis=1, inplace=True)

                # We change the name of the variables/columns
                rec.columns = (['date', 'grade'])
        
                # Now we add a new variable/column "value", which we give the value 1 for each row in order to sum up the values based on the contents of "grade"
                rec['value'] = 1

                # Now we group by the content of "grade" and sum their respective values 
                rec = rec.groupby(['grade']).sum()
                # The DataFrame "rec" has now 1 variable/column which is the value, the index are the different names from the variable "grade"
                # However for the plotting we need the index as a variable 
                rec = rec.reset_index()
        
                # For the labels we assign the content/names of the variable "grade" and for the values we assign the content of "values" 
                fig = go.Figure(data=[go.Surface(labels=rec.grade,
                                                values=rec.value,
                                                hole=.3)])
                # Give a title
                fig.update_layout(template='plotly_dark', title_text=f'Analyst Recommendations of {symbol} Stock from {six_months} to {today}')

                # Plotting the chart
                fig.show()  
            

    
        # For some stocks the imported data is distorted and in a wrong format, so that an error appears
        # In this cases the user gets the following message:
        except(ValueError,AttributeError):
            print(color.BOLD + color.UNDERLINE + '\n> Unfortunately, there are no recommendations provided for your chosen stock!' + color.END) 

 

    
    # OPTION 6: Quit the program
    elif choice == '6' or choice == 'Q' or choice == 'q':
        print(color.BLUE + color.BOLD + '\n> If you like our results, please share our solution with others! Thank you!' + color.END)
        choice = None
        

    # If user inputs a non valid option
    else:
        print(color.BOLD + color.UNDERLINE + '\n> Your Selection is INVALID! Please select a correct Option from our list.' + color.END)

"""By Emmanuel Martinez, Charllie Burd, and George Quintanilla. """

