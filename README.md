# TechMint-Assignment
This application calculates the credit and debit amount between users. Application is based on django restframework.

This application has 3 api's, 1 html and 1 celery task

Api's Explaination

index:

Purpose: This view is designed to render the main or homepage of your application.
Explanation: When a user accesses the root URL or the base URL of your application, the index function serves the 'index.html' template to them. This template could be a landing page, a dashboard, or any primary page you intend your users to see when they first arrive.
create_expense:

Purpose: This API endpoint allows clients to create a new expense and split it among various participants.
Explanation: The API takes the number of participants, their details, and the individual expenses they made. It first creates an expense entry, and then for each participant, it creates a participant entry and associates it with the expense. The total expense is divided equally among all participants, and the amount each owes is calculated. The response returns a bill split summary, showing how much each participant owes.
get_passbook:

Purpose: This API endpoint is meant to fetch the financial summary or passbook for a specific participant.
Explanation: Upon providing a participant's ID, the API retrieves all expense records related to that participant. It calculates the total amount the participant owes across all expenses. The detailed breakdown, including each expense description and amount, is also provided. This passbook gives a comprehensive financial history for a participant, making it easier for them to track and settle expenses.

Models:
Expense Model: Represents an individual expense entry, containing the total amount of the expense and a description to provide context or details about the expense. The string representation of an instance displays its description and amount.

Participant Model: Represents a person who is part of one or more expenses. It stores their name, email, and phone_number. It has a many-to-many relationship with the Expense model through the ExpenseParticipant model, enabling tracking of multiple participants per expense and vice versa.

ExpenseParticipant Model: Acts as a through model to manage the many-to-many relationship between Expense and Participant. It keeps track of how much each participant owes (owed_amount) for a particular expense. This way, the application can handle splitting of an expense among multiple participants, showing who owes what for each expense