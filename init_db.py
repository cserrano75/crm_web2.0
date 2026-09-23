import sqlite3
import hashlib

def inicializar_base_datos():
    # Conecta (o crea) el archivo de base de datos local
    conexion = sqlite3.connect("app.db")
    cursor = conexion.cursor()

    # 1. Crear la tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Crear un usuario administrador por defecto (Semilla / Seed)
    # Credenciales iniciales de ejemplo: admin@gestion.com / Admin123*
    email_admin = "admin@gestion.com"
    # Nota: En producción usa librerías como bcrypt; aquí usamos un hash seguro de ejemplo
    password_plana = "Admin123*"
    password_hash = hashlib.sha256(password_plana.encode()).hexdigest()
    rol_admin = "Administrador"

    try:
        cursor.execute("""
            INSERT INTO usuarios (email, password_hash, rol)
            VALUES (?, ?, ?)
        """, (email_admin, password_hash, rol_admin))
        conexion.commit()
        print("¡Base de datos creada con éxito!")
        print(f"Usuario Administrador creado por defecto: {email_admin} / Contraseña: {password_plana}")
    except sqlite3.IntegrityError:
        print("La base de datos ya estaba inicializada y el admin ya existe.")

    conexion.close()

if __name__ == "__main__":
    inicializar_base_datos()