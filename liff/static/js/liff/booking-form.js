document
    .addEventListener('DOMContentLoaded', (event) => {
        let round_date = document.getElementById('id_round_date');
        let round_time = document.getElementById('id_round_time');
        let pax = document.getElementById('id_pax');
        let cart = document.getElementById('id_cart');

        let green_fee_unit_price = document.getElementById('green-fee-unit-price');
        let green_fee_pax = document.getElementById('green-fee-pax');
        let green_fee_amount = document.getElementById('green-fee-amount');

        let caddie_fee_unit_price = document.getElementById('caddie-fee-unit-price');
        let caddie_fee_pax = document.getElementById('caddie-fee-pax');
        let caddie_fee_amount = document.getElementById('caddie-fee-amount');

        let cart_fee_unit_price = document.getElementById('cart-fee-unit-price');
        let cart_fee_pax = document.getElementById('cart-fee-pax');
        let cart_fee_amount = document.getElementById('cart-fee-amount');

        let fee_total_amount = document.getElementById('fee-total-amount');

        document
            .getElementById('pax-plus-button')
            .addEventListener('click', function (e) {
                pax.value = Number(pax.value) + 1;
            });

        document
            .getElementById('pax-minus-button')
            .addEventListener('click', function (e) {
                pax.value = Number(pax.value) - 1;
            });

        document
            .getElementById('cart-plus-button')
            .addEventListener('click', function (e) {
                cart.value = Number(cart.value) + 1;
            });

        document
            .getElementById('cart-minus-button')
            .addEventListener('click', function (e) {
                cart.value = Number(cart.value) - 1;
            });

        [round_date, round_time, pax, cart].forEach(function (element) {
            element.addEventListener('change', function (e) {
                if (round_date.value && round_time.value && pax.value && cart.value) {
                    console.log(round_date.value);
                    console.log(round_time.value);
                    console.log(pax.value);
                    console.log(cart.value);
                }
            });
        });
    });