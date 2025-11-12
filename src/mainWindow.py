import os
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar la interfaz desde el archivo .ui
        loadUi(os.path.join(os.path.dirname(__file__), "mainWindow.ui"), self)
        
        # Configurar la tabla
        self.setupTable()
        
        # Configurar logo (si existe)
        self.setupLogo()
        
        # Conectar señales
        self.searchButton.clicked.connect(self.searchCode)
        self.searchInput.returnPressed.connect(self.searchCode)
        
        # Datos de ejemplo
        self.sampleData = {
            "tornillo hexagonal": "TOR-HX-001",
            "tuerca galvanizada": "TNC-GZ-002",
            "arandela plana": "ARD-PL-003",
            "clavo acero": "CLV-AC-004",
            "taladro percutor": "TLD-PC-005",
        }
    
    def setupLogo(self):
        """Configurar el logo si existe el archivo"""
        logoPath = os.path.join(os.path.dirname(__file__), "..", "media", "logo-byspro.png")
        if os.path.exists(logoPath):
            pixmap = QPixmap(logoPath)
            self.label.setPixmap(pixmap.scaled(100, 40, Qt.AspectRatioMode.KeepAspectRatio, 
                                             Qt.TransformationMode.SmoothTransformation))
        else:
            # Si no existe el logo, ocultar el label
            self.label.setVisible(False)
    
    def setupTable(self):
        """Configurar la tabla de resultados"""
        header = self.resultsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    
    def searchCode(self):
        """Realizar la búsqueda del código"""
        searchText = self.searchInput.text().strip().lower()
        
        if not searchText:
            self.statusLabel.setText("Por favor, ingrese un término de búsqueda")
            self.resultsTable.setRowCount(0)
            return
        
        # Limpiar tabla
        self.resultsTable.setRowCount(0)
        
        # Buscar coincidencias
        matches = []
        for name, code in self.sampleData.items():
            if searchText in name.lower():
                matches.append((name, code))
        
        if matches:
            self.statusLabel.setText(f"Se encontraron {len(matches)} resultado(s)")
            # Mostrar resultados en la tabla
            self.resultsTable.setRowCount(len(matches))
            for row, (name, code) in enumerate(matches):
                self.resultsTable.setItem(row, 0, QTableWidgetItem(name.title()))
                self.resultsTable.setItem(row, 1, QTableWidgetItem(code))
        else:
            self.statusLabel.setText("No se encontraron resultados")
            self.resultsTable.setRowCount(0)