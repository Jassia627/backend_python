import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Conectar a la base de datos
    conn = psycopg2.connect(
        host=os.getenv('SUPABASE_HOST', 'aws-0-us-west-1.pooler.supabase.com'),
        database=os.getenv('SUPABASE_DB', 'postgres'),
        user=os.getenv('SUPABASE_USER', 'postgres.rfkkpjyglkyosjdolwyx'),
        password=os.getenv('SUPABASE_PASSWORD'),
        port=os.getenv('SUPABASE_PORT', '6543')
    )

    cursor = conn.cursor()

    # Verificar si la columna existe
    cursor.execute("""
    SELECT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'estudiantes' 
        AND column_name = 'riesgo_desercion'
    );
    """)

    exists = cursor.fetchone()[0]
    print(f'Columna riesgo_desercion existe: {exists}')

    if not exists:
        print('Agregando columna riesgo_desercion...')
        cursor.execute('ALTER TABLE estudiantes ADD COLUMN riesgo_desercion TEXT;')
        conn.commit()
        print('Columna agregada exitosamente')
    else:
        print('La columna ya existe')

    conn.close()
    print('✅ Script ejecutado correctamente')

except Exception as e:
    print(f'❌ Error: {str(e)}') 