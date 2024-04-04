import functions_framework
from google.cloud import storage
import vertexai

from vertexai.generative_models import (
    GenerativeModel,
    Image,
    Part,
)

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'prompt' in request_json:
        req_prompt = request_json['prompt']
    elif request_args and 'prompt' in request_args:
        req_prompt = request_args['prompt']
    else:
        name = 'Please help me take care of my plants'

    PROJECT_ID = 'aiden-419204'  
    LOCATION = 'us-central1' 
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    multimodal_model = GenerativeModel('gemini-1.0-pro-vision')

    gcs_uri = 'gs://test-img-aiden/screenshot'
    image = Part.from_uri(gcs_uri, mime_type='image/png')

    prompt = f'{req_prompt}. Make reference to the image when possible.'
    contents = [image, prompt]

    responses = multimodal_model.generate_content(contents, stream=True)

    response_string = ''
    for response in responses:
      response_string += response.text

    return response_string
