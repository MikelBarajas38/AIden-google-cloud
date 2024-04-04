import functions_framework
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
        vid_uri = request_json['uri']
    elif request_args and 'prompt' in request_args:
        req_prompt = request_args['prompt']
        vid_uri = request_args['uri']
    else:
        req_prompt = 'Please help me take care of my plants'
        vid_uri = 'test-img-aiden/screenshot'

    PROJECT_ID = 'aiden-419204'  
    LOCATION = 'us-central1' 
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    config = {
       "temperature": 0.2
    }

    multimodal_model = GenerativeModel('gemini-1.0-pro-vision')

    gcs_uri = f'gs://{vid_uri}'
    vid = Part.from_uri(gcs_uri, mime_type='video/x-msvideo')

    prompt = f'{req_prompt}. Make reference to the video when possible.'
    contents = [vid, prompt]

    responses = multimodal_model.generate_content(contents, stream=True, generation_config = config)

    response_string = ''
    for response in responses:
      response_string += response.text

    return response_string
