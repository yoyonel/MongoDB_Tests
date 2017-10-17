# Screencast - Docker + MongoDB + Admin/Création Collection/User/

## Docker installation

[asciicast](https://asciinema.org/a/kt3RXYU074hOgQvgKh9EfHs1w)
[![asciicast](https://asciinema.org/a/kt3RXYU074hOgQvgKh9EfHs1w.png)](https://asciinema.org/a/kt3RXYU074hOgQvgKh9EfHs1w)

## Docker running

[asciicast](https://asciinema.org/a/fpsBHdoUfsBovMdtlEIgB61cI)
[![asciicast](https://asciinema.org/a/fpsBHdoUfsBovMdtlEIgB61cI.png)](https://asciinema.org/a/fpsBHdoUfsBovMdtlEIgB61cI)

# Docker pour MongoDB

## Récupérer une image MongoDB
```bash
$ docker pull mongo:latest
```

## Créer des dossiers permanents pour les bases de données MongoDB
```bash
$ sudo mkdir -p /opt/mongodb/db 
```

## Lancer le server MongoDB en mode authentifié
```bash
$ docker run -p 27017:27017 -v /opt/mongodb/db:/data/db --name my-mongo-dev -d mongo mongod --auth
```

## Vérification et logs
```bash
$ docker ps
$ docker logs -f my-mongo-dev
```

## Lancer un client Mongo pour créer un super-admin
```bash
$ docker exec -it my-mongo-dev mongo
```

### super-admin dans la console mongo
```
	use admin

	db.createUser(
		{
		user: "siteUserAdmin",
		pwd: "unPasswordQuiVaBien",
		roles: [{role: "userAdminAnyDatabase", db: "admin"}]
		}
	)
```

## Ajouter un utilisateur pour notre base de données

### Connection en super-admin
$ mongo -p 27017 -u siteUserAdmin --authenticationDatabase admin

### Création de la base et d'un utilisateur (owner)

```
	use kanban

	db.createUser(
		{
			user: "kanbanUser",
			pwd: "unAutrePasswordQuiVaBien",
			roles: ["dbOwner"]
		}
	)
```

## Test de connection à la base sur la collection avec le bon user

```bash
$ mongo --port 27017 -u kanbanUser -p kanban --authenticationDatabase kanban
```

# Python: pymongo

http://api.mongodb.com/python/current/tutorial.html

```python
from pymongo import MongoClient

client = MongoClient(
	'mongodb://{user}:{passwd}@{host}:{port}/kanban'.format(
		host='127.0.0.1',
		port=27017
		user='kanbanUser',
		passwd='unAutrePasswordQuiVaBien',
	)
)
db = client.kanban
kanban = db.kanban

for cur in kanban.find():
	print(cur)
```

# Sources
urls: 
- https://www.tutorialspoint.com/mongodb/mongodb_advantages.htm
- http://pierrepironin.fr/docker-et-mongodb/
- https://hub.docker.com/_/mongo/
- https://stackoverflow.com/questions/9146123/pretty-print-in-mongodb-shell-as-default
- http://en.proft.me/2015/12/25/extend-and-colorize-mongodb-shell/
- http://api.mongodb.com/python/current/api/pymongo/database.html#pymongo.database.Database.drop_collection
- https://stackoverflow.com/questions/9805451/how-to-find-names-of-all-collections-using-pymongo
- https://docs.mongodb.com/getting-started/python/remove/
- http://api.mongodb.com/python/current/examples/authentication.html?highlight=password
- http://www.mongoalchemy.org/
- https://docs.mongodb.com/ecosystem/drivers/python/
- https://docs.mongodb.com/manual/tutorial/install-mongodb-on-debian/#install-mongodb-community-edition	