# API Authentication Guide

All API requests must include an Authorization header.

Required headers:

Authorization: Bearer YOUR_API_TOKEN
Content-Type: application/json

If the Authorization header is missing or the token is invalid, the API returns 401 Unauthorized.

If the token is valid but the user does not have permission for a resource, the API returns 403 Forbidden.

Recommended steps:
1. Confirm the token is copied correctly.
2. Confirm the token has not expired.
3. Confirm the request includes Content-Type: application/json.
4. Confirm the user has permission for the requested resource.