import sqlite3




class Database:
    def __init__(self,nombre_db):
        self.nombre_db=nombre_db if nombre_db else "MovimentosYCtaCte.db"
        self.connexion=sqlite3.connect(self.nombre_db) 

    def crear_tabla(self,nombre_table,columnas=""):
     TABLE_CREACIÓN_QUERY=f"""CREATE TABLE {nombre_table} ({columnas});""" 
     cursor=self.connexion.cursor()
     cursor.execute(TABLE_CREACIÓN_QUERY)
     self.connexion.commit()

    def insertar_datos(self,nombre_table,columnas=[],valores=[]):
       cursor=self.connexion.cursor();

       if len (valores)>0 and len(columnas)==0:  
        INSERT_QUERY=f"""INSERT INTO {nombre_table} VALUES ({1})"""
        cursor.execute(INSERT_QUERY.format(",".join(valores)))
        self.connexion.commit()

       if len(valores)==len(columnas):
          INSERT_QUERY=f"""INSERT INTO {nombre_table} ({0}) VALUES ({1})"""
          cursor.execute(INSERT_QUERY.format(",".join(columnas),",".join(valores)))
          self.connexion.commit()
       else:
          raise ValueError("NO SE PUEDE INSERTAR LOS DATOS EN EL DATABASE")  
       
    def buscar_datos(self,nombre_table,columnas=[],condicion=""):
        cursor=self.connexion.cursor()
        datos=[]
        if len(columnas)==0:
           SELECT_QUERY=f"""SELECT * FROM {nombre_table} WHERE {condicion};"""
           datos=cursor.execute(SELECT_QUERY).fetchall()
        else:
           SELECT_QUERY=f"""SELECT {0} FROM {nombre_table} WHERE {1};"""
           datos=cursor.execute(SELECT_QUERY.format(",".join(columnas),condicion)).fetchall()
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
          ACTUALIZAR_QUERY=f"""UPDATE {nombre_table} SET {0} WHERE {1};"""
          cursor.execute(ACTUALIZAR_QUERY.format(
             (f"{0}={1}".format(col,val) for col,val in zip(columnas,valores)),condicion))
          self.connexion.commit()
       else:
          raise ValueError("NO SE PUEDE ACTUALIZAR LOS DATOS EN EL DATABASE")  

    def cerrar_conexion(self):
       self.connexion.close()

