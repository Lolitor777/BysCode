from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtProperty, QSequentialAnimationGroup
from PyQt6.QtGui import QFont

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BysCode")
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #3498db);
            }
        """)
        
        # Widget central
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)
        
        # Label de animación
        self.animationLabel = QLabel("BysCode")
        self.animationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.animationLabel.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                border: none;
            }
        """)
        
        # Configurar fuente
        font = QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.animationLabel.setFont(font)
        
        layout.addWidget(self.animationLabel)
        
        # Configurar animaciones
        self._pos = QPoint(0, 180)
        
        # Animación 1: Entrada hasta el centro con bounce
        self.anim1 = QPropertyAnimation(self, b"position")
        self.anim1.setDuration(1200)
        self.anim1.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        # Animación 2: Salida después del bounce
        self.anim2 = QPropertyAnimation(self, b"position")
        self.anim2.setDuration(800)
        self.anim2.setEasingCurve(QEasingCurve.Type.InCubic)
        
        # Grupo de animaciones secuenciales
        self.animationGroup = QSequentialAnimationGroup()
        self.animationGroup.addAnimation(self.anim1)
        self.animationGroup.addAnimation(self.anim2)
        
        # Conectar señal de finalización
        self.animationGroup.finished.connect(self.animationFinished)
    
    @pyqtProperty(QPoint)
    def position(self):
        return self._pos
    
    @position.setter
    def position(self, value):
        self._pos = value
        self.animationLabel.move(value)
    
    def startAnimation(self):
        
        centerY = 180
        
        
        startPos = QPoint(-200, centerY)      
        centerPos = QPoint(200, centerY)     
        
        
        endPos = QPoint(800, centerY)         
        
    
        self.anim1.setStartValue(startPos)
        self.anim1.setEndValue(centerPos)
        
        # Configurar segunda animación (salida)
        self.anim2.setStartValue(centerPos)
        self.anim2.setEndValue(endPos)
        
        # Iniciar el grupo de animaciones
        self.animationGroup.start()
    
    def animationFinished(self):
        self.hide()
        from mainWindow import MainWindow
        self.mainWindow = MainWindow()
        self.mainWindow.show()