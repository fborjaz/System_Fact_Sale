# components.py

from utilities import gotoxy
import time

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

    def cedula(self):
        pass


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
