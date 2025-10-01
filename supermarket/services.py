from abc import ABC, abstractmethod
import csv
import os

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
        """
        Importa productos desde el archivo CSV especificado en el constructor.
        """
        ruta_absoluta = os.path.join(os.getcwd(), self.file_path)
        try:
            with open(ruta_absoluta, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            # Podríamos manejar el error aquí o dejar que la capa superior lo haga.
            # Por ahora, lo relanzamos para que el comando lo maneje.
            raise
        except Exception as e:
            # Manejar otros posibles errores durante la lectura del archivo
            print(f"Ocurrió un error al leer el archivo: {e}")
            return []
