from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants.code_constants import ACCOUNT_CURRENCY_CODE_LENGTH, ACCOUNT_NUMBER_LENGTH, ACCOUNT_TYPE_CODE_LENGTH
from src.constants.http_status_codes import API_210_RESPONSE_CODE, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from src.database import User
from flasgger import swag_from

mini_statement = Blueprint("mini_statement", __name__, url_prefix="/MiniStatement")

@mini_statement.get('/')
@jwt_required()
def invalid():
    return jsonify({
        "error": "Not allowed",
        "message": "Only post method allowed for this url"
    }), HTTP_403_FORBIDDEN

@mini_statement.post('/')
@jwt_required()
@swag_from('./docs/mini_statement.yaml')
def return_mini_statement():
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if user:

            if request.is_json:
                #print(request.is_json)

                if request.json.get('Account_Number') and request.json.get('Account_Type_Code') and request.json.get('Account_Currency_Code'):
                    #print("available")
                    account_number = request.json.get('Account_Number')
                    account_type_code = request.json.get('Account_Type_Code')
                    account_currency_code = request.json.get('Account_Currency_Code')

                    if (len(str(account_number))!=ACCOUNT_NUMBER_LENGTH) or (type(account_number) is not str):
                        return jsonify({
                            'error': "Account_Number is too short or too long or is not str, it must be of length " + str(ACCOUNT_NUMBER_LENGTH) + " of type string"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(account_type_code))!=ACCOUNT_TYPE_CODE_LENGTH) or (type(account_type_code) is not int):
                        return jsonify({
                            'error': "Account_Type_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_TYPE_CODE_LENGTH) + " of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(account_currency_code))!=ACCOUNT_CURRENCY_CODE_LENGTH) or (type(account_currency_code) is not int):
                        return jsonify({
                            'error': "Account_Currency_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_CURRENCY_CODE_LENGTH) + " of type integer"
                        }), HTTP_400_BAD_REQUEST

                    #
                    #Code to retrieve additional_data_length and additional_data
                    #

                    additional_data_length = 5 #Change this to the value retrieved from database
                    additional_data = {
                        1: {"Date": "2022-03-25","Description": "description of transaction","STAN": "stan of transaction no. 1","Amount": 99000.00},
                        2: {"Date": "2022-03-18","Description": "description of transaction","STAN": "stan of transaction no. 2","Amount": 88000.00},
                        3: {"Date": "2022-03-11","Description": "description of transaction","STAN": "stan of transaction no. 3","Amount": 77000.00},
                        4: {"Date": "2022-03-04","Description": "description of transaction","STAN": "stan of transaction no. 4","Amount": 66000.00},
                        5: {"Date": "2022-02-24","Description": "description of transaction","STAN": "stan of transaction no. 5","Amount": 55000.00}
                    } # Change this to the value retrieved from database

                    return jsonify({
                        "Account_Number": account_number,
                        "Account_Type_Code": account_type_code,
                        "Account_Currency_Code": account_currency_code,
                        "Additional_Data_Length": additional_data_length,
                        "Additional_Data": additional_data
                    }), API_210_RESPONSE_CODE

                else:
                    return jsonify({
                        "error": "Account_Number or Account_Type_Code or Account_Currency_Code is not passed",
                        "data_passed": request.json
                    }), HTTP_400_BAD_REQUEST

            else:
                return jsonify({
                    "error": "Data passed is not json type"
                }), HTTP_403_FORBIDDEN

        return jsonify({
            "error": "Authentication token is wrong"
        }), HTTP_404_NOT_FOUND

    except Exception as e:
        return jsonify({
            "error": e
        }), HTTP_400_BAD_REQUEST
