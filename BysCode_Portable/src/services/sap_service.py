import requests
import urllib3

# Suprimir warnings de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SAPService:
    def __init__(self):
        self.base_url = "https://byspro.heinsohncloud.com.co:50000/b1s/v2"
        self.headers = None
        self.is_connected = False
    
    def login(self):
        """Iniciar sesión en SAP Service Layer"""
        credentials = {
            "CompanyDB": "SBOLabAvantis",
            "UserName": "manager", 
            "Password": "2609"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/Login",
                json=credentials,
                headers={"Content-Type": "application/json"},
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                self.headers = {
                    "Content-Type": "application/json",
                    "Cookie": f"B1SESSION={response.cookies.get('B1SESSION')}"
                }
                self.is_connected = True
                return True
            else:
                self.is_connected = False
                return False
                
        except Exception as e:
            print(f"Error en login SAP: {e}")
            self.is_connected = False
            return False
    
    def search_items(self, search_term):
        """Buscar items en SAP por nombre"""
        if not self.is_connected:
            if not self.login():
                return []
        
        try:
            # Filtrar por nombre y que empiece con 1000
            search_url = f"{self.base_url}/Items?$filter=contains(ItemName, '{search_term}') and startswith(ItemCode, '1000')"
            
            response = requests.get(
                search_url,
                headers=self.headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('value', [])
            else:
                return []
                
        except Exception as e:
            print(f"Error en búsqueda SAP: {e}")
            return []
    
    def logout(self):
        """Cerrar sesión en SAP"""
        if self.headers and self.is_connected:
            try:
                requests.post(
                    f"{self.base_url}/Logout", 
                    headers=self.headers, 
                    verify=False, 
                    timeout=5
                )
                self.is_connected = False
                self.headers = None
            except Exception as e:
                print(f"Error en logout SAP: {e}")