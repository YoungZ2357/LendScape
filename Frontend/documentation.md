# User Onboarding System - Implementation Guide

## Overview
A JWT-based user authentication and onboarding system using Supabase (PostgreSQL + Auth) with vanilla HTML/CSS/JavaScript.

**Features:**
- User signup/signin with JWT authentication
- Location collection during onboarding
- Session persistence across page refreshes
- Row Level Security (RLS) for data protection

---

## System Flow

```
NEW USER:
Signup (index.html) → Add Location (add-location.html) → Welcome Screen (index.html)

RETURNING USER:
Signin (index.html) → Welcome Screen with Full Profile
```

---

## Prerequisites

1. Supabase account with project created
2. Database schema with `User` and `Location` tables in `lendscapev1` schema
3. Supabase project URL and anon key

---

## Database Setup

### Step 1: Add auth_id column to User table
```sql
ALTER TABLE lendscapev1."User" 
ADD COLUMN auth_id UUID UNIQUE;

CREATE INDEX idx_user_auth_id ON lendscapev1."User"(auth_id);
```

### Step 2: Enable password hashing
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE FUNCTION lendscapev1.hash_password(password TEXT)
RETURNS TEXT AS $$
BEGIN
  RETURN crypt(password, gen_salt('bf'));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### Step 3: Grant permissions
```sql
GRANT USAGE ON SCHEMA lendscapev1 TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON lendscapev1."User" TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON lendscapev1."Location" TO anon, authenticated;
GRANT USAGE, SELECT ON SEQUENCE lendscapev1."User_userid_seq" TO anon, authenticated;
GRANT USAGE, SELECT ON SEQUENCE lendscapev1."Location_locationid_seq" TO anon, authenticated;
GRANT EXECUTE ON FUNCTION lendscapev1.hash_password(TEXT) TO anon, authenticated;
```

### Step 4: Setup Row Level Security
```sql
-- User table
ALTER TABLE lendscapev1."User" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public signup" ON lendscapev1."User"
FOR INSERT TO anon, authenticated WITH CHECK (true);

CREATE POLICY "Users can view all profiles" ON lendscapev1."User"
FOR SELECT TO authenticated USING (true);

CREATE POLICY "Users can update own data" ON lendscapev1."User"
FOR UPDATE TO authenticated 
USING (auth.uid() = auth_id) WITH CHECK (auth.uid() = auth_id);

-- Location table
ALTER TABLE lendscapev1."Location" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow users to insert locations" ON lendscapev1."Location"
FOR INSERT TO anon, authenticated WITH CHECK (true);

CREATE POLICY "Allow users to view locations" ON lendscapev1."Location"
FOR SELECT TO authenticated USING (true);

CREATE POLICY "Allow users to update locations" ON lendscapev1."Location"
FOR UPDATE TO authenticated USING (true);
```

### Step 5: Fix sequences (if you have existing data)
```sql
SELECT setval('lendscapev1."User_userid_seq"', 
    (SELECT MAX(userid) FROM lendscapev1."User"));

SELECT setval('lendscapev1."Location_locationid_seq"', 
    (SELECT COALESCE(MAX(locationid), 0) FROM lendscapev1."Location"));
```

---

## Frontend Implementation

### File Structure
```
project/
├── index.html              # Auth + Welcome screen
└── add-location.html       # Location form
```

### index.html - Key Implementation Points

**1. Include Supabase SDK:**
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.39.3/dist/umd/supabase.min.js"></script>
```

**2. Initialize Supabase Client:**
```javascript
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_ANON_KEY';
const { createClient } = supabase;
const supabaseClient = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
```

**3. Signup Flow:**
```javascript
// a. Create Supabase Auth user
const { data: authData, error: authError } = 
    await supabaseClient.auth.signUp({ email, password });

// b. Hash password
const { data: hashedData, error: hashError } = 
    await supabaseClient.schema('lendscapev1')
    .rpc('hash_password', { password });

// c. Insert into User table
const { data: userData, error: insertError } = 
    await supabaseClient.schema('lendscapev1').from('User')
    .insert([{
        auth_id: authData.user.id,
        firstname, lastname, email, phonenumber,
        pwd: hashedData,
        class: 'active',
        status: 'active'
    }]).select().single();

// d. Check location and redirect
await displayUserInfo(userData);
```

**4. Signin Flow:**
```javascript
// a. Authenticate
const { data: authData, error: authError } = 
    await supabaseClient.auth.signInWithPassword({ email, password });

