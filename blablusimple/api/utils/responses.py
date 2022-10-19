from flask import make_response, jsonify


INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "code": "invalidField",
    "message": "Invalid fields found"
}

INVALID_INPUT_422 = {
    "http_code": 422,
    "code": "invalidInput",
    "message": "Invalid input"
}

MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "code": "missingParameter",
    "message": "Missing parameters."
}

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}

SERVER_ERROR_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Resource not found"
}

UNAUTHORIZED_403 = {
    "http_code": 403,
    "code": "notAuthorized",
    "message": "You are not authorised to execute this."
}

SUCCESS_200 = {
    'http_code': 200,
    'code': 'success'
}

SUCCESS_201 = {
    'http_code': 201,
    'code': 'success'
}

SUCCESS_204 = {
    'http_code': 204,
    'code': 'success'
}

USER_CREATED_SUCCESS_201 = {
    'http_code': 201,
    'code': 'success',
    'message': 'Your account has been created'
}

USERNAME_EMAIL_ALREADY_EXIST_422 = {
    'http_code': 422,
    'code': 'invalidField',
    'message': 'Username or email already exists'
}


USERNAME_CARD_ID_ALREADY_EXIST_422 = {
    'http_code': 422,
    'code': 'invalidField',
    'message': 'Card Id already exists'
}

USERNAME_CARD_ID_INVALID_422 = {
    'http_code': 422,
    'code': 'invalidField',
    'message': 'Length of Card Id must be 16'
}

USERNAME_CARD_ID_BIRTHDAY_422 = {
    'http_code': 422,
    'code': 'invalidField',
    'message': 'Card Id doesnt same with birtday'
}

TOTAL_TOP_LESS_THAN_ZERO_422 = {
    "http_code": 422,
    "code": "invalidInput",
    "message": "Total top up must be bigger than 0"
}


TOP_UP_CREATED_SUCCESS_201 = {
    'http_code': 201,
    'code': 'success',
    'message': 'Your wallet has been top up'
}


TRANSACTION_CREATED_SUCCESS_201 = {
    'http_code': 201,
    'code': 'success',
    'message': 'Your transaction has been created'
}


WALLET_LESS_THAN_TRANSACTION_422 = {
    'http_code': 422,
    'code': 'invalidInput',
    'message': 'Your balance is less than total transaction'
}


def response_with(response, value=None, message=None, error=None,
                  headers={}, pagination=None):

    result = {}
    if value is not None:
        result.update(value)

    if response.get('message', None) is not None:
        result.update({'message': response['message']})

    result.update({'code': response['code']})

    if error is not None:
        result.update({'errors': error})

    if pagination is not None:
        result.update({'pagination': pagination})\

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'FLask REST API'})

    return make_response(jsonify(result), response['http_code'], headers)
