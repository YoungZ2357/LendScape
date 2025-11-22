
const SUPABASE_URL = window.SUPABASE_CONFIG.url;
const SUPABASE_ANON_KEY = window.SUPABASE_CONFIG.anon_key;

const { createClient } = supabase;
const supabaseClient = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);


const signupToggle = document.getElementById('signupToggle');
const signinToggle = document.getElementById('signinToggle');
const signupForm = document.getElementById('signupForm');
const signinForm = document.getElementById('signinForm');
const signupFormElement = document.getElementById('signupFormElement');
const signinFormElement = document.getElementById('signinFormElement');
const errorMessage = document.getElementById('errorMessage');
const authSection = document.getElementById('authSection');
const welcomeScreen = document.getElementById('welcomeScreen');
const logoutBtn = document.getElementById('logoutBtn');
const loadingState = document.getElementById('loadingState');


signupToggle.addEventListener('click', () => {
    signupToggle.classList.add('active');
    signinToggle.classList.remove('active');
    signupForm.classList.add('active');
    signinForm.classList.remove('active');
    clearError();
});

signinToggle.addEventListener('click', () => {
    signinToggle.classList.add('active');
    signupToggle.classList.remove('active');
    signinForm.classList.add('active');
    signupForm.classList.remove('active');
    clearError();
});


function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('show');
}

function clearError() {
    errorMessage.textContent = '';
    errorMessage.classList.remove('show');
}

async function displayUserInfo(userData) {
    document.getElementById('displayName').textContent = `${userData.firstName} ${userData.lastName}`;
    document.getElementById('displayEmail').textContent = userData.email;
    document.getElementById('displayPhone').textContent = userData.phoneNumber || 'Not provided';


    if (!userData.locationId) {
        window.location.href = '/location/add';
        return;
    }

    try {
        const response = await fetch(`/api/locations/${userData.locationId}`, {
            headers: {
                'Authorization': `Bearer ${supabaseClient.auth.session()?.access_token}`
            }
        });

        if (response.ok) {
            const locationData = await response.json();
            const locationSection = document.getElementById('locationSection');
            const displayLocation = document.getElementById('displayLocation');
            displayLocation.textContent = `${locationData.address}, ${locationData.city}, ${locationData.state} ${locationData.postcode}`;
            locationSection.style.display = 'block';
        }
    } catch (error) {
        console.error('Error fetching location:', error);
    }

    authSection.style.display = 'none';
    welcomeScreen.classList.add('show');
}

signupFormElement.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearError();

    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const phoneNumber = document.getElementById('phoneNumber').value.trim();
    const password = document.getElementById('signupPassword').value;

    if (!firstName || !lastName || !email || !phoneNumber || !password) {
        showError('All fields are required');
        return;
    }

    if (password.length < 6) {
        showError('Password must be at least 6 characters');
        return;
    }

    const signupBtn = document.getElementById('signupBtn');
    signupBtn.disabled = true;
    signupBtn.textContent = 'Creating Account...';

    try {

        const response = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                firstName,
                lastName,
                email,
                phoneNumber,
                password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Signup failed');
        }


        const loginResponse = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const loginData = await loginResponse.json();

        if (loginResponse.ok) {

            localStorage.setItem('access_token', loginData.access_token);
            localStorage.setItem('refresh_token', loginData.refresh_token);
            localStorage.setItem('user', JSON.stringify(loginData.user));


            const userResponse = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${loginData.access_token}`
                }
            });

            if (userResponse.ok) {
                const userData = await userResponse.json();
                await displayUserInfo(userData);
            }
        }

    } catch (error) {
        console.error('Signup error:', error);
        if (error.message.includes('duplicate') || error.message.includes('exists')) {
            showError('Email already exists. Please sign in instead.');
        } else {
            showError(error.message || 'Signup failed. Please try again.');
        }
    } finally {
        signupBtn.disabled = false;
        signupBtn.textContent = 'Create Account';
    }
});


signinFormElement.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearError();

    const email = document.getElementById('signinEmail').value.trim();
    const password = document.getElementById('signinPassword').value;

    if (!email || !password) {
        showError('Email and password are required');
        return;
    }

    const signinBtn = document.getElementById('signinBtn');
    signinBtn.disabled = true;
    signinBtn.textContent = 'Signing In...';

    try {

        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Login failed');
        }


        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user', JSON.stringify(data.user));


        const userResponse = await fetch('/api/auth/me', {
            headers: {
                'Authorization': `Bearer ${data.access_token}`
            }
        });

        if (userResponse.ok) {
            const userData = await userResponse.json();
            await displayUserInfo(userData);
        }

    } catch (error) {
        console.error('Signin error:', error);
        showError('Invalid email or password');
    } finally {
        signinBtn.disabled = false;
        signinBtn.textContent = 'Sign In';
    }
});


logoutBtn.addEventListener('click', async () => {
    try {
        const token = localStorage.getItem('access_token');

        await fetch('/api/auth/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });


        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');

        welcomeScreen.classList.remove('show');
        authSection.style.display = 'block';
        signupFormElement.reset();
        signinFormElement.reset();
    } catch (error) {
        console.error('Logout error:', error);
    }
});

(async function checkAuth() {
    loadingState.style.display = 'block';
    authSection.style.display = 'none';

    const token = localStorage.getItem('access_token');

    if (token) {
        try {

            const response = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const userData = await response.json();
                await displayUserInfo(userData);
            } else {
                // Token 无效，清除并显示登录表单
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                authSection.style.display = 'block';
            }
        } catch (error) {
            console.error('Error checking auth:', error);
            authSection.style.display = 'block';
        }
    } else {
        authSection.style.display = 'block';
    }

    loadingState.style.display = 'none';
})();