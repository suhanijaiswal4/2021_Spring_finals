import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.plotting.backend = "plotly"


def clean_global_data(filename: str) -> pd.DataFrame:
    """

    :param filename:
    :return:
    """
    global_child_mortality_data = pd.read_csv(filename)
    global_child_mortality_data.drop_duplicates(inplace=True)
    global_child_mortality_data = global_child_mortality_data.rename(columns={
        "Share surviving first 5 years of life (based on Gapminder and World Bank (2019))": "Percentage_surviving_in_first_5_years",
        "Share dying in first 5 years (based on Gapminder and World Bank (2019))": "Percentage_dying_in_first_5_years"})
    global_child_mortality_data = global_child_mortality_data[global_child_mortality_data['Year'] >= 1960]
    return global_child_mortality_data


def plot_year_mortality(dataframe: str):
    """

    :param dataframe:
    :return:
    """
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.bar(dataframe['Year'], dataframe['Percentage_surviving_in_first_5_years'],
           label='Percentage surviving in first 5 years')
    ax.bar(dataframe['Year'], dataframe['Percentage_dying_in_first_5_years'],
           bottom=dataframe['Percentage_surviving_in_first_5_years'], label='Percentage dying in first 5 years')
    ax.set_title('Child Mortality Analysis')
    ax.legend()


def clean_country(filename: str) -> pd.DataFrame:
    """

    :param filename:
    :return:
    """
    country_data = pd.read_csv(filename)
    country_data = country_data[['Country', 'Infant mortality (per 1000 births)', 'GDP ($ per capita)']]
    country_data['Infant mortality (per 1000 births)'] = country_data['Infant mortality (per 1000 births)'].str.replace(
        ',', '.')
    country_data = country_data.astype({'Infant mortality (per 1000 births)': np.float})
    country_data = country_data.dropna(subset=["Infant mortality (per 1000 births)", "GDP ($ per capita)"])
    country_data = country_data.sort_values(by="Infant mortality (per 1000 births)", ascending=False)
    return country_data


def health_clean(filename: str) -> pd.DataFrame:
    """

    :param filename:
    :return:
    """
    Health_expenditure = pd.read_csv(filename, skiprows=4)
    Health_expenditure = Health_expenditure.drop(
        ['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973',
         '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987',
         '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2019', '2020',
         'Indicator Name', 'Indicator Code'], axis=1)
    Health_expenditure = Health_expenditure.melt(id_vars=['Country Name', 'Country Code'], var_name='Year',
                                                 value_name='Health Expenditure').dropna()
    Health_expenditure['Year'] = Health_expenditure['Year'].astype('int')
    return Health_expenditure


def country_plot(expenditure_mortality: pd.DataFrame, code_name: str):
    """

    :param expenditure_mortality:
    :param code_name:
    :return:
    """
    selected = expenditure_mortality[expenditure_mortality['Country Code'] == code_name]
    fig = selected.plot.scatter(x='Health Expenditure', y='Mortality rate, under-5 (per 1,000 live births)',
                                title=code_name)
    fig.show()