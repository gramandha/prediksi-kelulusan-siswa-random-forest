from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Memuat model
with open('model_kelulusan.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil_prediksi = None
    probabilitas = None

    if request.method == 'POST':
        try:
            # Mengambil input dari form
            nilai_tugas = float(request.form['nilai_tugas'])
            nilai_uts = float(request.form['nilai_uts'])
            nilai_uas = float(request.form['nilai_uas'])
            kehadiran = float(request.form['kehadiran'])
            jumlah_absen = float(request.form['jumlah_absen'])

            # Membuat DataFrame input
            data_input = pd.DataFrame([{
                'Nilai_Tugas': nilai_tugas,
                'Nilai_UTS': nilai_uts,
                'Nilai_UAS': nilai_uas,
                'Persentase_Kehadiran': kehadiran,
                'Jumlah_Absen': jumlah_absen
            }])

            # Melakukan prediksi
            pred = model.predict(data_input)[0]
            prob = model.predict_proba(data_input)[0]
            max_prob = float(np.max(prob)) * 100

            hasil_prediksi = pred
            probabilitas = f"{max_prob:.1f}%"

        except Exception as e:
            hasil_prediksi = f"Error: {str(e)}"

    return render_template('index.html', prediksi=hasil_prediksi, probabilitas=probabilitas)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
