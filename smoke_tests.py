import unittest
import requests
import time

class SmokeTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:8000'

        for i in range(0, 100):
            try:
                res = requests.get(self.url + '/.well-known/ready')
                if res.status_code == 204:
                    return
                else:
                    raise Exception(
                            "status code is {}".format(res.status_code))
            except Exception as e:
                print("Attempt {}: {}".format(i, e))
                time.sleep(1)

        raise Exception("did not start up")

    def testWellKnownReady(self):
        res = requests.get(self.url + '/.well-known/ready')

        self.assertEqual(res.status_code, 204)

    def testWellKnownLive(self):
        res = requests.get(self.url + '/.well-known/live')

        self.assertEqual(res.status_code, 204)

    def testMeta(self):
        res = requests.get(self.url + '/meta')

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), dict)

    def testRerank(self):
        url = 'http://localhost:8000/rerank'
        propertyText = """
        Module ref2Vec-centroid được sử dụng để tính toán vector đối tượng dựa trên trọng tâm của các vector tham chiếu.
        Ý tưởng là vector trọng tâm này sẽ được tính từ các vector của các tham chiếu của một đối tượng, cho phép
        liên kết giữa các cụm đối tượng. Điều này hữu ích trong các ứng dụng như đưa ra gợi ý
        dựa trên sự tổng hợp các hành động hoặc sở thích của người dùng.
        """

        req_body = {'query': 'ref2vec là gì?', 'property': propertyText}
        res = requests.post(url, json=req_body)
        resBody = res.json()
        print("Rerank with single document", resBody)

        self.assertEqual(200, res.status_code)
        self.assertEqual(resBody['query'], req_body['query'])
        self.assertEqual(resBody['property'], req_body['property'])
        self.assertTrue(resBody['score'] != 0)

    def testBatchRerank(self):
        url = 'http://localhost:8000/rerank'
        text1 = """
        TÔi yêu bạn nhất trên đời, đó là lời nói dối của anh
        """
        text2 = "SpaceX là một công ty toàn cầu thực hiện các dự án cho NASA"
        text3 = "Weaviate là một cơ sở dữ liệu ưu tiên AI."
        documents = [text1, text2, text3]

        req_body = {'query': 'tôi thích bạn', 'documents': documents}
        res = requests.post(url, json=req_body)
        resBody = res.json()
        print("Rerank with multi document", resBody)

        self.assertEqual(200, res.status_code)
        self.assertEqual(resBody['query'], req_body['query'])
        self.assertIsNone(resBody['property'])
        self.assertIsNone(resBody['score'])
        self.assertEqual(len(resBody['scores']), len(documents))

        # Sort the scores by document order in the original documents list
        sorted_scores = sorted(resBody['scores'], key=lambda x: documents.index(x['document']))

        self.assertEqual(sorted_scores[0]['document'], documents[0])
        self.assertEqual(sorted_scores[1]['document'], documents[1])
        self.assertEqual(sorted_scores[2]['document'], documents[2])
        self.assertTrue(sorted_scores[0]['score'] != 0)
        self.assertTrue(sorted_scores[1]['score'] != 0)
        self.assertTrue(sorted_scores[2]['score'] != 0)


if __name__ == "__main__":
    unittest.main()