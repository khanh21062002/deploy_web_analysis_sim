from flask import Flask, request, jsonify, render_template
from analysis_sim import identify_beautiful_sequences_with_positions
from servixe import add_dot_to_number, split_number, analysis_append_color, analysis_append_format
from get_data_elasticsearch import search_phone, save_data, get_detail_sim, save_comment
from elasticsearch import Elasticsearch

app = Flask(__name__)

elastic_local = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=('root', '123456') 
)

@app.route('/test')
def test():
    # Các số mặc định khi mở trang
    default_numbers = [
        "0923883737", "0586716868", "0962771111", "0926224422",
        "0563889988", "0583309309", "0924432929", "0923219979",
        "0589205205", "0583788668",
    ]

    # Phân tích các số mặc định
    default_results = []
    for number in default_numbers:
        result = identify_beautiful_sequences_with_positions(number)  # Kết quả result
        number_add_dot = add_dot_to_number(number, result) 
        number_split = split_number(number_add_dot)# Thêm dấu chấm phân tách giữa các khoảng

        # Xác định style cho từng phần của số
        styles = analysis_append_color(number_split, result)
        
        # Xác định format cho mỗi khoảng
        format = analysis_append_format(number_split, result)

        default_results.append({
            'result': result,
            'split_number': number_split,
            'styles': styles,
            'format': format
        })

    return render_template('index.html', default_results=default_results)

@app.route("/analyze", methods=["POST"])
def analyze_number():
    # Lấy số điện thoại từ form
    
    number = request.form.get('phone_number')
    if number:
        # Phân tích số mới
        result = identify_beautiful_sequences_with_positions(number)
        number_add_dot = add_dot_to_number(number, result)
        number_split = split_number(number_add_dot)  # Thêm dấu chấm phân tách giữa các khoảng
        
        # Xác định style cho từng phần của số
        styles = analysis_append_color(number_split, result)
        
        format = analysis_append_format(number_split, result)
        data = {
            'result': result,
            'split_number': number_split,
            'styles': styles,
            'format': format
        }
        
        # Trả về kết quả dưới dạng JSON
        return jsonify(data)
    
    return jsonify({"error": "Invalid input"})

@app.route("/search", methods=["POST", "GET"])
def search():
    phone_number = request.form.get('phone')
    if phone_number is None:
        phone_number = request.args.get('phone', "", type = str)
        
    if phone_number is None:
        show_page_index()
    page = request.args.get('page', 1, type=int)
    size = 49  # Số bản ghi trên mỗi trang
    from_index = (page - 1) * size
    
    response = search_phone(phone_number, size, from_index)
    data = response["data"]
    total = response["total"]
    total_page = (total + size - 1) // size  # Tính tổng số trang
    
    #nếu chưa tồn tại số có 10 chữ số thì phân tích + lưu vào elastic 
    if not data and len(phone_number) == 10:
        # lưu dữ liệu:
        print("save data")
        save_data(phone_number)
        # thêm dữ liệu mới vào data để phân tích và hiển thị kết quá
        data = [{"f": phone_number}]
        # Cập nhập lại dữ liệu tổng số trang: total_page
        total_page = 1
    # Phân tích các số mặc định
    default_results = []
    for item in data:
        number = item['f']
        
        result = identify_beautiful_sequences_with_positions(number)  # Kết quả result
        number_add_dot = add_dot_to_number(number, result) 
        number_split = split_number(number_add_dot)

        # Xác định style cho từng phần của số
        styles = analysis_append_color(number_split, result)
        
        # Xác định format cho từng split của cố
        format = analysis_append_format(number_split, result)

        # Lưu kết quả từng số với các phần đã được phân tách và style
        default_results.append({
            'result': result,
            'split_number': number_split,
            'styles': styles,
            'format': format,
            'phone': number
        })

    return render_template('page_sim.html', default_results=default_results, current_page=page, page_url="search", number=phone_number, total_page=total_page)
    

