
import requests

url = 'http://localhost:8080/rerank'
documents = [
    "Quĩ uỷ thác đầu tư (tiếng Anh: Unit Investment Trusts; viết tắt: UIT) là một công ty đầu tư mua hoặc nắm giữ một danh mục đầu tư cố định",
    "FPT software là một công ty phần mềm của tập đoàn FPT, chuyên cung cấp các giải pháp phần mềm cho các doanh nghiệp và tổ chức trên thế giới.",
    "Trường Đại học Kinh tế – Luật (tiếng Anh: University of Economics and Law – UEL) là trường đại học đào tạo và nghiên cứu khối ngành kinh tế, kinh doanh và luật hàng đầu Việt Nam.",
    "Trường Đại học Công nghệ Thông tin có tên tiếng Anh là University of Information Technology (viết tắt là UIT) là thành viên của Đại học Quốc Gia TP.HCM.",
    "Đại học FPT là một trường đại học tư thục tại Việt Nam, thành lập vào năm 2006"
]
query = " Tập đoàn FPT ?"
req_body = {'query': query, 'documents': documents}
res = requests.post(url, json=req_body)
resBody = res.json()

# Tìm tài liệu có điểm số cao nhất
highest_score_doc = max(resBody['scores'], key=lambda x: x['score'])

print(resBody)

print('Highest score doc:')

print(highest_score_doc)