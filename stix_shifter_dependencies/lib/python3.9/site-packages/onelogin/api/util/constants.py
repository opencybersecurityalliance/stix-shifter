# -*- coding: utf-8 -*-

""" Constants class

Copyright (c) 2021, OneLogin, Inc.
All rights reserved.

Constants class of the OneLogin's Python SDK.

"""


class Constants(object):
    """

    This class defines all the constants that will be used
    in the OneLogin's Python SDK.

    """

    # OAuth2 Tokens URLs
    TOKEN_REQUEST_URL = "https://%s.onelogin.com/auth/oauth2/v2/token"
    TOKEN_REFRESH_URL = "https://%s.onelogin.com/auth/oauth2/v2/token"
    TOKEN_REVOKE_URL = "https://%s.onelogin.com/auth/oauth2/revoke"
    GET_RATE_URL = "https://%s.onelogin.com/auth/rate_limit"

    # User URLs
    GET_USERS_URL = "https://%s.onelogin.com/api/%s/users"
    GET_USER_URL = "https://%s.onelogin.com/api/%s/users/%s"
    GET_APPS_FOR_USER_URL = "https://%s.onelogin.com/api/%s/users/%s/apps"
    GET_ROLES_FOR_USER_URL = "https://%s.onelogin.com/api/%s/users/%s/roles"
    GET_CUSTOM_ATTRIBUTES_URL = "https://%s.onelogin.com/api/%s/users/custom_attributes"
    CREATE_USER_URL = "https://%s.onelogin.com/api/%s/users"
    UPDATE_USER_URL = "https://%s.onelogin.com/api/%s/users/%s"
    DELETE_USER_URL = "https://%s.onelogin.com/api/%s/users/%s"
    ADD_ROLE_TO_USER_URL = "https://%s.onelogin.com/api/%s/users/%s/add_roles"
    DELETE_ROLE_TO_USER_URL = "https://%s.onelogin.com/api/%s/users/%s/remove_roles"
    SET_PW_CLEARTEXT = "https://%s.onelogin.com/api/%s/users/set_password_clear_text/%s"
    SET_PW_SALT = "https://%s.onelogin.com/api/%s/users/set_password_using_salt/%s"
    SET_STATE_TO_USER_URL = "https://%s.onelogin.com/api/%s/users/%s/set_state"
    SET_CUSTOM_ATTRIBUTE_TO_USER_URL = "https://%s.onelogin.com/api/%s/users/%s/set_custom_attributes"
    LOG_USER_OUT_URL = "https://%s.onelogin.com/api/%s/users/%s/logout"
    LOCK_USER_URL = "https://%s.onelogin.com/api/%s/users/%s/lock_user"
    GENERATE_MFA_TOKEN_URL = "https://%s.onelogin.com/api/%s/users/%s/mfa_token"

    # Connectors URLS
    GET_CONNECTORS_URL = "https://%s.onelogin.com/api/%s/connectors"

    # Apps URL
    GET_APPS_URL = "https://%s.onelogin.com/api/%s/apps"
    CREATE_APP_URL = "https://%s.onelogin.com/api/%s/apps"
    GET_APP_URL = "https://%s.onelogin.com/api/%s/apps/%s"
    UPDATE_APP_URL = "https://%s.onelogin.com/api/%s/apps/%s"
    DELETE_APP_URL = "https://%s.onelogin.com/api/%s/apps/%s"
    DELETE_APP_PARAMETER_URL = "https://%s.onelogin.com/api/%s/apps/%s/parameters/%s"
    GET_APP_USERS_URL = "https://%s.onelogin.com/api/%s/apps/%s/users"

    # App Rules URL
    GET_APP_RULES_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules"
    CREATE_APP_RULE_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules"
    GET_APP_RULE_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules/%s"
    UPDATE_APP_RULE_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules/%s"
    DELETE_APP_RULE_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules/%s"
    GET_APP_CONDITIONS_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules/conditions"
    GET_APP_CONDITION_OPERATORS_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules/conditions/%s/operators"
    GET_APP_CONDITION_VALUES_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules/conditions/%s/values"
    GET_APP_ACTIONS_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules/actions"
    GET_APP_ACTION_VALUES_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules/actions/%s/values"
    APP_RULE_SORT_URL = "https://%s.onelogin.com/api/%s/apps/%s/rules/sort"

    # Role URLs
    GET_ROLES_URL = "https://%s.onelogin.com/api/%s/roles"
    CREATE_ROLE_URL = "https://%s.onelogin.com/api/%s/roles"
    GET_ROLE_URL = "https://%s.onelogin.com/api/%s/roles/%s"
    UPDATE_ROLE_URL = "https://%s.onelogin.com/api/%s/roles/%s"
    GET_ROLE_APPS_URL = "https://%s.onelogin.com/api/%s/roles/%s/apps"
    SET_ROLE_APPS_URL = "https://%s.onelogin.com/api/%s/roles/%s/apps"
    GET_ROLE_USERS_URL = "https://%s.onelogin.com/api/%s/roles/%s/users"
    ADD_ROLE_USERS_URL = "https://%s.onelogin.com/api/%s/roles/%s/users"
    REMOVE_ROLE_USERS_URL = "https://%s.onelogin.com/api/%s/roles/%s/users"
    GET_ROLE_ADMINS_URL = "https://%s.onelogin.com/api/%s/roles/%s/admins"
    ADD_ROLE_ADMINS_URL = "https://%s.onelogin.com/api/%s/roles/%s/admins"
    REMOVE_ROLE_ADMINS_URL = "https://%s.onelogin.com/api/%s/roles/%s/admins"
    DELETE_ROLE_URL = "https://%s.onelogin.com/api/%s/roles/%s"

    # Event URLS
    GET_EVENT_TYPES_URL = "https://%s.onelogin.com/api/%s/events/types"
    GET_EVENTS_URL = "https://%s.onelogin.com/api/%s/events"
    CREATE_EVENT_URL = "https://%s.onelogin.com/api/%s/events"
    GET_EVENT_URL = "https://%s.onelogin.com/api/%s/events/%s"

    # Group URLs
    GET_GROUPS_URL = "https://%s.onelogin.com/api/%s/groups"
    CREATE_GROUP_URL = "https://%s.onelogin.com/api/%s/groups"
    GET_GROUP_URL = "https://%s.onelogin.com/api/%s/groups/%s"

    # Custom Login URLs
    SESSION_LOGIN_TOKEN_URL = "https://%s.onelogin.com/api/%s/login/auth"
    GET_TOKEN_VERIFY_FACTOR = "https://%s.onelogin.com/api/%s/login/verify_factor"

    # SAML Assertion URLs
    GET_SAML_ASSERTION_URL = "https://%s.onelogin.com/api/%s/saml_assertion"
    GET_SAML_VERIFY_FACTOR = "https://%s.onelogin.com/api/%s/saml_assertion/verify_factor"

    # Multi-Factor Authentication URLs
    GET_FACTORS_URL = "https://%s.onelogin.com/api/%s/users/%s/auth_factors"
    V2_GET_FACTORS_URL = "https://%s.onelogin.com/api/%s/mfa/users/%s/factors"
    ENROLL_FACTOR_URL = "https://%s.onelogin.com/api/%s/users/%s/otp_devices"
    V2_ENROLL_FACTOR_URL = "https://%s.onelogin.com/api/%s/mfa/users/%s/registrations"
    GET_ENROLLED_FACTORS_URL = "https://%s.onelogin.com/api/%s/users/%s/otp_devices"
    VERIFY_ENROLLMENT_SMS_EMAIL_PROTECT_AUTH_URL = "https://%s.onelogin.com/api/%s/mfa/users/%s/registrations/%s"
    VERIFY_ENROLLMENT__PROTECTPUSH_VOICE_URL = "https://%s.onelogin.com/api/%s/mfa/users/%s/registrations/%s"
    V2_GET_ENROLLED_FACTORS_URL = "https://%s.onelogin.com/api/%s/mfa/users/%s/devices"
    ACTIVATE_FACTOR_URL = "https://%s.onelogin.com/api/%s/users/%s/otp_devices/%s/trigger"
    V2_ACTIVATE_FACTOR_URL = "https://%s.onelogin.com/api/%s/mfa/users/%s/verifications"
    VERIFY_FACTOR_URL = "https://%s.onelogin.com/api/%s/users/%s/otp_devices/%s/verify"
    VERIFY_FACTOR_SMS_EMAIL_PROTECT_AUTH_URL = "https://%s.onelogin.com/api/%s/mfa/users/%s/verifications/%s"
    VERIFY_FACTOR_PROTECTPUSH_VOICE_URL = "https://%s.onelogin.com/api/%s/mfa/users/%s/verifications/%s"
    DELETE_FACTOR_URL = "https://%s.onelogin.com/api/%s/users/%s/otp_devices/%s"
    V2_DELETE_FACTOR_URL = "https://%s.onelogin.com/api/%s/mfa/users/%s/devices/%s"

    # Invite Link URLS
    GENERATE_INVITE_LINK_URL = "https://%s.onelogin.com/api/%s/invites/get_invite_link"
    SEND_INVITE_LINK_URL = "https://%s.onelogin.com/api/%s/invites/send_invite_link"

    # Embed Apps URL
    EMBED_APP_URL = "https://api.onelogin.com/client/apps/embed2"

    # Account Brands URLS
    GET_ACCOUNT_BRANDS_URL = "https://%s.onelogin.com/api/%s/branding/brands"
    CREATE_ACCOUNT_BRAND_URL = "https://%s.onelogin.com/api/%s/branding/brands"
    GET_ACCOUNT_BRAND_URL = "https://%s.onelogin.com/api/%s/branding/brands/%s"
    UPDATE_ACCOUNT_BRAND_URL = "https://%s.onelogin.com/api/%s/branding/brands/%s"
    DELETE_ACCOUNT_BRAND_URL = "https://%s.onelogin.com/api/%s/branding/brands/%s"
    GET_APPS_BRAND_URL = "https://%s.onelogin.com/api/%s/branding/%s/apps"
    GET_ACCOUNT_EMAIL_SETTINGS = "https://%s.onelogin.com/api/%s/branding/email_settings"
    UPDATE_ACCOUNT_EMAIL_SETTINGS = "https://%s.onelogin.com/api/%s/branding/email_settings"
    RESET_ACCOUNT_EMAIL_SETTINGS = "https://%s.onelogin.com/api/%s/branding/email_settings"

    # Smart Hooks URLS
    GET_HOOKS_URL = "https://%s.onelogin.com/api/%s/hooks"
    CREATE_HOOK_URL = "https://%s.onelogin.com/api/%s/hooks"
    GET_HOOK_URL = "https://%s.onelogin.com/api/%s/hooks/%s"
    UPDATE_HOOK_URL = "https://%s.onelogin.com/api/%s/hooks/%s"
    DELETE_HOOK_URL = "https://%s.onelogin.com/api/%s/hooks/%s"
    GET_HOOK_LOGS_URL = "https://%s.onelogin.com/api/%s/hooks/%s/logs"
    GET_HOOK_ENVS_URL = "https://%s.onelogin.com/api/%s/hooks/envs"
    CREATE_HOOK_ENV_URL = "https://%s.onelogin.com/api/%s/hooks/envs"
    GET_HOOK_ENV_URL = "https://%s.onelogin.com/api/%s/hooks/envs/%s"
    UPDATE_HOOK_ENV_URL = "https://%s.onelogin.com/api/%s/hooks/envs/%s"
    DELETE_HOOK_ENV_URL = "https://%s.onelogin.com/api/%s/hooks/envs/%s"

    # Smart MFA
    SMART_MFA_VALIDATE_USER = "https://%s.onelogin.com/api/%s/smart-mfa"
    SMART_MFA_VERFY_TOKEN = "https://%s.onelogin.com/api/%s/smart-mfa/verify"

    # Vigilance AI URLS
    TRACK_EVENT_URL = "https://%s.onelogin.com/api/%s/risk/events"
    GET_RISK_SCORE_URL = "https://%s.onelogin.com/api/%s/risk/verify"
    GET_RISK_RULES_URL = "https://%s.onelogin.com/api/%s/risk/rules"
    CREATE_RISK_RULE_URL = "https://%s.onelogin.com/api/%s/risk/rules"
    GET_RISK_RULE_URL = "https://%s.onelogin.com/api/%s/risk/rules/%s"
    UPDATE_RISK_RULE_URL = "https://%s.onelogin.com/api/%s/risk/rules/%s"
    DELETE_RISK_RULE_URL = "https://%s.onelogin.com/api/%s/risk/rules/%s"
    GET_SCORE_INSIGHTS = "https://%s.onelogin.com/api/%s/risk/scores"

    # Mappings URLS
    GET_MAPPINGS_URL = "https://%s.onelogin.com/api/%s/mappings"
    CREATE_MAPPING_URL = "https://%s.onelogin.com/api/%s/mappings"
    GET_MAPPING_URL = "https://%s.onelogin.com/api/%s/mappings/%s"
    UPDATE_MAPPING_URL = "https://%s.onelogin.com/api/%s/mappings/%s"
    DELETE_MAPPING_URL = "https://%s.onelogin.com/api/%s/mappings/%s"
    DRYRUN_MAPPING_URL = "https://%s.onelogin.com/api/%s/mappings/%s/dryrun"
    GET_MAPPING_CONDITIONS_URL = "https://%s.onelogin.com/api/%s/mappings/conditions"
    GET_MAPPING_CONDITION_OPERATORS_URL = "https://%s.onelogin.com/api/%s/mappings/conditions/%s/operators"
    GET_MAPPING_CONDITION_VALUES_URL = "https://%s.onelogin.com/api/%s/mappings/conditions/%s/values"
    GET_MAPPING_ACTIONS_URL = "https://%s.onelogin.com/api/%s/mappings/actions"
    GET_MAPPING_ACTION_VALUES_URL = "https://%s.onelogin.com/api/%s/mappings/actions/%s/values"
    MAPPING_SORT_URL = "https://%s.onelogin.com/api/%s/mappings/sort"

    # Privileges URLS
    LIST_PRIVILEGES_URL = "https://%s.onelogin.com/api/%s/privileges"
    CREATE_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges"
    UPDATE_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges/%s"
    GET_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges/%s"
    DELETE_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges/%s"
    GET_ROLES_ASSIGNED_TO_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges/%s/roles"
    ASSIGN_ROLES_TO_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges/%s/roles"
    REMOVE_ROLE_FROM_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges/%s/roles/%s"
    GET_USERS_ASSIGNED_TO_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges/%s/users"
    ASSIGN_USERS_TO_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges/%s/users"
    REMOVE_USER_FROM_PRIVILEGE_URL = "https://%s.onelogin.com/api/%s/privileges/%s/users/%s"
    VALID_ACTIONS = [
        "apps:List",
        "apps:Get",
        "apps:Create",
        "apps:Update",
        "apps:Delete",
        "apps:ManageRoles",
        "apps:ManageUsers",
        "directories:List",
        "directories:Get",
        "directories:Create",
        "directories:Update",
        "directories:Delete",
        "directories:SyncUsers",
        "directories:RefreshSchema",
        "events:List",
        "events:Get",
        "mappings:List",
        "mappings:Get",
        "mappings:Create",
        "mappings:Update",
        "mappings:Delete",
        "mappings:ReapplyAll",
        "policies:List",
        "policies:user:Get",
        "policies:user:Create",
        "policies:user:Update",
        "policies:user:Delete",
        "policies:app:Get",
        "policies:app:Create",
        "policies:app:Update",
        "policies:app:Delete",
        "privileges:List",
        "privileges:Get",
        "privileges:Create",
        "privileges:Update",
        "privileges:Delete",
        "privileges:ListUsers",
        "privileges:ListRoles",
        "privileges:ManageUsers",
        "privileges:ManageRoles",
        "reports:List",
        "reports:Get",
        "reports:Create",
        "reports:Update",
        "reports:Delete",
        "reports:Run",
        "roles:List",
        "roles:Get",
        "roles:Create",
        "roles:Update",
        "roles:Delete",
        "roles:ManageUsers",
        "roles:ManageApps",
        "trustedidp:List",
        "trustedidp:Get",
        "trustedidp:Create",
        "trustedidp:Update",
        "trustedidp:Delete",
        "users:List",
        "users:Get",
        "users:Create",
        "users:Update",
        "users:Delete",
        "users:Unlock",
        "users:ResetPassword",
        "users:ForceLogout",
        "users:Invite",
        "users:ReapplyMappings",
        "users:ManageRoles",
        "users:ManageApps",
        "users:GenerateTempMfaToken"
    ]
