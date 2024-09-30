function selectBus(busName) {
    document.getElementById('selected-bus').value = busName;
    document.getElementById('booking-form').style.display = 'block';
}

function submitBooking(event) {
    event.preventDefault();

    const name = document.getElementById('passenger-name').value;
    const email = document.getElementById('passenger-email').value;
    const bus = document.getElementById('selected-bus').value;

    const message = `Thank you, ${name}! You have successfully booked ${bus}. A confirmation has been sent to ${email}.`;
    
    document.getElementById('message').innerText = message;
    document.getElementById('form').reset();
    document.getElementById('booking-form').style.display = 'none';
}
