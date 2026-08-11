import sqlite3




class Database:
    def __init__(self,nombre_db):
        self.nombre_db=nombre_db if nombre_db else "MovimentosYCtaCte.db"
        self.connexion=sqlite3.connect(self.nombre_db) 

    def crear_tabla(self,nombre_tabla,columnas=[],tipo_columnas=[],unicos_columnas=[],foreign_keys=[],referencias=[]):
     cursor=self.connexion.cursor()
  
     columnasformateadas=[]
     if len(columnas) == len(tipo_columnas):
      for col, tipo in zip(columnas,tipo_columnas):
           if col in unicos_columnas:
            if tipo.upper() =="BIT":
             columnasformateadas.append(f"{col} INTEGER NOT NULL CHECK ({col} IN (0, 1)) PRIMARY KEY")
            else:    
             columnasformateadas.append(f"{col} {tipo} PRIMARY KEY")
           else:
            if tipo.upper() =="BIT":
               columnasformateadas.append(f"{col} INTEGER NOT NULL CHECK ({col} IN (0, 1))") 
            else:   
             columnasformateadas.append(f"{col} {tipo} ")  
      for col in columnas:
            if col in foreign_keys:
                                  columna_index=foreign_keys.index(col)
                                  columnasformateadas.append(f"FOREIGN KEY ({col}) REFERENCES {referencias[columna_index]}")    
      s=" , ".join(columnasformateadas)      
   
      TABLE_CREACIÓN_QUERY=f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({s});" 

      try:
       cursor.execute(f"DROP TABLE IF EXISTS {nombre_tabla}") 
       cursor.execute(TABLE_CREACIÓN_QUERY)
      except sqlite3.OperationalError as e:
         print (f"error in execute {e}")
      self.connexion.commit()
     else:
        raise ValueError("No SE PUEDE CREAR LA TABLE {nombre_table} EN DATABASE {self.nombre_db} PORQUE EL NUMERO DE COLUMNAS NO COINCIDE CON EL NUMERO DE TIPOS PRESENTADOS ") 
     
    

    def insertar_datos(self,nombre_tabla,columnas=[],valores=[]):
       cursor=self.connexion.cursor();
       valores=list(map(str,valores))
       espaciostr=",".join(["?"]*len(valores))
       if len (valores)>0 and len(columnas)==0:  
       
        INSERT_QUERY=f"""INSERT INTO {nombre_tabla} VALUES ({espaciostr})"""
        cursor.execute(INSERT_QUERY,valores)
        self.connexion.commit()

       elif len(valores)==len(columnas):
          
          INSERT_QUERY=f"""INSERT INTO {nombre_tabla} ({",".join(columnas)}) VALUES ({espaciostr})"""
          cursor.execute(INSERT_QUERY,valores)
          self.connexion.commit()
       else:
          raise ValueError("NO SE PUEDE INSERTAR LOS DATOS EN EL DATABASE")  
       
    def buscar_datos(self,nombre_table,columnas=[],condicion=""):
        cursor=self.connexion.cursor()
        datos=[]
        SELECT_QUERY=f"""SELECT * FROM {nombre_table} WHERE {condicion}""" if len(condicion)>0 else f"""SELECT * FROM {nombre_table}"""
        if len(columnas)>0:
           SELECT_QUERY=f"""SELECT {",".join(columnas)} FROM {nombre_table} WHERE {condicion}""" if len(condicion)>0 else f"""SELECT {",".join(columnas)} FROM {nombre_table}"""
       
        datos=cursor.execute(SELECT_QUERY).fetchall()
        return datos 

    def eliminar_datos(self,nombre_table,condicion=""):
        cursor=self.connexion.cursor()
        ELIMINAR_QUERY=f"""
                       DELETE FROM {nombre_table} WHERE {condicion}"""
        cursor.execute(ELIMINAR_QUERY)

        self.connexion.commit()      
   

    def actualizar_datos(self,nombre_table,columnas=[],valores=[],condicion=""):
       cursor=self.connexion.cursor()
       if len(valores)==len(columnas):
          ACTUALIZAR_QUERY=f"""UPDATE {nombre_table} SET {(f"{col}={val}" for col,val in zip(columnas,valores))} WHERE {condicion};"""
          cursor.execute(ACTUALIZAR_QUERY)
          self.connexion.commit()
       else:
          raise ValueError("NO SE PUEDE ACTUALIZAR LOS DATOS EN EL DATABASE")  

    def cerrar_conexion(self):
       self.connexion.close()

