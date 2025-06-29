create procedure job_passenger(load_type text DEFAULT 'full'::text)
    language plpgsql
as
$$
DECLARE
    v_proc_name       CONSTANT TEXT := 'JOB_PASSENGER';
    V_TABLE          CONSTANT TEXT := 'ft_passenger';
    V_TABLE_1           CONSTANT TEXT := 'str_passenger';
    V_TABLE_2          CONSTANT TEXT := 'tr_passenger';
    v_schema          CONSTANT TEXT := 'public';

    v_migration_time  TIMESTAMP;
BEGIN
    IF load_type = 'full' THEN
        v_migration_time := '1900-01-01 00:00:00';
    ELSIF load_type = 'delta' THEN
        EXECUTE
            'SELECT COALESCE(MAX(insert_date), ''1900-01-01 00:00:00'') FROM '
            || v_schema || '.' || V_TABLE_2
        INTO v_migration_time;
    ELSE
        RAISE EXCEPTION 'Invalid load_type: %, can only be “full” or “delta”', load_type;
    END IF;

    INSERT INTO public.etl_procedure_log (procedure_name, step_name, source_table, target_table)
    VALUES (v_proc_name, 'STARTED PROCEDURE', V_TABLE, V_TABLE_1);

    PERFORM public.fn_truncate_table(v_schema, V_TABLE_1);

EXECUTE
    'INSERT INTO ' || v_schema || '.' || V_TABLE_1 || ' (
        passenger_id,
        full_name,
        birth_date,
        nationality,
        frequent_flyer,
        loyalty_tier,
        email,
        phone_number,
        gender,
        registration_date,
        passport_number,
        ingestion_time,
        is_processed,
        created_at,
        insert_date
    ) ' ||
    'SELECT
       passenger_id,
        full_name,
        birth_date,
        nationality,
        frequent_flyer,
        loyalty_tier,
        email,
        phone_number,
        gender,
        registration_date,
        passport_number,
        ingestion_time,
        is_processed,
        created_at,
        now()
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY passenger_id ORDER BY created_at DESC) AS rn
        FROM ' || v_schema || '.' || V_TABLE || '
    ) sub
    WHERE rn = 1';

    INSERT INTO public.etl_procedure_log (procedure_name, step_name, source_table, target_table)
    VALUES (v_proc_name, 'INSERT FT TO STR', V_TABLE, V_TABLE_1);

    EXECUTE
        'DELETE FROM ' || v_schema || '.' || V_TABLE_2 || ' AS tgt ' ||
        'USING ' || v_schema || '.' || V_TABLE_1 || ' AS src ' ||
        'WHERE tgt.passenger_id = src.passenger_id ';

    INSERT INTO public.etl_procedure_log (procedure_name, step_name, source_table, target_table)
    VALUES (v_proc_name, 'DELETE TR BY STR', V_TABLE_1, V_TABLE_2);

    EXECUTE
        'INSERT INTO ' || v_schema || '.' || V_TABLE_2 || ' (
        passenger_id,
        full_name,
        birth_date,
        nationality,
        frequent_flyer,
        loyalty_tier,
        email,
        phone_number,
        gender,
        registration_date,
        passport_number,
        ingestion_time,
        is_processed,
        created_at,
        insert_date
    ) SELECT
       passenger_id,
        full_name,
        birth_date,
        nationality,
        frequent_flyer,
        loyalty_tier,
        email,
        phone_number,
        gender,
        registration_date,
        passport_number,
        ingestion_time,
        is_processed,
        created_at,
        insert_date
    FROM ' || v_schema || '.' || V_TABLE_1;

    INSERT INTO public.etl_procedure_log (procedure_name, step_name, source_table, target_table)
    VALUES (v_proc_name, 'INSERT STR TO TR', V_TABLE_1, V_TABLE_2);

    INSERT INTO public.etl_procedure_log (procedure_name, step_name, source_table, target_table, ended_at)
    VALUES (v_proc_name, 'COMPLETED', V_TABLE_1, V_TABLE_2, CURRENT_TIMESTAMP);

EXCEPTION
    WHEN OTHERS THEN
        INSERT INTO public.etl_procedure_log (procedure_name, step_name, source_table, target_table, error_message, ended_at)
        VALUES (v_proc_name, 'FAILED', V_TABLE_1, V_TABLE_2, REPLACE(SQLERRM, '''', ''''''), CURRENT_TIMESTAMP);
        RAISE;
END;
$$;


