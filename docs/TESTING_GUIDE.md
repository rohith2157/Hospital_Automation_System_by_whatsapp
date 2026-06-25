# Quick Testing Guide - Role-Based Dashboard & Persistence

## What's New? 🎉

### 1. Role-Based Dashboard
Your dashboard now shows different content based on your login role:
- **Admin/Superadmin**: See all 3 stats (Patients, Appointments Today, Total)
- **Reception**: See limited stats + welcome message
- **Staff**: See even more limited view + assigned modules

### 2. Data Persistence
All user changes now persist across page refreshes!
- Add a user → Refresh page → User still there ✓
- Edit user details → Refresh → Changes saved ✓
- Reset password → Logout → Login with new password ✓
- Delete user → Refresh → User gone ✓

---

## Test 1: Role-Based Dashboard

### Step 1: Login as Admin
```
Username: dheeraj
Password: password123
```

**You should see:**
- 3 stat cards at top (Patients, Appointments Today, Total)
- All cards with gradient backgrounds (blue, green, purple)
- Welcome message: "You can manage users, appointments, and patients."
- Your role shown as "admin"

### Step 2: Switch to Staff
```
Username: rahul
Password: password123
```

**You should see:**
- Fewer stat cards (limited dashboard view)
- Welcome message: "You can view and manage your assigned tasks."
- Your role shown as "staff"
- Only "dashboard" and "appointments" modules listed

### Step 3: Switch to Reception
```
Username: kushal
Password: password123
```

**You should see:**
- Different stat cards than staff
- Welcome message: "You can manage patient records and appointments."
- Your role shown as "reception"
- More modules available: dashboard, patients, appointments

---

## Test 2: Data Persistence (Add User)

### Step 1: Login and Add User
1. Login with admin account (dheeraj / password123)
2. Click "Users" in left sidebar
3. Click "+ Add User" button
4. Fill form:
   - Username: `testuser`
   - Full Name: `Test User`
   - Email: `test@hospital.com`
   - Role: `staff`
   - Password: `test123456`
   - Confirm: `test123456`
   - Modules: Check "appointments" (uncheck dashboard if needed)
5. Click "Add User" button

**Result:** User added to list

### Step 2: Refresh Page
Press F5 to refresh the page

**Result:** Test user should STILL be there! ✓

### Step 3: Clear localStorage and Refresh (Optional Reset)
1. Open browser console (F12)
2. Type: `localStorage.clear()`
3. Refresh page (F5)

**Result:** Original 7 users are back (default)

---

## Test 3: Data Persistence (Edit User)

### Step 1: Edit User Details
1. Login with admin account (dheeraj / password123)
2. Go to Users page
3. Click "Edit" on any user (e.g., rahul)
4. Change their name: `Rahul Kumar Updated`
5. Click "Save" button

**Result:** User list shows updated name

### Step 2: Refresh Page
Press F5

**Result:** Changed name is STILL there! ✓

---

## Test 4: Data Persistence (Password Reset)

### Step 1: Reset Password
1. Login with admin (dheeraj / password123)
2. Go to Users page
3. Click "🔒 Reset Password" on any user
4. Enter new password: `newpass123456`
5. Click "Reset Password" button

**Result:** "Password reset (saved locally)" message appears

### Step 2: Test New Password
1. Click Logout
2. Login with that user's username and OLD password
3. You should get "Invalid credentials"
4. Login with NEW password
5. You should succeed! ✓

### Step 3: Refresh and Test Again
1. Logout
2. Refresh page (F5)
3. Login with new password
4. Should work again! ✓

---

## Test 5: Data Persistence (Delete User)

### Step 1: Delete User
1. Login with admin (dheeraj / password123)
2. Go to Users page
3. Click "🗑️ Delete" on any user
4. Click "OK" on confirmation
5. Click "Delete" when prompted

**Result:** User removed from list

### Step 2: Refresh Page
Press F5

**Result:** User is STILL deleted! ✓

---

## Test 6: Data Persistence (Status Toggle)

### Step 1: Toggle Status
1. Login with admin (dheeraj / password123)
2. Go to Users page
3. Click "Inactive" toggle on any user

