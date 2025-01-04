// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Example: Handle a button click
    const button = document.getElementById('myButton');
    if (button) {
        button.addEventListener('click', () => {
            alert('Button was clicked!');
        });
    }

    // Example: Handle form submission
    const form = document.getElementById('myForm');
    if (form) {
        form.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevent the default form submission
            const formData = new FormData(form);
            // Process form data here
            console.log('Form submitted:', Object.fromEntries(formData));
            alert('Form submitted successfully!');
        });
    }

    // Chat popup functionality
    const chatPopup = document.getElementById('chat-popup');
    const openChat = document.getElementById('open-chat');
    const closeChat = document.getElementById('close-chat');

    if (openChat) {
        openChat.addEventListener('click', () => {
            chatPopup.style.display = 'block';
        });
    }

    if (closeChat) {
        closeChat.addEventListener('click', () => {
            chatPopup.style.display = 'none';
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // Example: Handle star rating hover effect
    const ratings = document.querySelectorAll('.rating');

    ratings.forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        const currentRating = parseInt(rating.getAttribute('data-rating'));

        // Highlight stars based on the current rating
        stars.forEach((star, index) => {
            if (index < currentRating) {
                star.style.display = 'inline'; // Show filled stars
            } else {
                star.style.display = 'none'; // Hide empty stars
            }
        });
    });
});

function updateCart(productId, quantity, price) {
    fetch(`/update_cart/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const totalElement = document.getElementById(`total-${productId}`);
            const totalPrice = price * quantity; // Calculate new total price
            totalElement.innerText = formatPrice(totalPrice);
            updateGrandTotal();
        }
    });
}

function removeFromCart(productId) {
    fetch(`/remove_from_cart/${productId}`, {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            const row = document.getElementById(`row-${productId}`);
            row.remove();
            updateGrandTotal(); // Update the grand total
        } else {
            alert('Failed to remove the product from the cart.');
        }
    });
}

function updateGrandTotal() {
    let grandTotal = 0;
    const totalElements = document.querySelectorAll('td[id^="total-"]');
    totalElements.forEach(element => {
        grandTotal += parseFloat(element.innerText.replace(/[^0-9.-]+/g, ""));
    });
    document.getElementById('grand-total').innerText = formatPrice(grandTotal);
}

function format_price(price) {
    return `Rp${price.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, '.')}`; // Format price to Indonesian Rupiah
}