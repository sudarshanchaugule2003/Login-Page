document.addEventListener("DOMContentLoaded", function () {
    const radioButtons = document.querySelectorAll('input[name="subject"]');
    const dynamicForm = document.createElement('div');
    const formContainer = document.querySelector('.fill-form');
    formContainer.appendChild(dynamicForm);
    let userResponses = {}; // To store user responses

    function renderForm(value) {
        let formContent = '';
        switch (value) {
            case 'subject1':
                formContent = `
                    <div class="sub-form-select">
                        <h2>Subject 1 Form</h2>
                        <form id="subject1-form">
                            <h3>Random Heading for Subject 1</h3>
                            <p>Question 1:</p>
                            <label><input type="radio" name="q1" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q1" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q1" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q1" value="option4"> Option 4</label><br><br>

                            <p>Question 2:</p>
                            <label><input type="radio" name="q2" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q2" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q2" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q2" value="option4"> Option 4</label><br><br>

                            <p>Question 3:</p>
                            <label><input type="radio" name="q3" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q3" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q3" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q3" value="option4"> Option 4</label><br><br>

                            <p>Question 4:</p>
                            <label><input type="radio" name="q4" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q4" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q4" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q4" value="option4"> Option 4</label><br><br>

                            <button type="button" id="next-btn">Next</button>
                        </form>
                    </div>
                `;
                break;

            case 'subject2':
                formContent = `
                    <div class="sub-form-select">
                        <h2>Subject 2 Form</h2>
                        <form id="subject2-form">
                            <h3>Random Heading for Subject 2</h3>
                            <p>Question 1:</p>
                            <label><input type="radio" name="q1" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q1" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q1" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q1" value="option4"> Option 4</label><br><br>

                            <p>Question 2:</p>
                            <label><input type="radio" name="q2" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q2" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q2" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q2" value="option4"> Option 4</label><br><br>

                            <p>Question 3:</p>
                            <label><input type="radio" name="q3" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q3" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q3" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q3" value="option4"> Option 4</label><br><br>

                            <p>Question 4:</p>
                            <label><input type="radio" name="q4" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q4" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q4" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q4" value="option4"> Option 4</label><br><br>

                            <button type="button" id="next-btn">Next</button>
                        </form>
                    </div>
                `;
                break;

            case 'subject3':
                formContent = `
                    <div class="sub-form-select">
                        <h2>Subject 3 Form</h2>
                        <form id="subject3-form">
                            <h3>Random Heading for Subject 3</h3>
                            <p>Question 1:</p>
                            <label><input type="radio" name="q1" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q1" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q1" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q1" value="option4"> Option 4</label><br><br>

                            <p>Question 2:</p>
                            <label><input type="radio" name="q2" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q2" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q2" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q2" value="option4"> Option 4</label><br><br>

                            <p>Question 3:</p>
                            <label><input type="radio" name="q3" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q3" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q3" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q3" value="option4"> Option 4</label><br><br>

                            <p>Question 4:</p>
                            <label><input type="radio" name="q4" value="option1"> Option 1</label><br>
                            <label><input type="radio" name="q4" value="option2"> Option 2</label><br>
                            <label><input type="radio" name="q4" value="option3"> Option 3</label><br>
                            <label><input type="radio" name="q4" value="option4"> Option 4</label><br><br>

                            <button type="button" id="next-btn">Next</button>
                        </form>
                    </div>
                `;
                break;

            default:
                formContent = '<p>Please select a subject to load the form.</p>';
        }

        dynamicForm.innerHTML = formContent;
        dynamicForm.style.display = formContent ? 'block' : 'none';

        // Attach event listener to the Next button
        const nextButton = document.getElementById('next-btn');
        if (nextButton) {
            nextButton.addEventListener('click', loadNextForm);
        }
    }

    // Event listener for radio buttons
    radioButtons.forEach((radio) => {
        radio.addEventListener('change', (event) => {
            renderForm(event.target.value);
        });
    });

    function loadNextForm() {
        dynamicForm.innerHTML = `
            <div class="sub-form-next">
                <h2>Follow-up Form</h2>
                <form id="followup-form">
                    <p>Follow-up Question 1:</p>
                    <input type="text" name="followup1" placeholder="Enter your answer"><br><br>
                    <p>Follow-up Question 2:</p>
                    <input type="text" name="followup2" placeholder="Enter your answer"><br><br>
                    <button type="submit" id="submit-btn">Submit</button>
                </form>
            </div>
        `;

        const submitButton = document.getElementById('submit-btn');
        if (submitButton) {
            submitButton.addEventListener('click', handleFinalSubmission);
        }
    }

    function handleFinalSubmission(event) {
        event.preventDefault();
        const formElement = document.querySelector('#followup-form');
        const formData = new FormData(formElement);

        userResponses = {}; // Clear previous responses
        formData.forEach((value, key) => {
            userResponses[key] = value;
        });

        alert('Final Responses Submitted: ' + JSON.stringify(userResponses));
        dynamicForm.innerHTML = ''; // Clear the form
    }
});
