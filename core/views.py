from django.conf import settings
import requests
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError

from django.core.files.storage import FileSystemStorage

# Setups
# This should be stored in a .env file in production
RAPIDAPI_KEY = "api-key"
DEMO_IMG = "https://traleor.com/images/image_2.png"

if settings.DEBUG == True:
    BASE_URL = "http://localhost:8000"
else:
    BASE_URL = "https://example.com"


class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


def call_microsoft_vision(image_url):
    """
    Calls Microsoft Vision API
    """
    vision_url = "https://microsoft-computer-vision3.p.rapidapi.com/ocr"
    headers = {
      "content-type": "application/json",
      "X-RapidAPI-Key": RAPIDAPI_KEY,
      "X-RapidAPI-Host": "microsoft-computer-vision3.p.rapidapi.com"
    }
    querystring = {"detectOrientation":"true","language":"en"}
    data = {
        # "url": image_url
        # If debug is true, use demo image
        "url": DEMO_IMG if settings.DEBUG == True else BASE_URL + image_url
    }
    print("DATA: Image Url", data)
    response = requests.post(vision_url, json=data, headers=headers, params=querystring)
    return response.json()


def ocr_image(request):
    """
    Gets Image and pass Url to call_microsoft_vision
    """
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        # print("Image", image.file)
        _image = fss.save(image.name, image)
        # image details
        image_url = fss.url(_image)
        res = call_microsoft_vision(image_url)

        # get text from response and format it
        output = "<br>"
        try:
            for region in res['regions']:
                for line in region['lines']:
                    sentence = ""
                    for word in line['words']:
                        sentence += word['text']
                        # add space
                        sentence += " "
                    output += "<p>" + sentence + "</p>"
                output += "<br><hr><br>"
        except Exception as e:
            output = "Error, Contact Developer with this information: " + str(e) + " " + str(res)
            print("Error", str(e) + " " + str(res))

        print("Output", output)

        return TemplateResponse(request, "core/ocr_image.html", 
            {
            "message": "Image Scanned successfully",
            "output": output
            }
        )

    except MultiValueDictKeyError:
        return TemplateResponse(request, "core/ocr_image.html", 
            {
            "message": "No Image Selected"
            }
        )

