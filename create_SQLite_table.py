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

# New columns to be added
new_column1 = 'Name'
new_column2 = 'Long'
new_column3 = 'Lat'
new_column4 = 'Country'
new_column5 = 'Institute'
new_column6 = 'Thermal Capacity'
new_column7 = 'Electricity Capacity'
new_column8 = 'Thermal Efficiency'
new_column9 = 'Capacity Factor'
new_column10 = 'Type'
new_column11 = 'Fuel'
new_column12 = 'Enrichment'

# New column types
column_type1 = 'TEXT'
column_type2 = 'REAL'


# Adding the columns, without row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column1, ct=column_type1))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column2, ct=column_type2))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column3, ct=column_type2))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column4, ct=column_type1))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column5, ct=column_type1))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column6, ct=column_type2))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column7, ct=column_type2))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column8, ct=column_type2))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column9, ct=column_type2))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column10, ct=column_type1))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column11, ct=column_type1))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column12, ct=column_type1))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()