import sqlite3

conn = sqlite3.connect('MovimentosYCtaCte.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS CtaCte (
    numeroCtaCte REAL PRIMARY KEY,
    rutTitularCta TEXT,
    nomTitularCta TEXT,
    saldoCta REAL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Movimientos (
    CtaCte_numeroCtaCte REAL,
    idMovimientos REAL PRIMARY KEY,
    tipoMovimiento INTEGER,
    monto REAL,
    FOREIGN KEY (CtaCte_numeroCtaCte) REFERENCES CtaCte(numeroCtaCte)
)''')
conn.commit()

class Cuenta_Corriente:
    """
    Clase que representa una cuenta corriente.
    """
    def __init__(self, numeroCtaCte, rutTitularCta, nomTitularCta, saldoCta):
        """
        Inicializa una nueva instancia de la clase Cuenta_Corriente.
        """
        self.numeroCtaCte = numeroCtaCte
        self.rutTitularCta = rutTitularCta
        self.nomTitularCta = nomTitularCta
        self.saldoCta = saldoCta
        self.guardar_en_db()

    def guardar_en_db(self):
        """
        Guarda la cuenta corriente en la base de datos.
        """
        cursor.execute('''INSERT INTO CtaCte (numeroCtaCte, rutTitularCta, nomTitularCta, saldoCta)
                          VALUES (?, ?, ?, ?)''',
                       (self.numeroCtaCte, self.rutTitularCta, self.nomTitularCta, self.saldoCta))
        conn.commit()