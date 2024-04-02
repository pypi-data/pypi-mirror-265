class   TRAMAS:
    """
    Dicha Librería implementa diferentes funciones que permiten calcular el checksum
    de una trama y crear una nueva trama, que posteriormente se podra enviar
    """
    def __init__(self) -> None:
        pass
    def calcular_checksum(trama):
        """
        Esta función toma una trama en hexadecimal como entrada y calcula 
        el checksum para esa trama. Devuelve el valor de checksum
        """
        # Convierto trama en hexadecimal a trama en bytes para sumarla
        trama_byte = bytes.fromhex(trama)
        # Suma todos los valores ASCII de los caracteres en la trama convertida
        check = sum(trama_byte)
        # Devuelve el checksum módulo 256, comprobando que si check > 256 , el cheksum es 256 menos la diferencia que hay entre ambos
        if check >= 256:
            checksum = 256 - (abs(256-check))
        else:
            checksum = abs(256-check)
        return checksum # valor absoluto por si checksum es mayor que 256
        
    def crear_trama(direccion_destino, numero_bits, direccion_origen, comando, datos):
        """
        Esta funcion construye una trama de acuerdo con la estructura proporcionada.Tiene 5 argumentos
        Hay que tener en cuenta que los datos que se introducen deben estar en formate hexadecimal 0XAB.
        También a la hora de introducir datos, estso deben estar en forma de lista datos=[0x00,0x00,..]
        Finalmente, se devuelve la trama creada.
        """
         # Construye la trama según la estructura proporcionada
        trama = " ".join([f"{direccion_destino:02X}", f"{numero_bits:02X}", f"{direccion_origen:02X}", f"{comando:02X}"]) 
        # Agregar cada elemento de la lista datos a la trama en formato hexadecimal
        trama +=" " + " ".join([f"{dato:02X}" for dato in datos]) + " "
        # Calcula el checksum de la trama
        checksum = calcular_checksum(trama)
        # Agrega el checksum a la trama
        trama += f"{checksum:02X}\n"  # Asegura que el checksum esté representado por dos caracteres hexadecimales
        return trama