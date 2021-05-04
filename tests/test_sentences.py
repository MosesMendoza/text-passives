from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_sentences():
  text = "Data modeling platform for our analysts;\nData quality monitoring system built into our pipelines;\nKnowledge discovery tool to help our co-workers find out where and how to ask questions that can be answered by our data."
  response = client.post(
    "/sentences",
    json={
      "text": text
    }
  )
  assert response.json() == { "sentences": ['Data modeling platform our our analysts;', 'Data quality monitoring system built into our pipelines;', 'Knowledge discovery tool to help our co-workers find out where and how to ask questions that can be answered by our data.'] }


def test_post_sentences():
  text = "Data modeling platform for our analysts;\nData quality monitoring system built into our pipelines;\nKnowledge discovery tool to help our co-workers find out where and how to ask questions that can be answered by our data."
  response = client.post(
    "/sentences",
    json={
      "text": text
    }
  )
  sentences = response.json()['sentences']
  assert len(sentences) == 3
