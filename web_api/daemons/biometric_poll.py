from statsmodels.tsa.ar_model import AutoReg
import requests

POLL_URL = "https://127.0.0.1:8000/data/read/{}/{}"


def poll_predict(user_id, since):
    r = requests.get(POLL_URL.format(user_id, since), verify=False)
    data = r.json()
    vals = data.get("points", [])
    vals = [v["heart_rate"] for v in vals]
    predictions = []
    if vals:
        num_steps = max(1, len(vals) - 10)
    else:
        num_steps = 0
    for i in range(num_steps):
        wanted = vals[i:i+10]
        model = AutoReg(wanted, lags=1)
        model_fit = model.fit()
        yhat = model_fit.predict(len(wanted), len(wanted))
        predictions.extend(list(yhat))

    return predictions[-10:]