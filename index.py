import os
from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import re


app = Flask(__name__)
#app.config['SECRET_KEY'] = "PYTHONSENHA"
app.config['UPLOAD_FOLDER'] = 'uploads' 

def get_resposta(livro, pergunta):
    try:
        with open(livro, 'rb') as pdf_reader:
            pdf = PdfReader(pdf_reader)
            contpage = len(pdf.pages)
            pergunta_formatada = re.sub(r'[^\w\s]', '', pergunta).lower()
            
            #lendo cada páginas do PDF
            for page_num in range(contpage):
                texto = pdf.pages[page_num].extract_text()
                texto_formatado = re.sub(r'[^\w\s]', '', texto).lower()
                
                if pergunta_formatada in texto_formatado:
                    print(f"Conteúdo da página {page_num + 1}:")
                    return texto
            
            print('Nada encontrado')
            return None
        
    except FileNotFoundError:
        print(f'Arquivo "{livro}" não encontrado.')
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index():
    livro = request.files['files']
    pergunta = request.form['pergunta']
    
    if livro:
        filename = secure_filename(livro.filename)
        livro_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        livro.save(livro_path)
    
        resposta = get_resposta(livro_path, pergunta)
        
        if resposta:
            os.remove(livro_path)
            return redirect(url_for('resposta', resposta=resposta))
        else:
           os.remove(livro_path)
           return redirect(url_for('error'))
    else:
        return "Nenhum arquivo enviado."

@app.route('/resposta')
def resposta():
    resposta = request.args.get('resposta')
    return render_template('resposta.html', resposta=resposta)

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    print("Por favor, clica neste link -> http://127.0.0.1:5000/ para usar o aplicativo.")
    app.run(debug=True)

