# Instructions to run dataGenerator.py

To upload the generated data using python to Supabase follow the given steps:
- When you open Supabase's project, at the top you will see Connect button. Click on it
- Under the connection string, change the method of Transaction pooler. Keep the Type as URI and Source as Primary Database.
- click on view paramaters and you'll be able to see details of host, port, database, user.
- for getting the password, in the database settings menu, at the top you can see database password. Click on reset database password.
- Click on generate password, copy it and write it somewhere. 
- Fill the necessary details at the starting of the datGenerator.py and run this python code.
- Data will be imported to Supabase