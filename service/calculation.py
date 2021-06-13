import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Dropout
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
import datetime

from helper.helpers import generate_filename


def calculate(
        data_file,
        batch_size=10,
        epochs=10,
        end_date=datetime.datetime.now().strftime("%Y-%m-%d")
):
    df = pd.read_csv('./data/' + data_file)

    # Separate dates for future plotting
    train_dates = pd.to_datetime(df['Date'])

    # Variables for training
    cols = list(df)[1:6]

    df_for_training = df[cols].astype(float)
    print(df_for_training)
    # df_for_plot=df_for_training.tail(5000)
    # df_for_plot.plot.line()

    # LSTM uses sigmoid and tanh that are sensitive to magnitude so values need to be normalized
    # normalize the dataset
    scaler = StandardScaler()
    scaler = scaler.fit(df_for_training)
    df_for_training_scaled = scaler.transform(df_for_training)

    print(df_for_training_scaled)
    # As required for LSTM networks, we require to reshape an input data into n_samples x timesteps x n_features.
    # In this example, the n_features is 2. We will make timesteps = 3.
    # With this, the resultant n_samples is 5 (as the input data has 9 rows).
    trainX = []
    trainY = []

    n_future = 5  # Number of days we want to predict into the future
    n_past = 10  # Number of past days we want to use to predict the future

    for i in range(n_past, len(df_for_training_scaled) - n_future + 1):
        trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])
        trainY.append(df_for_training_scaled[i + n_future - 1:i + n_future, 0])

    trainX, trainY = np.array(trainX), np.array(trainY)

    print('trainX shape == {}.'.format(trainX.shape))
    print('trainY shape == {}.'.format(trainY.shape))

    # define Autoencoder model

    model = Sequential()
    model.add(LSTM(64, activation='tanh', input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
    model.add(LSTM(32, activation='tanh', return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(trainY.shape[1]))

    model.compile(optimizer='adam', loss='mse')
    model.summary()

    # fit model
    model.fit(trainX, trainY, epochs=(epochs or 10), batch_size=(batch_size or 10), validation_split=0.1, verbose=1)

    # plt.plot(history.history['loss'], label='Training loss')
    # plt.plot(history.history['val_loss'], label='Validation loss')
    # plt.legend()
    # plt.show()

    # Forecasting...
    # Start with the last day in training date and predict future...
    n_future = 10  # Redefining n_future to extend prediction dates beyond original n_future dates...
    forecast_period_dates = pd.date_range(list(train_dates)[-1], periods=n_future, freq='1d').tolist()

    forecast = model.predict(trainX[-n_future:])  # forecast

    # Perform inverse transformation to rescale back to original range
    # Since we used 5 variables for transform, the inverse expects same dimensions
    # Therefore, let us copy our values 5 times and discard them after inverse transform
    forecast_copies = np.repeat(forecast, df_for_training.shape[1], axis=-1)
    y_pred_future = scaler.inverse_transform(forecast_copies)[:, 0]

    # Convert timestamp to date
    forecast_dates = []
    for time_i in forecast_period_dates:
        forecast_dates.append(time_i.date())

    df_forecast = pd.DataFrame({'Date': np.array(forecast_dates), 'Open': y_pred_future})
    df_forecast['Date'] = pd.to_datetime(df_forecast['Date'])

    original = df[['Date', 'Open']]
    original['Date'] = pd.to_datetime(original['Date'])
    print(len(original['Date']))
    # TODO change to endDate
    original = original.loc[original['Date'] >= end_date]
    # original.index = range(len(original.index))
    print(original[['Date', 'Open']])
    print(df_forecast[['Date', 'Open']])
    plt.plot(original['Date'], original['Open'], 'b')
    plt.plot(df_forecast['Date'], df_forecast['Open'], 'g')
    generated_file_name = generate_filename('png')
    plt.savefig('./figures/' + generated_file_name)
    return generated_file_name


