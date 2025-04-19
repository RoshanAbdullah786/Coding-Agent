


def response_text(text):
    return [
        {
            "type":"text",
            "text":text
        }
    ]

def response_text_and_image(text,image):
    return [
      {
        "type": "text",
        "text": text,
      },
      {
        "type": "image_url",
        "image_url": {
          "url": image,
        }
      }
    ]