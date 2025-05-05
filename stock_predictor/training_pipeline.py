import numpy as np
from sklearn.preprocessing import MinMaxScaler


def split_data(df, split_date=None, train_ratio=0.8):
    """
    Teilt die Daten dynamisch in Trainings- und Testdatensätze.

    Parameter:
        df (pd.DataFrame): Originaler DataFrame mit Zeitindex.
        split_date (str, optional): Explizites Datum, um die Daten zu trennen. z.B. '2023-12-31'.
        train_ratio (float, optional): Prozentualer Anteil der Trainingsdaten, falls kein split_date angegeben.

    Rückgabe:
        train_scaled, test_scaled, scaler, train_df, test_df
    """

    if split_date:
        train_df = df.loc[:split_date]
        test_df = df.loc[split_date:]
    else:
        split_point = int(len(df) * train_ratio)
        train_df = df.iloc[:split_point]
        test_df = df.iloc[split_point:]

    return train_df, test_df


def create_sequences(data, n_steps=60, target_col_index=3):
    """
    data: NumPy Array der Form (N, n_features).
    n_steps: Sequenzlänge (z. B. 60 Tage).
    target_col_index: Index der Zielspalte (z. B. 3 für 'close').

    return: X, y
       X -> shape (N-n_steps, n_steps, n_features)
       y -> shape (N-n_steps,)
    """
    X, y = [], []
    for i in range(len(data) - n_steps):
        seq_x = data[i : i + n_steps]
        seq_y = data[i + n_steps, target_col_index]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


def scale_data(train_df, test_df):
    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_df)
    test_scaled = scaler.transform(test_df)

    return train_scaled, test_scaled, scaler


def prepare_sequences(train_scaled, test_scaled, target_col_index=3, n_steps=60):
    X_train, y_train = create_sequences(
        train_scaled, n_steps=n_steps, target_col_index=target_col_index
    )
    X_test, y_test = create_sequences(
        test_scaled, n_steps=n_steps, target_col_index=target_col_index
    )
    return X_train, y_train, X_test, y_test
