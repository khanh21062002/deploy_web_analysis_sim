from analysis_sim import identify_beautiful_sequences_with_positions

def count_type_number(number):
    store = set()
    count = 0
    for digit in number:
      if digit not in store:
        count += 1
        store.add(digit)
        
    return count
  
   
def add_dot_to_number(number, result):
  #check phần số đẹp đầu trước
  is_head = 0
  is_tail = 0
  if result["Dãy đẹp đầu"]:
    length_day_dep_dau = len(result["Dãy đẹp đầu"])
    number = number[:length_day_dep_dau] + '.' + number[length_day_dep_dau:]
    is_head = 1
  
  if result["Dãy đẹp đuôi"]:
    number = number[:result["Vị trí đuôi"] + is_head] + '.' + number[result["Vị trí đuôi"] + is_head:]
    is_tail = 1
    
  #print(f"Dạng dãy giữa: {result["Vị trí giữa"][0]}")
    
  if result["Vị trí giữa"]:
      # Thêm các dấu vào vị trí trước và sau của dãy giữa đầu tiên
    leng_giua = len(result["Dãy đẹp giữa"][0])
    #Thêm dấu . ở sau nếu chưa có
    
    if number[result["Vị trí giữa"][0] + is_head + leng_giua] != '.':
      number = number[:result["Vị trí giữa"][0] + is_head + leng_giua] + '.' + number[result["Vị trí giữa"][0] + is_head + leng_giua:]
      
    #print(f"Check vị trí thứ: {result["Vị trí giữa"][0] + is_head - 1} của số : {number}")
    if number[result["Vị trí giữa"][0] + is_head - 1] != '.': 
      # Thêm dấu . ở trước
      number = number[:result["Vị trí giữa"][0] + is_head] + '.' + number[result["Vị trí giữa"][0] + is_head:]
      
    # Nếu có dãy giữa thứ 2 thì tiến hành thêm chấm/ không thì thôi
    if len(result["Dãy đẹp giữa"]) > 1 and result["Dãy đẹp giữa"][1]:
        # lấy độ dài của chính nó
        leng_giua = len(result["Dãy đẹp giữa"][1])
        number_of_dot_before = number.count('.') - is_tail
        # Nếu 
        if number[result["Vị trí giữa"][1] + number_of_dot_before + leng_giua] != '.':
            number = number[:result["Vị trí giữa"][1] + number_of_dot_before + leng_giua] + '.' + number[result["Vị trí giữa"][1] + number_of_dot_before + leng_giua:]
        
        #print(f"Check vị trí thứ: {result["Vị trí giữa"][0] + is_head - 1} của số : {number}")
        if number[result["Vị trí giữa"][1] + number_of_dot_before - 1] != '.': 
        # Thêm dấu . ở trước
            number = number[:result["Vị trí giữa"][1] + number_of_dot_before] + '.' + number[result["Vị trí giữa"][1] + number_of_dot_before:]
  return number 
#0459.33.2770
  
def split_number(number_with_dots):
    # Tách số thành các phần dựa trên dấu chấm
    return number_with_dots.split('.')
  
def analysis_append_color(number_split, result):
  styles = []
      # Theo cá nhân đang đánh giá thì khi chuỗi chỉ tách thành 2 đoạn thì giữa thường k có
  if len(number_split) == 2:
      for i, part in enumerate(number_split):
          if i == 0 and part == result.get("Dãy đẹp đầu", ""):
              styles.append('red-text')  # Đoạn đầu màu đỏ
          elif i == len(number_split)-1 and part == result.get("Dãy đẹp đuôi", ""):
              styles.append('yellow-text')  # Đoạn cuối màu vàng
          else:
              styles.append('default-text')  # Các đoạn khác màu đen
          
  # Nếu có 3 đoạn thì khả năng sẽ có từ dãy đẹp trở lên, có khả năng có cả ở giữa        
  if len(number_split) == 3:
      for i, part in enumerate(number_split):
          if i == 0 and part == result.get("Dãy đẹp đầu", ""):
              styles.append('red-text')  # Đoạn đầu màu đỏ
          elif i == 1 and part in result.get("Dãy đẹp giữa", []):
              styles.append('blue-text')  # Đoạn giữa màu xanh dương
          elif i == 2 and part == result.get("Dãy đẹp đuôi", ""):
              styles.append('yellow-text')  # Đoạn cuối màu vàng
          else:
              styles.append('default-text')  # Các đoạn khác màu đen
              
  # Nếu chiaw thành 4 đoạn thì khả năng cao sẻ có 3 dãy đẹp trở lên            
  if len(number_split) == 4:
      for i, part in enumerate(number_split):
          if i == 0 and part == result.get("Dãy đẹp đầu", ""):
              styles.append('red-text')  # Đoạn đầu màu đỏ
          elif i == 1 and part in result.get("Dãy đẹp giữa", []):
              styles.append('blue-text')  # Đoạn giữa màu xanh dương
          elif i == 2 and part in result.get("Dãy đẹp giữa", []):
              styles.append('blue-text')  # Đoạn giữa màu xanh dương    
          elif i == 3 and part == result.get("Dãy đẹp đuôi", ""):
              styles.append('yellow-text')  # Đoạn cuối màu vàng
          else:
              styles.append('default-text')  # Các đoạn khác màu đen
              
  if len(number_split) == 5:
      for i, part in enumerate(number_split):
          if i == 0 and part == result.get("Dãy đẹp đầu", ""):
              styles.append('red-text')  # Đoạn đầu màu đỏ
          elif i == 1 and part in result.get("Dãy đẹp giữa", []):
              styles.append('blue-text')  # Đoạn giữa màu xanh dương
          elif i == 2 and part in result.get("Dãy đẹp giữa", []):
              styles.append('blue-text')  # Đoạn giữa màu xanh dương   
          elif i == 3 and part in result.get("Dãy đẹp giữa", []):
              styles.append('blue-text')  # Đoạn giữa màu xanh dương    
          elif i == 4 and part == result.get("Dãy đẹp đuôi", ""):
              styles.append('yellow-text')  # Đoạn cuối màu vàng
          else:
              styles.append('default-text')  # Các đoạn khác màu đen
              
  return styles
  
  
