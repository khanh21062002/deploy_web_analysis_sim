from elasticsearch import Elasticsearch
from analysis_sim import identify_beautiful_sequences_with_positions
from servixe import count_type_number

# Kết nối tới Elasticsearch
elastic = Elasticsearch([{"host": "103.143.142.224", "port": 9200, "scheme": "http"}])
elastic_local = Elasticsearch(
    ["http://localhost:9200"],
    verify_certs=False
)

def fetch_data_from_server():
    all_data = []
    # Bắt đầu một phiên scroll
    initial_response = elastic.search(
        index="khostk",
        body={
            "query": {
                "match_all": {}
            },
        },
        size=100,  # Kích thước mỗi lần trả về (có thể điều chỉnh)
        scroll='2m'  # Thời gian sống của scroll
    )

    scroll_id = initial_response['_scroll_id']
    all_data.extend(initial_response['hits']['hits'])

    # Lặp qua các trang tiếp theo
    while len(initial_response['hits']['hits']) > 0:
        initial_response = elastic.scroll(scroll_id=scroll_id, scroll='2m')
        scroll_id = initial_response['_scroll_id']
        all_data.extend(initial_response['hits']['hits'])

    return all_data


def get_data_server_and_handle():
    data = fetch_data_from_server()
    if isinstance(data, dict) and 'error' in data:
        print(f"Error fetching data: {data['error']}")
        return
    
    if not data:  # Nếu không có dữ liệu
        return  # Lấy 100 dữ liệu
    
    if data:
        for item in data:
            source = item['_source']
            new_record = {}

            # Danh sách các trường trên server
            server_fields = [
                "c", "c2", "d", "d2", "d3", "e", "f", "f0", "f1", "f2", "f3", 
                "f4", "f5", "f6", "f7", "f8", "f9", "h", "hg", "i", "id", 
                "l", "m", "p", "pb", "pg", "pn", "pt", "s2", "s3", "t", 
                "ut", "utC", "utP", "utT"
            ]

            # Gán giá trị từ source hoặc None nếu không có
            for field in server_fields:
                new_record[field] = source.get(field, None)

            # Lấy dữ liệu số điện thoại ra và loại bỏ ký tự không phải số
            phone_number = source.get('f', None)
            if phone_number:
                # Loại bỏ ký tự không phải số
                phone_number = ''.join(filter(str.isdigit, phone_number))
                
                # Kiểm tra độ dài
                if len(phone_number) == 10:
                    result_analysis = identify_beautiful_sequences_with_positions(phone_number)

                    # Tính toán các giá trị rồi lưu giữ vào trong elastic local
                    new_record["duoi_dep"] = result_analysis["Dãy đẹp đuôi"]
                    new_record["dau_dep"] = result_analysis["Dãy đẹp đầu"]
                    new_record["giua_dep"] = result_analysis["Dãy đẹp giữa"]

                    new_record["duoi_dang"] = result_analysis["Dạng đẹp đuôi"]
                    new_record["dau_dang"] = result_analysis["Dạng đẹp đầu"]
                    new_record["giua_dang"] = result_analysis["Dạng đẹp giữa"]

                    new_record["duoi_index"] = result_analysis["Vị trí đuôi"]
                    new_record["dau_index"] = result_analysis["Vị trí đầu"]
                    new_record["giua_index"] = result_analysis["Vị trí giữa"]

                    number_of_digit = count_type_number(phone_number)
                    new_record["sl_phim"] = number_of_digit

                    try:
                        elastic_local.index(index='sim_number', body=new_record, id=phone_number)
                        print(f"Document indexed successfully with phone number as _id: {phone_number}")
                    except Exception as e:
                        print(f"Error indexing document: {e}")
                else:
                    print(f"Phone number {phone_number} is not valid (length not 10), skipping.")
            else:
                print("No phone number found, skipping.")

def search_phone(number, size, from_index):
    search_query = {
        "query": {
            "wildcard": {
                "f": {
                    "value": f"*{number}*",  # Tìm chuỗi chứa 'number' ở bất kỳ đâu
                }
            }
        },
        "size": size,  # Lấy số bản ghi theo kích thước đã chỉ định
        "from": from_index  # Chỉ định điểm bắt đầu
    }
    
    try:
        response = elastic_local.search(index="sim_number", body = search_query)
        hits = response["hits"]["hits"]
        results = [hit["_source"] for hit in hits]
        total = response["hits"]["total"]["value"]
        
        return { "data":results, "total":total}
    except Exception as e:
        return {"error": str(e)}

def save_data(new_phone_number):
    new_record = {}
    
    # Danh sách các trường trên server
    server_fields = [
        "c", "c2", "d", "d2", "d3", "e", "f0", "f1", "f2", "f3", 
        "f4", "f5", "f6", "f7", "f8", "f9", "h", "hg", "i", "id", 
        "l", "m", "p", "pb", "pg", "pn", "pt", "s2", "s3", "t", 
        "ut", "utC", "utP", "utT"
    ]

    new_record["f"] = new_phone_number

    # Gán giá trị từ source hoặc None nếu không có
    for field in server_fields:
        new_record[field] = None
    
    result_analysis = identify_beautiful_sequences_with_positions(new_phone_number)

    if result_analysis:  # Kiểm tra xem kết quả phân tích có hợp lệ không
        new_record["duoi_dep"] = result_analysis.get("Dãy đẹp đuôi")
        new_record["dau_dep"] = result_analysis.get("Dãy đẹp đầu")
        new_record["giua_dep"] = result_analysis.get("Dãy đẹp giữa")

        new_record["duoi_dang"] = result_analysis.get("Dạng đẹp đuôi")
        new_record["dau_dang"] = result_analysis.get("Dạng đẹp đầu")
        new_record["giua_dang"] = result_analysis.get("Dạng đẹp giữa")

        new_record["duoi_index"] = result_analysis.get("Vị trí đuôi")
        new_record["dau_index"] = result_analysis.get("Vị trí đầu")
        new_record["giua_index"] = result_analysis.get("Vị trí giữa")

    number_of_digit = count_type_number(new_phone_number)
    new_record["sl_phim"] = number_of_digit

    try:
        elastic_local.index(index='sim_number', body=new_record, id=new_phone_number)
        print(f"Document indexed successfully with phone number as _id: {new_phone_number}")
    except Exception as e:
        print(f"Error indexing document: {e}")

def get_detail_sim(number):
    search_query = {
        "query": {
            "term": {  # Tìm kiếm chính xác số SIM
                "_id": number  # Tìm chính xác số SIM
            }
        }
    }
    
    try:
        response = elastic_local.search(index="sim_number", body = search_query)
        hits = response["hits"]["hits"]
        results = [hit["_source"] for hit in hits]
        
        return results
    except Exception as e:
        return {"error": str(e)}
    
def save_comment(id, comment): # Địa chỉ Elasticsearch
    elastic_local.update(index='sim_number', id=id, body={"doc": {"comment": comment}})  # Cập nhật tài liệu

# get_data_server_and_handle()
#
# index_exists = elastic_local.indices.exists(index = "sim_number")
# if index_exists:
#     print("yes")
# else:
#     print("no")