import csv
from django.core.management.base import BaseCommand
from supermarket.models import Supermarket
from supermarket.services import CSVProductImporter

class Command(BaseCommand):
    help = 'Importa productos desde un archivo CSV utilizando un importador desacoplado.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='La ruta al archivo CSV para importar.')

    def handle(self, *args, **kwargs):
        archivo_csv = kwargs['csv_file']
        importer = CSVProductImporter(file_path=archivo_csv)

        try:
            products_data = importer.import_products()
            if not products_data:
                self.stderr.write(self.style.WARNING("No se encontraron datos en el archivo o el archivo está vacío."))
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
                    self.stderr.write(self.style.ERROR(f"Falta la columna requerida en el CSV: {e}"))
                except ValueError as e:
                    self.stderr.write(self.style.ERROR(f"Error de formato en la fila: {row} -> {e}"))

            self.stdout.write(self.style.SUCCESS(f'✅ Importación desde {archivo_csv} completada correctamente.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'❌ Archivo no encontrado: {archivo_csv}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ocurrió un error inesperado: {e}'))

