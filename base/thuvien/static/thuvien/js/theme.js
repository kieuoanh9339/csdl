function userMenuToggle() {
    const userMenu = document.querySelector('.user .userMenu');
    userMenu.classList.toggle('active');
}

function hideModal() {
    document.querySelectorAll('.modal-overlay').forEach(function (modal) {
        modal.classList.remove('active');
    });
}

function updateBooksInCart() {
    const books = JSON.parse(localStorage.getItem('cart'));
    const cart = document.querySelector('.cart .count');
    cart.innerText = books ? books.length : 0;
}

function viewCart() {
    window.location.href = '/cart';
}

document.querySelector('.siteName').onclick = function () {
    window.location.href = '/';
};