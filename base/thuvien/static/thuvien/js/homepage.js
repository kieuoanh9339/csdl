
(function () {
    updateBooksInCart();
})();

function showBookInfo(id) {
    const modal = document.getElementById('modal__sachInfo');

    fetch('/api/sach/' + id)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.maSach) {
                modal.querySelector('#btnAddToCart').setAttribute('book-id', data.maSach);

                Object.keys(data).forEach(key => {
                    const element = modal.querySelector('.' + key);
                    if (element) {
                        element.innerText = data[key];
                    }
                });

                modal.classList.add('active');
            }
        }).catch(function (err) {
            console.log(err);
        });
}

function addToCart() {
    const maSach = document.querySelector('#modal__sachInfo .maSach');
    const tenSach = document.querySelector('#modal__sachInfo .tenSach');
    if (!localStorage.getItem('cart')) {
        localStorage.setItem('cart', JSON.stringify([]));
    }
    const cart = JSON.parse(localStorage.getItem('cart'));
    const index = cart.findIndex(item => item.maSach === maSach.innerText);
    if (index === -1) {
        cart.push({
            maSach: maSach.innerText,
            tenSach: tenSach.innerText,
            soLuong: 1
        });
    } 
    localStorage.setItem('cart', JSON.stringify(cart));
    updateBooksInCart();
    alert('Đã thêm sách vào giỏ');
}