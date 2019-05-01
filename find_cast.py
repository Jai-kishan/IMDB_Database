#SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
#SQLite is the most used database engine in the world.
import sqlite3
import sys #The sys.exit() function allows the developer to exit from Python.
from pprint import pprint


def readData(user):
    conn = sqlite3.connect('cast.sqlite3')
    c = conn.cursor() # Acursor object is our interface to the database, that allows running anySQL query on our database.
    Movie_list=[]
    for i in range(user):
        Movie_Dic={}
        ids=i+1
        for row in c.execute("SELECT * from movie_details where id ='"+str(ids)+"';"):
            Movie_Dic["Name"]=row[1]
            Movie_Dic["Director"]=row[2]
            Movie_Dic["Country"]=row[3]
            Movie_Dic["Language"]=row[4]
            Movie_Dic['Poster_image_url']=row[5]
            Movie_Dic['Bio']=row[6]
            Movie_Dic['RunTime']=row[7]
            Movie_Dic['Genres']=row[8]
        
        Cast_list=[]
        for row in c.execute("SELECT * from movie_cast where id = '"+str(ids)+"';"):
            Cast_Dic={}
            Cast_Dic["Actor_name"]=row[1]
            Cast_Dic["imdb_ids"]=row[2]
            Cast_list.append(Cast_Dic)
        Movie_Dic["Cast"]=Cast_list
        Movie_list.append(Movie_Dic)
    return Movie_list

def create_table():
    #if the database does not exist, then it will be created and finally, a database object will be returned
    conn = sqlite3.connect('cast.sqlite3')
    c = conn.cursor()
    #The c.execute executes the SQL statement. Here we create a table "movie_details and movie_cast"
    c.execute('''CREATE TABLE IF NOT EXISTS movie_details(id INTEGER PRIMARY KEY AUTOINCREMENT,
        Movie_Title text,  Director TEXT, Country TEXT, Language TEXT, Poster_image_url TEXT, 
        Bio TEXT,RunTime INT, Genres TEXT)''') 
    c.execute('''CREATE TABLE IF NOT EXISTS movie_cast(id INTEGER , Actor_name TEXT, imdb_ids TEXT)''') 
    conn.commit() # this method after every transaction that modifies data for tables that use transactional storage engines.
    # conn.close() #If we are finished with our operations on the database file, we have to close the connection via the .close() method:


def cast_data(details): 
    #open the databse
    conn = sqlite3.connect('cast.sqlite3')
    c = conn.cursor()
    create_table() #calling here create_table() for creating tables
    dataCopy = c.execute("select count(*) from movie_details") # Counting the rows in the database
    #This method accepts number of records to fetch and returns tuple where each records itself is a tuple. 
    #If there are not more records then it returns an empty tuple.[(count,)]
    value = dataCopy.fetchmany() # its appending counted tuple rows in a list.
    values=value[0][0]
    if(values!=250): 
        # print (values)
        name  = details['Movie Title'] 
        director = ",".join(details['Director'])
        country = details['Country']
        language = ",".join(details['Language'])
        poster_image_url = details['Poster_image_url']
        bio = details['Bio']
        runtime = details['RunTime']
        #join method through we can join the list data into one string
        genre = ",".join(details['Genres'])
        data_1= [name,director, country,language, poster_image_url,bio,runtime,genre]
        c.execute('Insert into movie_details(Movie_Title,Director,Country,Language,Poster_image_url,Bio,RunTime,Genres) values (?,?,?,?,?,?,?,?)',data_1)
        for row in c.execute("SELECT * from movie_details where Movie_Title='" + name + "';"):
            ids= row[0]
        main_case  = details['Cast']

        for i in main_case:
            cname=i['Name']
            imdb_ids=i['IMDB_ids']

            data_2=[ids,cname,imdb_ids]
            c.execute('Insert into movie_cast(id,Actor_name,imdb_ids) values (?,?,?)',data_2)   
        # .commit()  this method after every transaction that modifies data for tables that use transactional storage engines.
        conn.commit()

    else:
        # print (values)
        user=int(input('Enter the number you want :- '))
        if(user<=values):
            pprint(readData(user))
            sys.exit() 
        else:
            print ('Number of data is not data in Database')

    
      







