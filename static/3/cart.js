function addToCart(event, productId) {
    event.preventDefault(); // جلوگیری از بارگذاری مجدد صفحه

    var form = document.getElementById('add-to-cart-form');
    var formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // به روز رسانی اطلاعات سبد خرید
        document.getElementById('total-price').innerText = data.total_price + ' تومان';
        document.getElementById('cart-summary').style.display = 'block';
        updateCartItems(data.cart_item_count, data.cart_items);
    })
    .catch(error => console.log('Error:', error));
}

function updateCartItems(cartItemCount, cartItems) {
    var cartItemsContainer = document.getElementById('cart-items');
    cartItemsContainer.innerHTML = ''; // پاک کردن محتویات قبلی

    cartItems.forEach(item => {
        var row = document.createElement('tr');
        row.innerHTML = `
            <td><img src="${item.product_image}" alt="${item.product_name}" width="50"></td>
            <td>${item.product_name}</td>
            <td>${item.quantity}</td>
            <td>${item.product_price} تومان</td>
            <td>${item.total_price} تومان</td>
            <td><button class="btn btn-danger btn-sm" onclick="removeFromCart(${item.id})">حذف</button></td>
        `;
        cartItemsContainer.appendChild(row);
    });
}
