(async function() {
    updateBooksInCart();

    try {
        const data = await getHistory();
        data.forEach(the => {
            the.sach.forEach(s => {
                const tr = `<tr>
                    <td>${the.maThe}</td>
                    <td>${s.maSach}</td>
                    <td>${s.tenSach}</td>
                    <td>${s.soLuong}</td>
                    <td>${the.ngayMuon}</td>
                    <td>${the.ngayTra}</td>
                </tr>`;
                document.querySelector('.history-area table tbody').innerHTML += tr;
            })
        })
    } catch (error) {
        console.log(error);
    }
        
})();


function getHistory() {
    return fetch('/api/themuon/').then(res => res.json());
}