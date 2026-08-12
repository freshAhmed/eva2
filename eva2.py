from db import Database
import csv
import random
class Cuenta_Corriente:
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
        self.saldoCta = saldoCta
        self.db.insertar_datos("CtaCte",["numeroCtaCte","rutTitularCta","nomTitularCta","saldoCta"],[self.numeroCtaCte,self.rutTitularCta,self.nomTitularCta,self.saldoCta])
    def abonar (self,monto):
        """
        Abona un monto a la cuenta corriente.
        """
        if monto <= 0:
            print("El monto a abondar debe ser mayor que cero.")
            return
        self.saldoCta += monto
        idMovimiento=random.randint(1000000,9999999)
        self.db.actualizar_datos("CtaCte",["saldoCta"],[self.saldoCta],f"numeroCtaCte={self.numeroCtaCte}")
        self.db.insertar_datos("Movimientos",["CtaCte_numeroCtaCte","idMovimientos","tipoMovimiento","monto"],[self.numeroCtaCte,idMovimiento,0,monto])
    def cargar (self,monto):
       """
       Carga un monto a la cuenta corriente.
       """
       saldoCta=self.saldoCta
       numeroCtaCte=self.numeroCtaCte
       idMovimiento=random.randint(100000,999999)
       if monto <= 0:
           print("El monto a cargar debe ser mayor que cero.")
           return
       if self.saldoCta < monto:
           print("Saldo insuficiente para realizar la carga.")
           return
       self.saldoCta -= monto
       #print(self.db.buscar_datos("Movimientos",[],f"CtaCte_numeroCtaCte={self.numeroCtaCte}")[-1][1]+1 if self.db.buscar_datos("Movimientos",[],f"CtaCte_numeroCtaCte={self.numeroCtaCte}") else 1)
       self.db.actualizar_datos("CtaCte",["saldoCta"],[saldoCta],f"numeroCtaCte={numeroCtaCte}")
       self.db.insertar_datos("Movimientos",["CtaCte_numeroCtaCte","idMovimientos","tipoMovimiento","monto"],
                [numeroCtaCte,idMovimiento,1,monto])    
    def exportar_registros(self,nombre_tabla):
       """
       Exporta los registros de la tabla especificada a un archivo CSV.
       """
       datos=self.db.buscar_datos(nombre_tabla)
       nombres_columnas=[descripción[0] for descripción in self.db.get_columnas(nombre_tabla)]
       with open(f"{nombre_tabla}.csv","w",newline="",encoding="utf-8") as archivo:
         escritor=csv.writer(archivo)
         escritor.writerow(nombres_columnas)
         escritor.writerows(datos)
       print("CVS archivo creado correctamente") 

if "__main__" == __name__:
 try:
#iniciar la base de datos
  db=Database("MovimentosYCtaCte.db")
#crear la tabla CtaCte
  nombre_tabla="CtaCte"
  columnas=["numeroCtaCte","rutTitularCta","nomTitularCta","saldoCta"]
  tipo_columnas=["DOUBLE","VARCHAR(12)","VARCHAR(105)","DOUBLE"]
  unicos_columnas=["numeroCtaCte"]
  db.crear_tabla(nombre_tabla,columnas,tipo_columnas,unicos_columnas)
  db.insertar_datos("CtaCte",["numeroCtaCte","rutTitularCta","nomTitularCta","saldoCta"],[12341232,"12360322-2","johan",12312.2])

#crear la tabla Movimientos
  nombre_tabla="Movimientos"
  columnas=["CtaCte_numeroCtaCte","idMovimientos","tipoMovimiento","monto"]
  tipo_columnas=["DOUBLE","DOUBLE","BIT","DOUBLE"]
  unicos_columnas=["idMovimientos"]    
  foreign_keys=["CtaCte_numeroCtaCte"]
  referencias=["CtaCte(numeroCtaCte)"]
  db.crear_tabla(nombre_tabla,columnas,tipo_columnas,unicos_columnas,foreign_keys,referencias)
  db.insertar_datos("Movimientos",["CtaCte_numeroCtaCte","idMovimientos","tipoMovimiento","monto"],[12341232,321231,0,1000.0])
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

