(function () {
    console.log('Hello');

    const button = document.getElementById('btnSignUp');
    button.onclick = function () {
        const studentId = document.querySelector('[name=studentID]').value;
        const fullname = document.querySelector('[name=fullname]').value;
        const birthday = document.querySelector('[name=birthday]').value;
        const email = document.querySelector('[name=email]').value;
        const password = document.querySelector('[name=password]').value;
        const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const userData = {
            masv: studentId,
            ten: fullname,
            namSinh: birthday,
            email: email,
            matkhau: password
        };

        const result = validate(userData);

        if (result.is_valid) {
            createUser(userData, csrfmiddlewaretoken)
                .then(res => {
                    console.log(res);
                    if (res.error) {
                        alert(res.message);
                    }
                    else if (res.data) {
                        alert(res.message);
                        console.log(res.data);
                    }
                    else {
                        console.log('');
                    }
                });
        } else {
            console.log(result.errors);
            alert(result.errors.join('\n'));
        }

        return false;
    }
})();


function validate(userData) {// xác thực dữ liệu người dùng nhập vào
    const errors = [];

    if (!userData.masv || !/^[a-z0-9_]{6,100}$/i.test(userData.masv)) {
        errors.push('Mã sinh viên bao gồm các kí tự a-z 0-9 và _ từ 6 đến 100 kí tự');
    }

    if (!userData.ten || userData.ten.length < 6) {
        errors.push('Tên không được để trống và ít nhất 6 kí tự');
    }

    if (!userData.namSinh || !/^[0-9]{4}$/.test(userData.namSinh)) {
        errors.push('Năm sinh phải là số có 4 chữ số');
    }

    if (!userData.email || !/^[a-z0-9_\.]{6,100}@[a-z0-9_]{2,20}\.[a-z]{2,3}$/i.test(userData.email)) {
        errors.push('Email không hợp lệ');
    }

    if (!userData.matkhau || !/^[a-z0-9_]{6,100}$/i.test(userData.matkhau)) {
        errors.push('Mật khẩu bao gồm các kí tự a-z 0-9 và _ từ 6 đến 100 kí tự');
    }

    return {
        is_valid: errors.length === 0,
        errors: errors
    };
}


function createUser(userData, csrfmiddlewaretoken) {
    const path = '/api/auth/register/';

    return fetch(path, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfmiddlewaretoken
        },
        body: JSON.stringify(userData)
    }).then(res => res.json());
}