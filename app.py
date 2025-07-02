
from flask import Flask, request, render_template_string
from fpdf import FPDF
from cryptography.fernet import Fernet
from drive_upload import upload_file_to_drive
from transformers import pipeline
import os
from datetime import datetime

# Modelo Falcon RW 1B
gerador = pipeline("text-generation", model="tiiuae/falcon-rw-1b", trust_remote_code=True)

app = Flask(__name__)

# Senha de acesso ao formulário
SENHA_CORRETA = "valentecare"

def gerar_perguntas(resposta_inicial):
    prompt = f"O funcionário respondeu: '{resposta_inicial}'. Gere 5 perguntas objetivas sobre saúde ocupacional, riscos psicossociais, assédio ou estresse no trabalho, de forma empática."
    resposta = gerador(prompt, max_new_tokens=200)[0]["generated_text"]
    linhas = resposta.split("\n")
    perguntas = [linha.strip() for linha in linhas if "?" in linha]
    return perguntas[:5]

@app.route("/", methods=["GET", "POST"])
def index():
    with open("formulario.html", encoding="utf-8") as f:
        html = f.read()

    if request.method == "POST":
        if request.form.get("senha") != SENHA_CORRETA:
            return "Senha incorreta. Acesso negado."

        nome = request.form["nome"]
        cpf = request.form["cpf"]
        empresa = request.form["empresa"]
        funcao = request.form["funcao"]
        sentimento = request.form["sentimento"]
        perguntas = gerar_perguntas(sentimento)
        respostas = [request.form.get(f"resposta_{i}") for i in range(len(perguntas))]

        # Criar PDF
        pdf_path = f"{cpf}_respostas.pdf"
        key = Fernet.generate_key()
        cipher = Fernet(key)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Funcionário: {nome} | CPF: {cpf}", ln=True)
        pdf.cell(200, 10, f"Empresa: {empresa} | Função: {funcao}", ln=True)
        pdf.cell(200, 10, f"Sentimento inicial: {sentimento}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)

        for i, (pergunta, resposta) in enumerate(zip(perguntas, respostas)):
            pdf.multi_cell(0, 10, f"{i+1}. {pergunta}
Resposta: {resposta}")

        pdf.output(pdf_path)

        with open(pdf_path, "rb") as file:
            encrypted = cipher.encrypt(file.read())

        encrypted_path = pdf_path.replace(".pdf", "_enc.pdf")
        with open(encrypted_path, "wb") as f:
            f.write(encrypted)

        # Upload em pasta da empresa
        upload_file_to_drive(encrypted_path, pasta=empresa)

        # Log local
        with open("log.txt", "a", encoding="utf-8") as log:
            horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log.write(f"{horario} | Nome: {nome} | CPF: {cpf} | Empresa: {empresa}\n")

        return "Arquivo criptografado enviado com sucesso!"

    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True)
