document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('booking_form');
    const totalPriceDisplay = document.getElementById('total_price');
    const hiddenTotalPrice = document.getElementById('hidden_total_price');
    const basePrice = parseFloat(document.getElementById('base_price').dataset.price);
    const youthPrice = parseFloat(document.getElementById('youth_price').dataset.price);

    // Set minimum date for date input
    const dateInput = form.querySelector('[name="booking_date"]');
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    // Format date to YYYY-MM-DD
    const formattedTomorrow = tomorrow.toISOString().split('T')[0];
    dateInput.setAttribute('min', formattedTomorrow);
    
    // If selected date is before tomorrow, reset it
    dateInput.addEventListener('change', function() {
        const selectedDate = new Date(this.value);
        if (selectedDate < tomorrow) {
            this.value = formattedTomorrow;
            alert('Please select a future date');
        }
    });

    function formatIndianCurrency(number) {
        const result = number.toString().split('.');
        let lastThree = result[0].substring(result[0].length - 3);
        let otherNumbers = result[0].substring(0, result[0].length - 3);
        if (otherNumbers != '') {
            lastThree = ',' + lastThree;
        }
        let formatted = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree;
        return formatted + (result[1] ? '.' + result[1] : '');
    }

    function calculateTotal() {
        // Get guest counts
        const adults = parseInt(form.querySelector('[name="adults"]').value) || 0;
        const youth = parseInt(form.querySelector('[name="youth"]').value) || 0;
        const children = parseInt(form.querySelector('[name="children"]').value) || 0;

        // Calculate base price for guests
        let total = (adults * basePrice) + (youth * youthPrice);

        // Add additional services
        const services = form.querySelectorAll('input[name="services[]"]:checked');
        services.forEach(service => {
            const price = parseFloat(service.dataset.price);
            const type = service.dataset.type;
            
            if (type === 'per_booking') {
                total += price;
            } else if (type === 'per_person') {
                total += price * (adults + youth); // Children don't count for per-person services
            }
        });

        // Update displays with Indian currency format
        totalPriceDisplay.textContent = `Rs.${formatIndianCurrency(total)}`;
        hiddenTotalPrice.value = total.toFixed(2);
    }

    // Add event listeners for all inputs that affect price
    form.querySelectorAll('select, input[type="checkbox"]').forEach(input => {
        input.addEventListener('change', calculateTotal);
    });

    // Calculate initial total
    calculateTotal();

    // Update form submission handler with better validation
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Always prevent default first

        // Get values
        const adults = parseInt(form.querySelector('[name="adults"]').value) || 0;
        const youth = parseInt(form.querySelector('[name="youth"]').value) || 0;
        const total = parseFloat(hiddenTotalPrice.value) || 0;

        // Check if there's at least one person
        if (adults === 0 && youth === 0) {
            Swal.fire({
                title: 'Select Guests',
                text: 'Please select at least one adult or youth guest to continue.',
                icon: 'warning',
                confirmButtonText: 'OK',
                confirmButtonColor: '#3085d6'
            });
            return false;
        }

        // Check if total price is greater than 0
        if (total <= 0) {
            Swal.fire({
                title: 'Invalid Amount',
                text: 'The total amount must be greater than zero.',
                icon: 'error',
                confirmButtonText: 'OK',
                confirmButtonColor: '#3085d6'
            });
            return false;
        }

        // If all validations pass, submit the form
        form.submit();
    });
});
