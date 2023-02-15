(function () {
    console.log('Hello!');

    const btnLogin = document.getElementById('btnLogin'); // lay cai button login

    btnLogin.onclick = function () {
        const masv = document.querySelector('[name=studentID]').value;  // lay cai input studentID
        const matkhau = document.querySelector('[name=password]').value; // lay cai input password

        if (masv === '' || matkhau === '') {
            alert('Vui lòng nhập đầy đủ thông tin!');
        } else {
            const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value; // ma bao mat form
            login({
                masv, matkhau
            }, csrf_token).then(response => {
                if (response.data) { // neu dang nhap thanh cong
                    window.location.href = '/';
                } else { // neu dang nhap that bai
                    alert(response.message);
                }
            });
        }
        return false;
    }
})();


function login(userData, csrf_token) {  // ham dang nhap, gui thong tin len server de xu ly dang nhap va tra ve ket qua
    const path = '/api/auth/login/';
    return fetch(path, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(userData)
    }).then(response => {
        return response.json();
    });
}