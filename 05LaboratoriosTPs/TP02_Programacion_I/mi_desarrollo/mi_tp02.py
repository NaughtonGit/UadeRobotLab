# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  .....................................
#  Comision:           .....................................
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    
    if not isinstance(comando, tuple) or len(comando) == 0:
        return False

    nombre = comando[0]

    if nombre == "detenerse" or nombre == "saludar":
        return len(comando) == 1

    if nombre == "avanzar" or nombre == "girar":
        if len(comando) != 3:
            return False

        velocidad = comando[1]
        tiempo = comando[2]

        if type(velocidad) not in (int, float):
            return False

        if type(tiempo) not in (int, float):
            return False

        if tiempo < 0:
            return False

        return True

    return False
    pass


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    if not comando_es_valido(comando):
        return "Comando invalido"

    nombre = comando[0]

    try:
        if nombre == "avanzar":
            velocidad = comando[1]
            tiempo = comando[2]
            robot.avanzar(velocidad=velocidad, tiempo=tiempo)

        elif nombre == "girar":
            velocidad = comando[1]
            tiempo = comando[2]
            robot.girar(velocidad=velocidad, tiempo=tiempo)

        elif nombre == "detenerse":
            robot.detenerse()

        elif nombre == "saludar":
            robot.saludar()

        return "Comando ejecutado correctamente"

    except ErrorDeSeguridad as error:
        return "Error de seguridad: " + str(error)
    pass


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    for comando in mision:

        if not comando_es_valido(comando):
            historial.append("Comando invalido: " + str(comando))
            continue

        resultado = ejecutar_comando(robot, comando)
        historial.append(str(comando) + " -> " + resultado)
    pass


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    ejecutados = 0
    rechazados = 0
    motivos_rechazo = []

    for resultado in historial:

        if "Comando ejecutado correctamente" in resultado:
            ejecutados += 1

        else:
            rechazados += 1
            motivos_rechazo.append(resultado)

    print("\n--- REPORTE DE LA MISION ---")
    print("Comandos ejecutados correctamente:", ejecutados)
    print("Comandos rechazados:", rechazados)

    if rechazados > 0:
        print("\nMotivos de rechazo:")

        for motivo in motivos_rechazo:
            print("-", motivo)
    pass


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_LARGA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()