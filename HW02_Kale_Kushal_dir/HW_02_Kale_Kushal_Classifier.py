def classify_based_on_threshold(threshold, data):             #new classifier content
    data_after_classification = {1: [], 2: []}
    for speed in data:
        if speed < threshold:
            data_after_classification[1].append(speed)
        else:
            data_after_classification[2].append(speed)
    return data_after_classification