from flask import Flask, render_template, request, jsonify
import os
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_playlist():
    data = request.get_json()
    url = data.get('url')
    destination = data.get('destination')

    if not url or not destination:
        return jsonify({"error": "URL o ruta de destino no válida."}), 400

    # Crear la carpeta de destino si no existe
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Definir las opciones para yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Descarga el mejor audio disponible
        'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),  # Guarda los archivos en la carpeta de destino
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extraer solo el audio
            'preferredcodec': 'mp3',  # Convertir a MP3
            'preferredquality': '192',  # Calidad del audio
        }],
        'postprocessor_args': [
            '-ar', '44100',  # Establecer la frecuencia de muestreo
            '-ac', '2'       # Establecer a estéreo
        ],
        'ignoreerrors': True,  # Ignora los errores y sigue con la siguiente canción en la playlist
    }

    try:
        # Descargar la playlist usando yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return jsonify({"message": "Descarga de la playlist completada con éxito."})
    except Exception as e:
        print(f"Error durante la descarga: {e}")
        return jsonify({"error": "Ocurrió un error durante la descarga."}), 500

if __name__ == '__main__':
    app.run(debug=True)
