# API Troubleshooting Guide

Common API errors:

401 Unauthorized:
This means the request does not have valid authentication. The user should check the API token, login session, or Authorization header.

403 Forbidden:
This means authentication is valid, but the user does not have permission to access that resource.

404 Not Found:
This means the requested endpoint or resource does not exist.

500 Internal Server Error:
This means something failed on the server side. The user should retry later or contact support if the issue continues.

Basic troubleshooting:
1. Check the request URL.
2. Check the HTTP method.
3. Check the Authorization header.
4. Check request body format.
5. Review the error message returned by the API.