from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants.code_constants import ACCOUNT_CURRENCY_CODE_LENGTH, ACCOUNT_NUMBER_LENGTH, ACCOUNT_TYPE_CODE_LENGTH, BILL_CONSUMER_NUMBER_LENGTH, UTILITY_COMPANY_ID_LENGTH
from src.constants.http_status_codes import API_210_RESPONSE_CODE, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from src.database import User
from flasgger import swag_from

bill_payment = Blueprint("bill_payment", __name__, url_prefix="/BillPayment")

@bill_payment.get('/')
@jwt_required()
def invalid():
    return jsonify({
        "error": "Not allowed",
        "message": "Only post method allowed for this url"
    }), HTTP_403_FORBIDDEN

@bill_payment.post('/')
@jwt_required()
@swag_from('./docs/bill_payment.yaml')
def process_bill_payment():
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if user:

            if request.is_json:
                #print(request.is_json)

                if request.json.get('Utility_Company_Id') and request.json.get('Consumer_Number') and request.json.get('Amount_Paid') and request.json.get('Transaction_Fee') and request.json.get('From_Account_Number') and request.json.get('From_Account_Type_Code') and request.json.get('From_Account_Currency_Code') and request.json.get('Transaction_Description'):
                    #print("available")
                    utility_company_id = request.json.get('Utility_Company_Id')
                    consumer_number = request.json.get('Consumer_Number')
                    amount_paid = request.json.get('Amount_Paid')
                    transaction_fee = request.json.get('Transaction_Fee')
                    from_account_number = request.json.get('From_Account_Number')
                    from_account_type_code = request.json.get('From_Account_Type_Code')
                    from_account_currency_code = request.json.get('From_Account_Currency_Code')
                    transaction_description = request.json.get('Transaction_Description')

                    if (len(str(utility_company_id))!=UTILITY_COMPANY_ID_LENGTH) or (type(utility_company_id) is not str):
                        return jsonify({
                            'error': "Utility_Company_Id is too short or too long or is not str, it must be of length " + str(UTILITY_COMPANY_ID_LENGTH) + " of type string"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(consumer_number))!=BILL_CONSUMER_NUMBER_LENGTH) or (type(consumer_number) is not str):
                        return jsonify({
                            'error': "Consumer_Number is too short or too long or is not str, it must be of length " + str(BILL_CONSUMER_NUMBER_LENGTH) + " of type string"
                        }), HTTP_400_BAD_REQUEST
                    
                    if (type(amount_paid) is not int):
                        return jsonify({
                            'error': "Amount_Paid is not int, it must be of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (type(transaction_fee) is not int):
                        return jsonify({
                            'error': "Transaction_Fee is not int, it must be of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(from_account_number))!=ACCOUNT_NUMBER_LENGTH) or (type(from_account_number) is not str):
                        return jsonify({
                            'error': "Account_Number is too short or too long or is not str, it must be of length " + str(ACCOUNT_NUMBER_LENGTH) + " of type string"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(from_account_type_code))!=ACCOUNT_TYPE_CODE_LENGTH) or (type(from_account_type_code) is not int):
                        return jsonify({
                            'error': "Account_Type_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_TYPE_CODE_LENGTH) + " of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(from_account_currency_code))!=ACCOUNT_CURRENCY_CODE_LENGTH) or (type(from_account_currency_code) is not int):
                        return jsonify({
                            'error': "Account_Currency_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_CURRENCY_CODE_LENGTH) + " of type integer"
                        }), HTTP_400_BAD_REQUEST

                    if (type(transaction_description) is not str):
                        return jsonify({
                            'error': "Transaction_Description is not str, it must be of type string"
                        }), HTTP_400_BAD_REQUEST
                    
                    #
                    #Code to process bill payment
                    #

                    return jsonify({
                        "Utility_Company_Id": utility_company_id,
                        "Consumer_Number": consumer_number,
                        "Amount_Paid": amount_paid,
                        "From_Account_Number": from_account_number,
                        "From_Account_Type_Code": from_account_type_code,
                        "From_Account_Currency_Code": from_account_currency_code
                    }), API_210_RESPONSE_CODE

                else:
                    return jsonify({
                        "error": "Utility_Company_Id or Consumer_Number or Amount_Paid or Transaction_Fee or From_Account_Number or From_Account_Type_Code or From_Account_Currency_Code or Transaction_Description is not passed or is invalid",
                        "data_passed": request.json
                    }), HTTP_400_BAD_REQUEST
                
            else:
                return jsonify({
                    "error": "Data passed is not json"
                }), HTTP_403_FORBIDDEN

        return jsonify({
            "error": "Authentication token is wrong"
        }), HTTP_404_NOT_FOUND

    except Exception as e:
        return jsonify({
            "error": e
        }), HTTP_400_BAD_REQUEST
