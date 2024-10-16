from rocketry import Rocketry
from rocketry.conds import daily, every
import os
import subprocess

app = Rocketry()

# Tark para atualizar token e extender  
# @app.task(every('15 days'))
@app.task('daily')
def verificar_atualizar_token():
    print("Verificando vencimento dos Tokens...")
    script_path = os.path.join(os.path.dirname(__file__), 'script_atualiza_token.py')
    os.system(f'python {script_path}')
    print("Verificação finalizada! ")

# Task para postagem de publicações
#@app.task(every("10 minutes"))
#def script_cria_publi_bau():
#    print("Verificando Publicações do Banco para serem postadas...")
#    script_path = os.path.join(os.path.dirname(__file__), 'script_cria_publi_bau.py')
#    os.system(f'python {script_path}')
#    print("Verificação finalizada! ")
    
# Task para verificar publicações pendentes de serem postadas
@app.task('minutely')
def verificar_publicacoes():
    print("Verificando publicações pendentes...")
    # Corrija o caminho do script para corresponder ao local correto
    script_path = os.path.join(os.path.dirname(__file__), 'script_verificar_post.py')
    subprocess.run(['python', script_path], check=True)
    print("Verificação finalizada! ")

if __name__ == "__main__":
    app.run()

