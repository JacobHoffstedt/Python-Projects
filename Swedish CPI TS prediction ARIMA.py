import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import itertools

print("Script is running...")

df = pd.read_excel(r"C:\Users\Jacob\Downloads\Inflation data.xlsx")

print(df.head)



df['Period'] = df['Period'].str.replace('M', '')  # Remove 'M'
df['Period'] = pd.to_datetime(df['Period'], format='%Y%m')  # Convert to datetime

# Set "Period" as index, inplace means that the changes are made to the existing dataset.
df.set_index('Period', inplace=True)
#Checking changes
print(df.head())

df = df.loc['2010-01-01':'2019-12-01']


df.rename(columns={df.columns[0]: "Inflation"}, inplace=True)

plt.figure(figsize=(12, 6)) #Making the figure 12 by 6 inches. 
plt.plot(df, label="Inflation Rate", color = "orange") #Plots the TS
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
adf_test(df['Inflation'])

#Since the data is not stationary the solution is differencing meaning that Y_t* = Y_t - Y_{t-1} i.e. the differenced series is created by 
#taking the difference of each output which removes the trend. 

df_diff = df.diff().dropna()

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
plot_acf(df_diff, ax=ax[0], title="Autocorrelation (ACF)")
plot_pacf(df_diff, ax=ax[1], title="Partial Autocorrelation (PACF)")
plt.show()

#It seems the plots do not give any definitive information on which model to use.
#A loop will find the best solution using 



p = range(0, 3)  # AR terms
d = [0]  # Data already differenced
q = range(0, 3)  # MA terms

pdq_combinations = list(itertools.product(range(0,3), [0], range(0,3))) #Generates different combiations of ARIMA models

best_aic = float("inf") #Creates an INF AIC score that the first model.fit will always be lower, allows for the if statement to start. 
best_pdq = None #The best pdq combiation
best_model = None #The best AIC score of the best pdq

for pdq in pdq_combinations:
    try:
        model = ARIMA(df_diff, order=pdq)  # Use differenced data
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
plt.figure(figsize=(10, 5))
plt.plot(residuals, label="Residuals", color="orange")
plt.axhline(y=0, color='r', linestyle='--')
plt.title(f"Residuals of ARIMA{best_pdq}")
plt.legend()
plt.show()