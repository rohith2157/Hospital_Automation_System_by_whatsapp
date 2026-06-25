
# Detailed Guide: Using Hashing with JWT for Secure Authentication

## Table of Contents
1. Introduction
2. What is Hashing?
3. What is JWT?
4. Why Use Both Together?
5. Step-by-Step Implementation
		- 5.1. Hashing Passwords (Storing Securely)
		- 5.2. Verifying Passwords (Login)
		- 5.3. Generating JWT (After Authentication)
		- 5.4. Verifying JWT (Protecting Routes)
6. Security Considerations
7. Example Implementation (Node.js)
8. Best Practices
9. References

---

## 1. Introduction
This guide provides a comprehensive explanation of how to combine password hashing and JWT (JSON Web Tokens) for secure authentication in modern web applications. It covers the theory, security notes, and practical code examples.

## 2. What is Hashing?
- **Hashing** is a one-way cryptographic function that transforms data (like a password) into a fixed-size string of characters, which is nearly impossible to reverse.
- Hashing is used to store passwords securely in databases. Even if the database is compromised, attackers cannot retrieve the original passwords.
- Common algorithms: **bcrypt**, **Argon2**, **PBKDF2**, **SHA256** (avoid MD5/SHA1 for passwords alone).

### Example: How Passwords Look in Database
```
Plain Text Password → Hashed Value (Stored in DB)
user123             → 2d2c8f6e4e8f9b5c1a3d7e9f2b4a6c8d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9
password456         → 8f9e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f
admin@2025          → 5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a
```

## SHA256 Hashing Details
- **SHA256** is a cryptographic hash function that produces a 256-bit (64 hexadecimal character) hash.
- It's fast and widely used for password hashing.
- However, for maximum security, **bcrypt** is recommended (it includes salt automatically and is slower, making brute-force attacks harder).
- **SHA256 alone** is considered weak for passwords without additional salting and iteration.

## 3. What is JWT?
- **JWT (JSON Web Token)** is a compact, URL-safe token format used to securely transmit information between parties.
- A JWT consists of three parts: Header, Payload, and Signature.
- The signature ensures the token’s integrity and authenticity.
- JWTs are commonly used for stateless authentication (no server-side session storage required).

## 4. Why Use Both Together?
- **Hashing** protects user credentials at rest (in the database).
- **JWT** provides a secure, stateless way to authenticate users after login.
- Together: Users log in with a password (hashed for storage), and upon successful authentication, receive a JWT for subsequent requests.

## 5. Step-by-Step Implementation

### 5.1. Hashing Passwords (Storing Securely)
1. When a user registers, hash their password before saving it to the database.
2. Use a strong algorithm (e.g., bcrypt with a salt, or SHA256 with salt).
3. Never store plain-text passwords.

**Option A: Using SHA256 with Salt (Node.js):**
```js
const crypto = require('crypto');
const password = 'user_password';
const salt = crypto.randomBytes(16).toString('hex'); // Generate random salt

function hashPasswordSHA256(password, salt) {
  return crypto
    .pbkdf2Sync(password, salt, 1000, 64, 'sha256')
    .toString('hex');
}

const hashedPassword = hashPasswordSHA256(password, salt);
// Store both 'salt' and 'hashedPassword' in database

// Database row example:
// {
//   id: 1,
//   username: 'john_doe',
//   email: 'john@example.com',
//   password: 'a1b2c3d4e5f6...(64 hex characters)',
//   salt: 'f7g8h9i0j1k2...(32 hex characters)',
//   created_at: '2026-01-03'
// }
```

**Option B: Using bcrypt (Recommended - includes salt automatically):**
```js
const bcrypt = require('bcrypt');
const password = 'user_password';
const saltRounds = 12; // Higher is more secure but slower
bcrypt.hash(password, saltRounds, (err, hash) => {
  // Store 'hash' in your database
  // Database row example:
  // {
  //   id: 1,
  //   username: 'john_doe',
  //   password: '$2b$12$R9h/cIPz0gi.URNNX3kh2O...(60 characters)',
  //   created_at: '2026-01-03'
  // }

### 5.2. Verifying Passwords (Login)
1. When a user logs in, retrieve the stored hash (and salt if using SHA256) from the database.
2. Use the same hashing method to compare the input password with the stored hash.

**Example with SHA256:**
```js
const crypto = require('crypto');

function hashPasswordSHA256(password, salt) {
  return crypto
    .pbkdf2Sync(password, salt, 1000, 64, 'sha256')
    .toString('hex');
}

// During login:
const inputPassword = 'user_password';
const storedHash = 'a1b2c3d4e5f6...'; // From database
const storedSalt = 'f7g8h9i0j1k2...'; // From database

const inputHash = hashPasswordSHA256(inputPassword, storedSalt);
if (inputHash === storedHash) {
  // Password is correct - generate JWT
} else {
  // Invalid credentials
}
```

**Example with bcrypt:**
bcrypt.compare(inputPassword, storedHash, (err, result) => {
	if (result) {
		// Password is correct
	} else {
		// Invalid credentials
	}
});
```

### 5.3. Generating JWT (After Authentication)
1. After successful password verification, generate a JWT.
2. Include only non-sensitive data in the payload (e.g., user ID, role).
3. Sign the token with a strong secret key.
4. Set an expiration time.

