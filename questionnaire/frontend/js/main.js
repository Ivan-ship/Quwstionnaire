document.getElementById('signon').addEventListener('submit', function(e){
    const email = document.getElementById('email').value;

    if(!email.include('@')){
        alert('Email должен включать @');
        e.preventDefault();
    }
});