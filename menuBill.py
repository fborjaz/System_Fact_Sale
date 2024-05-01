import os.path as path
import json
import datetime
import time
import os
import math
import platform
from functools import reduce
from components import Menu, Valida
from utilities import borrarPantalla, gotoxy, reset_color, red_color, green_color, yellow_color, blue_color, purple_color, cyan_color
from clsJson import JsonFile
from company import Company
from customer import RegularClient, VipClient
from sales import Sale
from product import Product
from iCrud import ICrud

# Validación de comparación de existencia de archivo JSON.
# Validar la existencia de archivos
def validate_file_existence(file_path):
    # Verificar si el archivo no existe
    if not path.exists(file_path):
        # Si el archivo no existe, mostrar un mensaje indicando que se creará un archivo vacío
        print(f"El archivo {file_path} no existe. Creando un archivo vacío...")
        # Crear un archivo vacío con el nombre especificado en la ruta
        with open(file_path, 'w') as file:
            file.write('[]')  # Escribir una lista vacía en el archivo

# Ejemplos de uso para cada archivo necesario en tu aplicación
validate_file_existence('archivos/clients.json')
validate_file_existence('archivos/products.json')
validate_file_existence('archivos/invoices.json')
validate_file_existence('archivos/companies.json')

path, _ = os.path.split(os.path.abspath(__file__))

