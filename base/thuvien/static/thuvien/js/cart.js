(function () {
    updateBooksInCart();
    const tableBody = document.querySelector('.checkout-area table tbody');
    const cart = JSON.parse(localStorage.getItem('cart'));
    if (cart) {
        cart.forEach(sach => {
            const td = `<tr class="sach-item">
                            <td>${sach.maSach}</td>
                            <td>${sach.tenSach}</td>
                            <td>
                                <div class="form-element">
                                    <input type="number" name="soLuong" value="${sach.soLuong}">
                                </div>
                            </td>
                        </tr>`;
            tableBody.innerHTML += td;
        })
    } else {
        tableBody.innerHTML = `<tr><td colspan="3">Không có sách nào trong giỏ hàng</td></tr>`;
    }


    const btnSubmit = document.getElementById('btnSubmit');
    btnSubmit.onclick = () => {
        const sach = [];
        document.querySelectorAll('.checkout-area table tbody tr.sach-item').forEach(tr => {
            const maSach = tr.querySelector('td:nth-child(1)').innerText;
            const soLuong = tr.querySelector('td:nth-child(3) input').value;
            if (soLuong > 0) {
                sach.push({
                    maSach: maSach,
                    soLuong: soLuong
                })
            }
        });
        const date = new Date();
        const ngayTra = document.querySelector('#ngayTra').value;
        if (sach.length && ngayTra && new Date(ngayTra) > date) {
            const data = {
                ngayTra,
                sach,
                ngayMuon: date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
            };
            taoTheMuon(data).then(res => {
                if (res.success) {
                    alert(res.message);
                    localStorage.removeItem('cart');
                    window.location.href = '/';
                } else {
                    alert(res.message);
                }
            })
        } else {
            alert('Vui lòng nhập đầy đủ thông tin (phải có ít nhất 1 cuốn sách, ngày mượn phải sau ngày hôm nay)');
        }
    }
})();

function taoTheMuon(data) {
    return fetch('/api/themuon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': getCookieByName('csrftoken')
        },
        body: JSON.stringify(data)
    }).then(res => res.json());
}