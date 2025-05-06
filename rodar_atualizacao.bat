@echo off
cd "C:\Users\nathyyy\Downloads\pySYSINV"
echo --- >> log_execucao.txt
echo Executando em: %date% %time% >> log_execucao.txt
"C:\Python310\python.exe" atualizacoes.py >> log_execucao.txt 2>&1