@app.route('/')
def show_page_index():
    # Lấy số trang từ tham số URL, mặc định là 1
    page = request.args.get('page', 1, type=int)
    size = 49  # Số bản ghi trên mỗi trang
    from_index = (page - 1) * size

    response = get_data_elastis(from_index, size)
    data = response["data"]  # Lấy mảng kết quả

    # Phân tích các số mặc định
    default_results = []
    for item in data:
        number = item['f']
        
        result = identify_beautiful_sequences_with_positions(number)  # Kết quả result
        number_add_dot = add_dot_to_number(number, result) 
        number_split = split_number(number_add_dot)

        # Xác định style cho từng phần của số
        styles = analysis_append_color(number_split, result)
        
        # Xác định format cho từng split của cố
        format = analysis_append_format(number_split, result)

        # Lưu kết quả từng số với các phần đã được phân tách và style
        default_results.append({
            'result': result,
            'split_number': number_split,
            'styles': styles,
            'format': format,
            'phone': number
        })
    
    return render_template('page_sim.html', default_results=default_results, current_page=page, page_url="show_page_index")

def get_data_elastis(from_index, size):
    query = {
        "query": {
            "match_all": {}
        },
        "_source": [
            "f"
        ],
        "size": size,  # Lấy số bản ghi theo kích thước đã chỉ định
        "from": from_index  # Chỉ định điểm bắt đầu
    }
    
    try:
        response = elastic_local.search(index="sim_number", body=query)
        hits = response["hits"]["hits"]
        results = [hit["_source"] for hit in hits]
        total = response["hits"]["total"]["value"]
        return { "data": results, "total": total }

    except Exception as e:
        return {"error": str(e)}

@app.route('/detail')
def detail_analysis():
    # Lấy thông tin từ query parameter 'id'
    phone_id = request.args.get('id', None)
    # Lấy dữ liệu từ Elasticsearch dựa trên số điện thoại
    data_list = get_detail_sim(phone_id)  # Giả sử hàm trả về danh sách các kết quả
    
    if data_list and isinstance(data_list, list) and len(data_list) > 0:
        data = data_list[0]  # Truy xuất phần tử đầu tiên trong danh sách kết quả
    else:
        return jsonify({"error": "Không tìm thấy dữ liệu cho số điện thoại này"}), 404
    
    # Chuẩn bị dữ liệu trả về
    result = {
        "Phone Number": phone_id,
        "Dãy đẹp đầu": data.get('dau_dep', 'Không có dữ liệu'),
        "Dạng đẹp đầu": data.get('dau_dang', 'Không có dữ liệu'),
        "Dãy đẹp giữa": data.get('giua_dep', 'Không có dữ liệu'),
        "Dạng đẹp giữa": data.get('giua_dang', 'Không có dữ liệu'),
        "Vị trí đẹp giữa": data.get('giua_index', 'Không có dữ liệu'),
        "Dãy đẹp đuôi": data.get('duoi_dep', 'Không có dữ liệu'),
        "Dạng đẹp đuôi": data.get('duoi_dang', 'Không có dữ liệu'),
        "Vị trí đuôi": data.get('duoi_index', 'Không có dữ liệu'),
        "Số lượng phím": data.get('sl_phim', 'Không có dữ liệu'),
        "Comment": data.get('comment',"Chưa có bình luận cũ")
    }
    
    return jsonify(result)

@app.route("/update_comment", methods=["POST"])
def update_comment():
    # Lấy id từ query parameters
    id = request.args.get('id', "", type=str)
    
    # Lấy comment từ body của yêu cầu
    data = request.get_json()
    comment = data.get('comment', "")

    # Kiểm tra nếu id và comment không rỗng
    if not id or not comment:
        return jsonify({"error": "ID hoặc bình luận không hợp lệ"}), 400
    
    # Lưu comment vào Elasticsearch (thay thế save_comment bằng logic của bạn)
    save_comment(id, comment)
    
    return jsonify({"message": "Bình luận đã được cập nhật thành công"}), 200

if __name__ == "__main__":
  app.run(debug=True, port=8080)
