import os
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
import os
import sys


def get_resource_path(relative_path):
    """Obtiene la ruta correcta para archivos, funciona en dev y en exe"""
    try:
        # PyInstaller crea una carpeta temporal en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no estamos en PyInstaller, usar la ruta normal
        base_path = os.path.abspath(".")
    
    # Si el archivo está en el mismo directorio que el exe
    exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    
    # Probar diferentes rutas
    possible_paths = [
        os.path.join(base_path, relative_path),
        os.path.join(exe_dir, relative_path),
        os.path.join(os.path.dirname(__file__), relative_path),
        relative_path
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return relative_path 


from services.sap_service import SAPService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        loadUi("src/mainWindow.ui", self)
        
        # DEBUG: Ver qué widgets tenemos disponibles
        print("Widgets disponibles:")
        for attr_name in dir(self):
            if not attr_name.startswith('_'):  # Evitar métodos privados
                attr = getattr(self, attr_name)
                if hasattr(attr, 'objectName'):
                    print(f"  {attr_name}: {attr.objectName()}")

        ui_paths = [
        get_resource_path('src/mainWindow.ui'),
        get_resource_path('mainWindow.ui'),
        'src/mainWindow.ui',
        'mainWindow.ui'
    ]
    
        ui_loaded = False
        for ui_path in ui_paths:
            try:
                if os.path.exists(ui_path):
                    loadUi(ui_path, self)
                    print(f"✅ UI cargada desde: {ui_path}")
                    ui_loaded = True
                    break
                else:
                    print(f"❌ No existe: {ui_path}")
            except Exception as e:
                print(f"❌ Error cargando {ui_path}: {e}")
                continue
        
        if not ui_loaded:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(None, "Error", "No se pudo cargar la interfaz de usuario")
            sys.exit(1)
        
        # Inicializar servicio SAP
        self.sap_service = SAPService()
        
        # Configurar la tabla
        self.setupTable()
        
        # Configurar logo
        self.setupLogo()
        
        # Conectar señales
        self.searchButton.clicked.connect(self.searchCode)
        self.searchInput.returnPressed.connect(self.searchCode)
        
        # Intentar login inicial
        self.initialLogin()
    
    def initialLogin(self):
        """Intentar login al iniciar la aplicación"""
        # Usar titleLabel temporalmente hasta que agregues statusLabel
        if hasattr(self, 'titleLabel'):
            self.titleLabel.setText("BysCode - Conectando...")
        
        if self.sap_service.login():
            if hasattr(self, 'titleLabel'):
                self.titleLabel.setText("BysCode - Conectado")
        else:
            if hasattr(self, 'titleLabel'):
                self.titleLabel.setText("BysCode - Error conexión")
            QMessageBox.warning(self, "Error", "No se pudo conectar con SAP Service Layer")
    
    
    def setupLogo(self):
        """Configurar el logo - busca diferentes formatos y ubicaciones"""
        print("🖼️ Buscando logo...")
        
        # Lista de posibles logos y ubicaciones
        logo_paths = [
            get_resource_path('media/logo-byscode.png'),  # Logo personalizado
            get_resource_path('media/logo-byspro.png'),   # Logo original
            get_resource_path('media/logo-byscode.ico'),  # Icono como fallback
            'media/logo-byscode.png',
            'media/logo-byspro.png', 
            'media/logo-byscode.ico',
            os.path.join(os.path.dirname(__file__), '..', 'media', 'logo-byscode.png'),
            os.path.join(os.path.dirname(__file__), '..', 'media', 'logo-byspro.png')
        ]
        
        logo_cargado = False
        for logo_path in logo_paths:
            try:
                if os.path.exists(logo_path):
                    pixmap = QPixmap(logo_path)
                    if not pixmap.isNull():
                        # Escalar manteniendo proporciones, máximo 100x40
                        scaled_pixmap = pixmap.scaled(100, 40, Qt.AspectRatioMode.KeepAspectRatio, 
                                                    Qt.TransformationMode.SmoothTransformation)
                        self.label.setPixmap(scaled_pixmap)
                        print(f"✅ Logo cargado: {logo_path}")
                        logo_cargado = True
                        break
                    else:
                        print(f"❌ Pixmap inválido: {logo_path}")
                else:
                    print(f"🔍 No existe: {logo_path}")
            except Exception as e:
                print(f"⚠️ Error cargando {logo_path}: {e}")
                continue
        
        if not logo_cargado:
            # Si no se encuentra ningún logo, ocultar el label
            self.label.setVisible(False)
            print("⚠️ No se encontró ningún logo, ocultando label")
        else:
            # Asegurar que el label sea visible si se cargó un logo
            self.label.setVisible(True)

    
    def setupTable(self):
        """Configurar la tabla de resultados"""
        header = self.resultsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    
    def searchCode(self):
        """Realizar la búsqueda en SAP"""
        search_text = self.searchInput.text().strip()
        
        if not search_text:
            if hasattr(self, 'titleLabel'):
                self.titleLabel.setText("BysCode - Ingrese término")
            self.resultsTable.setRowCount(0)
            return
        
        # Mostrar que está buscando
        if hasattr(self, 'titleLabel'):
            self.titleLabel.setText("BysCode - Buscando...")
        
        # Limpiar tabla
        self.resultsTable.setRowCount(0)
        
        # Buscar en SAP
        results = self.sap_service.search_items(search_text)
        
        if results:
            if hasattr(self, 'titleLabel'):
                self.titleLabel.setText("BysCode - Listo")
            # Mostrar resultados en la tabla
            self.resultsTable.setRowCount(len(results))
            for row, item in enumerate(results):
                self.resultsTable.setItem(row, 0, QTableWidgetItem(item.get('ItemName', 'N/A')))
                self.resultsTable.setItem(row, 1, QTableWidgetItem(item.get('ItemCode', 'N/A')))
        else:
            if hasattr(self, 'titleLabel'):
                self.titleLabel.setText("BysCode - Sin resultados")
            self.resultsTable.setRowCount(0)
    
    def closeEvent(self, event):
        """Cerrar sesión al salir de la aplicación"""
        self.sap_service.logout()
        event.accept()