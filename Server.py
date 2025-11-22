from pymongo import AsyncMongoClient
import asyncio
import tornado.web
import bson

client = AsyncMongoClient("mongodb://localhost:27017")
db = client["library_DB"]
publishers = db["publisher"]
books = db["books"]

class PublishersHandler(tornado.web.RequestHandler):
    
    async def get(self, id=None):
        
        self.set_header("Content-Type", "application/json")


        if id == None:

            name = self.get_query_argument("name", None)
            country = self.get_query_argument("country", None)
            
            if name != None and country != None:
                filter = publishers.find({"name": name, "country": country})
            
            elif name != None:
                filter = publishers.find({"name": name})

            elif country != None:
                filter = publishers.find({"country": country})

            else:
                filter = publishers.find()
            
            string = ""
            async for i in filter:
                string = string + str(i) + "\n"
            
            self.write(string.encode())

        else:

            try:
                publisher = await publishers.find_one({"_id": bson.ObjectId(id)})
            
            except bson.errors.invalindId:

                self.set_status(404)
                self.write("Editore non trovato")
            
            else:

                if publisher != None:
                    self.write(str(publisher).encode())
                    self.set_status(200)
                
                else:
                    self.set_status(404)
                    self.write("Editore non trovato")

    async def put(self, id):
        
        self.set_header("Content-Type", "application/json")

        data = tornado.escape.json_decode(self.request.body)

        try:

            await publishers.find_one_and_replace({"_id": bson.ObjectId(id)}, data)

        except:

            self.set_status(404)
            self.write("Editore non trovato")

        else: 

            self.set_status(200)
            self.write("Editore modificato".encode())

    async def post(self):
        
        self.set_header("Content-Type", "application/json")

        data = tornado.escape.json_decode(self.request.body)

        if list(data.keys()) == ["name", "founded_year", "country"]:

            await publishers.insert_one(data)
            self.set_status(200)
            self.write(str({"message": "Editore aggiunto", "publisher": publishers.find_one(data)}).encode())
        
        else:

            self.set_status(404)
            self.write("Formato dati invalido".encode())



    async def delete(self, id):
        
        self.set_header("Content-Type", "application/json")

        try:

            await publishers.find_one_and_delete({"_id": bson.ObjectId(id)})
            await books.delete_many({"publisher_id": id})

        except bson.errors.InvalidId:

            self.set_status(404)
            self.write("Editore non trovato".encode())

        else:

            self.set_status(200)
            self.write("Editore e i suoi libri sono stati eliminati con successo".encode())



class BooksHandler(tornado.web.RequestHandler):
    
    async def get(self, publisher_id, id = None):

        self.set_header("Content-Type", "application/json")

        publisher = await publishers.find_one({"_id": bson.ObjectId(publisher_id)})

        if publisher != None:

            if id == None:

                title = self.get_query_argument("title", ".+")
                author = self.get_query_argument("author", ".+")
                genre = self.get_query_argument("genre", ".+")
                
                filter = books.find({
                    "publisher_id": publisher_id,
                    "title": {"$regex": title},
                    "author": {"$regex": author},
                    "genre": {"$regex": genre},
                    })

                filter = await filter.to_list()
                if len(filter) > 0:
                    string = ""
                    for i in filter:
                        string = string + str(i) + "\n"     
                    self.write(string.encode())
                    self.set_status(200)

                else:
                    self.set_status(404)
                    self.write("Libro non trovato, prova un altro editore")

            else:
                publisher = await books.find_one({"_id": bson.ObjectId(id), "publisher_id": publisher_id})

                if publisher != None:
                    self.write(str(publisher).encode())
                    self.set_status(200)
                
                else:
                    self.set_status(404)
                    self.write("Libro non trovato".encode())
        else:

            self.set_status(404)
            self.write("Editore non trovato".encode())


    async def delete(self, publisher_id, id):

        self.set_header("Content-Type", "application/json")

        try:
            await books.find_one_and_delete({"_id": bson.ObjectId(id), "publisher_id": publisher_id})

        except bson.errors.invaliId:
            self.set_status(404)
            self.wrte("Libro non trovato")

        else:
            self.set_status(200)
            self.write("Libro eliminato con successo".encode())


    async def post(self, publisher_id):

        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)

        try:

            publisher = await publishers.find_one({"_id": bson.ObjectId(publisher_id)})
        
        except:

            self.set_status(404)
            self.write("Id editore non valido".encode())

        if list(data.keys()) == ["title", "author", "genre", "year"] or publisher != None:

            data["publisher_id"] = publisher_id
            await books.insert_one(data)
            self.set_status(200)
            self.write(str({"message": "libro aggiunto con successo", "book": books.find_one(data)}).encode())

        else:

            self.set_status(404)
            self.write("Parametri invalidi".encode())

    
    async def put(self, publisher_id, id):

        self.set_header("Content-Type", "application/json")
        data = tornado.escape.json_decode(self.request.body)
        data["publisher_id"] = publisher_id

        book = await books.find_one({"_id": bson.ObjectId(id), "publisher_id": publisher_id})

        if book != None:

            await books.find_one_and_replace(book, data)

            self.set_status(200)
            self.write("Libro modificato con successo".encode())

        else:

            self.set_status(404)
            self.write("Libro non trovato".encode())



def make_app():
    return tornado.web.Application([
        (r"/publishers/([^/]+)/books/([^/]+)", BooksHandler),
        (r"/publishers/([^/]+)/books", BooksHandler),
        (r"/publishers/([^/]+)", PublishersHandler),
        (r"/publishers", PublishersHandler),
    ])

async def main(shutdown_event):
    app = make_app()
    app.listen(8888)
    print("Server attivo su http://localhost:8888/publishers")
    await shutdown_event.wait()
    print("Chiusura server...")


if __name__ == "__main__":
    shutdown_event = asyncio.Event()
    try:
        asyncio.run(main(shutdown_event))
    except KeyboardInterrupt:
        shutdown_event.set()