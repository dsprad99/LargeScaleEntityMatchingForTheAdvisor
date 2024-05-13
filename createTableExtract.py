import gzip

'''
@author: Davis Spradling 

@brief: Purpose of script is to extract create table statements. 
'''

'''
@param: sql_file - file name of the sql file 

@param: tables - list of tables we want to extract
'''
def extract_tables(sql_file):
    with gzip.open(sql_file, 'rt', encoding='utf-8') as f:
        inCreateStatement = False
        create_statement = []

        for line in f:
            if not line.startswith('INSERT INTO'):
                if not inCreateStatement:
                    inCreateStatement = True
                create_statement.append(line)
            elif inCreateStatement:
                create_statement.append(line)

                # Check if the current line completes the CREATE TABLE statement
                if ';' in line:
                    inCreateStatement = False
                    write_create_statement(create_statement)
                    create_statement = []

def write_create_statement(statement_lines):
    create_sql = ''.join(statement_lines)
    with open('create_tables.sql', 'a', encoding='utf-8') as f:
        f.write(create_sql)


sql_file = 'csx_db_7_15_2014.sql.gz'
#sql_file = 'my_guitar_shop.sql'


extract_tables(sql_file)