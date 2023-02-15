(function () {
    updateBooksInCart();

    const btnSubmit = document.getElementById('btnSubmit');
    btnSubmit.onclick = () => {
        const data = {};
        const errors = [];
        let check = true;
        document.querySelectorAll('.account-area table tbody input').forEach(input => {
            if (input.value) {
                data[input.name] = input.value;
            } else {
                errors.push('Vui lòng nhập ' + input.ariaPlaceholder);
                check = false;
            }
        });
        if (check) {
            updateUser(data).then(res => {
                if (res.success) {
                    alert('Cập nhật thành công');
                    window.location.href = '/';
                } else {
                    alert('Cập nhật thất bại');
                }
            });
        } else {
            if (errors.length) {
                alert(errors.join('\n'));
            }
        }
    }
})();


function updateUser(data) {
    return fetch('/api/me/', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': getCookieByName('csrftoken'),
        },
        body: JSON.stringify(data)
    }).then(res => res.json());
}