**Result:** User status changes to "Active" or vice versa

### Step 2: Refresh Page
Press F5

**Result:** Status change is STILL there! ✓

---

## Test 7: Module Assignment Persistence

### Step 1: Assign Modules to User
1. Login with admin (dheeraj / password123)
2. Go to Users page
3. Click "Edit" on a user (e.g., rahul)
4. Scroll to "Modules" section
5. Check/uncheck different modules
6. Click "Save"

**Result:** Modules updated in user list

### Step 2: Login as That User
1. Logout
2. Login as that user (e.g., rahul / password123)
3. Look at left sidebar

**Result:** Only assigned modules show in menu! ✓

### Step 3: Change Assignment Again
1. Logout, login as admin
2. Edit same user and change modules
3. Logout and login as that user again

**Result:** Sidebar modules updated to match new assignment! ✓

---

## Test 8: Role-Based Dashboard + Permissions

### Admin View
```
Login: dheeraj / password123
```
See:
- All stats cards
- Full user management
- Can edit/delete users
- Welcome: "You can manage users, appointments, and patients."

### Staff View
```
Login: rahul / password123
```
See:
- Limited stats
- Can only see their info
- Welcome: "You can view and manage your assigned tasks."

### Reception View
```
Login: kushal / password123
```
See:
- Patient-focused stats
- Can manage patients
- Welcome: "You can manage patient records and appointments."

---

## What to Look For ✅

### Dashboard:
- [ ] Different cards shown for different roles
- [ ] Welcome message changes per role
- [ ] Module list shows assigned modules
- [ ] Stats update based on user role

### Persistence:
- [ ] Add user → Refresh → Still there
- [ ] Edit name → Refresh → Change saved
- [ ] Reset password → Works with new password
- [ ] Delete user → Refresh → Still deleted
- [ ] Toggle status → Refresh → Change saved
- [ ] Assign modules → Works in sidebar

### Data Format:
- [ ] Open browser console (F12)
- [ ] Type: `JSON.parse(localStorage.getItem('hospital_users'))`
- [ ] See all users with updated data

---

## Troubleshooting

### If data doesn't persist after refresh:
1. Check if localStorage is enabled in browser
2. Check browser console for errors (F12 → Console)
3. Try `localStorage.clear()` and refresh
4. Check file was saved properly

### If dashboard looks wrong:
1. Login out and back in
2. Check that user.role is correct (shown in header)
3. Check browser console for JS errors

### If password reset doesn't work:
1. Ensure password is 6+ characters
2. Check that new password appears in localStorage
3. Try clearing localStorage and refreshing

---

## Test Users Available

| Username | Password | Role | Modules |
|----------|----------|------|---------|
| admin | admin123 | superadmin | All 5 |
| dheeraj | password123 | admin | All 5 |
| rohith | password123 | superadmin | All 5 |
| rahul | password123 | staff | dashboard, appointments |
| kushal | password123 | reception | dashboard, patients, appointments |
| suddhu | password123 | staff | dashboard |
| gopal | password123 | reception | dashboard, patients |
| kumar | password123 | staff | dashboard, doctors |

---

## Quick Commands for Testing

### View all saved users:
```javascript
JSON.parse(localStorage.getItem('hospital_users'))
```

### Clear all data:
```javascript
localStorage.clear()
```

### View specific user:
```javascript
const users = JSON.parse(localStorage.getItem('hospital_users'));
console.table(users);
```

### Check if key exists:
```javascript
localStorage.getItem('hospital_users') ? 'YES' : 'NO'
```

---

## Summary

✅ **What Works Now:**
1. Different dashboard views based on role
2. All user edits persist to browser storage
3. Passwords save and work after refresh
4. Module assignments reflected in sidebar
5. Data survives page refresh, logout, and browser close

🎯 **Next Steps (When DB Comes Online):**
- Backend will sync localStorage to remote database
- No code changes needed on frontend
- Everything will automatically persist to database

🔧 **Current Limitation:**
- Data only stored in browser localStorage
- Different browser = different data
- Clearing browser storage = data gone

---

**Enjoy testing! 🚀**
