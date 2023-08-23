def eliminar_por_valor(lista, clave, valor):
    # Usamos un bucle para recorrer la lista de diccionarios
    # y buscamos la fila que contenga el valor deseado en la clave especificada.
    # Luego, eliminamos la fila de la lista si se encuentra una coincidencia.

    # Creamos una lista para almacenar los índices de las filas que coinciden con el valor.
    indices_a_eliminar = []

    for i, diccionario in enumerate(lista):
        if clave in diccionario and diccionario[clave] == valor:
            # Agregamos el índice de la fila a la lista de índices a eliminar.
            indices_a_eliminar.append(i)

    # Eliminamos las filas con los índices almacenados en la lista indices_a_eliminar.
    for index in sorted(indices_a_eliminar, reverse=True):
        lista.pop(index)