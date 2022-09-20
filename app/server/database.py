import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.stackoverflow
questions_collection = database.get_collection("Questions")

aggregate_find_score_gt_10000 = [
    {'$match': {
        'score': {'$gt': 10000}
    }
    }
]


async def add_question(data: dict) -> dict:
    question = await questions_collection.insert_one(data)
    new_question = await questions_collection.find_one({"_id": question.inserted_id})
    return question_helper(new_question)


async def retrieve_questions() -> list:
    questions = []
    res = await questions_collection.aggregate(aggregate_find_score_gt_10000).to_list(length=100)
    print(res)
    async for question in questions_collection.aggregate(aggregate_find_score_gt_10000):
        questions.append(question_helper(question))
    return questions


async def retrieve_question(id: str) -> dict:
    question = await questions_collection.find_one({"_id": int(id)})
    if question:
        return question_helper(question)


async def update_question(id: str, data: dict):
    if len(data) < 1:
        return False
    question = await questions_collection.find_one({"_id": id})
    if question:
        updated_question = await questions_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_question:
            return True
        return False


async def delete_question(id: str):
    question = await questions_collection.find_one({"_id": ObjectId(id)})
    if question:
        await questions_collection.delete_one({"_id": ObjectId(id)})
        return True


# helpers

def question_helper(question) -> dict:
    return {
        "id": str(question["_id"]),
        "title": question["title"],
        "accepted_answer_id": question["accepted_answer_id"],
        "answer_count": question["answer_count"],
        "comment_count": question["comment_count"],
        "creation_date": question["creation_date"],
        "favorite_count": question["favorite_count"],
        "owner_user_id": question["owner_user_id"],
        "score": question["score"],
        "view_count": question["view_count"],
        "related_posts": question["related_posts"],
        "tags": question["tags"]
    }
