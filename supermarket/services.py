from abc import ABC, abstractmethod
import csv
import os
import json

class ProductImporter(ABC):
    """
    Interfaz abstracta para importadores de productos.
    """
    @abstractmethod
    def import_products(self):
        """
        Método abstracto para importar productos.
        Debe ser implementado por las clases concretas.
        """
        pass

class CSVProductImporter(ProductImporter):
    """
    Implementación concreta para importar productos desde un archivo CSV.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def import_products(self):
        ruta_absoluta = os.path.join(os.getcwd(), self.file_path)
        try:
            with open(ruta_absoluta, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            raise
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo CSV: {e}")
            return []

class JSONProductImporter(ProductImporter):
    """
    Implementación concreta para importar productos desde un archivo JSON.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def import_products(self):
        # Esta es una implementación de ejemplo. Se necesitaría un archivo JSON con la estructura adecuada.
        self.stdout.write(self.style.NOTICE("Importador JSON aún no implementado al 100%."))
        return []

class ImporterFactory:
    """
    Fábrica que crea el tipo de importador de productos adecuado según el archivo.
    """
    @staticmethod
    def get_importer(file_path):
        """
        Inspecciona la extensión del archivo y devuelve una instancia del importador correcto.
        """
        extension = os.path.splitext(file_path)[1].lower()
        if extension == '.csv':
            return CSVProductImporter(file_path)
        elif extension == '.json':
            # Aunque no tengamos archivos JSON, la fábrica ya está lista para soportarlos.
            return JSONProductImporter(file_path)
        else:
            raise ValueError(f"El formato de archivo '{extension}' no es soportado.")