**Example:**
```js
const jwt = require('jsonwebtoken');
const payload = { userId: user.id, role: user.role };
const secret = process.env.JWT_SECRET;
const options = { expiresIn: '1h' };
const token = jwt.sign(payload, secret, options);
```

### 5.4. Verifying JWT (Protecting Routes)
1. On protected routes, require the JWT in the Authorization header.
2. Verify the token’s signature and expiration.
3. If valid, allow access; otherwise, reject the request.

**Example (Express middleware):**
```js
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
	const authHeader = req.headers['authorization'];
	const token = authHeader && authHeader.split(' ')[1];
	if (!token) return res.sendStatus(401);
	jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
		if (err) return res.sendStatus(403);
		req.user = user;
		next();
	});
}
```

## 6. Security Considerations
- **Never store plain-text passwords.**
- **Always use a salt** when hashing passwords (bcrypt does this automatically).
- **Keep your JWT secret safe** (use environment variables, not hard-coded values).
- **Set short expiration times** for JWTs (e.g., 15 minutes to 1 hour).
- **Use HTTPS** to prevent token interception.
- **Blacklist/rotate tokens** if a user logs out or a token is compromised.
- **Do not store sensitive data** (like passwords or personal info) in JWT payloads.

## 7. Example Implementation (Node.js)

```js
const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// ====== REGISTRATION: Hash password with SHA256 ======
function registerUser(username, password, email) {
  // Option 1: Using SHA256 with PBKDF2
  const salt = crypto.randomBytes(16).toString('hex');
  const hashedPassword = crypto
    .pbkdf2Sync(password, salt, 1000, 64, 'sha256')
    .toString('hex');
  
  // Save to database
  const user = {
    id: 1,
    username: username,
    email: email,
    password: hashedPassword,
    salt: salt,
    created_at: new Date()
  };
  
  console.log('User saved to database:', user);
  // DB Query: INSERT INTO users (username, email, password, salt) VALUES (...)
}

// ====== LOGIN: Verify password ======
function loginUser(username, inputPassword) {
  // Retrieve from database
  const userFromDB = {
    id: 1,
    username: 'john_doe',
    password: 'a1b2c3d4e5f6...(stored hash)',
    salt: 'f7g8h9i0j1k2...(stored salt)'
  };

  // Hash the input password with the stored salt
  const inputHash = crypto
    .pbkdf2Sync(inputPassword, userFromDB.salt, 1000, 64, 'sha256')
    .toString('hex');

  if (inputHash === userFromDB.password) {
    console.log('Password verified successfully!');
    // Generate JWT
    const token = jwt.sign(
      { userId: userFromDB.id, username: userFromDB.username },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );
    return { success: true, token: token };
  } else {
    return { success: false, error: 'Invalid credentials' };
  }
}

// ====== VERIFY JWT on Protected Routes ======
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) return res.sendStatus(401);
  
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

// ====== DATABASE SCHEMA EXAMPLE ======
/*
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  salt VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

EXAMPLE DATA IN DATABASE:
+----+-----------+-------------------+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
| id | username  | email             | password                                                         | salt                                                             | created_at          |
+----+-----------+-------------------+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
| 1  | john_doe  | john@example.com  | a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0 | f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f3g4h5i6 | 2026-01-03 10:30:00 |
| 2  | jane_doe  | jane@example.com  | 8f9e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a | 9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f3g4h5i6j7k8l | 2026-01-02 15:45:00 |
+----+-----------+-------------------+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+

Notice: Passwords are NOT plain text - they are SHA256 hashes!
You cannot see what the original password was by looking at the database.
*/
```

## 8. Best Practices
- Use strong, unique secrets for JWT signing.
- Store secrets in environment variables.
- Use HTTPS everywhere.
- For passwords: Use **bcrypt** (automatic salting) or **SHA256 with PBKDF2** (manual salting).
- If using SHA256, use at least **1000 iterations** (as shown in examples).
- Always store the **salt separately** if not using bcrypt.
- Regularly update dependencies (bcrypt, jsonwebtoken, etc.).
- Log authentication attempts and monitor for suspicious activity.
- Consider using refresh tokens for longer sessions.
- **Never hash a password twice** - one hash per password is sufficient.

## 9. SHA256 vs bcrypt Comparison

| Feature | SHA256 + PBKDF2 | bcrypt |
|---------|-----------------|--------|
| Speed | Fast | Slow (intentional) |
| Salt Handling | Manual (must store separately) | Automatic (included in hash) |
| Iterations | Configurable (1000+) | Configurable (auto) |
| Brute-force Resistance | Good | Better (slower) |
| Ease of Use | Moderate | Easy |
| Recommendation | Good for systems with many logins | Best for security |

**Recommendation:** Use **bcrypt** for maximum security. Use **SHA256 + PBKDF2** if you need more control.

## 10. References
- [JWT Introduction](https://jwt.io/introduction)
- [bcrypt Documentation](https://www.npmjs.com/package/bcrypt)
- [jsonwebtoken Documentation](https://www.npmjs.com/package/jsonwebtoken)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [SHA256 and PBKDF2](https://en.wikipedia.org/wiki/PBKDF2)

---
This guide provides a detailed, step-by-step approach to securely combining SHA256 hashing and JWT in your authentication flow. Remember: **passwords are hashed and stored in the database** - you will see the hashed values (64 hex characters for SHA256) in the database, not the original passwords. Adapt the code and recommendations to your specific tech stack and security requirements.
