from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants.code_constants import ACCOUNT_CURRENCY_CODE_LENGTH, ACCOUNT_NUMBER_LENGTH, ACCOUNT_TYPE_CODE_LENGTH
from src.constants.http_status_codes import API_210_RESPONSE_CODE, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from src.database import User

funds_transfer = Blueprint("funds_transfer", __name__, url_prefix="/FundsTransfer")

@funds_transfer.get('/')
@jwt_required()
def invalid():
    return jsonify({
        "error": "Not allowed",
        "message": "Only post method allowed for this url"
    }), HTTP_403_FORBIDDEN

@funds_transfer.post('/')
@jwt_required()
def transfer_funds():
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if user:

            if request.is_json:
                #print(request.is_json)

                if request.json.get('From_Account_Number') and request.json.get('From_Account_Type_Code') and request.json.get('From_Account_Currency_Code') and request.json.get('To_Account_Number') and request.json.get('To_Account_Type_Code') and request.json.get('To_Account_Currency_Code') and request.json.get('Transaction_Amount') and request.json.get('Transaction_Currency_Code'):
                    #print("available")
                    from_account_number = request.json.get('From_Account_Number')
                    from_account_type_code = request.json.get('From_Account_Type_Code')
                    from_account_currency_code = request.json.get('From_Account_Currency_Code')
                    to_account_number = request.json.get('To_Account_Number')
                    to_account_type_code = request.json.get('To_Account_Type_Code')
                    to_account_currency_code = request.json.get('To_Account_Currency_Code')
                    transaction_amount = request.json.get('Transaction_Amount')
                    transaction_currency_code = request.json.get('Transaction_Currency_Code')

                    if (len(str(from_account_number))!=ACCOUNT_NUMBER_LENGTH) or (type(from_account_number) is not str):
                        return jsonify({
                            'error': "From_Account_Number is too short or too long or is not str, it must be of length " + str(ACCOUNT_NUMBER_LENGTH) + " of type string"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(from_account_type_code))!=ACCOUNT_TYPE_CODE_LENGTH) or (type(from_account_type_code) is not int):
                        return jsonify({
                            'error': "From_Account_Type_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_TYPE_CODE_LENGTH) + " of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(from_account_currency_code))!=ACCOUNT_CURRENCY_CODE_LENGTH) or (type(from_account_currency_code) is not int):
                        return jsonify({
                            'error': "From_Account_Currency_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_CURRENCY_CODE_LENGTH) + " of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(to_account_number))!=ACCOUNT_NUMBER_LENGTH) or (type(to_account_number) is not str):
                        return jsonify({
                            'error': "To_Account_Number is too short or too long or is not str, it must be of length " + str(ACCOUNT_NUMBER_LENGTH) + " of type string"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(to_account_type_code))!=ACCOUNT_TYPE_CODE_LENGTH) or (type(to_account_type_code) is not int):
                        return jsonify({
                            'error': "To_Account_Type_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_TYPE_CODE_LENGTH) + " of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(to_account_currency_code))!=ACCOUNT_CURRENCY_CODE_LENGTH) or (type(to_account_currency_code) is not int):
                        return jsonify({
                            'error': "To_Account_Currency_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_CURRENCY_CODE_LENGTH) + " of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (type(transaction_amount) is not int):
                        return jsonify({
                            'error': "Transaction_Amount is not int, it must be of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(transaction_currency_code))!=ACCOUNT_CURRENCY_CODE_LENGTH) or (type(transaction_currency_code) is not int):
                        return jsonify({
                            'error': "Transaction_Currency_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_CURRENCY_CODE_LENGTH) + " of type integer"
                        }), HTTP_400_BAD_REQUEST
                    
                    #
                    #Code to process transfer of funds
                    #

                    return jsonify({
                        "From_Account_Number": from_account_number,
                        "From_Account_Type_Code": from_account_type_code,
                        "From_Account_Currency_Code": from_account_currency_code,
                        "To_Account_Number": to_account_number,
                        "To_Account_Type_Code": to_account_type_code,
                        "To_Account_Currency_Code": to_account_currency_code,
                        "Transaction_Amount": transaction_amount,
                        "Transaction_Currency_Code": transaction_currency_code
                    }), API_210_RESPONSE_CODE

                else:
                    return jsonify({
                        "error": "From_Account_Number or From_Account_Type_Code or From_Account_Currency_Code or To_Account_Number or To_Account_Type_Code or To_Account_Currency_Code or Transaction_Amount or Transaction_Currency_Code is not passed",
                        "data_passed": request.json
                    }), HTTP_400_BAD_REQUEST

            else:
                return jsonify({
                    "error": "Data passed is noy json type"
                }), HTTP_403_FORBIDDEN

        return jsonify({
            "error": "Authentication token is wrong"
        }), HTTP_404_NOT_FOUND

    except Exception as e:
        return jsonify({
            "error": e
        }), HTTP_400_BAD_REQUEST
