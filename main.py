from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configura tu API Key aquí o mediante variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificación del webhook para Meta (opcional si usas ManyChat)
        verify_token = "my_verify_token"  # cámbialo por el tuyo
        if request.args.get("hub.verify_token") == verify_token:
            return request.args.get("hub.challenge")
        return "Unauthorized", 403

    if request.method == "POST":
        data = request.get_json()

        # Extraemos el mensaje del usuario (ajusta según cómo lo mande ManyChat)
        usuario = data.get("usuario")
        mensaje = data.get("mensaje")

        if not mensaje:
            return jsonify({"error": "No se recibió ningún mensaje"}), 400

        # Llamada a OpenAI
        try:
            respuesta = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres el asistente de un entrenador personal que responde en tono motivador, claro y comercial."},
                    {"role": "user", "content": mensaje}
                ]
            )
            texto = respuesta.choices[0].message.content.strip()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        # Devolver la respuesta a ManyChat
        return jsonify({
            "respuesta": {
                "text": texto
            }
        })

if __name__ == "__main__":
    app.run(port=5000, debug=True)