// b. Fetch user data
const { data: userData, error: fetchError } = 
    await supabaseClient.schema('lendscapev1').from('User')
    .select('*').eq('auth_id', authData.user.id).single();

// c. Display or redirect
await displayUserInfo(userData);
```

**5. Display User Info:**
```javascript
async function displayUserInfo(userData) {
    // Check location
    if (!userData.locationid) {
        window.location.href = 'add-location.html';
        return;
    }
    
    // Fetch location
    const { data: locationData } = await supabaseClient
        .schema('lendscapev1').from('Location')
        .select('address, city, state, postcode')
        .eq('locationid', userData.locationid).single();
    
    // Display profile with location
    // Show welcome screen
}
```

**6. Check Session on Page Load:**
```javascript
(async function checkAuth() {
    const { data: { session } } = await supabaseClient.auth.getSession();
    
    if (session) {
        const { data: userData } = await supabaseClient
            .schema('lendscapev1').from('User')
            .select('*').eq('auth_id', session.user.id).single();
        
        await displayUserInfo(userData);
    } else {
        // Show login forms
    }
})();
```

**7. Logout:**
```javascript
await supabaseClient.auth.signOut();
// Clear UI and show login forms
```

### add-location.html - Key Implementation Points

**1. Auth Check on Page Load:**
```javascript
(async function checkAuth() {
    const { data: { session } } = await supabaseClient.auth.getSession();
    
    if (!session) {
        window.location.href = 'index.html';
        return;
    }
    
    // Check if user already has location
    const { data: userData } = await supabaseClient
        .schema('lendscapev1').from('User')
        .select('locationid').eq('auth_id', session.user.id).single();
    
    if (userData.locationid) {
        window.location.href = 'index.html';
        return;
    }
    
    // Show form
})();
```

**2. Save Location:**
```javascript
// a. Insert location
const { data: locationData, error: locationError } = 
    await supabaseClient.schema('lendscapev1').from('Location')
    .insert([{
        address, city, state, country, postcode,
        is_default: true
    }]).select().single();

// b. Update User with locationId
const { error: updateError } = 
    await supabaseClient.schema('lendscapev1').from('User')
    .update({ locationid: locationData.locationid })
    .eq('auth_id', currentUser.id);

// c. Redirect to index
window.location.href = 'index.html';
```

---

## Authentication Mechanism

**How JWT Works:**
1. Supabase Auth creates JWT token on signup/signin
2. Token automatically stored in browser's localStorage
3. Supabase SDK includes token in all API requests
4. Server verifies JWT and applies RLS policies
5. `auth.uid()` in RLS comes from the JWT token

**You never manually handle JWT** - Supabase SDK does it automatically.

---

## Key Design Decisions

1. **Dual Password Storage**: 
   - Supabase Auth handles authentication
   - Hashed copy stored in User.pwd for backup/reference

2. **Location Required**: 
   - Users redirected to add-location.html if no location
   - Prevents incomplete profiles

3. **Session Persistence**: 
   - JWT in localStorage maintains login across refreshes
   - checkAuth() runs on every page load

4. **RLS Policies**: 
   - Users can view all profiles (marketplace requirement)
   - Users can only update their own data
   - Anyone can signup (insert)

---

## Testing Steps

1. **Signup Test:**
   - Fill signup form → Should redirect to add-location.html
   - Fill location form → Should redirect back with full profile

2. **Signin Test:**
   - User without location → Redirects to add-location.html
   - User with location → Shows welcome screen

3. **Session Test:**
   - Refresh page → Should stay logged in
   - Logout → Should clear session

4. **Protection Test:**
   - Access add-location.html without login → Redirects to index.html
   - Access add-location.html with location → Redirects to index.html

---

## Common Issues & Fixes

| Issue | Cause | Solution |
|-------|-------|----------|
| Permission denied | Missing grants | Run GRANT statements |
| Duplicate key error | Sequence out of sync | Run setval() to fix sequence |
| Function not found | Missing function | Create hash_password function |
| RLS violation | Policy too restrictive | Check/update RLS policies |
| Infinite redirects | Logic error | Check locationid properly set |

---

## Configuration Checklist

- [ ] Database schema created in lendscapev1
- [ ] auth_id column added to User table
- [ ] pgcrypto extension enabled
- [ ] hash_password function created
- [ ] All GRANT permissions applied
- [ ] RLS policies created for User and Location
- [ ] Sequences fixed if needed
- [ ] Supabase URL and anon key added to both HTML files
- [ ] Email confirmation disabled in Supabase settings
- [ ] Both HTML files in same directory

---
