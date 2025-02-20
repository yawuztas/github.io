function showOrderSummary() {
    const orderForm = document.getElementById('orderForm');
    const products = orderForm.querySelectorAll('.product');
    let total = 0;
    
    products.forEach(product => {
        const productName = product.querySelector('h3').textContent;
        const productQuantity = parseInt(product.querySelector('input').value);
        
        if (productQuantity > 0) {
            total += 1000 * productQuantity;
        }
    });

    if (total === 0) {
        alert('Lütfen en az bir ürün seçiniz!');
        return;
    }

    const orderSummary = document.getElementById('orderSummary');
    orderSummary.innerHTML = '<h3>Sipariş Özeti</h3>';
    
    products.forEach(product => {
        const productName = product.querySelector('h3').textContent;
        const productQuantity = parseInt(product.querySelector('input').value);
        
        if (productQuantity > 0) {
            orderSummary.innerHTML += `
                <p>Ürün: ${productName}</p>
                <p>Adet: ${productQuantity}</p>
                <p>Fiyat: ${1000 * productQuantity} TL</p>
                <hr>
            `;
        }
    });

    orderSummary.innerHTML += `<p>Total: ${total} TL</p>`;
    
    window.location.href = 'siparis.html';
}

function completeOrder() {
    alert('Siparişiniz başarıyla tamamlandı!');
    window.location.href = 'index.html';
}
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

