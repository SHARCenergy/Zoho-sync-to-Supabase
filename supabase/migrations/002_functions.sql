-- Function to create schema if not exists
CREATE OR REPLACE FUNCTION create_schema_if_not_exists(schema_name TEXT)
RETURNS VOID AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = $1) THEN
        EXECUTE 'CREATE SCHEMA ' || quote_ident($1);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to upsert record in any schema.table
CREATE OR REPLACE FUNCTION upsert_record(
    p_schema TEXT,
    p_table TEXT,
    p_data JSONB,
    p_unique_field TEXT DEFAULT 'id'
)
RETURNS JSONB AS $$
DECLARE
    sql_query TEXT;
    result JSONB;
    columns_list TEXT;
    values_list TEXT;
    update_list TEXT;
BEGIN
    -- Build dynamic SQL for upsert
    SELECT 
        string_agg(quote_ident(key), ','),
        string_agg('$1->>' || quote_literal(key), ','),
        string_agg(quote_ident(key) || ' = EXCLUDED.' || quote_ident(key), ',')
    INTO columns_list, values_list, update_list
    FROM jsonb_object_keys(p_data);
    
    sql_query := format(
        'INSERT INTO %I.%I (%s) VALUES (%s) 
         ON CONFLICT (%I) DO UPDATE SET %s, updated_at = NOW()
         RETURNING to_jsonb(%I.*)',
        p_schema, p_table, columns_list, values_list, p_unique_field, update_list, p_table
    );
    
    EXECUTE sql_query INTO result USING p_data;
    RETURN result;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in upsert_record: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to get records from any schema.table
CREATE OR REPLACE FUNCTION get_records(
    p_schema TEXT,
    p_table TEXT,
    p_filters JSONB DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    sql_query TEXT;
    where_clause TEXT := '';
    result JSONB;
BEGIN
    -- Build WHERE clause from filters
    IF p_filters IS NOT NULL THEN
        SELECT string_agg(quote_ident(key) || ' = ' || quote_literal(value::text), ' AND ')
        INTO where_clause
        FROM jsonb_each(p_filters);
        
        where_clause := ' WHERE ' || where_clause;
    END IF;
    
    -- Build dynamic SQL
    sql_query := format(
        'SELECT to_jsonb(array_agg(%I.*)) FROM %I.%I%s',
        p_table, p_schema, p_table, where_clause
    );
    
    EXECUTE sql_query INTO result;
    RETURN COALESCE(result, '[]'::jsonb);
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in get_records: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to delete record from any schema.table
CREATE OR REPLACE FUNCTION delete_record(
    p_schema TEXT,
    p_table TEXT,
    p_record_id TEXT
)
RETURNS BOOLEAN AS $$
DECLARE
    sql_query TEXT;
    affected_rows INTEGER;
BEGIN
    sql_query := format(
        'DELETE FROM %I.%I WHERE id = %L',
        p_schema, p_table, p_record_id
    );
    
    EXECUTE sql_query;
    GET DIAGNOSTICS affected_rows = ROW_COUNT;
    RETURN affected_rows > 0;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in delete_record: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to get sync status
CREATE OR REPLACE FUNCTION get_sync_status(
    p_schema TEXT,
    p_table TEXT
)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    SELECT to_jsonb(s.*) INTO result
    FROM sync_status s
    WHERE s.schema_name = p_schema AND s.table_name = p_table;
    
    RETURN result;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in get_sync_status: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to update sync status
CREATE OR REPLACE FUNCTION update_sync_status(
    p_schema TEXT,
    p_table TEXT,
    p_last_sync TEXT,
    p_status TEXT
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO sync_status (schema_name, table_name, last_sync, status, updated_at)
    VALUES (p_schema, p_table, p_last_sync::timestamp with time zone, p_status, NOW())
    ON CONFLICT (schema_name, table_name)
    DO UPDATE SET 
        last_sync = EXCLUDED.last_sync,
        status = EXCLUDED.status,
        updated_at = NOW();
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in update_sync_status: %', SQLERRM;
END;
$$ LANGUAGE plpgsql; 