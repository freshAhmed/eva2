from db import Database
import csv


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
        pass
    def cargar (self,monto):
       pass       
    def exportar_registros(self,nombre_tabla):
       datos=self.db.buscar_datos(nombre_tabla)
       nombres_columnas=[descripción[0] for descripción in self.db.get_columnas("CtaCte")]
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
  foreign_keys=["numeroCtaCte"]
  referencias=["Movimientos(numeroCtaCte)"]
  db.crear_tabla(nombre_tabla,columnas,tipo_columnas,unicos_columnas,foreign_keys,referencias)



#crear la tabla Movimientos
  nombre_tabla="Movimientos"
  columnas=["CtaCte_numeroCtaCte","idMovimientos","tipoMovimiento","monto"]
  tipo_columnas=["DOUBLE","DOUBLE","BIT","DOUBLE"]
  unicos_columnas=["idMovimientos"]    
  db.crear_tabla(nombre_tabla,columnas,tipo_columnas,unicos_columnas)
  db.insertar_datos("CtaCte",[],[12341232,"12360322-2","johan",12312.2])

 except ValueError as e :
   print(e)
 CtaCte=Cuenta_Corriente(db,22341232,"12360322-2","johan",12312.2)  
 CtaCte.exportar_registros("CtaCte")
 datos=db.buscar_datos("CtaCte") # buscar todas los datos
 print(datos) 