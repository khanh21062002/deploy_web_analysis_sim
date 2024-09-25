import re
def identify_beautiful_sequences_with_positions(sim_number):
    # Định nghĩa các mẫu dãy số đẹp, bổ sung các quy tắc mới
    patterns = {
        "AAAAAAAAA": r"(\d)\1{8}",
        "ABCDEABCDE": r"(\d)(\d)(\d)(\d)(\d)\1\2\3\4\5",
        "ABABABABAB": r"(\d)(\d)\1\2\1\2\1\2\1\2",
        "ABCDEEDCBA": r"(\d)(\d)(\d)(\d)(\d)\5\4\3\2\1",
        "ABCDEABCDE1": r"(\d)(\d)(\d)(\d)(\d)\5\4\3\2(\d)",
        "ABCDEABCD1E": r"(\d)(\d)(\d)(\d)(\d)\1\2\3(\d)\5",
        "ABCDEABC1DE": r"(\d)(\d)(\d)(\d)(\d)\1\2(\d)\4\5",
        "ABCDEAB1CDE": r"(\d)(\d)(\d)(\d)(\d)\1(\d)\3\4\5",
        "ABCDEA1BCDE": r"(\d)(\d)(\d)(\d)(\d)(\d)\2\3\4\5",
        "ABBBBACCCC": r"(\d)(\d)\2{3}\1(\d)\3{3}",
        "ABCDE.FBCDE": r"(\d)(\d)(\d)(\d)(\d)(\d)\2\3\4\5",
        "AAAAAAAA": r"(\d)\1{7}",
        "ABCABCABC": r"(\d)(\d)(\d)\1\2\3\1\2\3",
        "AAABBBCCC": r"(\d)\1\1(\d)\2\2(\d)\3\3",
        "ABCDXDCBA": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)\9\8\7\6",
        "AAAAAAAAA+": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "345678910": r"345678910",
        "979899100": r"979899100",
        "AAAAAAAAA-": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "AAAAAAA": r"(\d)\1{6}",
        "ABCDABCD": r"(\d)(\d)(\d)(\d)\1\2\3\4",
        "ABABABAB": r"(\d)(\d)\1\2\1\2\1\2",
        "AABBCCDD": r"(\d)\1(\d)\2(\d)\3(\d)\4",
        "AAAABBBB": r"(\d)\1\1\1(\d)\2\2\2",
        "ABCDDCBA": r"(\d)(\d)(\d)(\d)\4\3\2\1",
        "AAAAAAAA+": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "ABCDABCD1": r"(\d)(\d)(\d)(\d)\1\2\3(\d)",
        "ABCDABC1D": r"(\d)(\d)(\d)(\d)\1\2(\d)\4",
        "ABCDAB1CD": r"(\d)(\d)(\d)(\d)\1(\d)\3\4",
        "ABCDA1BCD": r"(\d)(\d)(\d)(\d)(\d)\2\3\4",
        "45678910": r"45678910",
        "ABBBACCC": r"(\d)(\d)\2\2\1(\d)\3\3",
        "AAABAAAC": r"(\d)\1\1(\d)\1\1(\d)",
        "ABCDEBCD": r"(\d)(\d)(\d)(\d)(\d)\2\3\4",
        "ABCDAECD": r"(\d)(\d)(\d)(\d)\1(\d)\3\4",
        "ABCDABED": r"(\d)(\d)(\d)(\d)\1\2(\d)\4",
        "ABCDABCE": r"(\d)(\d)(\d)(\d)\1\2\3(\d)",
        "ABACADAE": r"(\d)(\d)\1(\d)\1(\d)\1(\d)",
        "ABCBDBEB": r"(\d)(\d)(\d)\2(\d)\2(\d)\2",
        "AAAAAAAA-": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "ABCDABCD-1": r"(\d)(\d)(\d)(\d)\1\2\3(\d)",
        "ABCDABC-1D": r"(\d)(\d)(\d)(\d)\1\2(\d)\4",
        "ABCDAB-1CD": r"(\d)(\d)(\d)(\d)\1(\d)\3\4",
        "ABCDA-1BCD": r"(\d)(\d)(\d)(\d)(\d)\2\3\4",
        "AAAAAA": r"(\d)\1{5}",
        "ABCXCBA": r"(\d)(\d)(\d)(\d)\3\2\1",
        "AAAAAAA+": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "5678910": r"5678910",
        "9899100": r"9899100",
        "AAAAAAA-": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "AAAAA": r"(\d)\1{4}",
        "ABCABC": r"(\d)(\d)(\d)\1\2\3",
        "ABABAB": r"(\d)(\d)\1\2\1\2",
        "AABBCC": r"(\d)\1(\d)\2(\d)\3",
        "AAABBB": r"(\d)\1\1(\d)\2\2",
        "ABCCBA": r"(\d)(\d)(\d)\3\2\1",
        "ABCABC1": r"(\d)(\d)(\d)\1\2(\d)",
        "ABCAB1C": r"(\d)(\d)(\d)\1(\d)\3",
        "ABCA1BC": r"(\d)(\d)(\d)(\d)\2\3",
        "AAAAAA+": r"(\d)(\d)(\d)(\d)(\d)(\d)",
        "678910": r"678910",
        "ABBACC": r"(\d)(\d)\2\1(\d)\3",
        "AABAAC": r"(\d)\1(\d)\1\1(\d)",
        "ACCBCC": r"(\d)(\d)\2(\d)\2\2",
        "ABCDBC": r"(\d)(\d)(\d)(\d)\2\3",
        "ABACAD": r"(\d)(\d)\1(\d)\1(\d)",
        "ABCBDB": r"(\d)(\d)(\d)\2(\d)\2",
        "ABCABD": r"(\d)(\d)(\d)\1\2(\d)",
        "ABCADC": r"(\d)(\d)(\d)\1(\d)\3",
        "ABCABC-": r"(\d)(\d)(\d)\1\2(\d)",
        "ABCAB-C": r"(\d)(\d)(\d)\1(\d)\3",
        "ABCA-BC": r"(\d)(\d)(\d)(\d)\2\3",
        "AAAAAA-": r"(\d)(\d)(\d)(\d)(\d)(\d)",
        "AAAA": r"(\d)\1{3}",
        "ABXBA": r"(\d)(\d)(\d)\2\1",
        "AAAAA+": r"(\d)(\d)(\d)(\d)(\d)",
        "AAAAA++": r"13579",
        "AAAAA++": r"02468",
        "78910": r"78910",
        "91011": r"91011",
        "99100": r"99100",
        "AAAAA-": r"(\d)(\d)(\d)(\d)(\d)",
        "AAAAA--": r"97531",
        "AAAAA--": r"86420",
        "AAA": r"(\d)\1\1",
        "ABAB": r"(\d)(\d)\1\2",
        "AABB": r"(\d)\1(\d)\2",
        "ABBA": r"(\d)(\d)\2\1",
        "ABAB1": r"(\d)(\d)\1(\d)",
        "ABA1B": r"(\d)(\d)(\d)\2",
        "AAAA+": r"(\d)(\d)(\d)(\d)",
        "AAAA++": r"(\d)(\d)(\d)(\d)",
        "AAAA+": r"8910",
        "ABAC": r"(\d)(\d)\1(?!\2)(\d)",
        "ABCB": r"(\d)(\d)(\d)\2",
        "ABAB-": r"(\d)(\d)\1(\d)",
        "ABA-B": r"(\d)(\d)(\d)\2",
        "AAAA-": r"(\d)(\d)(\d)(\d)",
        "AAAA--": r"(\d)(\d)(\d)(\d)",
        "AA": r"(\d)\1",
        "AXA": r"(\d)(\d)\1",
        "AAA+": r"(\d)(\d)(\d)",
        "AAA++": r"(\d)(\d)(\d)",
        "AAA-": r"(\d)(\d)(\d)",
        "AAA--": r"(\d)(\d)(\d)",
        "AA1": r"(\d)(\d)"
    }
    
    detail_number = [69, 96, 68, 86, 39, 79, 38, 18, 16, 36, 365, 78, 389, 569, 369, 1102, 1314, 2204, 1368, 1369, 1569, 4078, 578, 2283, 1486, 9574]

    # Chuẩn hóa số sim bằng cách loại bỏ các ký tự không phải số
    if not isinstance(sim_number, str):
        sim_number = str(sim_number) if sim_number is not None else ''
    sim_number = re.sub(r'\D', '', sim_number)
    
    sim_number_backup = sim_number

    # Danh sách kết quả
    result = {
        "Dạng đẹp đầu": "",
        "Dãy đẹp đầu": "",
        "Vị trí đầu": "",
        "Dạng đẹp giữa": [],
        "Dãy đẹp giữa": [],
        "Vị trí giữa": [],
        "Dạng đẹp đuôi": "",
        "Dãy đẹp đuôi": "",
        "Vị trí đuôi": ""
    }

    def is_valid_pattern(pattern_name, sequence):
      match pattern_name:
          case "ABCB":
              return sequence[0] != sequence[1] != sequence[2]
          case "ABCCBA":
              return sequence[0] != sequence[1] != sequence[2]
          case "ABA-B":
              return int(sequence[0]) == int(sequence[2]) + 1
          case "ABAB-":
              return int(sequence[1]) == int(sequence[3]) + 1
          case "AAA+":
              if len(sequence) != 3:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) + 1:
                    return False
        
              return True
          case "AAA-":
              if len(sequence) != 3:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 1:
                    return False
        
              return True
          case "AAA++":
              if len(sequence) != 3:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) + 2:
                    return False
        
              return True
          case "AAA--":
              if len(sequence) != 3:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 2:
                    return False
        
              return True
          case "AAAA++":
              if len(sequence) != 4:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) + 2:
                    return False
        
              return True
          case "AAAA--":
              if len(sequence) != 4:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 2:
                    return False
        
              return True
          case "AAAA-":
              if len(sequence) != 4:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 1:
                    return False
        
              return True
          case "AAAA+":
              if len(sequence) != 4:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) + 1:
                    return False
        
              return True
          case "AAAAA-":
              if len(sequence) != 5:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 1:
                    return False
        
              return True
          case "AAAAA+":
              if len(sequence) != 5:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) + 1:
                    return False
        
              return True
          case "AAAAAA-":
              if len(sequence) != 6:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 1:
                    return False
        
              return True
          case "AAAAAAA-":
              if len(sequence) != 7:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 1:
                    return False
        
              return True
          case "AAAAAA+":
              if len(sequence) != 6:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) + 1:
                    return False
        
              return True
          case "AAAAAAA-":
              if len(sequence) != 7:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 1:
                    return False
        
              return True
          case "AAAAAAA+":
              if len(sequence) != 7:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) + 1:
                    return False
        
              return True
          case "AAAAAAAA-":
              if len(sequence) != 8:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 1:
                    return False
        
              return True
          case "ABCDABCD1":
              return len(sequence) == 8 and int(sequence[3]) == int(sequence[7]) - 1
          case "ABCDABC1D":
              return len(sequence) == 8 and int(sequence[2]) == int(sequence[6]) - 1
          case "ABCDAB1CD":
              return len(sequence) == 8 and int(sequence[1]) == int(sequence[5]) - 1
          case "ABCDA1BCD":
              return len(sequence) == 8 and int(sequence[0]) == int(sequence[4]) - 1
          case "AAAAAAAA+":
              if len(sequence) != 8:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) + 1:
                    return False
        
              return True
          case "AAAAAAAAA+":
              if len(sequence) != 9:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) + 1:
                    return False
        
              return True
          case "AAAAAAAAA-":
              if len(sequence) != 9:
                return False
            
              for i in range(1, len(sequence)):
                #print(f"{sequence[i]} and {sequence[i-1]}")
                if int(sequence[i]) != int(sequence[i-1]) - 1:
                    return False
        
              return True
          case "AABBCC":
              return len(set(sequence[:3])) == 3
          case "ABAC":
              # Đảm bảo rằng A, B, C phải khác nhau
              return len(set(sequence[:3])) == 3  # A, B, C phải là các số khác nhau
          case "AA1":
              return len(sequence) == 2 and int(sequence[1]) == int(sequence[0]) + 1  # Kiểm tra điều kiện AA1
          case "ABAB1":
              return (len(sequence) == 4 and
                      int(sequence[3]) + 1 == int(sequence[1]))  # Kiểm tra điều kiện ABAB1
          case "ABA1B":
              return (len(sequence) == 4 and
                      int(sequence[2]) + 1 == int(sequence[0]))
          case "ABCDEABCDE1":
              return (len(sequence) == 10 and
                      int(sequence[5]) == int(sequence[0]) and
                      int(sequence[6]) == int(sequence[1]) and
                      int(sequence[7]) == int(sequence[2]) and
                      int(sequence[8]) == int(sequence[3]) and
                      int(sequence[9]) == int(sequence[4]) + 1)  # Kiểm tra điều kiện ABCDEABCDE1
          case _ if pattern_name not in ["AA", "AAA", "AAAA", "AAAAA", "AAAAAA", "AAAAAAA", "AAAAAAAA", "AAAAAAAAA"]:
              unique_chars = set(sequence)
              return len(unique_chars) > 1  # Ít nhất 2 ký tự khác nhau
          case _:
              return True  # Các quy tắc AA, AAA,... không yêu cầu


    # Tìm dãy số đẹp ở đuôi
    # for pattern_name, pattern in sorted(patterns.items(), key=lambda x: -len(x[1])):  # Ưu tiên các mẫu dài nhất
    for pattern_name, pattern in patterns.items():
        match = re.search(pattern + r'$', sim_number)
        if match and is_valid_pattern(pattern_name, match.group()):
            result["Dạng đẹp đuôi"] = pattern_name
            result["Dãy đẹp đuôi"] = match.group()
            result["Vị trí đuôi"] = len(sim_number) - len(match.group())
            sim_number = sim_number[:-len(match.group())]  # Loại bỏ dãy đẹp đuôi
            break
          
    if result["Dạng đẹp đuôi"] == "":
      for length in range(1, 4):
          if length > len(sim_number):
              break  # Dừng lại nếu độ dài vượt quá chiều dài của sim_number
              
          end_segment = sim_number[-length:]

          if end_segment:  # Kiểm tra xem end_segment không rỗng
              if int(end_segment) in detail_number:
                  result["Dạng đẹp đuôi"] = "DN"
                  result["Dãy đẹp đuôi"] = end_segment
                  result["Vị trí đuôi"] = len(sim_number) - length
                  sim_number = sim_number[:-length]  # Loại bỏ dãy số đã đối chiếu
                  break

    # Tìm dãy số đẹp ở đầu
    # for pattern_name, pattern in sorted(patterns.items(), key=lambda x: -len(x[1])):  # Ưu tiên các mẫu dài nhất
    for pattern_name, pattern in patterns.items():
        match = re.match(pattern, sim_number)
        if match and is_valid_pattern(pattern_name, match.group()):
            result["Dạng đẹp đầu"] = pattern_name
            result["Dãy đẹp đầu"] = match.group()
            result["Vị trí đầu"] = 0
            sim_number = sim_number[len(match.group()):]  # Loại bỏ dãy đẹp đầu
            break
    if result["Dãy đẹp đầu"] == "":  # Sử dụng == thay vì is
        for size in range(2, 4):
            start_segment = sim_number[:size]
            # Kiểm tra nếu start_segment không phải là chuỗi trống
            if start_segment and start_segment.isdigit():
                if int(start_segment) in detail_number:
                    result["Dạng đẹp đầu"] = "DN"
                    result["Dãy đẹp đầu"] = start_segment
                    result["Vị trí đầu"] = 0
                    sim_number = sim_number[size:]  # Loại bỏ dãy số đã đối chiếu
                    break

    # Tìm các dãy số đẹp còn lại từ trái sang phải
    current_position = 0
    
    while sim_number:
        max_length = 0
        max_pattern_name = ""
        max_sequence = ""
        max_start_pos = -1

        # Duyệt qua tất cả các mẫu, ưu tiên theo độ dài hoặc ưu tiên bạn muốn
        for pattern_name, pattern in patterns.items():
            matches = list(re.finditer(pattern, sim_number))
            for m in matches:
                matched_string = m.group()
                start_pos = m.start()

                # Kiểm tra xem dãy có dài hơn dãy trước không và có khớp với điều kiện hợp lệ không
                if len(matched_string) > max_length and is_valid_pattern(pattern_name, matched_string):
                    max_length = len(matched_string)
                    max_pattern_name = pattern_name
                    max_sequence = matched_string
                    max_start_pos = start_pos

        # Nếu không tìm được dãy đẹp, thoát khỏi vòng lặp
        if max_length == 0:
            break

        # Nếu có dãy đẹp đầu, tính độ dài để cộng vị trí
        if result["Dãy đẹp đầu"] is not None:
            length_day_dep_dau = len(result["Dãy đẹp đầu"])
        else:
            length_day_dep_dau = 0

        # Lưu dãy số đẹp tìm được vào result
        result["Dãy đẹp giữa"].append(max_sequence)
        result["Dạng đẹp giữa"].append(max_pattern_name)
        result["Vị trí giữa"].append(current_position + max_start_pos + length_day_dep_dau)

        # Thay thế dãy số đẹp bằng 'x'
        sim_number = sim_number[:max_start_pos] + 'x' * len(max_sequence) + sim_number[max_start_pos + len(max_sequence):]
        current_position = 0  # Reset vị trí về đầu để duyệt toàn bộ dãy mới
  
    if len(result["Dạng đẹp giữa"]) >=2:
      result = reorder_sequences_by_phone_number(sim_number_backup, result)
      
    return result

def reorder_sequences_by_phone_number(phone_number, result):
    # Kết hợp các phần tử thành danh sách các tuple
    combined = list(zip(result["Dạng đẹp giữa"], result["Dãy đẹp giữa"], result["Vị trí giữa"]))

    # Sắp xếp danh sách theo vị trí trong số điện thoại
    combined.sort(key=lambda x: phone_number.find(x[1]))  # Sắp xếp theo vị trí trong số điện thoại

    # Tách lại thành ba danh sách
    result["Dạng đẹp giữa"], result["Dãy đẹp giữa"], result["Vị trí giữa"] = zip(*combined)

    # Chuyển đổi từ tuple về danh sách
    result["Dạng đẹp giữa"] = list(result["Dạng đẹp giữa"])
    result["Dãy đẹp giữa"] = list(result["Dãy đẹp giữa"])
    result["Vị trí giữa"] = list(result["Vị trí giữa"])

    return result


# #Chạy hàm với input mới
# sim_input = "0822131126"
# result = identify_beautiful_sequences_with_positions(sim_input)
# print(sim_input + ": " + str(result))
