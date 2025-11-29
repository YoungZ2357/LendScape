

const supabase = supabase.createClient(
    'https://nrvwkdppdznvorrwhogs.supabase.co',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5ydndrZHBwZHpudm9ycndob2dzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NjkxOTMsImV4cCI6MjA3OTA0NTE5M30.MUzz48qCj_fv01SrhgpWVp_MmdBbueclhQXeS7yqdpo'
);

// ------------ UI 切换函数 ------------

async function refreshUI() {
    const session = (await supabase.auth.getSession()).data.session;

    if (session) {
        // 有用户 → 显示用户界面
        const user = session.user;

        document.getElementById("userName").innerText = user.user_metadata?.name || "(无名字)";
        document.getElementById("userEmail").innerText = user.email;

        document.getElementById("loginPanel").style.display = "none";
        document.getElementById("registerPanel").style.display = "none";
        document.getElementById("userPanel").style.display = "block";
    } else {
        // 未登录 → 显示登录界面
        document.getElementById("loginPanel").style.display = "block";
        document.getElementById("registerPanel").style.display = "none";
        document.getElementById("userPanel").style.display = "none";
    }
}

refreshUI(); // 页面首次加载检查 session


// ------------ 登录功能 ------------

document.getElementById("loginBtn").onclick = async () => {
    let email = document.getElementById("loginEmail").value;
    let pwd = document.getElementById("loginPassword").value;

    const { data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: pwd
    });

    if (error) {
        document.getElementById("loginMsg").innerText = error.message;
    } else {
        document.getElementById("loginMsg").innerText = "登录成功！";
        await refreshUI();
    }
};


// ------------ 注册功能 ------------

document.getElementById("registerBtn").onclick = async () => {
    let email = document.getElementById("regEmail").value;
    let pwd = document.getElementById("regPassword").value;
    let name = document.getElementById("regName").value;

    const { data, error } = await supabase.auth.signUp({
        email: email,
        password: pwd,
        options: {
            data: { name: name }
        }
    });

    if (error) {
        document.getElementById("regMsg").innerText = error.message;
    } else {
        document.getElementById("regMsg").innerText = "注册成功！请检查邮箱验证";
    }
};


// ------------ 登出功能 ------------

document.getElementById("logoutBtn").onclick = async () => {
    await supabase.auth.signOut();
    refreshUI();
};


// ------------ 页面切换按钮 ------------

document.getElementById("goRegister").onclick = () => {
    document.getElementById("loginPanel").style.display = "none";
    document.getElementById("registerPanel").style.display = "block";
};

document.getElementById("goLogin").onclick = () => {
    document.getElementById("registerPanel").style.display = "none";
    document.getElementById("loginPanel").style.display = "block";
};




async function apiFetch(url, options = {}) {
    const session = (await supabase.auth.getSession()).data.session;

    if (!session) {
        alert("未登录");
        return;
    }

    const token = session.access_token;

    options.headers = {
        ...(options.headers || {}),
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
    };

    return fetch(url, options);
}
