import sys
from PyQt6.QtWidgets import QApplication
from splashScreen import SplashScreen

def main():
    app = QApplication(sys.argv)
    
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
    splash = SplashScreen()
    splash.show()
    splash.startAnimation()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()