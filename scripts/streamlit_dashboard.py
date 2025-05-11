# scripts/streamlit_dashboard.py

from dotenv import load_dotenv
import os
from stock_predictor.data_loader import fetch_alpha_vantage
from stock_predictor.training_pipeline import (
    split_data,
    scale_data,
    prepare_sequences,
    create_sequences,
)
from stock_predictor.model_building import build_and_train_model, predict_and_inverse

import streamlit as st


st.title("📈 Aktien-Vorhersage (Demo)")


import os
from dotenv import load_dotenv
import streamlit as st


################
###  API Key ###
################

# 🔁 .env laden
load_dotenv()

# 🔎 Finde alle gespeicherten Keys
env_keys = [v for k, v in os.environ.items() if k.startswith("ALPHAVANTAGE_API_KEY_")]

api_key = None

if env_keys:
    selected = st.selectbox(
        "🔑 Wähle einen gespeicherten API Key", env_keys + ["❌ Eigene Eingabe"]
    )
    if selected != "❌ Eigene Eingabe":
        api_key = selected
    else:
        api_key = st.text_input("🔐 Eigener API Key", type="password")
else:
    st.warning("⚠️ Keine API Keys in .env gefunden.")
    api_key = st.text_input("🔐 API Key manuell eingeben", type="password")

#######################
###  Ausahl Symbol  ###
#######################

symbol = st.selectbox("Symbol auswählen", ["IBM", "AAPL", "MSFT"])


#####################
###  Daten Laden  ###
#####################

if st.button("📥 Daten laden"):
    try:
        df = fetch_alpha_vantage(symbol, api_key)
        st.session_state["df"] = df
        st.success(f"Daten für {symbol} geladen!")

        # ✅ Vorschau anzeigen
        st.markdown("### 📊 Vorschau der letzten 10 Einträge")
        st.dataframe(
            df.tail(10).style.format(
                {
                    "open": "{:.2f}",
                    "high": "{:.2f}",
                    "low": "{:.2f}",
                    "close": "{:.2f}",
                    "volume": "{:,.0f}",
                }
            )
        )

        # Zusatzinfo: Zeitbereich
        st.markdown(
            f"**🕒 Zeitraum:** {df.index.min().date()} → {df.index.max().date()}"
        )
        st.markdown(f"**📈 Anzahl Einträge:** {len(df)}")

    except Exception as e:
        st.error(f"❌ Fehler beim Laden: {str(e)}")


###########################
###  Split Data Button  ###
###########################


from stock_predictor.training_pipeline import split_data, scale_data


###########################
###  Split Data Button  ###
###########################

if "df" in st.session_state:
    if st.button("📂 Daten aufteilen (Train/Test)"):
        train_df, test_df = split_data(st.session_state["df"], train_ratio=0.8)
        st.session_state["train_df"] = train_df
        st.session_state["test_df"] = test_df
        st.success(
            f"✅ Daten wurden aufgeteilt: {len(train_df)} Training | {len(test_df)} Test"
        )

############################
###  Scalte Data Button  ###
############################

