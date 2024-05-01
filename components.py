# components.py

from utilities import gotoxy, mensaje
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
import time
import math

class Menu:
    def __init__(self, titulo = "", opciones = [], col = 6, fil = 1):
        self.titulo = titulo
        self.opciones = opciones
        self.col = col
        self.fil = fil

    def menu(self):
        gotoxy(self.col, self.fil)
        print(self.titulo)
        for opcion in self.opciones:
            self.fil += 1
            gotoxy(self.col, self.fil)
            print(opcion)
        gotoxy(self.col + 5, self.fil + 2)
        opc = input(f"Elija una opción [1...{len(self.opciones)}]: ")
        return opc


class Valida:
    def solo_numeros(self, mensajeError, col, fil):
        while True:
            gotoxy(col, fil)
            valor = input("        ------>   | {} ".format("Ingrese solo números: "))
            try:
                if int(valor) > 0:
                    break
            except ValueError:
                gotoxy(col, fil)
                print(mensajeError)
                time.sleep(1)
                gotoxy(col, fil)
                print(" " * 20)
        return valor

    # Proceso recursivo
    def solo_numeros_recursivo(self, mensajeError, col, fil):
        valor = input("        ------>   | {} ".format("Ingrese solo números: "))
        try:
            if int(valor) > 0:
                return valor
        except ValueError:
            print(mensajeError)
            return self.solo_numeros_recursivo(mensajeError, col, fil)

    def solo_letras(self, mensajeError, col, fil):
        while True:
            gotoxy(col, fil)
            valor = input("         ------>   | {} ".format("Ingrese solo letra: "))
            if valor.isalpha():
                break
            else:
                gotoxy(col, fil)
                print(mensajeError)
                time.sleep(1)
                gotoxy(col, fil)
                print(" " * 20)
        return valor

    def solo_decimales(self, mensaje, mensajeError):
        while True:
            valor = input("          ------>   | {} ".format(mensaje))
            try:
                valor = float(valor)
                if valor > float(0):
                    break
            except ValueError:
                print("          ------><  | {} ".format(mensajeError))
        return valor

    def cedula(self, mensajeError, col, fil):
        while True:
            gotoxy(col, fil)
            cedula = input("        ------>   | {} ".format("Ingrese cédula: "))
            if Valida.validar_cedula(cedula):
                break
            else:
                gotoxy(col, fil)
                print(mensajeError)
                time.sleep(1)
                gotoxy(col, fil)
                print(" " * 20)
        return cedula

    def validar_numeros(frase, col1, fil1, col2, fil2):
        while True:
            gotoxy(col1, fil1)
            print(blue_color + f"{frase}")
            gotoxy(col2, fil2)
            numero = input(purple_color)
            if numero.isdigit():
                return numero
            else:
                gotoxy(col2, fil2)
                print(purple_color + "El campo solo puede contener números.")
                time.sleep(1)
                gotoxy(col2, fil2)
                print(" " * 40)

    @staticmethod
    def validar_cedula(cedula):
        if len(cedula) != 10:
            return False
        else:
            multiplicador = [2, 1, 2, 1, 2, 1, 2, 1, 2]
            ced_array = list(map(lambda k: int(k), list(cedula)))[0:9]
            ultimo_digito = int(cedula[9])
            resultado = []
            arr = map(lambda x, j: (x, j), ced_array, multiplicador)
            for (i, j) in arr:
                if i * j < 10:
                    resultado.append(i * j)
                else:
                    resultado.append((i * j)-9)
            if ultimo_digito == int(math.ceil(float(sum(resultado)) / 10) * 10) - sum(resultado):
                return True
            else:
                return False


if __name__ == '__main__':
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    opcion_elegida = menu.mostrar_menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if opcion_elegida == "1":
        numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
        print("Número validado:", numero_validado)
    elif opcion_elegida == "2":
        letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
        print("Letra validada:", letra_validada)
    elif opcion_elegida == "3":
        decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
        print("Decimal validado:", decimal_validado)
