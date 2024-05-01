import os.path as path
import json
import datetime
import time
import os
from functools import reduce
from components import Menu, Valida
from utilities import borrarPantalla, gotoxy, reset_color, red_color, green_color, yellow_color, blue_color, purple_color, cyan_color
from clsJson import JsonFile
from company import Company
from customer import RegularClient
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
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Registro de Clientes")

        gotoxy(5, 4)
        print("Nombre: ")
        name = validar.solo_letras("Error: Solo letras", 13, 4)
        gotoxy(5, 5)
        print("Apellido: ")
        lastname = validar.solo_letras("Error: Solo letras", 13, 5)
        gotoxy(5, 6)
        print("DNI: ")
        dni = validar.solo_numeros("Error: Solo números", 13, 6)

        gotoxy(5, 7)
        print("Tipo de cliente:")
        gotoxy(5, 8)
        print("1) Cliente Regular")
        gotoxy(5, 9)
        print("2) Cliente VIP")
        gotoxy(5, 10)
        tipo_cliente = validar.solo_numeros("Error: Solo números", 27, 7)
        while tipo_cliente not in {"1", "2"}:
            gotoxy(5, 11)
            print("Opción inválida. Intente de nuevo.")
            tipo_cliente = validar.solo_numeros("Error: Solo números", 27, 7)

        cliente_tipo = "Regular" if tipo_cliente == "1" else "VIP"

        if tipo_cliente == "1":
            gotoxy(5, 12)
            print("¿El cliente tiene tarjeta de descuento? (s/n): ")
            card = input().lower() == "s"
            cliente = RegularClient(name, lastname, dni, card)
        else:
            cliente = VipClient(name, lastname, dni)

        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()
        clients.append(cliente.getJson())
        json_file.save(clients)

        gotoxy(5, 14)
        print("Cliente registrado exitosamente!")
        input("Presiona Enter para regresar al menú principal")

    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end = '')
        gotoxy(2,1);print(green_color + "*" * 90 + reset_color)
        gotoxy(30,2);print(blue_color + "Actualización de Clientes")

        gotoxy(5,4);print("Ingrese el DNI del cliente a actualizar: ")
        dni = validar.solo_numeros("Error: Solo números", 40, 4)

        json_file = JsonFile(path + '/archivos/clients.json')
        client_list = json_file.read()
        found = False

        for client in client_list:
            if client['dni'] == dni:
                found = True
                gotoxy(5,5);print("Nombre: ")
                new_name = validar.solo_letras("Error: Solo letras", 13, 5)

                gotoxy(5,6);print("Apellido: ")
                new_lastname = validar.solo_letras("Error: Solo letras", 13, 6)

                client['nombre'] = new_name
                client['apellido'] = new_lastname
                json_file.save(client_list)
                gotoxy(5,8);print("Cliente actualizado con éxito")
                input("Presiona Enter para regresar al menú principal")
                break
        if not found:
            print("Cliente no encontrado.")

    def delete(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2);print(blue_color + "Eliminación de Clientes")

        gotoxy(5, 4);print("Ingrese el DNI del cliente a eliminar: ")
        dni = validar.solo_numeros("Error: Solo números", 40, 4)

        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()
        found = False

        for client in clients:
            if client['dni'] == dni:
                found = True
                gotoxy(5, 6);print("¿Está seguro de eliminar este cliente? (S/N): ")
                confirmacion = input().lower()
                if confirmacion == "s":
                    gotoxy(5, 7);print("Por seguridad, escriba 'ELIMINAR' para confirmar la eliminación: ")
                    confirmacion_final = input().lower()

                    if confirmacion_final == "eliminar":
                        del clients[clients.index(client)]
                        json_file.save(clients)
                        gotoxy(5, 9);print("Cliente eliminado con éxito")
                        input("Presiona Enter para regresar al menú principal")
                    else:
                        gotoxy(5, 9);print("Confirmación incorrecta. No se ha eliminado el cliente.")
                else:
                    gotoxy(5, 9);print("Operación cancelada.")
                break
        if not found:
            print("Cliente no encontrado.")

    def consult(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1);
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2);
        print(blue_color + "Consulta de Clientes")
        print("\n")
        print("Seleccione una opción:")
        print("1) Buscar cliente por DNI")
        print("2) Ver todos los clientes")

        opcion = input("Ingrese su opción (1 o 2): ")

        if opcion == "1":
            validar = Valida()
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2, 1);
            print(green_color + "*" * 90 + reset_color)
            gotoxy(30, 2);
            print(blue_color + "Consulta de Cliente por DNI")
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
            gotoxy(2, 1);
            print(green_color + "*" * 90 + reset_color)
            gotoxy(30, 2);
            print(blue_color + "Lista de Todos los Clientes")
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
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end = '')
        gotoxy(2,1);print(green_color + "*" * 90 + reset_color)
        gotoxy(30,2);print(blue_color + "Registro de Venta")
        gotoxy(17,3);print(blue_color + Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' ' * 3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni = validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path + '/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card = True)
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color + "*" * 90 + reset_color)
        gotoxy(5,9);print(purple_color + "Linea")
        gotoxy(12,9);print("Id_Articulo")
        gotoxy(24,9);print("Descripcion")
        gotoxy(38,9);print("Precio")
        gotoxy(48,9);print("Cantidad")
        gotoxy(58,9);print("Subtotal")
        gotoxy(70,9);print("n-> Terminar Venta)" + reset_color)
        # detalle de la venta
        follow = "s"
        line = 1
        while follow.lower() == "s":
            gotoxy(7,9 + line);print(line)
            gotoxy(15,9 + line);
            id = int(validar.solo_numeros("Error: Solo numeros",15,9 + line))
            json_file = JsonFile(path + '/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9 + line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9 + line);print(" "*20)
            else:
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9 + line);print(product.descrip)
                gotoxy(38,9 + line);print(product.preci)
                gotoxy(49,9 + line);qyt = int(validar.solo_numeros("Error:Solo numeros",49,9 + line))
                gotoxy(59,9 + line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9 + line);follow =  input() or "s"
                gotoxy(76,9 + line);print(green_color + "✔" + reset_color)
                line += 1
        gotoxy(15,9 + line);print(red_color + "Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9 + line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10 + line);print("😊 Venta Grabada satisfactoriamente 😊" + reset_color)
            # print(sale.getJson())
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"] + 1
            data = sale.getJson()
            data["factura"] = ult_invoices
            invoices.append(data)
            json_file = JsonFile(path + '/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣" +reset_color)
        time.sleep(2)

    def update(self):
        pass

    def delete(self):
        pass

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
                pass
            elif opc3 == "3":
                pass
            elif opc3 == "4":
                sales.consult()
            print("Regresando al menu Ventas...")
            time.sleep(2)
print("Gracias por su visita...")

