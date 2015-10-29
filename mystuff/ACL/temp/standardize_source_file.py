# INGEST ORIGINAL .TXT FILE
with open('sourcefile.txt', 'r') as f:
    my_temp_config = f.read()

# WRITE STANDARDIZED .TXT FILE (ACL FORMATTING LOWERCASE)      # remove this:  OUTSIDE_IN is not the same as OUTSIDE_in (only one can be applied to interface)
with open('standardized.txt', 'w') as f:
    for item in my_temp_config.strip().split('\n'):
        f.write(item.lower() + '\n')

# INGEST STANDARDIZED .TXT FILE
with open('standardized.txt', 'r') as f:
    my_config = f.read()
