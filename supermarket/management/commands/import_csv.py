import csv
import os
from django.core.management.base import BaseCommand
from supermarket.models import Supermarket

class Command(BaseCommand):
    help = 'Importa productos desde un archivo CSV'

    def handle(self, *args, **kwargs):
        archivo_csv = 'productos_carulle.csv'
        ruta_absoluta = os.path.join(os.getcwd(), archivo_csv)

        try:
            with open(ruta_absoluta, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
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
                        self.stderr.write(self.style.ERROR(f"Falta columna: {e}"))
                    except ValueError as e:
                        self.stderr.write(self.style.ERROR(f"Formato inválido en fila: {row} → {e}"))
            self.stdout.write(self.style.SUCCESS('✅ Importación completada correctamente.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ Archivo no encontrado: {ruta_absoluta}"))

