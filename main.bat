@echo off
:: Muda o diretório de trabalho para o local do script
cd /d %~dp0

:: Diretório onde estão os arquivos dependentes
set "PROJETOS_DIR=C:\Users\bionico\Documents\Projetos21\caixa"
set "SCRIPT_DIR=%PROJETOS_DIR%\caixa2022"

:: Caminhos para o script Python e as pastas e arquivos dependentes
set "SCRIPT_PATH=%SCRIPT_DIR%\home.py"
set "CONEXAO_PATH=%SCRIPT_DIR%\conexao.py"
set "RELATORIO_FECHAMENTO_PATH=%SCRIPT_DIR%\relatorio_fechamento3.py"
set "ICONES_PATH=%SCRIPT_DIR%\Icones"
set "IMG_PATH=%SCRIPT_DIR%\img"

:: Verifica se os arquivos e pastas dependentes existem antes de executar o script Python
if exist "%SCRIPT_PATH%" if exist "%CONEXAO_PATH%" if exist "%RELATORIO_FECHAMENTO_PATH%" if exist "%ICONES_PATH%" if exist "%IMG_PATH%" (
    python "%SCRIPT_PATH%"
) else (
    echo Alguns arquivos ou pastas dependentes estão faltando. Verifique o caminho e a estrutura do seu projeto.
)

:: Aguarde um pressionamento de tecla antes de fechar a janela
pause
