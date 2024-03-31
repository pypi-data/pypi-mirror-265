# import objects
from dataferry import SqlServerConnection, Etl

# define mandatory generic variables
config_params_path = r'C:\my_local_folder\my_config\config_params.ini'

# define optional generic variables
log_path = r'C:\Users\timpe\OneDrive\master_folder\my_folder\my_apps\my_python\myprojects\DataFerry-main\tests\log.log'

# make connections
source_connection = SqlServerConnection('MSSQLSVRA', config_params_path)
destination_connection = SqlServerConnection('MSSQLSVRB', config_params_path)

# define etl class variables
source_sql = r'''SELECT * FROM TESTDB.dbo.tbl_test'''
destination_database = 'TESTDB'
destination_table = 'tbl_test'

# define optional etl variables
xforms = [
    "my_chunk['test_id'] = my_chunk['test_id'] * 10"
    , "my_chunk['test_id'] = my_chunk['test_id'].astype(str)"
    ]
# destination_schema = 'SOMESCHEMA'

# create etl class
etl_a = Etl(source_sql, destination_database, destination_table, source_connection, destination_connection
    , xforms=xforms
    # , schema=destination_schema
    , log_path=log_path)

# create other etl classes as required

# create a list of etl classes
xfers = [
    etl_a
    , # etl_b
    ]

# iterate through the etl list and execute the etl classes
for xf in xfers:
    
    # either drop or truncate the destination table
    xf.drop_table()
    # xf.truncate_table()
    
    # transfer the data
    xf.transfer_data()