# Procesos de las Opciones del Menu Facturacion
# Procesos de clientes
class CrudClients(ICrud):
    def create(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(blue_color + "Registro de Clientes")

        gotoxy(5, 4); print("Nombre: ")
        name = validar.solo_letras("Error: Solo letras", 13, 4)
        gotoxy(5, 5); print("Apellido: ")
        lastname = validar.solo_letras("Error: Solo letras", 13, 5)
        gotoxy(5, 6); print("DNI: ")
        dni = validar.cedula("Error: Cédula inválida", 13, 6)

        # Leer la lista de clientes existentes desde el archivo JSON
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()

        # Verificar si la cédula ya está en uso
        for client in clients:
            if client['dni'] == dni:
                gotoxy(5, 7); print("La cédula ya está registrada para otro cliente.")
                input("Presiona Enter para regresar al menú principal")
                return  # Salir del método si la cédula está duplicada

        # Continuar con el registro del nuevo cliente si la cédula no está duplicada
        gotoxy(5, 7); print("Tipo de cliente:")
        gotoxy(5, 8); print("1) Cliente Regular")
        gotoxy(5, 9); print("2) Cliente VIP")
        gotoxy(5, 10)
        tipo_cliente = validar.solo_numeros("Error: Solo números", 27, 7)

        while tipo_cliente not in {"1", "2"}:
            gotoxy(5, 11)
            print("Opción inválida. Intente de nuevo.")
            tipo_cliente = validar.solo_numeros("Error: Solo números", 27, 7)

        cliente_tipo = "Regular" if tipo_cliente == "1" else "VIP"

        if tipo_cliente == "1":
            gotoxy(5, 12); print("¿El cliente tiene tarjeta de descuento? (s/n): ")
            card = input().lower() == "s"
            cliente = RegularClient(name, lastname, dni, card)
        else:
            cliente = VipClient(name, lastname, dni)

        # Agregar el nuevo cliente a la lista de clientes y guardar en el archivo JSON
        clients.append(cliente.getJson())
        json_file.save(clients)

        gotoxy(5, 14); print("Cliente registrado exitosamente!")
        input("Presiona Enter para regresar al menú principal")

    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end = '')
        gotoxy(2,1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30,2); print(blue_color + "Actualización de Clientes")

        gotoxy(5,4); print("Ingrese el DNI del cliente a actualizar: ")
        dni = validar.solo_numeros("Error: Solo números", 40, 4)

        json_file = JsonFile(path + '/archivos/clients.json')
        client_list = json_file.read()
        found = False

        for client in client_list:
            if client['dni'] == dni:
                found = True
                gotoxy(5,5); print("Nombre: ")
                new_name = validar.solo_letras("Error: Solo letras", 13, 5)

                gotoxy(5,6); print("Apellido: ")
                new_lastname = validar.solo_letras("Error: Solo letras", 13, 6)

                client['nombre'] = new_name
                client['apellido'] = new_lastname
                json_file.save(client_list)
                gotoxy(5,8); print("Cliente actualizado con éxito")
                input("Presiona Enter para regresar al menú principal")
                break
        if not found:
            print("Cliente no encontrado.")

    def delete(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(blue_color + "Eliminación de Clientes")

        gotoxy(5, 4); print("Ingrese el DNI del cliente a eliminar: ")
        dni = validar.solo_numeros("Error: Solo números", 40, 4)

        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()
        found = False

        for client in clients:
            if client['dni'] == dni:
                found = True
                gotoxy(5, 6); print("¿Está seguro de eliminar este cliente? (S/N): ")
                confirmacion = input().lower()
                if confirmacion == "s":
                    gotoxy(5, 7); print("Por seguridad, escriba 'ELIMINAR' para confirmar la eliminación: ")
                    confirmacion_final = input().lower()

                    if confirmacion_final == "eliminar":
                        del clients[clients.index(client)]
                        json_file.save(clients)
                        gotoxy(5, 9); print("Cliente eliminado con éxito")
                        input("Presiona Enter para regresar al menú principal")
                    else:
                        gotoxy(5, 9); print("Confirmación incorrecta. No se ha eliminado el cliente.")
                else:
                    gotoxy(5, 9); print("Operación cancelada.")
                break
        if not found:
            print("Cliente no encontrado.")

    def consult(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(blue_color + "Consulta de Clientes")
        print("\n")
        print("Seleccione una opción:")
        print("1) Buscar cliente por DNI")
        print("2) Ver todos los clientes")

        opcion = input("Ingrese su opción (1 o 2): ")

        if opcion == "1":
            validar = Valida()
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
            gotoxy(30, 2); print(blue_color + "Consulta de Cliente por DNI")
            print("\n")
            dni = validar.solo_numeros("Ingrese el DNI del cliente a buscar: ", 5, 4)

            json_file = JsonFile(path + '/archivos/clients.json')
            clients = json_file.read()
            found = False
            for client in clients:
                if client['dni'] == dni:
                    found = True
                    print("Cliente encontrado:")
                    print(f"Nombre: {client['nombre']} | Apellido: {client['apellido']} | DNI: {client['dni']}")
                    input("Presiona Enter para regresar al menú principal")
                    break
            if not found:
                print("Cliente no encontrado.")

        elif opcion == "2":
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
            gotoxy(30, 2); print(blue_color + "Lista de Todos los Clientes")
            print("\n")
            json_file = JsonFile(path + '/archivos/clients.json')
            clients = json_file.read()
            print("Lista de Clientes:")
            for idx, client in enumerate(clients):
                gotoxy(5, 4 + idx);
                print(f"Nombre: {client['nombre']} | Apellido: {client['apellido']} | DNI: {client['dni']}")

            input("Presiona Enter para regresar al menú principal")

        else:
            print("Opción no válida.")

# Proceso de Productos
class CrudProducts(ICrud):
    def create(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1);print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2);print(blue_color + "Registro de Productos")

        # Leer la lista actual de productos del archivo products.json
        with open('archivos/products.json', 'r') as file:
            products = json.load(file)

        # Obtener el ID más alto de la lista actual de productos
        highest_id = max(products, key=lambda x: x['id'])['id'] if products else 0

        # Incrementar el ID más alto en uno para asignar al nuevo producto
        new_product_id = highest_id + 1

        gotoxy(5, 4);print("Descripción: ");description = validar.solo_letras("Ingrese la descripción del producto: ", 13, 4)

        gotoxy(5, 5);print("Precio: ");price = validar.solo_decimales("Ingrese el precio del producto: ", "Error: Solo números decimales")

        gotoxy(5, 6);print("Stock: ");stock = validar.solo_numeros("Ingrese el stock del producto: ", 13, 6)

        new_product = {"id": new_product_id, "descripcion": description, "precio": price, "stock": stock}

        # Agregar el nuevo producto a la lista
        products.append(new_product)

        # Guardar la lista actualizada de productos en el archivo products.json
        with open('archivos/products.json', 'w') as file:
            json.dump(products, file)

        gotoxy(5, 8);print("Producto registrado con éxito")
        input("Presiona Enter para regresar al menú principal")

    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Actualización de Productos")

        # Mostrar las opciones para actualizar
        print("Seleccione una opción:")
        print("1) Ingresar ID del producto a actualizar")
        print("2) Ver todos los productos")

        option = input("Ingrese su opción (1 o 2): ")

        # Obtener la lista de productos
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        if option == "1":
            # Ingresar ID del producto a actualizar
            gotoxy(5, 4)
            print("Ingrese el ID del producto a actualizar: ")
            product_id = validar.solo_numeros("Error: Solo números", 45, 4)

            # Convertir el ID ingresado a entero
            product_id = int(product_id)

            # Buscar el producto por su ID
            found_product = self.buscar_producto_por_id(products, product_id)
            if found_product:
                new_description = input("Ingrese la nueva descripción del producto: ")
                new_description = validar.solo_letras("Error: Solo letras", 45, 6)  # Validación de solo texto
                new_price = validar.solo_decimales("Ingrese el nuevo precio del producto: ",
                                                   "Error: Solo números decimales")
                new_stock = validar.solo_numeros("Ingrese el nuevo stock del producto: ", 45, 8)

                # Actualizar la información del producto
                found_product['descripcion'] = new_description
                found_product['precio'] = new_price
                found_product['stock'] = new_stock

                json_file.save(products)

                gotoxy(5, 10)
                print("Producto actualizado con éxito.")
                input("Presiona Enter para regresar al menú principal")
            else:
                gotoxy(5, 10)
                print("Producto no encontrado.")

        elif option == "2":
            # Mostrar todos los productos con sus IDs
            print("Lista de Productos:")
            for idx, product in enumerate(products):
                gotoxy(5, 4 + idx)
                print(
                    f"ID: {product['id']} | Descripción: {product['descripcion']} | Precio: {product['precio']} | Stock: {product['stock']}")

            # Solicitar el ID del producto a actualizar
            gotoxy(5, len(products) + 5)
            print("Ingrese el ID del producto a actualizar: ")
            product_id = validar.solo_numeros("Error: Solo números", 45, len(products) + 5)

            # Convertir el ID ingresado a entero
            product_id = int(product_id)

            # Buscar el producto por su ID
            found_product = self.buscar_producto_por_id(products, product_id)
            if found_product:
                new_description = input("Ingrese la nueva descripción del producto: ")
                new_description = validar.solo_letras("Error: Solo letras", 45,
                                                      len(products) + 6)  # Validación de solo texto
                new_price = validar.solo_decimales("Ingrese el nuevo precio del producto: ",
                                                   "Error: Solo números decimales")
                new_stock = validar.solo_numeros("Ingrese el nuevo stock del producto: ", 45, len(products) + 8)

                # Actualizar la información del producto
                found_product['descripcion'] = new_description
                found_product['precio'] = new_price
                found_product['stock'] = new_stock

                json_file.save(products)

                gotoxy(5, len(products) + 10)
                print("Producto actualizado con éxito.")
                input("Presiona Enter para regresar al menú principal")
            else:
                gotoxy(5, len(products) + 10)
                print("Producto no encontrado.")

        else:
            gotoxy(5, 10)
            print("Opción no válida.")

    def buscar_producto_por_id(self, products, product_id):
        for product in products:
            if product['id'] == product_id:
                return product
        return None

    def delete(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Eliminación de Producto")

        # Obtener la lista de productos
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        # Mostrar todos los productos con sus IDs
        print("Lista de Productos:")
        for idx, product in enumerate(products):
            gotoxy(5, 4 + idx)
            print(
                f"ID: {product['id']} | Descripción: {product['descripcion']} | Precio: {product['precio']} | Stock: {product['stock']}")

        # Solicitar el ID del producto a eliminar
        gotoxy(5, len(products) + 5)
        print("Ingrese el ID del producto a eliminar: ")
        product_id = validar.solo_numeros("Error: Solo números", 45, len(products) + 5)

        # Convertir el ID ingresado a entero
        product_id = int(product_id)

        # Buscar el producto por su ID
        found_product = self.buscar_producto_por_id(products, product_id)
        if found_product:
            # Confirmar la eliminación del producto
            confirmacion = input("¿Está seguro de que desea eliminar este producto? (s/n): ").lower()
            if confirmacion == "s":
                confirmacion_final = input("Por seguridad, escriba 'ELIMINAR' para confirmar la eliminación: ").lower()
                if confirmacion_final == "eliminar":
                    # Eliminar el producto de la lista
                    products.remove(found_product)
                    # Guardar la lista actualizada en el archivo JSON
                    json_file.save(products)
                    gotoxy(5, len(products) + 8)
                    print("Producto eliminado con éxito.")
                    input("Presiona Enter para regresar al menú principal")
                else:
                    gotoxy(5, len(products) + 8)
                    print("Eliminación cancelada.")
            else:
                gotoxy(5, len(products) + 8)
                print("Eliminación cancelada.")
        else:
            gotoxy(5, len(products) + 8)
            print("Producto no encontrado.")
            input("\nPresione Enter para regresar al menú principal...")

    def consult(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Consulta de Productos")

        # Mostrar las opciones para consultar
        print("Seleccione una opción:")
        print("1) Mostrar todos los productos")
        print("2) Buscar un producto por ID")

        option = input("Ingrese su opción (1 o 2): ")

        # Obtener la lista de productos
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        if option == "1":
            # Mostrar todos los productos con sus IDs
            print("Lista de Productos:")
            for idx, product in enumerate(products):
                gotoxy(5, 4 + idx)
                print(
                    f"ID: {product['id']} | Descripción: {product['descripcion']} | Precio: {product['precio']} | Stock: {product['stock']}")

        elif option == "2":
            # Ingresar ID del producto a buscar
            gotoxy(5, 4)
            print("Ingrese el ID del producto a buscar: ")
            product_id = validar.solo_numeros("Error: Solo números", 40, 4)

            # Buscar el producto por su ID
            found = False
            for product in products:
                if product['id'] == product_id:
                    found = True
                    gotoxy(5, 6)
                    print(
                        f"ID: {product['id']} | Descripción: {product['descripcion']} | Precio: {product['precio']} | Stock: {product['stock']}")
                    break

            if not found:
                gotoxy(5, 6)
                print("Producto no encontrado.")

        else:
            gotoxy(5, 6)
            print("Opción no válida.")

        input("\nPresione Enter para regresar al menú principal...")

# Clase de registro de ventas
class CrudSales(ICrud):
    def create(self):
        # Cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1);
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2);
        print(blue_color + "Registro de Venta")
        gotoxy(17, 3);
        print(blue_color + Company.get_business_name())
        gotoxy(5, 4);
        print(f"Factura#:F0999999 {' ' * 3} Fecha:{datetime.datetime.now()}")
        gotoxy(66, 4);
        print("Subtotal:")
        gotoxy(66, 5);
        print("Descuento:")
        gotoxy(66, 6);
        print("IVA     :")
        gotoxy(66, 7);
        print("Total   :")
        gotoxy(15, 6);
        print("Cedula:")
        dni = validar.solo_numeros("Error: Solo números", 23, 6)

        # Validar existencia de cliente
        json_file = JsonFile(path + '/archivos/clients.json')
        client = json_file.find("dni", dni)
        if not client:
            gotoxy(35, 6);
            print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"], client["apellido"], client["dni"], card=True)
        sale = Sale(cli)
        gotoxy(35, 6);
        print(cli.fullName())
        gotoxy(2, 8);
        print(green_color + "*" * 90 + reset_color)
        gotoxy(5, 9);
        print(purple_color + "Línea")
        gotoxy(12, 9);
        print("Id_Articulo")
        gotoxy(24, 9);
        print("Descripción")
        gotoxy(38, 9);
        print("Precio")
        gotoxy(48, 9);
        print("Cantidad")
        gotoxy(58, 9);
        print("Subtotal")
        gotoxy(70, 9);
        print("n->Terminar Venta)" + reset_color)

        # Detalle de la venta
        follow = "s"
        line = 1
        while follow.lower() == "s":
            gotoxy(7, 9 + line);
            print(line)
            gotoxy(15, 9 + line);
            id = int(validar.solo_numeros("Error: Solo números", 15, 9 + line))
            json_file = JsonFile(path + '/archivos/products.json')
            prods = json_file.find("id", id)
            if not prods:
                gotoxy(24, 9 + line);
                print("Producto no existe")
                time.sleep(1)
                gotoxy(24, 9 + line);
                print(" " * 20)
            else:
                prods = prods[0]
                product = Product(prods["id"], prods["descripcion"], prods["precio"], prods["stock"])
                gotoxy(24, 9 + line);
                print(product.descrip)
                gotoxy(38, 9 + line);
                print(product.preci)

                # Solicitar cantidad del producto
                qyt = int(validar.solo_numeros("Error: Solo números", 49, 9 + line))

                # Validar cantidad disponible
                if int(product.stock) < qyt:
                    gotoxy(49, 9 + line)
                    print("Cantidad insuficiente")
                    time.sleep(1)
                    gotoxy(49, 9 + line)
                    print(" " * 20)
                    continue

                gotoxy(24, 9 + line);
                print(product.descrip)
                gotoxy(38, 9 + line);
                print(product.preci)
                gotoxy(49, 9 + line);
                print(qyt)
                gotoxy(59, 9 + line);
                print(product.preci * qyt)
                sale.add_detail(product, qyt)
                gotoxy(76, 4);
                print(round(sale.subtotal, 2))
                gotoxy(76, 5);
                print(round(sale.discount, 2))
                gotoxy(76, 6);
                print(round(sale.iva, 2))
                gotoxy(76, 7);
                print(round(sale.total, 2))
                gotoxy(74, 9 + line);
                follow = input() or "s"
                gotoxy(76, 9 + line);
                print(green_color + "✔" + reset_color)
                line += 1

        # Confirmar la venta
        gotoxy(15, 9 + line);
        print(red_color + "¿Está seguro de grabar la venta (s/n)?:")
        gotoxy(54, 9 + line);
        procesar = input().lower()
        if procesar == "s":
            gotoxy(15, 10 + line);
            print("😊 Venta grabada satisfactoriamente 😊" + reset_color)
            # print(sale.getJson())
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"] + 1 if invoices else 1
            data = sale.getJson()
            data["factura"] = ult_invoices
            invoices.append(data)
            json_file = JsonFile(path + '/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20, 10 + line);
            print("🤣 Venta cancelada 🤣" + reset_color)

        time.sleep(2)

    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Actualización de Venta")

        gotoxy(5, 4)
        invoice_number = Valida.validar_numeros("Ingrese el número de factura que desea actualizar: ", 2, 6, 53, 6)
        invoice_number = int(invoice_number)

        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()

        if invoices:
            found = False
            for invoice in invoices:
                if invoice["factura"] == invoice_number:
                    found = True
                    while True:
                        os.system('cls' if os.name == 'nt' else 'clear')  # Borra la pantalla

                        # Imprime el encabezado y la información de la factura
                        gotoxy(2, 1)
                        print(green_color + "=" * 90 + reset_color)
                        gotoxy(30, 2)
                        print(blue_color + "Actualización de Venta")
                        gotoxy(2, 3)
                        print(green_color + "=" * 90 + reset_color)
                        gotoxy(2, 4)
                        print(blue_color + "Empresa: " + purple_color + "Corporación el Rosado")
                        gotoxy(60, 4)
                        print(blue_color + "RUC:" + purple_color + "1790097870001")
                        gotoxy(2, 5)
                        gotoxy(2, 7)
                        print(green_color + "=" * 90 + reset_color)
                        gotoxy(2, 8)
                        print(blue_color + "Número de Factura: " + purple_color + f"{invoice['factura']}")
                        print(blue_color + "Fecha:" + purple_color + f"{invoice['Fecha']}")
                        print(blue_color + "Cliente:" + purple_color + f"{invoice['cliente']}")
                        print(blue_color + "Total:" + purple_color + f"{invoice['total']}")
                        gotoxy(2, 12)
                        print("\nDetalle de la Venta:")
                        detalles = invoice['detalle']
                        print(f"{blue_color +'num'.center(5)} {blue_color + 'Producto'.center(28)} {blue_color + 'Cantidad'.center(15)} {blue_color + 'Precio'.center(13)}")
                        for i, detalle in enumerate(detalles, start=1):
                            print(purple_color + f" {i}) {detalle['poducto'].center(28)} {str(detalle['cantidad']).center(10)} x {str(detalle['precio']).center(10)}")
                        print(green_color + "=" * 90 + reset_color)
                        gotoxy(2, 20), print(blue_color + "\nOpciones:")
                        print("1. Modificar cantidad de un producto")
                        print("2. Eliminar un producto")
                        print("3. Agregar un nuevo producto")
                        print("4. Terminar actualización")
                        option = Valida.validar_numeros("Seleccione una opción: ", 2, 26, 25, 26)

                        if option == "1":
                            # Modificar cantidad de un producto en la factura
                            detalle_index = int(validar.validar_numeros("Ingrese el número de línea del detalle que desea modificar: ", 2, 27, 62, 27)) - 1
                            if 0 <= detalle_index < len(detalles):
                                new_quantity = int(validar.validar_numeros("Ingrese la nueva cantidad: ", 2, 28, 29, 28))
                                detalles[detalle_index]['cantidad'] = new_quantity
                                # Recalcular el total de la factura
                                invoice['total'] = sum(item['cantidad'] * item['precio'] for item in detalles)
                                print(green_color + "=" * 90 + reset_color)
                                gotoxy(4, 30)
                                print(blue_color + "Cantidad modificada correctamente.")
                                gotoxy(4, 31)
                                input("Presione Enter para continuar...")
                            else:
                                print("Número de línea inválido.")
                                input("Presione Enter para continuar...")
                        elif option == "2":
                            # Eliminar un producto de la factura
                            detalle_index = int(Valida.validar_numeros("Ingrese el número de línea del detalle que desea eliminar: ",2, 27,62,27)) - 1
                            if 0 <= detalle_index < len(detalles):
                                del detalles[detalle_index]
                                # Recalcular el total de la factura
                                invoice['total'] = sum(item['cantidad'] * item['precio'] for item in detalles)
                                print(green_color + "=" * 90 + reset_color)
                                gotoxy(3, 29)
                                print(blue_color + "Producto eliminado correctamente.")
                                gotoxy(4, 30)
                                input("Presione Enter para continuar...")
                            else:
                                print("Número de línea inválido.")
                                input("Presione Enter para continuar...")
                        elif option == "3":
                            # Agregar un nuevo producto a la factura
                            product_id = int(Valida.validar_numeros("Ingrese el ID del nuevo producto: ", 2, 27, 35, 27))
                            product_quantity = int(Valida.validar_numeros("Ingrese la cantidad del nuevo producto: ", 2, 28, 42, 28))
                            product_details = self.find_product_details(product_id)
                            if product_details:
                                new_product = {
                                    'poducto': product_details['descripcion'],
                                    'precio': product_details['precio'],
                                    'cantidad': product_quantity
                                }
                                detalles.append(new_product)
                                # Recalcular el total de la factura
                                invoice['total'] = sum(item['cantidad'] * item['precio'] for item in detalles)
                                print("Producto agregado correctamente.")
                                input("Presione Enter para continuar...")
                            else:
                                print("Producto no encontrado.")
                                input("Presione Enter para continuar...")
                        elif option == "4":
                            print("Actualización de factura terminada.")
                            # Guardar los cambios en el archivo JSON
                            invoice['detalle'] = detalles
                            for index, inv in enumerate(invoices):
                                if inv["factura"] == invoice_number:
                                    invoices[index] = invoice
                                    break
                            json_file.save(invoices)
                            break
                        else:
                            print("Opción inválida. Intente nuevamente.")
                            input("Presione Enter para continuar...")
                    break

            if not found:
                print("Factura no encontrada.")
                input("Presione Enter para regresar al menú principal")
        else:
            print("No hay facturas disponibles.")
            input("Presione Enter para regresar al menú principal")

    def find_product_details(self, product_id):
        # Cargar los datos de productos desde el archivo JSON
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()
        # Buscar el producto por su ID
        for product in products:
            if product.get("id") == product_id:
                return product  # Devolver detalles del producto encontrado
        return None  # Devolver None si el producto no se encuentra

    def delete(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Eliminación de Venta")

        gotoxy(5, 4)
        invoice_number = Valida.validar_numeros("Ingrese el número de factura que desea eliminar: ", 2, 6, 53, 6)
        invoice_number = int(invoice_number)

        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()

        if invoices:
            found = False
            for index, invoice in enumerate(invoices):
                if invoice["factura"] == invoice_number:
                    found = True
                    confirmation = input("¿Está seguro de que desea eliminar esta factura? (s/n): ").lower()
                    if confirmation == "s":
                        confirmacion_final = input(
                            "Por seguridad, escriba 'ELIMINAR' para confirmar la eliminación: ").lower()
                        if confirmacion_final == "eliminar":
                            # Eliminar la factura de la lista
                            del invoices[index]
                            # Guardar la lista actualizada en el archivo JSON
                            json_file.save(invoices)
                            gotoxy(5, 8)
                            print("Factura eliminada con éxito.")
                        else:
                            gotoxy(5, 8)
                            print("Eliminación cancelada.")
                    else:
                        gotoxy(5, 8)
                        print("Eliminación cancelada.")
                    input("Presiona Enter para regresar al menú principal")
                    break
            if not found:
                gotoxy(5, 8)
                print("Factura no encontrada.")
                input("\nPresione Enter para regresar al menú principal...")
        else:
            print("No hay facturas disponibles.")
            input("Presione Enter para regresar al menú principal")

    # Consulta de ventas
    def consult(self):
        print('\033c', end ='')
        gotoxy(2,1);print(green_color + "█" *90)
        gotoxy(2,2);print("██"+" "* 34 + "Consulta de Venta" + " " * 35 + "██")
        gotoxy(2,4);invoice= input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")

            suma = reduce(lambda total, invoice: round(total + invoice["total"],2),
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x=input("presione una tecla para continuar...")

# Menu Proceso Principal
opc=''
while opc != '4':
    borrarPantalla()
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    # Menu de clientes
    if opc == "1":
        opc1 = ''
        while opc1 != '5':
            borrarPantalla()
            client = CrudClients()
            menu_clients = Menu("Menu Clientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                client.create()
            elif opc1 == "2":
                client.update()
            elif opc1 == "3":
                client.delete()
            elif opc1 == "4":
                client.consult()
                time.sleep(2)
            print("Regresando al menu Clientes...")
            # time.sleep(2)
    # Menu de Productos
    elif opc == "2":
        opc2 = ''
        while opc2 != '5':
            borrarPantalla()
            Products = CrudProducts()
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                Products.create()
            elif opc2 == "2":
                Products.update()
            elif opc2 == "3":
                Products.delete()
            elif opc2 == "4":
                Products.consult()
                time.sleep(2)
            print("Regresando al menu Productos...")
            time.sleep(2)
    # Menu de Ventas
    elif opc == "3":
        opc3 = ''
        while opc3 != '5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.update()
            elif opc3 == "3":
                sales.delete()
            elif opc3 == "4":
                sales.consult()
            print("Regresando al menu Ventas...")
            time.sleep(2)
print("Gracias por su visita...")

