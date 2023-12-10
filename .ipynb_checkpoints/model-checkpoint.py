import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class FieldName:
    WeatherId = 'Ідентифікатор погоди'
    CityId = 'Ідентифікатор міста'
    City =  'Місто'
    Date =  'Дата'
    Pressure =  'Тиск'
    Temperature =  'Температура'
    Humidity =  'Вологість'
    Range =  'Розмах'
    Minimum =  'Мін.'
    Maximum =  'Макс.'
    Mean =  "Середнє"
    Median =  "Медіана"
    Variance =  "Дисперсія"
    CoefficientOfVariation = 'Коеф. варіації'
    Longitude =  'Довгота'
    Latitude =  'Широта'

class LabModel:

    def __init__(self, cities_df, weather_df):
        self.cities_df = cities_df
        self.weather_df = weather_df

    # ------------------------------------------------------ #
    # ОСНОВНІ ФРЕЙМИ
    # ------------------------------------------------------ #

    def get_cities_df(self):
        """Повертає DataFrame з інформацією про міста."""
        return self.cities_df

    def get_weather_df(self):
        """Повертає DataFrame з прогнозом погоди."""
        return self.weather_df

    def get_forecast_df(self):
        """Об'єднує фрейми міст і погоди за спільним ідентифікатором міста."""
        return pd.merge(self.cities_df, self.weather_df, left_on=FieldName.CityId, right_on=FieldName.CityId, how='inner')

    # ------------------------------------------------------ #
    # ТЕМПЕРАТУРА
    # ------------------------------------------------------ #

    def get_temperature_df(self):
        """Повертає DataFrame з температурою за датами для різних міст."""
        temperature_df = self.get_forecast_df().drop(columns=[
            FieldName.Longitude, 
            FieldName.Latitude
        ])
        temperature_df = temperature_df.pivot_table(
                index=[FieldName.CityId, FieldName.City], 
                columns=FieldName.Date, 
                values=FieldName.Temperature
        )
        temperature_df = temperature_df.reset_index()
        return temperature_df

    def get_temperature_agg_df(self, axis="index"):
        """Повертає агрегований DataFrame з інформацією про температуру."""
        temperature = 0
        match(axis):
            case "index":
                temperature = self.get_forecast_df().groupby(FieldName.Date)[FieldName.Temperature]
            case "columns":
                temperature = self.get_forecast_df().groupby(FieldName.City)[FieldName.Temperature]

        return pd.DataFrame({
            FieldName.Minimum: temperature.min(),
            FieldName.Maximum: temperature.max(),
            FieldName.Range: temperature.max() - temperature.min(),
            FieldName.Mean: temperature.mean(),
            FieldName.Range: temperature.median(),
            FieldName.Variance: temperature.var(),
            FieldName.CoefficientOfVariation: (temperature.std() - temperature.mean()) * 100
        }).round()

    def print_temperatures_plot(self):
        """Виводить лінійний графік температур для різних міст."""
        df = self.get_forecast_df()
        fig = px.line(df, x=FieldName.Date, y=FieldName.Temperature, color=FieldName.City)
        fig.show()

    # ------------------------------------------------------ #
    # ВОЛОГІСТЬ
    # ------------------------------------------------------ #

    def get_humidity_df(self):
        """Повертає DataFrame з вологістю за датами для різних міст."""
        humidity_df = self.get_forecast_df().drop(columns=[FieldName.Longitude, FieldName.Latitude])
        humidity_df = humidity_df.pivot_table(index=[FieldName.CityId, FieldName.City], columns=FieldName.Date, values=FieldName.Humidity)
        return humidity_df.reset_index()

    def get_humidity_agg_df(self, axis="index"):
        """Повертає агрегований DataFrame з інформацією про вологість."""
        humidity = self.get_forecast_df().groupby(FieldName.Date)[FieldName.Humidity]
        match(axis):
            case "index":
                humidity = self.get_forecast_df().groupby(FieldName.Date)[FieldName.Humidity]
            case "columns":
                humidity = self.get_forecast_df().groupby(FieldName.City)[FieldName.Humidity]

        return pd.DataFrame({
            FieldName.Minimum: humidity.min(),
            FieldName.Maximum: humidity.max(),
            FieldName.Range: humidity.max() - humidity.min(),
            FieldName.Mean: humidity.mean(),
            FieldName.Variance: humidity.var(),
            FieldName.CoefficientOfVariation: (humidity.std() / humidity.mean()) * 100
        }).round(2)

    def print_humidity_plot(self):
        """Виводить лінійний графік вологості для різних міст."""
        df = self.get_forecast_df()
        fig = px.line(
                df, 
                x=FieldName.Date, 
                y=FieldName.Humidity, 
                color=FieldName.City
        )
        fig.show()

    # ------------------------------------------------------ #
    # ТИСК
    # ------------------------------------------------------ #

    def get_pressure_df(self):
        """Повертає DataFrame з тиском за датами для різних міст."""

        pressure_df = self.get_forecast_df().drop(columns=[
            FieldName.Longitude,
            FieldName.Latitude
        ])

        pressure_df = pressure_df.pivot_table(
                index=[FieldName.CityId, FieldName.City], 
                columns=FieldName.Date, 
                values=FieldName.Pressure
        )

        return pressure_df.reset_index()

    def get_pressure_agg_df(self, axis="index"):
        """Повертає агрегований DataFrame з інформацією про тиск."""
        pressure = self.get_forecast_df().groupby(FieldName.Date)[FieldName.Pressure]
        match(axis):
            case "index":
                pressure = self.get_forecast_df().groupby(FieldName.Date)[FieldName.Pressure]
            case "columns":
                pressure = self.get_forecast_df().groupby(FieldName.City)[FieldName.Pressure]

        return pd.DataFrame({
            FieldName.Minimum: pressure.min(),
            FieldName.Maximum: pressure.max(),
            FieldName.Range: pressure.max() - pressure.min(),
            FieldName.Mean: pressure.mean(),
            FieldName.Variance: pressure.var(),
            FieldName.CoefficientOfVariation: (pressure.std() / pressure.mean()) * 100
        }).round(2)

    def print_pressure_plot(self):
        """Виводить лінійний графік тиску для різних міст."""
        df = self.get_forecast_df()
        fig = px.line(
                df, 
                x=FieldName.Date, 
                y=FieldName.Pressure, 
                color=FieldName.City
        )
        fig.show()

    def get_correlation_matrix(self):
        """Повертає матрицю кореляції між температурою, тиском і вологістю для різних міст."""
        forecast_df = self.get_forecast_df()
        columns = [FieldName.Temperature, FieldName.Pressure, FieldName.Humidity]
        return forecast_df.groupby(FieldName.City)[columns].corr()

    def print_scatterplot_for_correlation_matrix(self):
        """Виводить діаграму розсіювання для матриці кореляції між температурою, тиском і вологістю."""
        forecast_df = self.get_forecast_df()
        columns = [FieldName.Temperature, FieldName.Pressure, FieldName.Humidity]
        df = forecast_df.groupby(FieldName.City)[columns].corr()
        fig = px.scatter_matrix(df)
        fig.show()

def load_model():
    """Завантажує дані про міста та погоду і повертає об'єкт LabModel."""
    cities_df = pd.read_csv("./resources/cities.csv", index_col=0)
    weather_df = pd.read_csv("./resources/weather.csv", index_col=0)
    return LabModel(cities_df, weather_df)
