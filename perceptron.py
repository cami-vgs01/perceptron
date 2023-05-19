from tkinter import filedialog
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random

dataframe = pd.DataFrame()
def lecturaArchivo():
    global dataframe
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv")])
    # Leer el archivo CSV seleccionado
    try:
        dataframe.drop(index=dataframe.index, columns=dataframe.columns, inplace=True)
        datos = pd.read_csv(archivo_csv, index_col=None)
        dataframe = pd.concat([dataframe, datos], ignore_index=True)
        print("Datos ingresados correctamente")
        return dataframe
    except FileNotFoundError:
        print("No se eligió el archivo")

def calcular_suma(suma,primerasfilas, numcolumnas, numeroTeta, i,numero_aleatorio):
    for j in range(numcolumnas):
        suma += primerasfilas.iloc[i,j] * numero_aleatorio[j]
    suma += numeroTeta
    print("Fila: ", primerasfilas.iloc[i].values)
    print("Suma: ", suma)
    if suma >= 0:
        y = 1
    else:
        y = -1
    return y

def ajustar_pesos(primerasfilas, numero_aleatorio, numeroTeta,i):
    for k in range(len(numero_aleatorio)):
        numero_aleatorio[k] += primerasfilas.iloc[i,-1]*primerasfilas.iloc[i,k]
    numeroTeta += primerasfilas.iloc[i,-1]
    return numero_aleatorio, numeroTeta

def perceptron(numero_aleatorio,numeroTeta,pasadas):
    primerasfilas = dataframe.head(10)
    num_filas, num_columnas = dataframe.shape
    nombresColumnas = list(dataframe.columns)
    nombre_ultima_columna = dataframe.columns[-1]  # obtiene el nombre de la ultima columna
    palette = sns.color_palette("bright", len(primerasfilas[nombre_ultima_columna].unique()))
    color_dict = dict(zip(primerasfilas[nombre_ultima_columna].unique(), palette))
    if num_columnas-1 <3:
        dibujar2D(nombresColumnas,primerasfilas,color_dict,nombre_ultima_columna)
    elif num_columnas-1 == 3:
        dibujar3D(nombresColumnas,primerasfilas,nombre_ultima_columna)
    # Generar un número aleatorio entre 0 y 1 la librería random
    """for _ in range(num_columnas -1):
        numero_aleatorio.append(random.random())
    numeroTeta = random.random()"""
    numero_aleatorio = [0,0.4,0.9,0.2,1,1,0.1,0.3,0]
    numeroTeta = 0.8
    while pasadas > 0:
        print("Pasada: ", pasadas)
        for i in range(primerasfilas.shape[0]):
            suma = 0
            y = calcular_suma(suma,primerasfilas, num_columnas-1, numeroTeta,i,numero_aleatorio)
            print("Y: ", y)
            if y != primerasfilas.iloc[i,-1]:
                numero_aleatorio, numeroTeta = ajustar_pesos(primerasfilas, numero_aleatorio, numeroTeta,i)
                print("Pesos:", numero_aleatorio)
                # Verificar si la fila actual coincide después del ajuste
                suma_despues_ajuste = calcular_suma(suma,primerasfilas, num_columnas-1, numeroTeta,i,numero_aleatorio)
                print("Y despues del ajuste: ", suma_despues_ajuste)
                if suma_despues_ajuste >= 0:
                    y_despues_ajuste = 1
                else:
                    y_despues_ajuste = -1

                if y_despues_ajuste != primerasfilas.iloc[i,-1]:
                    i-=1

        pasadas = pasadas - 1

    print("Pesos finales: ", numero_aleatorio)
    print("Teta final: ", numeroTeta)
    return numero_aleatorio, numeroTeta

def predecir(numero_aleatorio, numeroTeta):
    resto_filas = dataframe.iloc[10:]
    num_filas, num_columnas = dataframe.shape
    predicciones = []  # Lista para almacenar los resultados de las predicciones

    for i in range(resto_filas.shape[0]):
        suma = 0
        y = calcular_suma(suma, resto_filas, num_columnas-1, numeroTeta, i, numero_aleatorio)

        # Agregar el resultado de la predicción a la lista de predicciones
        predicciones.append(y)

    dfModificado = resto_filas.copy()
    # Agregar la lista de predicciones como una nueva columna al DataFrame
    dfModificado['Prediccion'] = predicciones

    # Imprimir el DataFrame con las predicciones
    print(dfModificado)


def dibujar2D(nombres_columnas,sub_df,color_dict,nombre_ultima_columna):
    sns.scatterplot(x=nombres_columnas[0], y=nombres_columnas[1], hue=nombre_ultima_columna, data=sub_df, palette=color_dict)
    plt.scatter(sub_df.iloc[:,0], sub_df.iloc[:,1], c=sub_df[nombre_ultima_columna].apply(lambda x: color_dict[x]), marker='s')
    plt.xlabel(nombres_columnas[0])
    plt.ylabel(nombres_columnas[1])
    plt.show()

def dibujar3D(nombres_columnas, df, nombre_ultima_columna):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    clases = df[nombre_ultima_columna].unique()
    color_dict = {clase: np.random.rand(3,) for clase in clases} # generamos un diccionario con un color aleatorio por cada clase
    for clase, color in color_dict.items():
        temp_df = df[df[nombre_ultima_columna] == clase]
        ax.scatter(temp_df[nombres_columnas[0]], temp_df[nombres_columnas[1]], temp_df[nombres_columnas[2]], color=color, marker='s', label=str(clase))
    ax.set_xlabel(nombres_columnas[0])
    ax.set_ylabel(nombres_columnas[1])
    ax.set_zlabel(nombres_columnas[2])
    plt.legend()
    plt.show()
def menu():
    numero_aleatorio = []
    numeroTeta = 0
    while True:
        print("1. Cargar archivo")
        print("2. Visualizar datos")
        print("3. Entrenar modelo")
        print("4. Predecir")
        print("5. Salir")
        try:
            opcion = int(input("Ingrese la opcion: "))
            if opcion == 1:
                try:
                    dataframe.drop(index=dataframe.index, columns=dataframe.columns, inplace=True)
                    # Crear la ventana principal
                    root = tk.Tk()
                    # Agregar un botón para abrir el cuadro de diálogo de selección de archivos
                    boton_abrir = tk.Button(root, text="Abrir archivo CSV", command=lecturaArchivo)
                    boton_abrir.pack()
                    # Mostrar la ventana principal
                    root.mainloop()
                except:
                    print("No se eligió el archivo")
            elif opcion == 2:
                print(dataframe)
            elif opcion == 3:
                print("Ingrese en número de pasadas del modelo")
                try:
                    pasadas = int(input())
                    numero_aleatorio, numeroTeta=perceptron(numero_aleatorio,numeroTeta, pasadas)
                except ValueError:
                    print("Ingrese un valor númerico")
            elif opcion == 4:
                predecir(numero_aleatorio,numeroTeta)
            elif opcion == 5:
                break
        except ValueError:
            print("Opcion invalida")


menu()