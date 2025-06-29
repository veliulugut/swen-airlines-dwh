create function fn_truncate_table(schema_name text, table_name text) returns void
    language plpgsql
as
$$
BEGIN
    EXECUTE format('TRUNCATE TABLE %I.%I', schema_name, table_name);
END;
$$;

alter function fn_truncate_table(text, text) owner to admin;

