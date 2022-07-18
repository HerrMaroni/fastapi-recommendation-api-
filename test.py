
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Please send a request to /recommendSimilarArticles or /recommendOutfit"}

def test_recommend_similar_articles():
    response = client.post("/recommendSimilarArticles", json={'product_id': 13795822, 'top_k': 10})
    print(response.json())
    assert response.status_code == 200
    # TODO

def recommend_outfit():
    response = client.post("/recommendOutfit", json={'product_id': 13784032, 'color_palette':'Complementary',
                                                     'recommend_bags': True, 'recommend_accessories': True,
                                                     'recommend_jewelry':True})
    print(response.json())
    assert response.status_code == 200


if __name__ == '__main__':
    test_read_main()
    test_recommend_similar_articles()
    recommend_outfit()