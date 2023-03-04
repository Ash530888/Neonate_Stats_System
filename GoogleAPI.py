import json
def handwritten_v2(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    import os
    # json file should be changed to your account
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service.json"
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    tr = vision.ImageContext(language_hints=["en-t-i0-handwrit"])
    image = vision.Image(content=content)
    text = []

    response = client.document_text_detection(image=image, image_context=tr)

    #response = client.document_text_detection(image=image)
    for page in response.full_text_annotation.pages:
        #print(page)
        for block in page.blocks:
            confidence = block.confidence
            #print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                #print('Paragraph confidence: {}'.format(
                #paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    text.append(word_text)
                    #print('Word text: {} (confidence: {})'.format(
                    #word_text, word.confidence))

                    #for symbol in word.symbols:
                        #print('\tSymbol: {} (confidence: {})'.format(
                        #symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    print("Confidence of Google:",confidence)
    print("Text of Google:",text)
    return confidence,text