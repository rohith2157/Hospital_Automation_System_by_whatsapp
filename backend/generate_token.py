from flask_jwt_extended import create_access_token
from datetime import timedelta

# Create a token that lasts 7 days
token = create_access_token(
    identity={'id': 1, 'username': 'admin', 'role': 'superadmin'},
    expires_delta=timedelta(days=7)
)

print("\n" + "="*80)
print("NEW JWT TOKEN (Valid for 7 days):")
print("="*80)
print(f"Bearer {token}")
print("="*80 + "\n")
