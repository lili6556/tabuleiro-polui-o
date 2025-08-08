from flask import Flask, render_template, request, redirect, url_for, session
import random
import json
import sqlite3

app = Flask(__name__)
app.secret_key = 'segredo-bonito-do-jogo'

# Cria banco de dados se não existir
def init_db():
    with sqlite3.connect("jogo.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS jogadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome1 TEXT,
                nome2 TEXT
            );
        ''')
init_db()

# Carrega perguntas do JSON
def carregar_perguntas():
    with open("perguntas.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados["perguntas"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    mensagem = None
    jogadores_cadastrados = False

    if request.method == "POST":
        nome1 = request.form.get("jogador1", "").strip()
        nome2 = request.form.get("jogador2", "").strip()

        if nome1 and nome2:
            with sqlite3.connect("jogo.db") as conn:
                conn.execute("DELETE FROM jogadores")
                conn.execute("INSERT INTO jogadores (nome1, nome2) VALUES (?, ?)", (nome1, nome2))

            session.clear()  # Limpa a sessão anterior
            session["jogador_atual"] = 1
            session["perguntas_restantes"] = carregar_perguntas()
            session["nomes_jogadores"] = {"1": nome1, "2": nome2}
            session["estado"] = {"aguardando_resposta_do": 1, "pergunta_em_aberto": None, "respondeu_errado_anterior": False}

            return redirect(url_for("perguntas"))
        else:
            mensagem = "Preencha os dois nomes corretamente."

    return render_template("cadastro.html", mensagem=mensagem, jogadores_cadastrados=jogadores_cadastrados)

@app.route("/perguntas", methods=["GET", "POST"])
def perguntas():
    perguntas = session.get("perguntas_restantes", [])
    nomes = session.get("nomes_jogadores")
    estado = session.get("estado", {"respondeu_errado_anterior": False})

    if not nomes or not isinstance(nomes, dict):
        return redirect(url_for("cadastro"))

    if not perguntas and not session.get("pergunta_atual"):
        return "Acabaram as perguntas!"

    jogador_num = session.get("jogador_atual", 1)
    jogador_atual = nomes.get(str(jogador_num), f"Jogador {jogador_num}")
    resultado = None
    mostrar_botao_dado = False

    # Trata ação de pular vez
    if request.args.get("acao") == "pular_vez":
        estado["respondeu_errado_anterior"] = False  # reseta o erro
        session["jogador_atual"] = 2 if session["jogador_atual"] == 1 else 1
        session["estado"] = estado
        return redirect(url_for("perguntas"))

    if request.method == "POST":
        resposta = request.form.get("resposta")
        pergunta_atual = session.get("pergunta_atual", {})
        correta = pergunta_atual.get("resposta")

        if resposta == correta:
            resultado = "Acertou!"
            mostrar_botao_dado = True
            estado["respondeu_errado_anterior"] = False

            if pergunta_atual in perguntas:
                perguntas.remove(pergunta_atual)
            session["pergunta_atual"] = None

        else:
            if not estado["respondeu_errado_anterior"]:
                estado["respondeu_errado_anterior"] = True
                session["jogador_atual"] = 2 if session["jogador_atual"] == 1 else 1
            else:
                estado["respondeu_errado_anterior"] = False
                session["jogador_atual"] = 2 if session["jogador_atual"] == 1 else 1

                if pergunta_atual in perguntas:
                    perguntas.remove(pergunta_atual)
                session["pergunta_atual"] = None

            resultado = "Errou!"

        session["estado"] = estado
        session["perguntas_restantes"] = perguntas

    if not session.get("pergunta_atual") and perguntas:
        nova_pergunta = random.choice(perguntas)
        session["pergunta_atual"] = nova_pergunta

    pergunta = session.get("pergunta_atual")

    return render_template("perguntas.html",
                           pergunta=pergunta,
                           jogador_atual=jogador_atual,
                           mensagem_resultado=resultado,
                           mostrar_botao_dado=mostrar_botao_dado,
                           mostrar_botao_continuar=resultado == "Errou!")

@app.route("/continuar", methods=["POST"])
def continuar():
    if "indice_pergunta_atual" not in session:
        session["indice_pergunta_atual"] = 0  # ou outro valor inicial
    
    session["indice_pergunta_atual"] += 1
    
    return redirect(url_for("perguntas"))


@app.route("/pular_vez", methods=["POST"])
def pular_vez():
    atual = session.get("jogador_atual", 1)
    session["jogador_atual"] = 2 if atual == 1 else 1

    # Zera os estados de controle
    session["respondeu_certo"] = False
    session["aguardando_outro"] = False

    return redirect(url_for("perguntas"))



@app.route("/pular_pergunta", methods=["POST"])
def pular_pergunta():
    perguntas = session.get("perguntas_restantes", [])
    nomes = session.get("nomes_jogadores")

    if not nomes:
        return redirect(url_for("cadastro"))

    if not perguntas:
        return "Acabaram as perguntas!"

    pergunta = random.choice(perguntas)
    perguntas.remove(pergunta)
    session["pergunta_atual"] = pergunta
    session["perguntas_restantes"] = perguntas

    return redirect(url_for("perguntas"))

@app.route("/dado")
def dado():
    return render_template("dado.html")

@app.route("/tabuleiro")
def tabuleiro():
    return render_template("tabuleiro.html")

if __name__ == "__main__":
    app.run(debug=True)
