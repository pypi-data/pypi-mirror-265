import json
import os
import jsonschema
from ref_Resolver import ExtendedRefResolver
from configs import mappingObject
from pkg_resources import resource_filename


def executeValidateJson(data, schema):
    try:
        jsonschema.validate(
            data,
            schema,
            resolver=ExtendedRefResolver(
                base_uri=resource_filename(__name__, '/Schema'),
                referrer=schema,
            ),
        )
    except jsonschema.exceptions.ValidationError as err:
        validation_msg = err.message
        if err.validator == "type" and len(err.path) > 0:
            key = err.path[len(err.path) - 1]
            validation_msg = f"{key} field should be a {err.validator_value}"
        return {"status": "SCHEMA_VALIDATION_FAILED", "message": validation_msg}   
    except Exception as err:
        return {"status": "SCHEMA_VALIDATION_FAILED", "message": err}    
    return {
        "status": "SCHEMA_VALIDATION_SUCCESS",
        "message": "Schema successfully validated",
    }


def extract_data_from_file(schema_file):
    path_for_schema = resource_filename(__name__, '/Schema')
    
    with open(f"{path_for_schema}/{schema_file}.json", "r") as schema_file:
        schemaObj = json.load(schema_file)

    return schemaObj


def validateJson(dataJsonString, reportType):
    # Temporary fix for report type exceptions
    arrExceptions = [
        "amazon_onsiteSponsoredProductsCampaign",
        "amazon_storeKeyMetrics",
        "amazon_storeKeyMetricsMonthly",
        "amazon_storeKeyMetricsMonthlyBackFill",
        "shopee_productSponsoredAffiliateReport",
        "shopee_onsiteKeyword",
        "shopee_marketingShippingFeePromotion",
        "shopee_marketingShippingFeePromotionMonthly",
        "shopee_marketingShippingFeePromotionMonthlyBackFill",
        "shopee_productOverview",
        "shopee_productOverviewMonthly",
        "shopee_productOverviewMonthlyBackFill",
        "shopee_storeKeyMetricsMonthlyBackFill",
        "lazada_storeKeyMetrics",
        "lazada_storeKeyMetricsMonthly",
        "lazada_storeKeyMetricsMonthlyBackFill",
        "lazada_onsiteKeyword",
        "flipkart_storeRevenue",
        "flipkart_PLAConsolidatedFSNSellerPortal",
        "flipkart_BrandAdsCampaign",
        "flipkart_DisplayAdsCampaign",
        "flipkart_PLAConsolidatedFSN",
        "flipkart_PCACampaign",
        "flipkart_PLACampaign",
        "flipkart_PLACampaignSellerPortal",
        "flipkart_searchTrafficReport",
        "flipkart_PCAProductPagePerformance"
    ]

    if reportType is None or not reportType:
        return {
            "status": "SCHEMA_VALIDATION_FAILED",
            "message": "Report type is Empty or None please enter valid string value!"
        }
    elif reportType in arrExceptions:
        return {
            "status": "SCHEMA_VALIDATION_SUCCESS",
            "message": "Schema successfully validated"
        }

    schema_file = mappingObject.get(reportType, "")

    if schema_file:
        try:
            jsonObject = json.loads(dataJsonString)
        except Exception as err:
            print("Error in converting data from string to json", err)
            return {
                "status": "FILE_FAILED_TO_CONVERT_JSON",
                "message": "Invalid JSON format"
            }
        if jsonObject:
            schemaObject = extract_data_from_file(schema_file)
            isValidated = executeValidateJson(jsonObject, schemaObject)
            return isValidated
        else:
            return {
                "status": "SCHEMA_VALIDATION_FAILED",
                "message": "Object is empty please enter correct object"
            }
    else:
        # Temporary fix
        return {
            "status": "SCHEMA_VALIDATION_SUCCESS",
            "message": "Schema successfully validated"
        }

answer = validateJson(
        json.dumps(
            {
                "merchantID": "TC1",
                "siteNickNameId": "shopee-4",
                "countryCode": "SG",
                "currencyCode": "SGD",
                "result": [
                    {
                        "Sequence": 1,
                        "Product_Name_Ad_Name": "Iklan Pencarian Toko Pengaturan Otomatis",
                        "Status": "Paused",
                        "Product_ID": 12,
                        "Ads_Type": "Iklan Pencarian Toko",
                        "Placement_Keyword": "Semua",
                        "Start_Date": "21-09-2023 00:00",
                        "End_Date": "Unlimited",
                        "Impression": 0,
                        "Clicks": 0,
                        "CTR": 0.0,
                        "Conversions": 0,
                        "Direct_Conversions": 0,
                        "Conversion_Rate": 0.0,
                        "Direct_Conversion_Rate": 0.0,
                        "Cost_per_Conversion": {
                            "amount": 0,
                            "currencyCode": "IDR"
                        },
                        "Cost_per_Direct_Conversion": {
                            "amount": 0,
                            "currencyCode": "IDR"
                        },
                        "Items_Sold": 0,
                        "Direct_Items_Sold": 0,
                        "GMV": {
                            "amount": 0,
                            "currencyCode": "IDR"
                        },
                        "Direct_GMV": {
                            "amount": 0,
                            "currencyCode": "IDR"
                        },
                        "Expense": {
                            "amount": 0,
                            "currencyCode": "IDR"
                        },
                        "ROAS": 0.0,
                        "Direct_ROAS": 0.0,
                        "ACOS": 0.0,
                        "Direct_ACOS": 0.0,
                        "Product_Impressions": 0,
                        "Product_Clicks": 0,
                        "Product_CTR": 0.0,
                        "Date": "16-12-2023"
                    }
                ]
            }
        ),
        "shopee_onsiteCampaign",
    )
print(answer)