// urunlerimiz.html için
function showOrderSummary() {
    const orderItems = [];
    let total = 0;
    
    document.querySelectorAll('.product').forEach(product => {
        const quantity = parseInt(product.querySelector('input').value);
        if(quantity > 0) {
            const productName = product.querySelector('h3').textContent;
            const productPrice = 1000;
            orderItems.push({
                name: productName,
                quantity: quantity,
                price: productPrice
            });
            total += productPrice * quantity;
        }
    });

    if(total === 0) {
        alert('Lütfen en az bir ürün seçiniz!');
        return;
    }

    localStorage.setItem('orderSummary', JSON.stringify({
        items: orderItems,
        total: total
    }));

    window.location.href = 'siparis.html';
}

// siparis.html için
function loadOrderSummary() {
    const orderData = JSON.parse(localStorage.getItem('orderSummary'));
    const orderSummary = document.getElementById('orderSummary');
    
    if(!orderData) {
        orderSummary.innerHTML = '<p>Henüz sipariş verilmemiş</p>';
        return;
    }

    orderSummary.innerHTML = '<h3>Sipariş Detayları</h3>';
    orderData.items.forEach(item => {
        orderSummary.innerHTML += `
            <div class="order-item">
                <p>Ürün: ${item.name}</p>
                <p>Adet: ${item.quantity}</p>
                <p>Tutar: ${item.price * item.quantity} TL</p>
            </div>
        `;
    });
    orderSummary.innerHTML += `<h4 class="total-price">Toplam: ${orderData.total} TL</h4>`;
}

function completeOrder() {
    localStorage.removeItem('orderSummary');
    alert('Siparişiniz başarıyla tamamlandı!');
    window.location.href = 'index.html';
}

// ai.html için

document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', function() {
        const message = userInput.value.trim();
        if (message) {
            addMessageToChat(message, 'user');
            userInput.value = '';
            // Burada AI'a soru göndermek için API çağrısı ekleyebilirsiniz
            setTimeout(function() {
                addMessageToChat('Bu bir demo cevaptır. Gerçek bir AI entegrasyonu için API anahtarınız gereklidir.', 'assistant');
            }, 1000);
        }
    });

    function addMessageToChat(message, sender) {
        const chatMessage = document.createElement('div');
        chatMessage.className = `chat-message ${sender}`;
        chatMessage.textContent = message;
        chatBox.appendChild(chatMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Enter tuşuna basıldığında mesaj gönderilsin
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.contact-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Mesajınız başarıyla gönderildi!');
        form.reset();
    });
});

