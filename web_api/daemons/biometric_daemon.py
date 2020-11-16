from influxdb import DataFrameClient
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg

client = DataFrameClient(host="localhost", port=7086, database="user_metrics")


def poll_predict(user_id):
    res = client.query('select timestamp, heart_rate, movement from biometrics where user_id = "{}" and time > now - 30s;'.format(user_id))
    df = res["biometrics"]
    vals = list(df.heart_rate.values)

    predictions = []
    if len(df):
        num_steps = max(1, len(vals) - 10)
    else:
        num_steps = 0
    for i in range(num_steps):
        wanted = vals[i:i+10]
        model = AutoReg(wanted, lags=1)
        model_fit = model.fit()
        yhat = model_fit.predict(len(wanted), len(wanted))
        predictions.extend(list(yhat))

    return predictions