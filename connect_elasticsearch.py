from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import json

# khởi tọa ứng dụng Flask
app = Flask(__name__)

# kết nối tới Elasticsearch
elastic = Elasticsearch([{"host":"103.143.142.224","port":9200,"scheme": "http"}])

elastic_local = Elasticsearch(
    ["http://localhost:9200"]
)

def fetch_data_from_server():
    query = {
        "query": {
            "match_all": {}
        },
        "size": 100  # Lấy 100 dữ liệu
    }
    
    try:
        response = elastic.search(index="khoso", body=query)
        # Lưu dữ liệu vào biến json
        data = response['hits']['hits']
        
        # Chuyển đổi dữ liệu sang định dạng JSON
        return data
    except Exception as e:
        return {"error": str(e)}
    
def get_data_server_and_handle():
    data = fetch_data_from_server()
    if data:
        print(data)

@app.route('/get_all', methods=['GET'])
def get_all_data():
  query = {"query": {"match_all": {}}}
  try:
    result = elastic.search(index="khostk",body=query)
    data = result['hits']['hits']
    return jsonify(data), 200 # trả về dưới dạng json
  except Exception as e:
    return jsonify({"error": str(e)}), 500

# get data follow param
@app.route('/search4', methods=['GET'])
def search4():
    params = request.args
    result = perform_elasticsearch_search(params)
    return jsonify(result)
  
@app.route('/test', methods=['GET'])
def test():
    return "Test Successful!"
  
def perform_elasticsearch_search(params):
    # Lấy các tham số từ params
    cat_id = params.get("catId", "")
    head = params.get("head", "").split(",") if params.get("head", "") else []
    d = params.get("d", "false").lower() == "true"
    t = params.get("t", "").split(",") if params.get("t", "") else []
    not_in = params.get("notIn", "").split(",") if params.get("notIn", "") else []
    prices = params.get("prices", "").split("-") if params.get("prices", "") else []
    l_sec = params.get("l_sec", "")
    priority_stores = params.get("priority_stores", "").split(",") if params.get("priority_stores", "") else []
    
    limit = min(int(params.get("limit", "50")), 100)
    page = int(params.get("page", "1"))

    # Tính toán vị trí lấy dữ liệu
    khoang_chia_du = (page - 1) // 35
    from_index = 35 * limit * khoang_chia_du

    # Khởi tạo filter
    filter = []
    must_not = []
    should = []

    # Lọc theo khoảng giá
    if prices:
        filter.append({
            "bool": {
                "should": [
                    {
                        "bool": {
                            "filter": [
                                {"range": {"pn": {"gte": prices[0]}}},
                                {"range": {"pn": {"lte": prices[1]}}}
                            ]
                        }
                    }
                ]
            }
        })

    # Lọc theo thời gian l_sec
    if l_sec:
        current_time = int(datetime.utcnow().timestamp())
        l_sec_convert = current_time - int(l_sec) * 86400
        filter.append({"range": {"l.sec": {"gte": l_sec_convert}}})

    # Lọc theo cat_id
    if cat_id:
        filter.append({"term": {"c": cat_id}})

    # Lọc theo các số đầu tiên (head)
    if head:
        filter.append({
            "bool": {
                "should": [{"wildcard": {"id": f"{h}*"}} for h in head]
            }
        })

    # Lọc theo nhà mạng viễn thông (t)
    if t:
        filter.append({"terms": {"t": t}})

    # Lọc theo tình trạng đã bán/chưa bán (d)
    filter.append({"term": {"d": d}})

    # Loại bỏ các số notIn
    if not_in:
        must_not += [{"wildcard": {"e": f"*{e}*"}} for e in not_in]
        must_not.append({"terms": {"f3": not_in}})

    # Lọc theo các kho ưu tiên
    if priority_stores:
        should.append({
            "constant_score": {
                "filter": {"terms": {"s3": priority_stores}},
                "boost": 15
            }
        })

    # Tạo query Elasticsearch
    query = {
        "query": {
            "bool": {
                "filter": filter,
                "must_not": must_not,
                "should": should
            }
        },
        "_source": ["id", "t"],
        "size": limit * 35,
        "from": from_index,
        "track_total_hits": True,
        "sort": [{"_score": "desc"}]  # Sắp xếp theo điểm số
    }
    
    query_json = json.dumps(query, indent=2)  # 'indent=2' để có định dạng dễ đọc
    print(query_json)

    try:
        # Thực hiện tìm kiếm Elasticsearch
        result = elastic.search(index="khoso", body=query)
        total = result["hits"]["total"]["value"]
        hits = result["hits"]["hits"]

        # Lấy kết quả và xử lý nếu cần
        results = [hit["_source"] for hit in hits]

        return {
            "total": total,
            "results": results
        }
    except Exception as e:
        return {"error": str(e)}
    
# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)
    
