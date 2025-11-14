import sys
import os
from PyQt6.QtWidgets import QApplication

# Determinar si estamos en un ejecutable de PyInstaller
def get_base_path():
    if getattr(sys, 'frozen', False):
        # Si es ejecutable, la base es la carpeta del ejecutable
        return os.path.dirname(sys.executable)
    else:
        # Si es script, la base es la carpeta del script
        return os.path.dirname(__file__)

def main():
    app = QApplication(sys.argv)
    
    # Establecer el path base para recursos
    base_path = get_base_path()
    print(f"📍 Path base: {base_path}")
    
    # Establecer estilo general de la aplicación
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QLineEdit {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-family: 'Open Sans';
        }
        QLineEdit:focus {
            border-color: #39234f;
        }
        QPushButton {
            background-color: #39234f;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-family: 'Open Sans';
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #4a2d6c;
        }
        QPushButton:pressed {
            background-color: #2d1c3f;
        }
        QLabel {
            font-family: 'Open Sans';
        }
    """)
    
    # Mostrar splash screen con animación
    from splashScreen import SplashScreen
    splash = SplashScreen()
    splash.show()
    splash.startAnimation()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()