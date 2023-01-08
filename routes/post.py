import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from mongo import db
from models.Articles import Article
from models.Users import User
from routes.auth import get_current_user

router = APIRouter()


@router.post('/posts', summary="Create post", status_code=201)
async def create_post(data: Article, current_user: User = Depends(get_current_user)):
    new_record = dict(data)
    new_record['username'] = current_user['username']
    new_record['created_at'] = datetime.datetime.utcnow()
    new_record['updated_at'] = new_record['created_at']
    posts = db['posts']
    result = posts.insert_one(new_record)
    current_post = posts.find_one({'_id': result.inserted_id}, {"_id": 0})
    return {"status": 201, "post": current_post}


@router.get('/posts', summary="List posts")
async def list_posts(current_user: User = Depends(get_current_user)):
    posts = db['posts']
    current_posts = posts.find({}, {"_id": 0})
    return {"status": 200, "posts": list(current_posts)}


@router.get('/my-posts', summary="List my posts")
async def list_my_posts(current_user: User = Depends(get_current_user)):
    posts = db['posts']
    current_posts = posts.find({"username": current_user['username']}, {"_id": 0})
    return {"status": 200, "posts": list(current_posts)}


@router.get('/posts/{caption}', summary="View post")
async def view_post(caption: str, current_user: User = Depends(get_current_user)):
    posts = db['posts']
    current_post = posts.find_one({"caption": caption}, {"_id": 0})
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record don't exists"
        )
    return {"status": 200, "post": current_post}


@router.put('/posts/{caption}', summary="Update post")
async def update_post(caption: str, data: Article, current_user: User = Depends(get_current_user)):
    posts = db['posts']
    current_post = posts.find_one({"caption": caption, "username": current_user['username']}, {"_id": 0})
    if not current_post:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    posts.update_one(
        {"caption": caption, "username": current_user['username']},
        {"$set": {"caption": data.caption, "text": data.text, "updated_at": datetime.datetime.utcnow()}}
    )
    current_post = posts.find_one({"caption": data.caption}, {"_id": 0})
    return {"status": 200, "post": current_post}


@router.delete('/posts/{caption}', summary="Delete post")
async def delete_post(caption: str, current_user: User = Depends(get_current_user)):
    posts = db['posts']
    posts.delete_one({"caption": caption, "username": current_user['username']})
    return {"success": 200}


@router.post('/like', summary="Like post")
async def like_post(data: Article, current_user: User = Depends(get_current_user)):
    posts = db['posts']
    current_post = posts.find_one({"caption": data.caption}, {"_id": 0})
    if not current_post:
        raise HTTPException(
            status_code=status.HTTP_404_FORBIDDEN,
            detail="Record is not exists"
        )
    if current_post['username'] == current_user['username']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    if "dislike_voices" in current_post.keys():
        if current_user['username'] in current_post['dislike_voices']:
            posts.update_one(
                {"caption": data.caption},
                {"$pull": {"dislike_voices": current_user['username']}, "$inc": {"dislikes": -1}}
            )
    if "like_voices" not in current_post.keys():
        posts.update_one(
            {"caption": data.caption},
            {"$set": {"like_voices": [current_user['username']]}, "$inc": {"likes": 1}}
        )
    else:
        if current_user['username'] not in current_post['like_voices']:
            posts.update_one(
                {"caption": data.caption},
                {"$push": {"like_voices": [current_user['username']]}, "$inc": {"likes": 1}}
            )
    return {"success": 200}


@router.post('/dislike', summary="Dislike post")
async def dislike_post(data: Article, current_user: User = Depends(get_current_user)):
    posts = db['posts']
    current_post = posts.find_one({"caption": data.caption}, {"_id": 0})
    if not current_post:
        raise HTTPException(
            status_code=status.HTTP_404_FORBIDDEN,
            detail="Record is not exists"
        )
    if current_post['username'] == current_user['username']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    if "like_voices" in current_post.keys():
        if current_user['username'] in current_post['like_voices']:
            posts.update_one(
                {"caption": data.caption},
                {"$pull": {"like_voices": current_user['username']}, "$inc": {"likes": -1}}
            )
    if "dislike_voices" not in current_post.keys():
        posts.update_one(
            {"caption": data.caption},
            {"$set": {"dislike_voices": [current_user['username']]}, "$inc": {"dislikes": 1}}
        )
    else:
        if current_user['username'] not in current_post['dislike_voices']:
            posts.update_one(
                {"caption": data.caption},
                {"$push": {"like_voices": [current_user['username']]}, "$inc": {"dislikes": 1}}
            )
    return {"success": 200}


