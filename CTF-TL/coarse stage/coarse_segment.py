def yolo(file_path):
    data = []
    results = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                values = line.strip().split()
                if len(values) >= 11:
                    data.append([float(values[9]), float(values[10])])
    except Exception as e:
        print(f"读取文件出错: {e}")
        return

    data = np.array(data)
    if len(data) == 0:
        print("文件为空或格式不正确")
        return

    non_zero_mask = data[:, 1] != 0
    start_idx = 0
    
    while start_idx < len(data):
        if non_zero_mask[start_idx]:
            end_idx = start_idx
            while end_idx < len(data) and non_zero_mask[end_idx]:
                end_idx += 1
            
            if end_idx - start_idx >= 3:
                sequence = data[max(start_idx-2,0):min(end_idx+2,len(data)), 0]
                if not all(x == sequence[0] for x in sequence):
                    count_0 = np.sum(sequence == 0)
                    count_1 = np.sum(sequence == 1)
                    total_count = len(sequence)
                    
                    if (set(sequence) == {0, 1} or set(sequence) == {0.0, 1.0}):
                        if (count_0 / total_count >= 0.05 and count_1 / total_count >= 0.05):
                            if np.sum(sequence[:10] == 0) / 10 > 0.5:
                                behavior = "turn_over: chest to side"
                            else:
                                behavior = "turn_over: side to chest"
                            
                        else:
                            behavior = "unknown"
                    else:
                        if abs(sequence[0] - sequence[-1]) < 1e-6:
                            behavior = "unknown"
                        elif sequence[0] > sequence[-1]:
                            behavior = "down"
                        else:
                            behavior = "up"

                    
                    result = {
                        "behavior": behavior,
                        "start_time": float((start_idx + 1)/25),
                        "end_time": float(end_idx/25)
                    }
                    results.append(result)
                    results = [r for r in results if r['behavior'] != 'unknown']
            
            start_idx = end_idx
        else:
            start_idx += 1
    return results