def generate_questions(profile):
    nome = profile.get("nome")
    return [
        {"pergunta": f"Olá {nome}, você está se sentindo bem no trabalho hoje?"},
        {"pergunta": "Você já presenciou ou sofreu algum tipo de assédio no ambiente de trabalho?"},
        {"pergunta": "Sente que há riscos ergonômicos na sua função atual?"},
        {"pergunta": "Como você avalia seu nível de estresse no trabalho?"}
    ]

def generate_pdf_and_encrypt(respostas, senha, nome_arquivo):
    from fpdf import FPDF
    from cryptography.fernet import Fernet
    import os

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for r in respostas:
        pdf.multi_cell(0, 10, f"{r['pergunta']}\nResposta: {r['resposta']}")

    temp_pdf_path = f"temp_{nome_arquivo}"
    pdf.output(temp_pdf_path)

    key = Fernet.generate_key()
    fernet = Fernet(key)
    with open(temp_pdf_path, "rb") as file:
        encrypted = fernet.encrypt(file.read())

    enc_path = f"enc_{nome_arquivo}"
    with open(enc_path, "wb") as file:
        file.write(encrypted)

    os.remove(temp_pdf_path)
    return enc_path