if "train_df" in st.session_state and "test_df" in st.session_state:
    if st.button("📊 Daten skalieren"):
        train_scaled, test_scaled, scaler = scale_data(
            st.session_state["train_df"], st.session_state["test_df"]
        )
        st.session_state["train_scaled"] = train_scaled
        st.session_state["test_scaled"] = test_scaled
        st.session_state["scaler"] = scaler
        st.success("✅ Daten wurden erfolgreich skaliert")
        import matplotlib.pyplot as plt

        # Beispiel: "close"-Spalte ist Spalte 3
        feature_index = 3

        # Werte extrahieren
        original = st.session_state["train_df"].iloc[:, feature_index].values
        scaled = st.session_state["train_scaled"][:, feature_index]

        fig, ax1 = plt.subplots(figsize=(10, 4))

        # Linke Y-Achse: Originalwerte
        ax1.plot(original, label="Original (USD)", color="blue")
        ax1.set_ylabel("Originalpreis (USD)", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        # Rechte Y-Achse: Skalierte Werte
        ax2 = ax1.twinx()
        ax2.plot(scaled, label="Skaliert (0–1)", color="orange")
        ax2.set_ylabel("Skalierte Werte", color="orange")
        ax2.tick_params(axis="y", labelcolor="orange")

        # Titel und Beschriftung
        ax1.set_title("Vergleich: Originalwerte vs. Skalierte Werte ('Close')")
        ax1.set_xlabel("Tage")

        # Legende
        fig.legend(loc="upper right", bbox_to_anchor=(0.9, 0.85))
        ax1.grid(True)

        st.pyplot(fig)


from stock_predictor.training_pipeline import prepare_sequences

# 🔘 Sequenzen erstellen Button
if "train_scaled" in st.session_state and "test_scaled" in st.session_state:
    if st.button("📐 Sequenzen erstellen (für LSTM)"):
        X_train, y_train, X_test, y_test = prepare_sequences(
            st.session_state["train_scaled"],
            st.session_state["test_scaled"],
            target_col_index=3,  # close price
            n_steps=60,
        )
        st.session_state["X_train"] = X_train
        st.session_state["y_train"] = y_train
        st.session_state["X_test"] = X_test
        st.session_state["y_test"] = y_test

        st.success(
            f"✅ Sequenzen erstellt! Trainingsdaten: {X_train.shape}, Testdaten: {X_test.shape}"
        )

        # 👉 Vorschau einer Sequenz darstellen
        st.markdown("### 🔍 Beispiel einer Trainingssequenz:")
        st.line_chart(X_train[0])  # Erstes Beispiel visualisieren


import streamlit as st
import io
import sys
from contextlib import redirect_stdout
from stock_predictor.model_building import build_and_train_model

if "X_train" in st.session_state and "y_train" in st.session_state:
    if st.button("🚀 Live Training starten"):
        st.markdown("### 📺 Live Trainingsausgabe")
        output_area = st.empty()  # Für live Updates

        buffer = io.StringIO()

        with redirect_stdout(buffer):
            model = build_and_train_model(
                st.session_state["X_train"], st.session_state["y_train"], epochs=10
            )

        # Nach Training: alles auf einmal anzeigen
        output_text = buffer.getvalue()
        output_area.code(output_text, language="bash")  # Zeigt wie Konsole

        st.session_state["model"] = model
        st.success("✅ Training abgeschlossen.")


###########################
###  Save Model Button  ###
###########################

from stock_predictor.model_building import save_model

if "model" in st.session_state:
    st.markdown("### 💾 Modell speichern")
    if st.button("💾 Modell speichern"):
        filepath = save_model(st.session_state["model"], symbol, "../models")
        st.success(f"✅ Modell gespeichert unter: `{filepath}`")

###########################
###   Model Plotting  ###
###########################

import pandas as pd

if st.button("🔍 Vorhersage (Streamlit GUI)"):
    pred_rescaled, true_rescaled = predict_and_inverse(
        model=st.session_state["model"],
        X_test=st.session_state["X_test"],
        y_test=st.session_state["y_test"],
        scaler=st.session_state["scaler"],
        n_features=st.session_state["train_scaled"].shape[1],
        target_col_index=3,
    )

    # Zeitachse
    dates = st.session_state["test_df"].index[-len(pred_rescaled) :]

    # Combine into DataFrame
    df_plot = pd.DataFrame(
        {"Tatsächlich (close)": true_rescaled, "Vorhersage": pred_rescaled}, index=dates
    )

    st.markdown("### 📈 Interaktiver Vergleich (Streamlit GUI)")
    st.line_chart(df_plot)
    st.success("✅ Streamlit GUI-Vorhersage erfolgreich dargestellt.")
