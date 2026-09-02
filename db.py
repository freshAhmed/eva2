import sqlite3

class Database:
    def __init__(self,nombre_db):
        self.nombre_db=nombre_db if nombre_db else "MovimentosYCtaCte.db"
        self.connexion=sqlite3.connect(self.nombre_db) 

    def crear_tabla(self,
                    nombre_tabla,columnas=[],
                    tipo_columnas=[],
                    unicos_columnas=[],
                    foreign_keys=[],
                    referencias=[]):
     cursor=self.connexion.cursor()
  
     COLUMNAS_FORMATEADAS=[]
     if len(columnas) == len(tipo_columnas):
      for col, tipo in zip(columnas,tipo_columnas):
           if col in unicos_columnas:
            if tipo.upper() =="BIT":
             COLUMNAS_FORMATEADAS.append(f"""{col} INTEGER NOT NULL CHECK 
                                           ({col} IN (0, 1)) PRIMARY KEY""")
            else:    
             COLUMNAS_FORMATEADAS.append(f"{col} {tipo} PRIMARY KEY")
           else:
            if tipo.upper() =="BIT":
               COLUMNAS_FORMATEADAS.append(f"""{col} INTEGER NOT NULL CHECK
                                             ({col} IN (0, 1))""") 
            else:   
             COLUMNAS_FORMATEADAS.append(f"{col} {tipo} ")  
      for col in columnas:
       if col in foreign_keys:
         columna_index=foreign_keys.index(col)  
         COLUMNAS_FORMATEADAS.append(f"""FOREIGN KEY ({col})
                                        REFERENCES {referencias[columna_index]}""")    
      s=" , ".join(COLUMNAS_FORMATEADAS)      
      TABLE_CREACIÓN_QUERY=f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({s});" 
      try:
       cursor.execute(f"DROP TABLE IF EXISTS {nombre_tabla}") 
       cursor.execute(TABLE_CREACIÓN_QUERY)
      except sqlite3.OperationalError as e:
         print (f"error in execute {e}")
      self.connexion.commit()
     else:
        raise ValueError("""No SE PUEDE CREAR LA TABLE {nombre_table} 
                            EN DATABASE {self.nombre_db} PORQUE EL NUMERO DE COLUMNAS
                            NO COINCIDE CON EL NUMERO 
                            DE TIPOS PRESENTADOS """) 
     
    

    def insertar_datos(self,
                       nombre_tabla,
                       columnas=[],
                       valores=[]):
       cursor=self.connexion.cursor();
       valores=list(map(str,valores))
       ESPACIO_STR=",".join(["?"]*len(valores))
       if len (valores)>0 and len(columnas)==0:  
        CONSULTA_AGREGAR=f"""INSERT INTO {nombre_tabla} VALUES ({ESPACIO_STR})"""
        cursor.execute(CONSULTA_AGREGAR,valores)
        self.connexion.commit()
       elif len(valores)==len(columnas):
          CONSULTA_AGREGAR=f"""INSERT INTO {nombre_tabla} ({",".join(columnas)}) 
          VALUES ({ESPACIO_STR})"""
          cursor.execute(CONSULTA_AGREGAR,valores)
          self.connexion.commit()
       else:
          raise ValueError("NO SE PUEDE INSERTAR LOS DATOS EN EL DATABASE")  
       
    def buscar_datos(self,nombre_tabla,columnas=[],condicion=""):
        cursor=self.connexion.cursor()
        datos=[]
        CONSULTA_BUSCAR=f"""SELECT * FROM {nombre_tabla}
                            WHERE {condicion}
                            """if len(condicion)>0 else f"""SELECT * FROM {nombre_tabla}"""

        if len(columnas)>0:
           CONSULTA_BUSCAR=f"""SELECT {",".join(columnas)}
                               FROM {nombre_tabla}
                               WHERE {condicion} """ if len(condicion)>0 else f"""
                               SELECT {",".join(columnas)} FROM {nombre_tabla}"""
       
        datos=cursor.execute(CONSULTA_BUSCAR).fetchall()
        return datos 

    def eliminar_datos(self,
                       nombre_tabla,
                       condicion=""):
        cursor=self.connexion.cursor()
        CONSULTA_ELIMINACION=f"""
                              DELETE FROM {nombre_tabla}
                              WHERE {condicion}"""
        cursor.execute(CONSULTA_ELIMINACION)

        self.connexion.commit()      
   

    def actualizar_datos(self,
                         nombre_tabla,
                         columnas=[],
                         valores=[],
                         condicion=""):
       cursor=self.connexion.cursor()
       if len(valores)==len(columnas):
          CONSULTA_ACTUALIZACION=f"""
          UPDATE {nombre_tabla} SET
          {", ".join(f"{col}={val}" for col, val in zip(columnas, valores))}
          WHERE {condicion};"""
          cursor.execute(CONSULTA_ACTUALIZACION)
          self.connexion.commit() 
       else:
          raise ValueError("NO SE PUEDE ACTUALIZAR LOS DATOS EN EL DATABASE")  

    def cerrar_conexion(self):
       self.connexion.close()

    def get_columnas(self,nombra_tabla):
       cursor=self.connexion.cursor()
       cursor.execute(f"SELECT * FROM {nombra_tabla}") #add something
       return cursor.description