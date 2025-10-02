from django.core.management.base import BaseCommand
from supermarket.models import Supermarket
from supermarket.services import ImporterFactory

class Command(BaseCommand):
    help = 'Importa productos desde un archivo (CSV, JSON, etc.) usando una fábrica de importadores.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='La ruta al archivo de datos para importar.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        try:
            # Usamos la fábrica para obtener el importador adecuado.
            importer = ImporterFactory.get_importer(file_path)
            products_data = importer.import_products()
            
            if not products_data:
                self.stderr.write(self.style.WARNING("No se encontraron datos en el archivo o el importador no devolvió nada."))
                return

            for row in products_data:
                try:
                    Supermarket.objects.create(
                        nombre_supermercado=row['nombre_supermercado'],
                        nombre_producto=row['nombre_producto'],
                        marca_producto=row['marca_producto'],
                        precio_producto=float(row['precio_producto']),
                        calorias=float(row['calorias']),
                        proteinas=float(row['proteinas']),
                        carbohidratos=float(row['carbohidratos']),
                        grasas=float(row['grasas']),
                        imagen='images/default_image.jpg'
                    )
                except KeyError as e:
                    self.stderr.write(self.style.ERROR(f"Falta la columna requerida en el archivo: {e}"))
                except ValueError as e:
                    self.stderr.write(self.style.ERROR(f"Error de formato en la fila: {row} -> {e}"))

            self.stdout.write(self.style.SUCCESS(f'✅ Importación desde {file_path} completada correctamente.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'❌ Archivo no encontrado: {file_path}'))
        except ValueError as e:
            # Captura el error de la fábrica si el formato no es soportado.
            self.stderr.write(self.style.ERROR(str(e)))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ocurrió un error inesperado: {e}'))

