# this would fetch posts from social media regarding help or whatsoever
from db.database import supabase
from fastapi import APIRouter

router = APIRouter()


@router.get("/social-media/posts")
def getPosts():
    return {
        "posts":[
            {
                "platform":"twitter","content":"floods in mumbai are worsening"
            },
            {
                "platform":"Instagram","content":"Roads underwater in bandra"
            }
        ]
    }