from langchain.tools import BaseTool
from pydantic import BaseModel, Extra


class FeatureDescriptionsWrapper(BaseModel):
    """Wrapper for Feature Descriptions custom tool. We use this tool because we want to save on tokens, we don't
    need to provide this into context every time (moreover some features are self-explanatory for LLM). """
    # TODO! gather all features LLM is unsure about and call this function across all of them once

    FEATURE_DESCRIPTIONS = {

        'user_id': 'id of Wise customer',
        'date_created': 'date of transfer check',
        'request_id': 'id of transfer check',
        'first_name': 'first name of Wise customer',
        'last_name': 'last name of Wise customer',
        'profile_age': 'Age in days of the sender user profile',
        'sender_age': 'Age in years of the sender',
        'sender_email': 'email address of the sender',
        'recipient_email': 'email address of the recipient (can be the same as sender_email)',
        'last_24h_invoice_amount_gbp': 'Total amount transacted (in GBP) within the last 24 hours by user',
        'last_24h_transfer_count': 'Total number of transfers made within the last 24 hours by user',

        'balance_7d_count': 'Total bank transfers made by the user in the last 7 days',
        'bank7d_count': 'Total bank transfers made by the user in the last 7 days',
        'count_cards_1_week': 'Total card transfers made by the user in the last 7 days',
        'user_card_refusal_count7d': 'Number of refused card payments in the last 7 days',
        'same_ccy_payments_cnt_1d': 'Count of same currency transactions in a 24 hours time window',
        'ratio_volume': 'Volume calculation based on the lifetime volume and the daily volume',
        'ratio_count': 'Count calculation based on the lifetime count and the daily count',

        'oldest_pmnt_age': 'Difference in days between submit time of current payment and submit time of oldest '
                           'transfer (for user setting up current payment)',
        'same_route_age': 'Difference in seconds between submit time of current payment and submit time of first '
                          'transfer with same source and target currency ids as current transfer for current user',
        'same_route_pmnts_cnt': 'Number of transfers user made on same route as the one of the current payment',
        'source_ccy_cnt': 'Number of unique source currencies user made transfers from',
        'target_ccy_cnt': 'Number of unique target currencies user made transfers to',
        'sender_completed_transfers': 'Number of completed transfers made by the sender',
        'transfer_submitted_after_profile_creation_log_s': 'The log of time in seconds between submit time and time '
                                                           'the profile was created',
        'invoice_anomaly': 'Ratio of invoice value of current transaction raised to average of past invoice values '
                           'for profile',
        'oldest_similar_recipient_pmnt_age': 'Time since oldest payment with similar recipient',
        'recipient_pmnt_cnt': 'Number of payments to same recipient made by the user of current payment',

        'device_language': 'Preferred language for the desktop device',
        'mobile_locale_country': 'The country of the locale (i.e. the set of preferences regarding language, country, '
                                 'etc.. set by the user)',

        'recipient_bl_hits_count': 'Number of attempts to send money to blacklisted recipients with reason = fraud',
        'recipient_age': 'Age (in days) of recipient used for current payment across all users',
        'recipient_name_matching_ratio': 'Ratio of similarity between recipient and fraudsters (range 0-100)',
        'current_recipient_fraud_ratio': 'Fraud ratio for the recipient used for the current payment',
        'recipient_cnt': 'Number of recipients for user of current payment',
        'bene_name_significant_missmatch_7': 'Mismatch between beneficiary name from third party deposit and Wise '
                                             'profile name (Levensthein distance gerater than 7 transformations)',

        'payment_reference_fraud_pct': 'Fraud ratio associated with the payment reference used in the current payment',
        'successful_bank_transfers_cnt': 'Number of successfully completed transfers where payin method '
                                         'is bank or SOFORT',
        'invoice_value': 'Invoice value in local currency for the current payment',
        'payin_method': 'Payin method (ACH, bank, card, SOFORT, etc..) used to fund the current payment',
        'source_currency_code': 'The source currency code of the current payment',
        'target_currency_code': 'The target currency code of the current payment',
        'transfer_sender_name_matches_recipient_name': 'The sender name matches the recipient name of the '
                                                       'current payment',
        'transfer_segregation_type': 'The typology of payment, e.g., third-party-deposit, etc.',

        'nonsense_email': 'Flag that indicates if the email syntax is non-sensical / unusual',

        'user_reviewed': 'Whether the user has been reviewed by fraud agents before current payment',
        'sender_inferred_country_of_residence': 'Inferred country of residence of the sender',
        'phone_and_email_and_password_change_30_days': 'Has the phone number and email and password been changed '
                                                       'in the last 30 days',
        'phone_and_password_change_30_days': 'Has the phone number and password been changed in the last 30 days',
        'verifications_rejected_lifetime': 'Count of fraudulent rejection reasons received from verification partner',
        'hr3c_touchpoint_count': 'number of HR3C (High Risk 3rd party countries) touchpoints',

        'aml_state_reviewed': 'Has the user been reviewed by an AML agent before',
        'account_dormancy_from_last_transfer': 'Time difference since last successful Transfer and now '
                                               '(bucketised to power of 10)',

        'ip_data_country': 'Country gathered from the IP address',
        'ip_data_fraud_ratio': 'Fraud ratio on IP used by user (for current payment)',

        'payment_reference': 'message attached to the transfer by the sender',
        'transfer_state': 'State of the transfer. When aggregating volumes, consider only transfers with '
                          'transfer_state = TRANSFERRED.',

        'document_type': 'Type of document the user used during verification process',
        'issuer_country': 'Country that issued the document used during verification process',
        'nationality': 'Nationality of the user'

    }

    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid

    def run(self, feature_name=None):
        return self.FEATURE_DESCRIPTIONS.get(feature_name, 'No description available')


class FeatureDescriptionsTool(BaseTool):
    name = "FeatureDescriptions"
    description = "A tool for retrieving feature descriptions for feature names."

    def run(self, feature_name: str):
        feature_descriptions = FeatureDescriptionsWrapper()
        results = feature_descriptions.run(feature_name)
        return results

    def _run(self, feature_name: str):
        feature_descriptions = FeatureDescriptionsWrapper()
        results = feature_descriptions.run(feature_name)
        return results

    async def _arun(self, feature_name: str):
        # If the tool doesn't support async, you can just call the _run method
        return self._run(feature_name)