def ocr_test(request):
    """
    Test OCR Formatting
    """
    res = {
          "language": "en",
          "textAngle": 0.0,
          "orientation": "Up",
          "regions": [
            {
              "boundingBox": "147,411,304,128",
              "lines": [
                {
                  "boundingBox": "147,411,304,41",
                  "words": [{ "boundingBox": "147,411,304,41", "text": "SIGNATURE" }]
                },
                {
                  "boundingBox": "147,464,172,40",
                  "words": [{ "boundingBox": "147,464,172,40", "text": "ROLLS" }]
                },
                {
                  "boundingBox": "148,519,72,20",
                  "words": [
                    { "boundingBox": "148,519,13,20", "text": "3" },
                    { "boundingBox": "169,519,51,20", "text": "PCS" }
                  ]
                }
              ]
            },
            {
              "boundingBox": "509,28,258,497",
              "lines": [
                {
                  "boundingBox": "510,28,146,10",
                  "words": [
                    { "boundingBox": "510,28,41,10", "text": "PORK" },
                    { "boundingBox": "557,29,33,9", "text": "AND" },
                    { "boundingBox": "597,28,59,10", "text": "SHRIMP" }
                  ]
                },
                {
                  "boundingBox": "509,51,254,11",
                  "words": [
                    { "boundingBox": "509,51,23,9", "text": "Pork" },
                    { "boundingBox": "535,51,19,9", "text": "and" },
                    { "boundingBox": "557,51,39,11", "text": "Shrimm" },
                    { "boundingBox": "598,51,54,10", "text": "Vermicelli." },
                    { "boundingBox": "655,51,36,9", "text": "Pickled" },
                    { "boundingBox": "694,51,40,11", "text": "Medley." },
                    { "boundingBox": "737,51,26,10", "text": "Mint." }
                  ]
                },
                {
                  "boundingBox": "509,72,209,10",
                  "words": [
                    { "boundingBox": "509,72,41,9", "text": "Lettuce." },
                    { "boundingBox": "553,72,61,9", "text": "Cucumbers." },
                    { "boundingBox": "617,72,32,10", "text": "Crispy" },
                    { "boundingBox": "651,72,24,9", "text": "rolls." },
                    { "boundingBox": "678,72,40,8", "text": "Cilantro" }
                  ]
                },
                {
                  "boundingBox": "510,117,150,10",
                  "words": [
                    { "boundingBox": "510,117,106,10", "text": "LEMONGRASS" },
                    { "boundingBox": "623,117,37,10", "text": "BEEF" }
                  ]
                },
                {
                  "boundingBox": "573,140,194,11",
                  "words": [
                    { "boundingBox": "573,140,26,9", "text": "Beef." },
                    { "boundingBox": "602,140,53,10", "text": "Vermicelli." },
                    { "boundingBox": "698,140,40,11", "text": "Medley." },
                    { "boundingBox": "741,140,26,10", "text": "Mint." }
                  ]
                },
                {
                  "boundingBox": "509,160,105,10",
                  "words": [
                    { "boundingBox": "509,160,41,10", "text": "Lettuce." },
                    { "boundingBox": "553,160,61,10", "text": "Cucumbers." }
                  ]
                },
                {
                  "boundingBox": "510,205,173,11",
                  "words": [
                    { "boundingBox": "510,205,97,11", "text": "FIVE-SPICED" },
                    { "boundingBox": "614,206,69,10", "text": "CHICKEN" }
                  ]
                },
                {
                  "boundingBox": "509,228,245,11",
                  "words": [
                    { "boundingBox": "509,228,60,11", "text": "Five-spiced" },
                    { "boundingBox": "572,228,43,10", "text": "Chicken." },
                    { "boundingBox": "618,228,53,10", "text": "Vermicelli." },
                    { "boundingBox": "713,228,41,11", "text": "Medley." }
                  ]
                },
                {
                  "boundingBox": "509,249,242,10",
                  "words": [
                    { "boundingBox": "509,249,26,9", "text": "Mint." },
                    { "boundingBox": "538,249,41,9", "text": "Lettuce." },
                    { "boundingBox": "645,249,33,10", "text": "Crispy" },
                    { "boundingBox": "680,249,24,9", "text": "rolls." },
                    { "boundingBox": "706,249,45,8", "text": "Avocado" }
                  ]
                },
                {
                  "boundingBox": "509,294,113,10",
                  "words": [
                    { "boundingBox": "509,294,64,10", "text": "GRILLED" },
                    { "boundingBox": "580,294,42,10", "text": "PORK" }
                  ]
                },
                {
                  "boundingBox": "545,317,193,10",
                  "words": [
                    { "boundingBox": "545,317,25,10", "text": "pork." },
                    { "boundingBox": "573,317,53,10", "text": "Vermicelli," },
                    { "boundingBox": "712,317,26,10", "text": "Mint." }
                  ]
                },
                {
                  "boundingBox": "553,337,175,11",
                  "words": [
                    { "boundingBox": "553,337,61,10", "text": "Cucumbers." },
                    { "boundingBox": "678,337,50,11", "text": "pineapple" }
                  ]
                },
                {
                  "boundingBox": "509,383,59,10",
                  "words": [{ "boundingBox": "509,383,59,10", "text": "SHRIMP" }]
                },
                {
                  "boundingBox": "509,405,250,11",
                  "words": [
                    { "boundingBox": "509,405,39,11", "text": "Shrimp." },
                    { "boundingBox": "551,406,53,9", "text": "Vermicelli." },
                    { "boundingBox": "607,406,36,8", "text": "Pickled" },
                    { "boundingBox": "690,405,25,11", "text": "Mint," },
                    { "boundingBox": "718,406,41,9", "text": "Lettuce." }
                  ]
                },
                {
                  "boundingBox": "572,426,126,11",
                  "words": [
                    { "boundingBox": "572,426,33,11", "text": "Crispy" },
                    { "boundingBox": "607,426,24,9", "text": "rolls." },
                    { "boundingBox": "634,426,25,8", "text": "Fried" },
                    { "boundingBox": "662,426,36,9", "text": "Shallot" }
                  ]
                },
                {
                  "boundingBox": "510,471,156,10",
                  "words": [
                    { "boundingBox": "510,472,52,9", "text": "HONEY" },
                    { "boundingBox": "569,472,51,9", "text": "BAKED" },
                    { "boundingBox": "626,471,40,10", "text": "TOFU" }
                  ]
                },
                {
                  "boundingBox": "509,494,96,11",
                  "words": [
                    { "boundingBox": "509,495,33,10", "text": "Honey" },
                    { "boundingBox": "545,494,31,9", "text": "Baked" },
                    { "boundingBox": "578,494,27,10", "text": "Tofu." }
                  ]
                },
                {
                  "boundingBox": "509,514,169,11",
                  "words": [
                    { "boundingBox": "509,514,26,10", "text": "Mint." },
                    { "boundingBox": "538,515,41,9", "text": "Lettuce." },
                    { "boundingBox": "582,514,61,10", "text": "Cucumbers." },
                    { "boundingBox": "646,514,32,11", "text": "Crispy" }
                  ]
                }
              ]
            },
            {
              "boundingBox": "823,46,68,471",
              "lines": [
                {
                  "boundingBox": "823,46,68,18",
                  "words": [{ "boundingBox": "823,46,68,18", "text": "$10.35" }]
                },
                {
                  "boundingBox": "832,134,59,19",
                  "words": [{ "boundingBox": "832,134,59,19", "text": "$8.85" }]
                },
                {
                  "boundingBox": "832,223,59,18",
                  "words": [{ "boundingBox": "832,223,59,18", "text": "$8.85" }]
                },
                {
                  "boundingBox": "832,311,59,19",
                  "words": [{ "boundingBox": "832,311,59,19", "text": "$8.85" }]
                },
                {
                  "boundingBox": "823,400,68,19",
                  "words": [{ "boundingBox": "823,400,68,19", "text": "$10.35" }]
                },
                {
                  "boundingBox": "832,498,59,19",
                  "words": [{ "boundingBox": "832,498,59,19", "text": "$8.85" }]
                }
              ]
            }
          ]
    }

    # get all the words in res['regions']
    output = "<br>"
    sentences = []
    for region in res['regions']:
        for line in region['lines']:
            sentence = ""
            for word in line['words']:
                sentence += word['text']
                # add space
                sentence += " "
            sentences.append(sentence)
            output += "<p>" + sentence + "</p>"
        output += "<br><hr><br>"

    return TemplateResponse(request, "core/ocr_image.html", 
        {
        "message": "Image Scanned successfully",
        "output": output
        }
    )
    
