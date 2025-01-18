# import asyncio
# from crossencoder import CrossEncoderInput, CrossEncoderRanker
# import torch

# torch.set_default_dtype(torch.float16)

# model_ranker = CrossEncoderRanker("local-ranker-model")
# propertyText = """
# Module ref2Vec-centroid được sử dụng để tính toán vector đối tượng dựa trên trọng tâm của các vector tham chiếu.
# Ý tưởng là vector trọng tâm này sẽ được tính từ các vector của các tham chiếu của một đối tượng, cho phép
# liên kết giữa các cụm đối tượng. Điều này hữu ích trong các ứng dụng như đưa ra gợi ý
# dựa trên sự tổng hợp các hành động hoặc sở thích của người dùng.
# """
# documents = [
#     "Quĩ uỷ thác đầu tư (tiếng Anh: Unit Investment Trusts; viết tắt: UIT) là một công ty đầu tư mua hoặc nắm giữ một danh mục đầu tư cố định",
#     "FPT software là một công ty phần mềm của tập đoàn FPT, chuyên cung cấp các giải pháp phần mềm cho các doanh nghiệp và tổ chức trên thế giới.",
#     "Trường Đại học Kinh tế – Luật (tiếng Anh: University of Economics and Law – UEL) là trường đại học đào tạo và nghiên cứu khối ngành kinh tế, kinh doanh và luật hàng đầu Việt Nam.",
#     "Trường Đại học Công nghệ Thông tin có tên tiếng Anh là University of Information Technology (viết tắt là UIT) là thành viên của Đại học Quốc Gia TP.HCM.",
#     "Đại học FPT là một trường đại học tư thục tại Việt Nam, thành lập vào năm 2006"
# ]
# query = " Tập đoàn FPT ?"
# req_body = {'query': query, 'documents': documents}
# item = CrossEncoderInput(query=query, documents=documents)

# async def main():
#     result = await model_ranker.do(item)
#     print(result)

# asyncio.run(main())



import requests

url = 'http://localhost:8001/rerank'
# documents = [
#     "Quĩ uỷ thác đầu tư (tiếng Anh: Unit Investment Trusts; viết tắt: UIT) là một công ty đầu tư mua hoặc nắm giữ một danh mục đầu tư cố định",
#     "FPT software là một công ty phần mềm của tập đoàn FPT, chuyên cung cấp các giải pháp phần mềm cho các doanh nghiệp và tổ chức trên thế giới.",
#     "Trường Đại học Kinh tế – Luật (tiếng Anh: University of Economics and Law – UEL) là trường đại học đào tạo và nghiên cứu khối ngành kinh tế, kinh doanh và luật hàng đầu Việt Nam.",
#     "Trường Đại học Công nghệ Thông tin có tên tiếng Anh là University of Information Technology (viết tắt là UIT) là thành viên của Đại học Quốc Gia TP.HCM.",
#     "Đại học FPT là một trường đại học tư thục tại Việt Nam, thành lập vào năm 2006"
# ]
query = " Tập đoàn FPT ?"
property_text = """
FPT Software là công ty phần mềm hàng đầu thuộc tập đoàn FPT, cung cấp các giải pháp phần mềm trên toàn thế giới.
"""

req_body = {'query': query, 'property': property_text}
res = requests.post(url, json=req_body)
resBody = res.json()

# Tìm tài liệu có điểm số cao nhất
# highest_score_doc = max(resBody['scores'], key=lambda x: x['score'])

print(resBody)

# print('Highest score doc:')

# print(highest_score_doc)