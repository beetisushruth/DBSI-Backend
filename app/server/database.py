import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"
QUESTION_COLL = "Questions"
ANSWER_COLL = "Answers"
USER_COLL = "Users"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.stackoverflow
questions_collection = database.get_collection(QUESTION_COLL)
answers_collection = database.get_collection(ANSWER_COLL)
users_collection = database.get_collection(USER_COLL)


# Questions database functions

async def add_question(data: dict) -> dict:
    """
    Add a new question into to the database
    :param data: question object
    :return: added question
    """
    data['_id'] = int(data['id'])
    # remove id from data
    del data['id']
    question = await questions_collection.insert_one(data)
    new_question = await questions_collection.find_one({"_id": question.inserted_id})
    return new_question


async def retrieve_questions(length) -> list:
    """
    Retrieve all questions with limit 100
    :return:
    """
    questions = []
    res = await questions_collection.find().to_list(length=length)
    for question in res:
        questions.append(question)
    return questions


async def retrieve_question(id: str) -> dict:
    """
    Retrieve a question with a matching ID
    :param id: id of the question
    :return: question matching the id
    """
    question = await questions_collection.find_one({"_id": int(id)})
    if question:
        return question


async def update_question(id: str, data: dict):
    """
    Update a question with a matching ID
    :param id: id of the question
    :param data: question object
    :return: updated question
    """
    if len(data) < 1:
        return False
    question = await questions_collection.find_one({"_id": int(id)})
    if question:
        updated_question = await questions_collection.update_one(
            {"_id": int(id)}, {"$set": data}
        )
        if updated_question:
            return True
        return False


async def delete_question(id: str):
    """
    Delete a question from the database
    :param id: id of the question
    :return: true if deleted, false if not found
    """
    question = await questions_collection.find_one({"_id": int(id)})
    if question:
        await questions_collection.delete_one({"_id": int(id)})
        return True


async def retrieve_questions_by_aggregation_pipeline(pipeline):
    """
    Retrieve questions by aggregation pipeline
    :param pipeline: aggregation pipeline
    :return: questions matching the pipeline
    """
    questions = []
    async for question in questions_collection.aggregate(pipeline):
        questions.append(question)
    return questions


# Answers database functions

async def add_answer(data: dict) -> dict:
    """
    Add a new answer into to the database
    :param data: answer object
    :return: added answer
    """
    answer = await answers_collection.insert_one(data)
    new_answer = await answers_collection.find_one({"_id": answer.inserted_id})
    return new_answer


async def retrieve_answers(length) -> list:
    """
    Retrieve all answers with limit 100
    :return:
    """
    answers = []
    res = await answers_collection.find({}, {'_id': 0}).to_list(length=length)
    for answer in res:
        answers.append(answer)
    return answers


async def retrieve_answer(id: str) -> dict:
    """
    Retrieve an answer with a matching ID
    :param id: id of the answer
    :return: answer matching the id
    """
    answer = await answers_collection.find_one({"id": int(id)}, {'_id': 0})
    if answer:
        return answer


async def update_answer(id: str, data: dict):
    """
    Update an answer with a matching ID
    :param id: id of the answer
    :param data: answer object
    :return: updated answer
    """
    if len(data) < 1:
        return False
    answer = await answers_collection.find_one({"id": int(id)}, {'_id': 0})
    if answer:
        updated_answer = await answers_collection.update_one(
            {"id": id}, {"$set": data}
        )
        if updated_answer:
            return True
        return False


async def delete_answer(id: str):
    """
    Delete an answer from the database
    :param id: id of the answer
    :return: true if deleted, false if not found
    """
    answer = await answers_collection.find_one({"id": int(id)}, {'_id': 0})
    if answer:
        await answers_collection.delete_one({"id": int(id)})
        return True


async def retrieve_answers_by_aggregation_pipeline(pipeline):
    """
    Retrieve answers by aggregation pipeline
    :param pipeline: aggregation pipeline
    :return: answers matching the pipeline
    """
    answers = []
    async for answer in answers_collection.aggregate(pipeline):
        answers.append(answer)
    return answers


# User database functions

async def add_user(data: dict) -> dict:
    """
    Add a new user into to the database
    :param data: user object
    :return: added user
    """
    user = await users_collection.insert_one(data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return new_user


async def retrieve_users(length) -> list:
    """
    Retrieve all users with limit 100
    :return:
    """
    users = []
    res = await users_collection.find({}, {'_id': 0}).to_list(length=length)
    for user in res:
        users.append(user)
    return users


async def retrieve_user(id: str) -> dict:
    """
    Retrieve a user with a matching ID
    :param id: id of the user
    :return: user matching the id
    """
    user = await users_collection.find_one({"_id": int(id)})
    if user:
        return user


async def retrieve_user_by_username(display_name: str) -> dict:
    """
    Retrieve a user with a matching username
    :param display_name: username of the user
    :return: user matching the username
    """
    users = await users_collection.find({"display_name": display_name})
    if users:
        return users


async def update_user(id: str, data: dict):
    """
    Update a user with a matching ID
    :param id: id of the user
    :param data: user object
    :return: updated user
    """
    if len(data) < 1:
        return False
    user = await users_collection.find_one({"_id": int(id)})
    if user:
        updated_user = await users_collection.update_one(
            {"_id": id}, {"$set": data}
        )
        if updated_user:
            return True
        return False


async def delete_user(id: str):
    """
    Delete a user from the database
    :param id: id of the user
    :return: true if deleted, false if not found
    """
    user = await users_collection.find_one({"_id": int(id)})
    if user:
        await users_collection.delete_one({"_id": int(id)})
        return True


async def retrieve_users_by_aggregation_pipeline(pipeline):
    """
    Retrieve users by aggregation pipeline
    :param pipeline: aggregation pipeline
    :return: users matching the pipeline
    """
    users = []
    async for user in users_collection.aggregate(pipeline):
        users.append(user)
    return users