from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .template import ecoBeanBot, history_template, recycle_template
from langchain_teddynote.models import MultiModal
from .models import chatting
import boto3
from datetime import datetime
from config.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_STORAGE_BUCKET_NAME
import string
import random

def gemini_answer(messageQuestion, history):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
    # llm = ChatOpenAI(temperature=0.0,  # 창의성 (0.0 ~ 2.0)
    #                  max_tokens=2048,  # 최대 토큰수
    #                  model_name='gpt-4o',  # 모델명
    #                  )
    # if history == "":
    #     tmp_history = ""
    # else:
    #     tmp_history = history + history_template
    if history == "":
        tmp_history = ""
    else:
        tmp_history = history + history_template
    user_prompt = ChatPromptTemplate.from_template(tmp_history + ecoBeanBot +"{question}")
    chain = (
        user_prompt
        | llm
        | StrOutputParser()
    )
    return (chain.invoke({"question": messageQuestion}))

def gemini_img(messageQuestion, messageFile, history):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
    if history == "":
        tmp_history = ""
    else:
        tmp_history = history + history_template
    multimodal_gemini = MultiModal(
        llm, system_prompt= tmp_history + ecoBeanBot, user_prompt=messageQuestion
    )
    answer = multimodal_gemini.stream(messageFile)
    ret = ''
    for i in answer:
        ret += i.content
    return ret

def recycle_img(messageFile):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

    multimodal_gemini = MultiModal(
        llm, system_prompt=recycle_template, user_prompt="이 물건은 어떻게 분리수거해?"
    )
    answer = multimodal_gemini.stream(messageFile)
    ret = ''
    for i in answer:
        ret += i.content
    return ret

def get_history(user_id):
    try:
        chat_data = chatting.objects.filter(user=user_id).values()
        history = ""
        if chat_data is None:
            return ""
        for i in chat_data:
            history += '[human]:' + i['question'] + ' / [system]:' + i['answer'] + ' / '
        return history
    except chatting.DoesNotExist:
        return ""

def get_random_str():
    letters_set = string.ascii_letters
    random_list = random.sample(letters_set, 10)
    result = ''.join(random_list)
    return result

def s3_file_upload_by_file_data(upload_file, region_name=AWS_REGION, bucket_name=AWS_STORAGE_BUCKET_NAME, bucket_path="image", content_type=None, extension=None):
    bucket_name = bucket_name.replace('/', '')
    if content_type:
        content_type = content_type
    else:
        content_type = "image"
    if extension:
        extension = extension
    else:
        extension = "jpg"

    now = datetime.now()
    random_str = get_random_str()
    random_file_name = f"{now}_{random_str}.{extension}"
    upload_file_path_name = f"{bucket_path}/{random_file_name}"

    try:
        upload_file.seek(0)
    except Exception:
        pass

    s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    if s3.Bucket(bucket_name).put_object(Key=upload_file_path_name, Body=upload_file, ContentType=content_type, ACL='public-read') is not None:
        return f"https://s3-{region_name}.amazonaws.com/{bucket_name}/{bucket_path}/{random_file_name}"

    return False