def analysis_append_format(number_split, result):
    format = []
        # Theo cá nhân đang đánh giá thì khi chuỗi chỉ tách thành 2 đoạn thì giữa thường k có
    if len(number_split) == 2:
        for i, part in enumerate(number_split):
            if i == 0 and part == result.get("Dãy đẹp đầu", ""):
                format.append(result["Dạng đẹp đầu"])  # Đoạn đầu màu đỏ
            elif i == len(number_split)-1 and part == result.get("Dãy đẹp đuôi", ""):
                format.append(result["Dạng đẹp đuôi"])  # Đoạn cuối màu vàng
            else:
                array = "&nbsp;" * len(part) * 2  # Tạo chuỗi khoảng trắng tương ứng với độ dài của phần
                format.append(array)
            
    # Nếu có 3 đoạn thì khả năng sẽ có từ dãy đẹp trở lên, có khả năng có cả ở giữa        
    if len(number_split) == 3:
        for i, part in enumerate(number_split):
            if i == 0 and part == result.get("Dãy đẹp đầu", ""):
                format.append(result["Dạng đẹp đầu"])  # Đoạn đầu màu đỏ
            elif i == 1 and part in result.get("Dãy đẹp giữa", []):
                format.append(result["Dạng đẹp giữa"][0])  # Đoạn giữa màu xanh dương
            elif i == 2 and part == result.get("Dãy đẹp đuôi", ""):
                format.append(result["Dạng đẹp đuôi"])  # Đoạn cuối màu vàng
            else:
                array = "&nbsp;" * len(part) * 2  # Tạo chuỗi khoảng trắng tương ứng với độ dài của phần
                format.append(array)
                
    # Nếu chiaw thành 4 đoạn thì khả năng cao sẻ có 3 dãy đẹp trở lên            
    if len(number_split) == 4:
        for i, part in enumerate(number_split):
            if i == 0 and part == result.get("Dãy đẹp đầu", ""):
                format.append(result["Dạng đẹp đầu"])  # Đoạn đầu màu đỏ
            elif i == 1 and part in result.get("Dãy đẹp giữa", []):
                format.append(result["Dạng đẹp giữa"][0])  # Đoạn giữa màu xanh dương
            elif i == 2 and part in result.get("Dãy đẹp giữa", []):
                format.append(result["Dạng đẹp giữa"][0])
            elif i == 2 and len(result["Dãy đẹp giữa"]) >=2 and part == result.get(["Dãy đẹp giữa"][0],""): 
                format.append(result["Dạng đẹp giữa"][0])  
            elif i == 2 and len(result["Dãy đẹp giữa"]) >=2 and part == result.get(["Dãy đẹp giữa"][1],""): 
                format.append(result["Dạng đẹp giữa"][1])     
            elif i == 3 and part == result.get("Dãy đẹp đuôi", ""):
                format.append(result["Dạng đẹp đuôi"])  # Đoạn cuối màu vàng
            else:
                array = "&nbsp;" * len(part) # Tạo chuỗi khoảng trắng tương ứng với độ dài của phần
                format.append(array)
                
    if len(number_split) == 5:
        # Lưu các giá trị vào biến để giảm số lần gọi
        dãy_đẹp_đầu = result.get("Dãy đẹp đầu", "")
        dãy_đẹp_giữa = result.get("Dãy đẹp giữa", [])
        dãy_đẹp_đuôi = result.get("Dãy đẹp đuôi", "")
        
        # Tạo danh sách định dạng
        for i, part in enumerate(number_split):
            if i == 0:  # Đoạn đầu
                if part == dãy_đẹp_đầu:
                    format.append(result["Dạng đẹp đầu"])  # Màu đỏ
                else:
                    format.append("&nbsp;" * len(part))  # Khoảng trắng
            elif i == 1:  # Đoạn giữa đầu tiên
                if part in dãy_đẹp_giữa:
                    format.append(result["Dạng đẹp giữa"][0])  # Màu xanh dương
                else:
                    format.append("&nbsp;" * len(part))  # Khoảng trắng
            elif i == 2:  # Đoạn giữa thứ hai
                if len(dãy_đẹp_giữa) > 1:
                    if part == dãy_đẹp_giữa[0]:
                        format.append(result["Dạng đẹp giữa"][0])
                    elif part == dãy_đẹp_giữa[1]:
                        format.append(result["Dạng đẹp giữa"][1])
                    else:
                        format.append("&nbsp;" * len(part))  # Khoảng trắng
                else:
                    format.append("&nbsp;" * len(part))  # Khoảng trắng
            elif i == 3:  # Đoạn giữa thứ hai (nếu có)
                if part in dãy_đẹp_giữa:
                    format.append(result["Dạng đẹp giữa"][1] if len(dãy_đẹp_giữa) > 1 else result["Dạng đẹp giữa"][0])
                else:
                    format.append("&nbsp;" * len(part))  # Khoảng trắng
            elif i == 4:  # Đoạn cuối
                if part == dãy_đẹp_đuôi:
                    format.append(dãy_đẹp_đuôi)  # Màu vàng
                else:
                    format.append("&nbsp;" * len(part))  # Khoảng trắng
                
    return format
  
def count_dots(sim_number):
    return sim_number.count('.')

# Test
number = "0589205205"
print(count_type_number("1122456"))