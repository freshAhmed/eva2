import sqlite3

class Database:
    def __init__(self,nombre_db):
        self.nombre_db=nombre_db if nombre_db else "MovimentosYCtaCte.db"
        self.connexion=sqlite3.connect(self.nombre_db,detect_types=sqlite3.PARSE_DECLTYPES|
                                                                    sqlite3.PARSE_COLNAMES)

    def crear_tabla(self,nombre_tabla,columnas=[],tipo_columnas=[]
                        ,unicos_columnas=[],foreign_keys=[],referencias=[]):    
     cursor=self.connexion.cursor()
  
     columnas_formateadas=[]
     if len(columnas) == len(tipo_columnas):
      for col, tipo in zip(columnas,tipo_columnas):
           if col in unicos_columnas:
            if tipo.upper() =="BIT":
             columnas_formateadas.append(f"""{col} INTEGER NOT NULL CHECK 
                                           ({col} IN (0, 1)) PRIMARY KEY""")
            else:    
             columnas_formateadas.append(f"{col} {tipo} PRIMARY KEY")
           else:
            if tipo.upper() =="BIT":
               columnas_formateadas.append(f"""{col} INTEGER NOT NULL CHECK
                                             ({col} IN (0, 1))""") 
            else:   
             columnas_formateadas.append(f"{col} {tipo} ")  
      for col in columnas:
       if col in foreign_keys:
         columna_index=foreign_keys.index(col)  
         columnas_formateadas.append(f"""FOREIGN KEY ({col})
                                        REFERENCES {referencias[columna_index]}""")    
      s=" , ".join(columnas_formateadas)      
      consulta_creacion_tabla=f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({s});" 
      try:
       cursor.execute(f"DROP TABLE IF EXISTS {nombre_tabla}") 
       cursor.execute(consulta_creacion_tabla)
      except sqlite3.OperationalError as e:
         print (f"error in execute {e}")
      self.connexion.commit()
     else:
        raise ValueError("""No SE PUEDE CREAR LA TABLE {nombre_table} 
                            EN DATABASE {self.nombre_db} PORQUE EL NUMERO DE COLUMNAS
                            NO COINCIDE CON EL NUMERO 
                            DE TIPOS PRESENTADOS """) 
     
    

    def insertar_datos(self,nombre_tabla,columnas=[],valores=[]):
       cursor=self.connexion.cursor();
       valores=list(map(str,valores))
       espacio_str=",".join(["?"]*len(valores))
       if len (valores)>0 and len(columnas)==0:  
        consulta_agregar=f"""INSERT INTO {nombre_tabla} VALUES ({espacio_str})"""
        cursor.execute(consulta_agregar,valores)
        self.connexion.commit()
       elif len(valores)==len(columnas):
          consulta_agregar=f"""INSERT INTO {nombre_tabla} ({",".join(columnas)}) 
          VALUES ({espacio_str})"""
          cursor.execute(consulta_agregar,valores)
          self.connexion.commit()
       else:
          raise ValueError("NO SE PUEDE INSERTAR LOS DATOS EN EL DATABASE")  
       
    def buscar_datos(self,nombre_tabla,columnas=[],condicion=""):
        cursor=self.connexion.cursor()
        datos=[]
        consulta_buscar=f"""
              SELECT * FROM {nombre_tabla}
              WHERE {condicion}
               """if len(condicion)>0 else f"""SELECT * FROM {nombre_tabla}"""

        if len(columnas)>0:
           consulta_buscar=f"""SELECT {",".join(columnas)}
                               FROM {nombre_tabla}
                               WHERE {condicion} """ if len(condicion)>0 else f"""
                               SELECT {",".join(columnas)} FROM {nombre_tabla}"""
        datos=cursor.execute(consulta_buscar).fetchall()
        return datos 

    def eliminar_datos(self,nombre_tabla,condicion=""):
        cursor=self.connexion.cursor()
        consulta_eliminacion=f"""
                              DELETE FROM {nombre_tabla}
                              WHERE {condicion}"""
        cursor.execute(consulta_eliminacion)
        self.connexion.commit()      
   

    def actualizar_datos(self,nombre_tabla,columnas=[],
                         valores=[],condicion=""):
       cursor=self.connexion.cursor()
       if len(valores)==len(columnas):
          consulta_actualizacion=f"""
          UPDATE {nombre_tabla} SET
          {", ".join(f"{col}={val}" for col, val in zip(columnas, valores))}
          WHERE {condicion};"""
          cursor.execute(consulta_actualizacion)
          self.connexion.commit() 
       else:
          raise ValueError("NO SE PUEDE ACTUALIZAR LOS DATOS EN EL DATABASE")  

    def cerrar_conexion(self):
       self.connexion.close()

    def get_columnas(self,nombra_tabla):
       cursor=self.connexion.cursor()
       cursor.execute(f"SELECT * FROM {nombra_tabla}") #add something
       return cursor.description