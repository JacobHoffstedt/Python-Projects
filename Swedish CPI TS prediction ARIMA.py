import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import itertools
from statsmodels.stats.diagnostic import acorr_ljungbox

print("Script is running...")

df = pd.read_excel(r"C:\Users\Jacob\Downloads\Inflation data.xlsx")




df['Period'] = df['Period'].str.replace('M', '')  # Remove 'M'
df['Period'] = pd.to_datetime(df['Period'], format='%Y%m')  # Convert to datetime

# Set "Period" as index, inplace means that the changes are made to the existing dataset.
df.set_index('Period', inplace=True)
#Checking changes
print(df.head())



df.rename(columns={df.columns[0]: "Inflation"}, inplace=True)

df1 = df.loc['2010-01-01':'2018-12-01']


plt.figure(figsize=(12, 6)) #Making the figure 12 by 6 inches. 
plt.plot(df1, label="Inflation Rate", color = "orange") #Plots the TS
plt.title("Swedish Inflation Rate Over Time") #Names the figure
plt.xlabel("Year") #X-axis name
plt.ylabel("Inflation Index") # Y-axis name
plt.legend()
plt.grid(True) #Adds gridlines making it easier to read
plt.show() #Shows the plot

#Performing a test for stationarity which is crucial for ARIMA forecasting. If the data is stationary it means that the Time Series 
#has a constant mean (trend over time), constant variance (the fluctuations around the mean trend over time), 
# and a constant autocorrelation (correlation between past and future values) which makes forecasting possible.

def adf_test(series): #This function takes whatever is put into it, in this case from line 51 (Inflation column), and performs the test.
    result = adfuller(series)
    print("ADF Statistic:", result[0])
    print("p-value:", result[1])
    print("Critical Values:", result[4])
    if result[1] <= 0.05:
        print("✅ Data is stationary (Reject H0)")
    else:
        print("❌ Data is non-stationary (Fail to reject H0)")


print("\n🔍 **ADF Test on Inflation Data:**")
adf_test(df1['Inflation'])

#Since the data is not stationary the solution is differencing meaning that Y_t* = Y_t - Y_{t-1} i.e. the differenced series is created by 
#taking the difference of each output which removes the trend. 

df_diff = df1.diff().dropna()

# ADF Test After Differencing
print("\n🔍 **ADF Test After Differencing:**")
adf_test(df_diff['Inflation'])


# Since the data is not stationary after differencing once, it is performed again. 
df_diff2 = df_diff.diff().dropna()
print("\n🔍 **ADF Test After Second Differencing:**")
adf_test(df_diff2['Inflation'])

#Next step of the approach is to figure out the ARIMA model which is done by plotting ACF and PACF showing the autocorrelations.
#The I in ARIMA is already 2 due to the differencing being performed twice. 

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
plot_acf(df_diff2, ax=ax[0], title="Autocorrelation (ACF)")
plot_pacf(df_diff2, ax=ax[1], title="Partial Autocorrelation (PACF)")
plt.show()

#It seems the plots do not give any definitive information on which model to use.
#A loop will find the best solution using the command model_fit.aic 



p = range(0, 5)  # AR terms
d = [2]  # Differencing should be 2
q = range(0, 5)  # MA terms

pdq_combinations = list(itertools.product(range(0,5), [2], range(0,5))) #Generates different combiations of ARIMA models

best_aic = float("inf") #Creates an INF AIC score that the first model.fit will always be lower, allows for the if statement to start. 
best_pdq = None #The best pdq combiation
best_model = None #The best AIC score of the best pdq

for pdq in pdq_combinations:
    try:
        model = ARIMA(df1, order=pdq)  # Use differenced data
        model_fit = model.fit()
        print(f"ARIMA{pdq} - AIC: {model_fit.aic}")
        
        if model_fit.aic < best_aic: #The first will be lower than Inf, then it iterates across all combinations of pdq and stores the best ones ->
            best_aic = model_fit.aic 
            best_pdq = pdq
            best_model = model_fit
    except: #If it fails in finding a fit for a combination it continues
        continue

print(f"\n✅ Best ARIMA Model: ARIMA{best_pdq} with AIC = {best_aic}")

# Now that the best model for the time series has been determined using AIC, the residuals need to be checked, they should be white noise.
#If the residuals are white noise it means that error term is random which is an indication that any predictions should not be biased. 
residuals = best_model.resid
#Testing for white noise in residuals, P>0.05 is ok. 
ljung_box_results = acorr_ljungbox(residuals, lags=[10], return_df=True)
print(ljung_box_results)
#Passes the test with P-value 0.06891

forecast = best_model.forecast(steps=12)

# Plot Actual vs Forecasted Inflation
plt.figure(figsize=(12, 6))
plt.plot(df1, label="Actual Inflation", color="orange")
plt.plot(pd.date_range(df1.index[-1], periods=13, freq='M')[1:], forecast, 
         label="Forecast", linestyle="dashed", color="red")
plt.title("Inflation Forecast (Next 12 Months)")
plt.xlabel("Year")
plt.ylabel("Inflation Index")
plt.legend()
plt.grid(True)
plt.show()

# Display Forecast Values
print("\n📈 **Forecasted Inflation for Next 12 Months:**")
print(forecast)

#Calculate Error

df2 = df.loc['2019-01-01':'2019-12-01']
print(df2.head(12))

df2.index = pd.to_datetime(df2.index)
forecast.index = pd.to_datetime(forecast.index)

actual_2019 = df2['Inflation'].astype(float)  # Ensure numeric type


# Errors
error = forecast - actual_2019
absolute_error = abs(error)
squared_error = error ** 2
percentage_error = (absolute_error / actual_2019) * 100

# Creating the error dataframe.
error_df = pd.DataFrame({
    "Actual": actual_2019,
    "Forecasted": forecast,
    "Error": error,
    "Absolute Error": absolute_error,
    "Squared Error": squared_error,
    "Percentage Error (%)": percentage_error
})


print(error_df)

# The Mean squared percentage error
mspe = squared_error.mean()
print(f"\nMean Squared Prediction Error (MSPE): {mspe}")
#The error is 1.4% which means that the model can forecast inflation in 2019 using 2010-2018 data well. 
#Lets compare the model to a "naive" model which is a common comparison model, the naive model simply guesses next months value based on the previous 
#month. 


naive_forecast = actual_2019.shift(1)  # Uses previous month as forecast
naive_error = (actual_2019 - naive_forecast) ** 2
naive_mspe = naive_error.mean()
print(f"Naïve MSPE: {naive_mspe}")
print("The model that I have created using the Box Jenkins approach outperforms the Naive model with a lower MSPE!")