import sqlite3

sqlite_file = 'reactors'    # name of the sqlite database file
table_name = 'reactors'  # name of the table to be created
new_field = 'ID' # name of the column
field_type = 'INTEGER'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column and set it as PRIMARY KEY
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name, nf=new_field, ft=field_type))

# New column types
text_type  = 'TEXT'
real_type = 'REAL'

# New columns to be added
new_columns = [('Name', text_type),
               ('Long', real_type),
               ('Lat', real_type),
               ('Country', text_type),
               ('Institute', text_type),
               ('Thermal Capacity', real_type),
               ('Electricity Capacity', real_type),
               ('Thermal Efficiency', real_type),
               ('Capacity Factor', real_type),
               ('Type', text_type),
               ('Fuel', text_type),
               ('Enrichment', real_type)]

# Adding the columns, without row value
for col in new_columns: 
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
              .format(tn=table_name, cn=col[0], ct=col[1]))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
