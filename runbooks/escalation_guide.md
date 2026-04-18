# Tier 1 Escalation Runbook - SSO & Access Issues

## SAML_ASSERTION_INVALID
- Re-upload SP metadata in IdP console
- Verify system clock skew < 5 minutes
- If persists > 2 hours escalate to Tier 2

## TOKEN_EXPIRED / OIDC_MISMATCH
- Force token refresh in app settings
- Confirm redirect URIs match exactly in IdP
- Check OIDC client secret rotation schedule

## ACCOUNT_LOCKED
- Unlock in IdP admin panel
- If >5 attempts in 30 min escalate (potential brute force)
- Document in incident log

## FEDERATION_ERROR
- Verify IdP-SP trust relationship is active
- Check signing certificate expiry
- Escalate immediately if affecting >1 tenant

## PROVISIONING_ERROR
- Check SCIM connector logs in IdP
- Verify attribute mapping is current
- Re-trigger provisioning from admin console

## Escalation Path
Tier 1 -> Tier 2 (Identity Eng) -> Security Ops if auth anomaly suspected
