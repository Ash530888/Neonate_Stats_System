def handwritten_Azure(path):
    from azure.cognitiveservices.vision.computervision import ComputerVisionClient
    from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
    from msrest.authentication import CognitiveServicesCredentials
    from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
    import time
    import os
    # here region and key should be modified to your account detail
    region = "eastus"
    key = "b420eaf62d1748018ef965bce6854fb1"

    credentials = CognitiveServicesCredentials(key)
    client = ComputerVisionClient(
        endpoint="https://" + region + ".api.cognitive.microsoft.com/",
        credentials=credentials
    )

    import cv2
    # Async SDK call

    raw = True
    numberOfCharsInOperationId = 36
    read_image = open(path, "rb")
    # Call API with image and raw response (allows you to get the operation location)
    read_response = client.read_in_stream(read_image,language="en", raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]
    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
    # Print results, line by line
    confidence = 0
    count = 0
    text = []
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:

            for line in text_result.lines:
                count +=1
                text.append(line.text)
                confidence += line.appearance.style.confidence
    if count==0:
        confidence = confidence
        text = "NULL"
        print("Confidence of Azure:",confidence)
        print("Text of Azure:","NULL")
    else:
        confidence = confidence/count
        print("Confidence of Azure:",confidence)
        print("Text of Azure:",text)
    return confidence,text
"""
# SDK call
rawHttpResponse = client.read(imgfile, language="en", raw=True)
print(rawHttpResponse)
# Get ID from returned headers
operationLocation = rawHttpResponse.headers["Operation-Location"]
idLocation = len(operationLocation) - numberOfCharsInOperationId
operationId = operationLocation[idLocation:]

# SDK call
result = client.get_read_result(operationId)

# Get data
if result.status == OperationStatusCodes.succeeded:

    for line in result.analyze_result.read_results[0].lines:
        print(line.text)
        print(line.bounding_box)
"""
#handwritten_Azure("2.jpg")