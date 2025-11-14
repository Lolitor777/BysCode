import os
import shutil
import subprocess
import sys

def build_with_external_files():
    print("🔨 BUILD CON ARCHIVOS EXTERNOS")
    print("=" * 50)
    
    # 1. Limpiar
    for folder in ['build', 'dist', 'BysCode_Portable']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # 2. Crear estructura portable
    print("📁 Creando estructura portable...")
    portable_dir = "BysCode_Portable"
    os.makedirs(portable_dir)
    
    # Crear subcarpetas
    subfolders = ['src', 'src/services', 'media']
    for folder in subfolders:
        os.makedirs(os.path.join(portable_dir, folder), exist_ok=True)
    
    # 3. Copiar archivos necesarios
    files_to_copy = [
        ('src/mainWindow.ui', 'src/mainWindow.ui'),
        ('src/services/sap_service.py', 'src/services/sap_service.py'),
        ('media/logo-byscode.ico', 'media/logo-byscode.ico'),
        ('media/logo-byscode.png', 'media/logo-byscode.png'),
        ('media/logo-byscode.png', 'media/logo-byscode.png'),  
        ('media/logo-byspro.png', 'media/logo-byspro.png')
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(portable_dir, dst))
            print(f"   ✅ Copiado: {src} -> {dst}")
        else:
            print(f"   ❌ No encontrado: {src}")
    
    # 4. Crear ejecutable
    print("\n🔨 Creando ejecutable...")
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=BysCode',
        '--onefile',
        '--windowed',
        '--icon=media/logo-byscode.ico',
        '--add-data=src/mainWindow.ui;.',
        '--add-data=src/services/sap_service.py;.',
        '--hidden-import=PyQt6.uic',
        '--hidden-import=requests',
        '--hidden-import=urllib3',
        '--clean',
        'src/main.py'
    ]
    
    try:
        subprocess.check_call(cmd)
        
        # 5. Mover ejecutable a carpeta portable
        if os.path.exists('dist/BysCode.exe'):
            shutil.move('dist/BysCode.exe', os.path.join(portable_dir, 'BysCode.exe'))
            print(f"   ✅ Ejecutable movido a: {portable_dir}/BysCode.exe")
            
            # 6. Crear archivo README
            readme_content = """BYSCODE - Buscador de Códigos SAP

🎯 Cómo usar:
1. Ejecutar 'BysCode.exe'
2. La aplicación se conectará automáticamente a SAP
3. Escribir el nombre del material y presionar Buscar

📁 Estructura:
- BysCode.exe (Ejecutable principal)
- src/mainWindow.ui (Interfaz)
- src/services/sap_service.py (Conexión SAP)
- media/ (Logos e iconos)

⚡ Portable: No necesita instalación
"""
            with open(os.path.join(portable_dir, 'LEEME.txt'), 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"   ✅ Archivo LEEME.txt creado")
            
            return True
        else:
            print("   ❌ No se creó el ejecutable")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    if build_with_external_files():
        print("\n" + "=" * 50)
        print("🎉 ¡BUILD EXITOSO!")
        print("\n📁 Tu aplicación portable está en: BysCode_Portable/")
        print("   - BysCode.exe")
        print("   - src/mainWindow.ui") 
        print("   - src/services/sap_service.py")
        print("   - media/logo-byscode.ico")
        print("\n🚀 Para usar: Ejecuta 'BysCode_Portable/BysCode.exe'")
    else:
        print("\n❌ BUILD FALLIDO")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()