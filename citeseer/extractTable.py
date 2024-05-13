import gzip

'''
@author: Davis Spradling 

@brief: Purpose of extract table is to be able to parse through a SQL file and extract INSERT INTO statements in the 
file. By doing so it will split up all of the different INSERT INTO statements into their own file
allowing a user to build there own SQL database in an easy way with indepedent tables.
'''

'''
@param: sql_file - file name of the sql file 

@param: tables - list of tables we want to extract
'''
def extract_tables(sql_file, tables):
    encodings_to_try = ['utf-8']
    current_table = None
    table_files = {}
    detected_encoding = None

    for encoding in encodings_to_try:
        try:
            with gzip.open(sql_file, 'rt', encoding=encoding) as f:
                for line in f:
                    if line.startswith('INSERT INTO'):
                        table_name = line.split()[2].strip('`')
                        if table_name in tables:
                            current_table = table_name
                            if current_table not in table_files:
                                table_files[current_table] = []
                            table_files[current_table].append(line)
                        else:
                            current_table = None
                    elif current_table is not None:
                        table_files[current_table].append(line)
                detected_encoding = encoding
                break  
        except UnicodeDecodeError:
            continue  

    if detected_encoding is None:
        print("Failed to detect encoding or decode file.")
        return

    for table, lines in table_files.items():
        with open(f'csx_db_7_15_2014_{table}.sql.gz', 'w', encoding='utf-8') as f:
            f.writelines(lines)


sql_file = 'csx_db_7_15_2014.sql.gz'
#sql_file = 'my_guitar_shop.sql'

tables_to_extract = ['citations']  

extract_tables(sql_file, tables_to_extract)
