import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

companies = pd.read_csv("Unicorn_Companies.csv") # Load the dataset provided into a DataFrame.
companies.head(10) # Display the first 10 rows of the data.
companies.shape  # Identify the number of rows and columns in the dataset.
companies.drop_duplicates().shape # Check for duplicates.
companies.dtypes # Display the data types of the columns.
companies.sort_values(by="Year Founded", ascending=False).head(10)  # To arrange the data from latest to earliest `Year Founded`
companies["Year Founded"].value_counts().sort_values(ascending=False)  
# Display each unique year that occurs in the dataset
# along with the number of companies that were founded in each unique year.
sns.histplot(data=companies, x='Year Founded')
plt.title('Year Founded histogram');


# Convert `Date Joined` column to datetime.
# Update the column with the converted values.
companies["Date Joined"] = pd.to_datetime(companies["Date Joined"])


# Display the data types of the columns in `companies`
# to confirm that the update actually took place
companies.dtypes

# Obtain the names of the months when companies gained unicorn status.
# Use the result to create a `Month Joined` column.
companies["Month Joined"] = companies["Date Joined"].dt.month_name()


# Determine how many years it took for companies to reach unicorn status.
# Use the result to create a `Years To Join` column.
companies["Years To Join"] = companies["Date Joined"].dt.year - companies["Year Founded"]


# Filter dataset by a year of your interest (in terms of when companies reached unicorn status).
# Save the resulting subset in a new variable 
companies_2021 = companies[companies["Date Joined"].dt.year == 2021]

companies_2021.insert(3, "Week Joined", companies_2021["Date Joined"].dt.strftime('%Y-W%V'), True)
companies_by_week_2021 = companies_2021.groupby(by="Week Joined")["Company"].count().reset_index().rename(columns={"Company":"Company Count"})
companies_by_week_2021.head()

companies_2020 = companies[companies["Date Joined"].dt.year == 2020]
companies_2020_2021 = pd.concat([companies_2020, companies_2021.drop(columns="Week Joined")])
companies_2020_2021["Quarter Joined"] = companies_2020_2021["Date Joined"].dt.to_period('Q').dt.strftime('%Y-Q%q')
companies_2020_2021["Valuation"] =  companies_2020_2021["Valuation"].str.strip("$B").astype(float)
companies_by_quarter_2020_2021 = companies_2020_2021.groupby(by="Quarter Joined")["Valuation"].mean().reset_index().rename(columns={"Valuation":"Average Valuation"})
companies_by_quarter_2020_2021.head()


month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", 
               "December"]

sns.boxplot(x=companies['Month Joined'], 
            y=companies['Years To Join'], 
            order=month_order, 
            showfliers=False)
plt.title('Distribution of years to become unicorn with respect to month joined')
plt.xticks(rotation=45, horizontalalignment='right')
plt.show()


plt.figure(figsize=(10,6))
sns.barplot(x=companies["Year Founded"], y=companies["Years To Join"], ci=False)
plt.title("Bar plot of years to join with respect to year founded")
plt.xlabel("Year founded")
plt.ylabel("Years to join unicorn status")
plt.xticks(rotation=45, horizontalalignment='right')
plt.show()