#!/usr/bin/env python3
"""
Script para criar o arquivo ZIP de entrega do jogo
"""
import os
import zipfile
import shutil
from pathlib import Path

def criar_zip_entrega():
    """Cria o arquivo ZIP com o executável e assets"""
    
    print("=" * 50)
    print("Criando arquivo ZIP para entrega")
    print("=" * 50)
    print()
    
    # Nome do arquivo ZIP
    zip_name = "JogoSkate_Entrega.zip"
    
    # Verificar se o executável existe
    exe_path = Path("dist/JogoSkate.exe")
    if not exe_path.exists():
        print("ERRO: Executável não encontrado!")
        print(f"Procurando em: {exe_path.absolute()}")
        print()
        print("Por favor, compile o jogo primeiro usando:")
        print("  - Windows: build_windows.bat")
        print("  - Linux/Mac: python build_windows.sh")
        return False
    
    # Criar pasta temporária para organização
    temp_dir = Path("temp_entrega")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    print("Copiando arquivos...")
    
    # Copiar executável
    shutil.copy2(exe_path, temp_dir / "JogoSkate.exe")
    print(f"  ✓ {exe_path.name}")
    
    # Copiar requirements.txt (opcional, mas útil)
    if Path("requirements.txt").exists():
        shutil.copy2("requirements.txt", temp_dir / "requirements.txt")
        print("  ✓ requirements.txt")
    
    # Criar README.txt
    readme_content = """JOGO DE SKATE 2D
==================

INSTRUÇÕES:
1. Execute o arquivo JogoSkate.exe
2. Pressione ESPAÇO para começar
3. Use as setas para fazer manobras
4. Desvie dos obstáculos e ganhe pontos!

CONTROLES:
- ESPAÇO/SETA CIMA: Ollie (Pulo)
- SETA ESQUERDA: Kickflip
- SETA DIREITA: Heelflip  
- SETA BAIXO: 360° Spin

DICAS:
- Pouse em cima de barreiras ou rails para fazer grind!
- Use as rampas para ganhar altura e fazer manobras incríveis!
- Manobras feitas em rampas ganham +50% de pontos!

REQUISITOS:
- Windows 7 ou superior
- Não requer instalação de Python

PROBLEMAS?
Se o jogo não executar, tente:
1. Executar como Administrador
2. Verificar se o Windows Defender não está bloqueando
3. Executar via CMD para ver mensagens de erro

Desenvolvido com Python e Pygame
"""
    
    with open(temp_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("  ✓ README.txt")
    
    # Criar arquivo ZIP
    print()
    print("Criando arquivo ZIP...")
    
    if Path(zip_name).exists():
        os.remove(zip_name)
        print(f"  (Removendo {zip_name} existente)")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in temp_dir.iterdir():
            zipf.write(file, file.name)
            print(f"  ✓ Adicionado: {file.name}")
    
    # Limpar pasta temporária
    shutil.rmtree(temp_dir)
    
    print()
    print("=" * 50)
    print("SUCESSO!")
    print("=" * 50)
    print(f"Arquivo criado: {zip_name}")
    if Path(zip_name).exists():
        print(f"Tamanho: {Path(zip_name).stat().st_size / 1024 / 1024:.2f} MB")
    print()
    print("Pronto para entrega!")
    
    return True

if __name__ == "__main__":
    criar_zip_entrega()
