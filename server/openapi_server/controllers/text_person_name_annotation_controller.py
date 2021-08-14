import connexion
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_person_name_annotation_request import TextPersonNameAnnotationRequest  # noqa: E501
from openapi_server.models.text_person_name_annotation_response import TextPersonNameAnnotationResponse  # noqa: E501
from openapi_server.models.text_person_name_annotation import TextPersonNameAnnotation
from openapi_server import neuro_model as model


def create_text_person_name_annotations():  # noqa: E501
    """Annotate person names in a clinical note

    Return the person name annotations found in a clinical note # noqa: E501

    :rtype: TextPersonNameAnnotationResponse
    """
    res = None
    status = None
    if connexion.request.is_json:
        try:
            annotation_request = TextPersonNameAnnotationRequest.from_dict(connexion.request.get_json())  # noqa: E501
            note = annotation_request._note  # noqa: E501
            annotations = []
            matches = model.predict(note._text)
            add_name_annotation(annotations, matches)
            res = TextPersonNameAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            res = Error("Internal error", status, str(error))
    return res, status


def add_name_annotation(annotations, matches):
    """
    Converts matches to TextContactAnnotation objects and adds them to the
    annotations array specified.
    """
    for match in matches:
        if match['type'] in ["NAME", "PER"]:
            annotations.append(TextPersonNameAnnotation(
                start=match['start'],
                length=len(match['text']),
                text=match['text'],
                confidence=95.5
            ))
