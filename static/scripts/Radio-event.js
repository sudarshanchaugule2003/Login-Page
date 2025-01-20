document.addEventListener("DOMContentLoaded", function() {
    const radioButtons = document.querySelectorAll('input[name="subject"]');
    const dynamicForm = document.createElement('div');

    const form = document.querySelector('.fill-form');
    form.appendChild(dynamicForm);

    function renderForm(value) {
        let formContent = '';
        switch (value) {
            case 'subject1':
                formContent = `
                    <div class = "sub-form-select">
                            <h2>Subject 1 Form</h2>
                            <br><br>

                            <form>
                                <h3>Random Heading</h3>
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
                            </form>

                            <button type="button">Next</button>
                    </div>
                `;
                break;
            case 'subject2':
                formContent = `
                    <div class = "sub-form-select">
                            <h2>Subject 2 Form</h2>
                            <br><br>

                            <form>
                                <h3>Random Heading</h3>
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
                            </form>

                            <button type="button">Next</button>
                    </div>
                `;
                break;
            case 'subject3':
                formContent = `
                    <div class = "sub-form-select">
                            <h2>Subject 3 Form</h2>
                            <br><br>

                            <form>
                                <h3>Random Heading</h3>
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
                            </form>

                            <button type="button">Next</button>
                    </div>
                `;
                break;
            case 'subject4':
                formContent = `
                   <div class = "sub-form-select">
                            <h2>Subject 4 Form</h2>
                            <br><br>

                            <form>
                                <h3>Random Heading</h3>
                                <h4>Question 1:</h4>
                                <label><input type="radio" name="q1" value="option1"> Option 1</label><br>
                                <label><input type="radio" name="q1" value="option2"> Option 2</label><br>
                                <label><input type="radio" name="q1" value="option3"> Option 3</label><br>
                                <label><input type="radio" name="q1" value="option4"> Option 4</label><br><br>

                                <h4>Question 2:</h4>
                                <label><input type="radio" name="q2" value="option1"> Option 1</label><br>
                                <label><input type="radio" name="q2" value="option2"> Option 2</label><br>
                                <label><input type="radio" name="q2" value="option3"> Option 3</label><br>
                                <label><input type="radio" name="q2" value="option4"> Option 4</label><br><br>

                                <h4>Question 3:</h4>
                                <label><input type="radio" name="q3" value="option1"> Option 1</label><br>
                                <label><input type="radio" name="q3" value="option2"> Option 2</label><br>
                                <label><input type="radio" name="q3" value="option3"> Option 3</label><br>
                                <label><input type="radio" name="q3" value="option4"> Option 4</label><br><br>

                                <h4>Question 4:</h4>
                                <label><input type="radio" name="q4" value="option1"> Option 1</label><br>
                                <label><input type="radio" name="q4" value="option2"> Option 2</label><br>
                                <label><input type="radio" name="q4" value="option3"> Option 3</label><br>
                                <label><input type="radio" name="q4" value="option4"> Option 4</label><br><br>
                            </form>

                            <button type="button">Next</button>
                    </div>
                `;
                break;
            default:
                formContent = '';
        }
        dynamicForm.innerHTML = formContent;
        dynamicForm.style.display = formContent ? 'block' : 'none';
    }

    //event listener to radio button
    radioButtons.forEach(radio => {
        radio.addEventListener('change', (event) => {
            renderForm(event.target.value);
        });
    });
});
