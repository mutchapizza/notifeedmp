import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from gemini_client import GeminiClient
from utils import MUNICIPIOS_URLS

class NoticiasScraper:
    def __init__(self):
        self.gemini = GeminiClient()
        
    def ejecutar(self, dias):
        """Ejecuta scraping para todos los municipios"""
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=dias)
        
        noticias = []
        id_counter = 1
        
        for municipio, url in MUNICIPIOS_URLS.items():
            noticias.extend(
                self._scrap_municipio(municipio, url, fecha_inicio, fecha_fin, id_counter)
            )
            id_counter = len(noticias) + 1
            
        return pd.DataFrame(noticias)
    
    def _scrap_municipio(self, municipio, url, fecha_inicio, fecha_fin, start_id):
        """Scraping por municipio"""
        noticias = []
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Lógica específica por sitio (Telediario/El Heraldo)
            if "telediario" in url:
                articulos = soup.find_all('article', class_='nota')
            else:
                articulos = soup.find_all('div', class_='post')
                
            for art in articulos:
                noticia = self._procesar_articulo(art, municipio, url)
                if noticia and fecha_inicio <= noticia['fecha'] <= fecha_fin:
                    noticia['id'] = start_id + len(noticias)
                    noticias.append(noticia)
                    
        except Exception as e:
            print(f"Error en {municipio}: {str(e)}")
            
        return noticias
    
    def _procesar_articulo(self, articulo, municipio, url_base):
        """Procesa artículo con Gemini"""
        try:
            # Extraer datos básicos
            titulo = articulo.find('h2').text.strip()
            link = url_base + articulo.find('a')['href']
            fecha_str = articulo.find('time')['datetime']
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            
            # Usar Gemini para localización y resumen
            contenido = self._extraer_contenido(link)
            resumen = self.gemini.resumir(contenido)
            localizacion = self.gemini.extraer_localizacion(contenido, municipio)
            
            return {
                'FECHA': fecha.strftime("%d/%m/%Y"),
                'MUNICIPIO': municipio,
                'LOCALIZACIÓN': localizacion,
                'URL NOTICIA': link,
                'RESUMEN': resumen
            }
        except:
            return None
    
    def _extraer_contenido(self, url):
        """Extrae texto completo de la noticia"""
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return ' '.join([p.text for p in soup.find_all('p')])