from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants.code_constants import BILL_CONSUMER_NUMBER_LENGTH, UTILITY_COMPANY_ID_LENGTH
from src.constants.http_status_codes import API_210_RESPONSE_CODE, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from src.database import User
from flasgger import swag_from

bill_inquiry = Blueprint("bill_inquiry", __name__, url_prefix="/BillInquiry")

@bill_inquiry.get('/')
@jwt_required()
def invalid():
    return jsonify({
        "error": "Not allowed",
        "message": "Only post method allowed for this url"
    }), HTTP_403_FORBIDDEN

@bill_inquiry.post('/')
@jwt_required()
@swag_from('./docs/bill_inquiry.yaml')
def return_balance_inquiry():
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if user:

            if request.is_json:
                #print(request.is_json)

                if request.json.get('Utility_Company_Id') and request.json.get('Consumer_Number'):
                    #print("available")
                    utility_company_id = request.json.get('Utility_Company_Id')
                    consumer_number = request.json.get('Consumer_Number')

                    if (len(str(utility_company_id))!=UTILITY_COMPANY_ID_LENGTH) or (type(utility_company_id) is not str):
                        return jsonify({
                            'error': "Utility_Company_Id is too short or too long or is not str, it must be of length " + str(UTILITY_COMPANY_ID_LENGTH) + " of type string"
                        }), HTTP_400_BAD_REQUEST

                    if (len(str(consumer_number))!=BILL_CONSUMER_NUMBER_LENGTH) or (type(consumer_number) is not str):
                        return jsonify({
                            'error': "Consumer_Number is too short or too long or is not str, it must be of length " + str(BILL_CONSUMER_NUMBER_LENGTH) + " of type string"
                        }), HTTP_400_BAD_REQUEST
                    
                    #
                    #Code to retrieve transaction_fee, subscriber_name, billing_month, total_amount_payable_within_due_date, payment_due_date, total_amount_payable_after_due_date, bill_status, payment_auth_response_id, net_ced, net_withholding_tax and additional_data
                    #

                    transaction_fee = 90000900
                    subscriber_name = "Mr. Demo Example"
                    billing_month = 2203
                    total_payable_within_due_date = 99900000000
                    payment_due_date = 220405
                    total_payable_after_due_date = 99900099900
                    bill_status = 'U'
                    payment_auth_response_id = ""
                    net_ced = 90000000900
                    net_withholding_tax = 90000000000
                    additional_data = {"bill_information": {}}

                    return jsonify({
                        "Utility_Company_Id": utility_company_id,
                        "Consumer_Number": consumer_number,
                        "Transaction_Fee": transaction_fee,
                        "Subscriber_Name": subscriber_name,
                        "Billing_Month": billing_month,
                        "Total_Payable_Within_Due_Date": total_payable_within_due_date,
                        "Payment_Due_Date": payment_due_date,
                        "Total_Payable_After_Due_Date": total_payable_after_due_date,
                        "Bill_Status": bill_status,
                        "Payment_Auth_Response_Id": payment_auth_response_id,
                        "Net_CED": net_ced,
                        "Net_Withholding_Tax": net_withholding_tax,
                        "Additional_Data": additional_data
                    }), API_210_RESPONSE_CODE

                else:
                    return jsonify({
                        "error": "Utility_Company_Id or Consumer_Number is not passed or is invalid",
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
