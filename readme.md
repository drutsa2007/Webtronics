### Тестовое задание "Webtronics"  

### Change setting in file <font color="darkred">.env!</font>

#### Create on Windows
1. create virtual env:  
`python -m venv venv`
2. activate venv:  
`venv\scripts\activate.ps1`
3. update pip:  
`python -m pip install --upgrade pip`
4. install libraries:  
`python -m pip install -r requirements.txt`
5. start server:  
`python server.py` or play server.py in IDE  

#### Create MongoDB + MongoExpress in Docker
1. create network  
`docker network create mongo-express-network`
2. create MongoDB (path to DB only Windows!)  
`docker run -d --rm -p 27017:27017 --hostname myHostMongoDB -e MONGO_INITDB_ROOT_USERNAME=rootuser -e MONGO_INITDB_ROOT_PASSWORD=rootpass --name myMongoDB -v c:\mdb:/data/db --net mongo-express-network mongo:6.0.2`
3. create MongoExpress  
`docker run -d --rm -p 8081:8081 --hostname myHostMongoExpress -e ME_CONFIG_MONGODB_ADMINUSERNAME=rootuser -e ME_CONFIG_MONGODB_ADMINPASSWORD=rootpass -e ME_CONFIG_MONGODB_SERVER=myHostMongoDB --name myMongoExpress --net mongo-express-network mongo-express:1.0.0-alpha`

### Test in Postman or FastAPI.Docs
authorize through bearer JWT-token  
get token - login user `http://server/login`  
register user `http://server/register`

### ToDo-List Posts
- [x] Create Post `http://server/api/posts` - POST
- [x] List Post `http://server/api/posts` - GET
- [x] List My Post `http://server/api/my-posts` - GET
- [x] View Post `http://server/api/posts/{caption}` - GET
- [x] Update Post `http://server/api/posts/{caption}` - PUT
- [x] Delete Post `http://server/api/posts/{caption}` - DELETE
   
### ToDo-List Likes (data->raw->json send caption post)
- [x] Like Post `http://server/api/like` - POST 
- [x] Dislike Post `http://server/api/dislike` - POST (data->raw->json)

Description for action in app not exists, because code is little.