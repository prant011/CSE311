document.addEventListener('DOMContentLoaded', function() {
    const studentIdInput = document.getElementById('student_id');
    
    if (studentIdInput) {
        studentIdInput.addEventListener('blur', function() {
            const studentId = this.value.trim();
            const errorDiv = document.getElementById('id-error');
            
            if (studentId) {
                // Make AJAX request to validate
                fetch(`/validate-student-id/?student_id=${encodeURIComponent(studentId)}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.exists) {
                            errorDiv.textContent = '⚠️ Student ID already exists!';
                            errorDiv.classList.add('text-danger');
                            errorDiv.classList.remove('text-success');
                            studentIdInput.classList.add('is-invalid');
                            studentIdInput.classList.remove('is-valid');
                        } else {
                            errorDiv.textContent = '✓ Student ID available';
                            errorDiv.classList.add('text-success');
                            errorDiv.classList.remove('text-danger');
                            studentIdInput.classList.add('is-valid');
                            studentIdInput.classList.remove('is-invalid');
                        }
                    })
                    .catch(error => {
                        console.error('Error validating student ID:', error);
                        errorDiv.textContent = '';
                    });
            } else {
                errorDiv.textContent = '';
                studentIdInput.classList.remove('is-valid', 'is-invalid');
            }
        });

        // Clear error on input
        studentIdInput.addEventListener('input', function() {
            const errorDiv = document.getElementById('id-error');
            if (errorDiv.textContent) {
                errorDiv.textContent = '';
                studentIdInput.classList.remove('is-valid', 'is-invalid');
            }
        });
    }

    // Form submission validation
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            const password = document.querySelector('input[name="password"]').value;
            const password2 = document.querySelector('input[name="password2"]').value;

            if (password !== password2) {
                e.preventDefault();
                alert('Passwords do not match!');
                return false;
            }

            // Check if student ID exists
            const errorDiv = document.getElementById('id-error');
            if (errorDiv.classList.contains('text-danger')) {
                e.preventDefault();
                alert('Please use a different Student ID!');
                return false;
            }
        });
    }
});
