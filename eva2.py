from db import Database
import csv
import random
import decimal 

class Cuenta_Corriente:
    NOMBRE_TABLA_CTACTE="CtaCte"
    COLUMNAS_CTACTE=["numeroCtaCte","rutTitularCta","nomTitularCta","saldoCta"]
    TIPO_COLUMNAS_CTACTE=["DOUBLE","VARCHAR(12)","VARCHAR(105)","DOUBLE"]
    UNICOS_COLUMNAS_CTACTE=["numeroCtaCte"]
    NOMBRE_TABLA_MOVIMIENTOS="Movimientos"
    COLUMNAS_MOVIMIENTOS=["CtaCte_numeroCtaCte","idMovimientos","tipoMovimiento","monto"]
    TIPO_COLUMNAS_MOVIMIENTOS=["DOUBLE","DOUBLE","BIT","DOUBLE"]
    UNICOS_COLUMNAS_MOVIMIENTOS=["idMovimientos"]    
    LLAVE_PRIMARIA=["CtaCte_numeroCtaCte"]
    REFERENCIAS=["CtaCte(numeroCtaCte)"]    
    """
    Clase que representa una cuenta corriente.
    """
    def __init__(self, db, numeroCtaCte, rutTitularCta, nomTitularCta, saldoCta):
        """
        Inicializa una nueva instancia de la clase Cuenta_Corriente.
        """
        self.db=db if db else Database("MovimentosYCtaCte.db")
        self.numeroCtaCte = numeroCtaCte
        self.rutTitularCta = rutTitularCta
        self.nomTitularCta = nomTitularCta
        self.saldoCta = decimal.Decimal(saldoCta)

        # Crear las tablas si no existe
        db.crear_tabla(self.NOMBRE_TABLA_CTACTE,self.COLUMNAS_CTACTE,self.TIPO_COLUMNAS_CTACTE,self.UNICOS_COLUMNAS_CTACTE) 

        # crear la tabla Movimientos si no existe
        db.crear_tabla(self.NOMBRE_TABLA_MOVIMIENTOS,self.COLUMNAS_MOVIMIENTOS,self.TIPO_COLUMNAS_MOVIMIENTOS,
                       self.UNICOS_COLUMNAS_MOVIMIENTOS,self.LLAVE_PRIMARIA,self.REFERENCIAS) 

        # Insertar los datos de la cuenta corriente en la tabla CtaCte
        self.db.insertar_datos("CtaCte",["numeroCtaCte","rutTitularCta","nomTitularCta","saldoCta"],
                                        [self.numeroCtaCte,self.rutTitularCta,self.nomTitularCta,self.saldoCta])
        
    def abonar (self,monto):

        """
        Abona un monto a la cuenta corriente.
        """
        monto=decimal.Decimal(monto) # convertir el monto a decimal 

        if monto <= 0:
            print("El monto a abondar debe ser mayor que cero.")
            return

        self.saldoCta += monto
        idMovimiento   = decimal.Decimal(random.randint(1000000,9999999)) # generar un ID de movimiento aleatorio

        # actualizar el saldo de la cuenta corriente en la tabla CtaCte
        self.db.actualizar_datos("CtaCte",["saldoCta"],[self.saldoCta],f"numeroCtaCte={self.numeroCtaCte}") 

        # insertar un registro en la tabla Movimientos para reflejar el abono
        self.db.insertar_datos("Movimientos",["CtaCte_numeroCtaCte","idMovimientos","tipoMovimiento","monto"]
                                            ,[self.numeroCtaCte,idMovimiento,0,monto])

    def cargar (self,monto):

       """
       Carga un monto a la cuenta corriente.
       """

       monto=decimal.Decimal(monto)

       saldoCta=self.saldoCta
       numeroCtaCte=self.numeroCtaCte
       idMovimiento=decimal.Decimal(random.randint(1000000,9999999))

       if monto <= 0:
           print("El monto a cargar debe ser mayor que cero.")
           return

       if self.saldoCta < monto:
           print("Saldo insuficiente para realizar la carga.")
           return

       self.saldoCta -= monto
       self.db.actualizar_datos("CtaCte",["saldoCta"],[self.saldoCta],f"numeroCtaCte={numeroCtaCte}")
       self.db.insertar_datos("Movimientos",["CtaCte_numeroCtaCte","idMovimientos","tipoMovimiento","monto"]
                                           ,[numeroCtaCte,idMovimiento,1,monto])    

    def exportar_registros(self,nombre_tabla):

       """
       Exportar los registros de la tabla especificada a un archivo CSV.
       """

       # Obtener los datos de la tabla
       datos=self.db.buscar_datos(nombre_tabla)     
       # Obtener los nombres de las columnas de la tabla 
       nombres_columnas=[descripción[0] for descripción in self.db.get_columnas(nombre_tabla)]

       # Exportar los datos a un archivo CSV
       with open(f"{nombre_tabla}.csv","w",newline="",encoding="utf-8") as archivo:
         escritor=csv.writer(archivo)
         escritor.writerow(nombres_columnas)
         escritor.writerows(datos)

       print("CVS archivo creado correctamente") 

if "__main__" == __name__:
 try:
#iniciar la base de datos
  db=Database("MovimentosYCtaCte.db")
  CtaCte = Cuenta_Corriente(db, 22341232, "12360322-2", "johan", 12312.2)
  CtaCte.abonar(5000)
  CtaCte.cargar(2000)
  CtaCte.exportar_registros("CtaCte")
  CtaCte.exportar_registros("Movimientos")
  
  # Mostrar en consola para verificar los datos
  print("CtaCte:", db.buscar_datos("CtaCte"))
  print("Movimientos:", db.buscar_datos("Movimientos"))
  

 except ValueError as e:
        print(e)

