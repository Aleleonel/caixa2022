#!/bin/bash

# Mude o diretório de trabalho para o local do script
cd "$(dirname "$0")"

# Diretório onde estão os arquivos dependentes
PROJETOS_DIR="/home/bionico/Documentos/Projetos21/caixa"
SCRIPT_DIR="$PROJETOS_DIR/caixa2022"

# Caminhos para o script Python e as pastas e arquivos dependentes
SCRIPT_PATH="$SCRIPT_DIR/home.py"
CONEXAO_PATH="$SCRIPT_DIR/conexao.py"
RELATORIO_FECHAMENTO_PATH="$SCRIPT_DIR/relatorio_fechamento3.py"
ICONES_PATH="$SCRIPT_DIR/Icones"
IMG_PATH="$SCRIPT_DIR/img"

# Verifica se os arquivos e pastas dependentes existem antes de executar o script Python
if [ -f "$SCRIPT_PATH" ] && [ -f "$CONEXAO_PATH" ] && [ -f "$RELATORIO_FECHAMENTO_PATH" ] && [ -d "$ICONES_PATH" ] && [ -d "$IMG_PATH" ]; then
    python3 "$SCRIPT_PATH"
else
    echo "Alguns arquivos ou pastas dependentes estão faltando. Verifique o caminho e a estrutura do seu projeto."
fi
