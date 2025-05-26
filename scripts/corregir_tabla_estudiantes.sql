-- Script para corregir la estructura de la tabla estudiantes
-- Primero verificamos si la tabla existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'estudiantes') THEN
        -- Crear la tabla estudiantes si no existe
        CREATE TABLE estudiantes (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            documento TEXT NOT NULL UNIQUE,
            tipo_documento TEXT DEFAULT 'CC',
            nombre TEXT,
            apellido TEXT,
            codigo TEXT,
            email TEXT,
            telefono TEXT,
            programa_id UUID,
            semestre INTEGER,
            estrato INTEGER,
            riesgo_desercion TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        RAISE NOTICE 'Tabla estudiantes creada correctamente';
    ELSE
        -- Verificar si la columna apellido existe
        IF NOT EXISTS (SELECT FROM information_schema.columns 
                      WHERE table_schema = 'public' 
                      AND table_name = 'estudiantes' 
                      AND column_name = 'apellido') THEN
            -- Agregar la columna apellido
            ALTER TABLE estudiantes ADD COLUMN apellido TEXT;
            RAISE NOTICE 'Columna apellido agregada a la tabla estudiantes';
        ELSE
            RAISE NOTICE 'La columna apellido ya existe en la tabla estudiantes';
        END IF;
    END IF;
END
$$;

-- Verificar otras columnas necesarias
DO $$
BEGIN
    -- Verificar columna nombre
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'estudiantes' 
                  AND column_name = 'nombre') THEN
        ALTER TABLE estudiantes ADD COLUMN nombre TEXT;
        RAISE NOTICE 'Columna nombre agregada a la tabla estudiantes';
    END IF;
    
    -- Verificar columna codigo
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'estudiantes' 
                  AND column_name = 'codigo') THEN
        ALTER TABLE estudiantes ADD COLUMN codigo TEXT;
        RAISE NOTICE 'Columna codigo agregada a la tabla estudiantes';
    END IF;
    
    -- Verificar columna email
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'estudiantes' 
                  AND column_name = 'email') THEN
        ALTER TABLE estudiantes ADD COLUMN email TEXT;
        RAISE NOTICE 'Columna email agregada a la tabla estudiantes';
    END IF;
    
    -- Verificar columna telefono
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'estudiantes' 
                  AND column_name = 'telefono') THEN
        ALTER TABLE estudiantes ADD COLUMN telefono TEXT;
        RAISE NOTICE 'Columna telefono agregada a la tabla estudiantes';
    END IF;
    
    -- Verificar columna programa_id
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'estudiantes' 
                  AND column_name = 'programa_id') THEN
        ALTER TABLE estudiantes ADD COLUMN programa_id UUID;
        RAISE NOTICE 'Columna programa_id agregada a la tabla estudiantes';
    END IF;
    
    -- Verificar columna semestre
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'estudiantes' 
                  AND column_name = 'semestre') THEN
        ALTER TABLE estudiantes ADD COLUMN semestre INTEGER;
        RAISE NOTICE 'Columna semestre agregada a la tabla estudiantes';
    END IF;
    
    -- Verificar columna estrato
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'estudiantes' 
                  AND column_name = 'estrato') THEN
        ALTER TABLE estudiantes ADD COLUMN estrato INTEGER;
        RAISE NOTICE 'Columna estrato agregada a la tabla estudiantes';
    END IF;
    
    -- Verificar columna riesgo_desercion
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'estudiantes' 
                  AND column_name = 'riesgo_desercion') THEN
        ALTER TABLE estudiantes ADD COLUMN riesgo_desercion TEXT;
        RAISE NOTICE 'Columna riesgo_desercion agregada a la tabla estudiantes';
    END IF;
END
$$;

-- Verificar si hay datos en la tabla
SELECT COUNT(*) AS total_estudiantes FROM estudiantes;
