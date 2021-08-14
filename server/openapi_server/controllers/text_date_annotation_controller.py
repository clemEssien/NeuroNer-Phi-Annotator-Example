import connexion
import re

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_date_annotation_request import \
    TextDateAnnotationRequest  # noqa: E501
from openapi_server.models.text_date_annotation import TextDateAnnotation
from openapi_server.models.text_date_annotation_response import \
    TextDateAnnotationResponse  # noqa: E501
from openapi_server import neuro_model as model


def create_text_date_annotations():  # noqa: E501
    """Annotate dates in a clinical note

    Return the date annotations found in a clinical note # noqa: E501

    :rtype: TextDateAnnotations
    """
    res = None
    status = None
    if connexion.request.is_json:
        try:
            annotation_request = TextDateAnnotationRequest.from_dict(
                connexion.request.get_json())  # noqa: E501
            note = annotation_request._note
            annotations = []
            matches = model.predict(note._text)
            add_date_annotation(annotations, matches)
            res = TextDateAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            print(error)
            res = Error("Internal error", status, str(error))
    return res, status


def add_date_annotation(annotations, matches):
    """
    Converts matches to TextDateAnnotation objects and adds them to the
    annotations array specified.
    """
    for match in matches:
        if match['type'] in ["DATE"]:
            annotations.append(TextDateAnnotation(
                start=match['start'],
                length=len(match['text']),
                text=match['text'],
                date_format='MM/DD/YYYY',
                confidence=95.5
            ))

    for match in matches:
        if match['type'] in ["DATE"]:
            annotations.append(TextDateAnnotation(
                start=match['start'],
                length=len(match['text']),
                text=match['text'],
                date_format=match['type'].lower(),
                confidence=95.5
            ))


def get_date_format(date_str):
    date_pattern = {"MM/DD/YYYY": "([1-9]|0[1-9]|1[0-2])(/)\
                    ([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(/)(19[0-9][0-9]|20[0-9][0-9])",
                    "DD.MM.YYYY": "([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\\.)([1-9]|0[1-9]\
                    |1[0-2])(\\.)(19[0-9][0-9]|20[0-9][0-9])",
                    "YYYY": "([1-9][1-9][0-9][0-9]|2[0-9][0-9][0-9])",
                    "MMMM": "(January|February|March|April|May|June|July|August|September|October|November|December)"
                    }
    found = 'UNKNOWN'
    for key in date_pattern.keys():
        if re.search(date_pattern[key], date_str):
            found = key
            return found
        else:
            continue
    return found
