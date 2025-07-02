
from flask import Flask, render_template, request
from openai import OpenAI

client = OpenAI()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    perguntas = []
    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        empresa = request.form.get("empresa")
        funcao = request.form.get("funcao")
        sentimento = request.form.get("sentimento")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente de SST que gera perguntas com base no estado emocional do funcionário."},
                {"role": "user", "content": f"O funcionário respondeu que está se sentindo '{sentimento}'. Crie 5 perguntas relacionadas à saúde e segurança no trabalho com base nisso."}
            ]
        )
        perguntas = response.choices[0].message.content.strip().split("\n")

    return render_template("formulario.html", perguntas=perguntas)

if __name__ == "__main__":
    app.run(debug=True)
