##########################################################
########## COMANDI PRINCIPALI DI AsyncMongoClient #########
##########################################################

Importazione e connessione


client = AsyncMongoClient("mongodb://localhost:27017")

db = client["rubrica_db"]

Selezione della collezione

collection = db["contatti"]

Inserire un singolo documento (asincrono)

await collection.insert_one({"nome": "Mario", "citta": "Roma"})

Inserire più documenti

await collection.insert_many([
{"nome": "Luisa", "citta": "Milano"},
{"nome": "Carlo", "citta": "Napoli"}
])

Trovare un singolo documento

doc = await collection.find_one({"nome": "Mario"})
print(doc)

Trovare più documenti (ritorna un cursore asincrono)

cursor = collection.find({"citta": "Roma"})
async for documento in cursor:
print(documento)

Aggiornare un documento

await collection.update_one(
{"nome": "Mario"}, # filtro
{"$set": {"citta": "Torino"}} # operazione di aggiornamento
)

Aggiornare più documenti

await collection.update_many(
{"citta": "Roma"},
{"$set": {"citta": "Napoli"}}
)

Eliminare un documento

await collection.delete_one({"nome": "Carlo"})

Eliminare più documenti

await collection.delete_many({"citta": "Milano"})

Contare i documenti

count = await collection.count_documents({})
print(count)

Ordinare i risultati (1 = ascendente, -1 = discendente)

cursor = collection.find().sort("nome", 1)
async for documento in cursor:
print(documento)

Limitare e saltare risultati

cursor = collection.find().skip(2).limit(5)
async for documento in cursor:
print(documento)

Ricerca testuale con regex

cursor = collection.find({"nome": {"$regex": "Mar", "$options": "i"}})
async for documento in cursor:
print(documento)

Creare un indice per velocizzare le ricerche

await collection.create_index("nome")

Chiudere la connessione

await client.close()

##########################################################
############### COMANDI PRINCIPALI DI MONGODB ###########
##########################################################

Avviare la shell MongoDB da Docker

docker exec -it mongodb mongosh

Mostrare i database esistenti

show dbs

Selezionare (o creare) un database

use rubrica_db

Mostrare le collezioni del database

show collections

Creare una collezione (viene creata automaticamente al primo insert)

db.createCollection("contatti")

Inserire dati

Inserire un singolo documento

db.contatti.insertOne({nome: "Mario", citta: "Roma"})

Inserire più documenti

db.contatti.insertMany([
{nome: "Luisa", citta: "Milano"},
{nome: "Carlo", citta: "Napoli"}
])

Leggere dati

Visualizzare tutti i documenti

db.contatti.find()

Visualizzare in modo leggibile

db.contatti.find().pretty()

Filtrare i risultati

db.contatti.find({citta: "Roma"})

Cercare con regex (case-insensitive)

db.contatti.find({nome: {$regex: "mar", $options: "i"}})

Ordinare i risultati (1 ascendente, -1 discendente)

db.contatti.find().sort({nome: 1})

Limitare i risultati

db.contatti.find().limit(5)

Aggiornare dati

Aggiornare un documento

db.contatti.updateOne(
{nome: "Mario"},
{$set: {citta: "Torino"}}
)

Aggiornare più documenti

db.contatti.updateMany(
{citta: "Roma"},
{$set: {citta: "Napoli"}}
)

Eliminare dati

Eliminare un documento

db.contatti.deleteOne({nome: "Carlo"})

Eliminare più documenti

db.contatti.deleteMany({citta: "Milano"})

Varie operazioni utili

Contare i documenti

db.contatti.countDocuments({})

Creare un indice

db.contatti.createIndex({nome: 1})

Visualizzare gli indici

db.contatti.getIndexes()

Eliminare un indice

db.contatti.dropIndex("nome_1")

Eliminare tutti i documenti della collezione

db.contatti.deleteMany({})

Eliminare l’intera collezione

db.contatti.drop()

Eliminare l’intero database

db.dropDatabase()

Uscire dalla shell MongoDB

exit

