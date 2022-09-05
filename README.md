# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.


# Trivia API Endpoints Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample request: `curl http://127.0.0.1:5000/categories`

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'`

- Fetches a list of question objects in which each object contains the question, the answer to the question, the question category and the difficulty level
- Request Arguments: None
- Returns: An object with a `questions` key that that contains a list of paginated 10 question objects having `question:question_string, answer:answer_string,category:category_string,difficulty:difficulty_value` key: value pairs, `categories` key having an object of `id: category_string` key: value pairs, the `success:True` key: value pair, the `current_category:value` key:value pair and the `total_questions` key: value pair .
- Sample request: `curl http://127.0.0.1:5000/questions`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }    
  ],
  "success": true,
  "total_questions": 18
}
```


`DELETE '/questions/<int:question_id>'`

- Deletes a particular question given the question id
- Request Arguments: question id
- Returns: An object with a `success:True` key: value pair.
- Sample request: `curl http://127.0.0.1:5000/questions/6 -X DELETE`

```json
{
  "success": true,
}
```

`POST '/questions'`

- Creates a new question
- Request Arguments: `question_string`, `answer text`, `category`, and `difficulty score`
- Returns: An object with a `questions` key that that contains a list of paginated 10 question objects having `question:question_string, answer:answer_text,category:category_string,difficulty:difficulty_score` key: value pairs, the `success:True` key: value pair, and the `total_questions` key: value pair .
- Sample request: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{\"question\":\"First club in Europe to win 20 EPL titles\", \"answer\":\"Manchester United\", \"difficulty\":2, \"category\":2}"`

```json
{
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }    
  ],
  "success": true,
  "total_questions": 18
}
```


`POST '/questions/search'`

- Fetches any questions for whom the search term is a substring of the question
- Request Arguments: `searchTerm`
- Returns: An object with a `questions` key that that contains a list of paginated 10 question objects having `question:question_string, answer:answer_text,category:category_string,difficulty:difficulty_score` key: value pairs, the `success:True` key: value pair, the `current_category:value` key:value pair, and the `total_questions` key: value pair .
- Sample request: `curl http://127.0.0.1:5000/questions/search  -X POST -H "Content-Type: application/json" -d "{\"searchTerm\":\"Tom\"}"`

```json
{
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }    
  ],
  "current_category": null,
  "success": true,
  "total_questions": 18
}
```

`GET '/categories/<int:category_id>/questions'`

- Fetches questions based on category
- Request Arguments: `category_id`
- Returns: An object with a `questions` key that that contains a list of paginated 10 question objects having `question:question_string, answer:answer_text,category:category_string,difficulty:difficulty_score` key: value pairs, the `success:True` key: value pair, the `current_category:category_id` key:value pair, and the `total_questions` key: value pair.
- Sample request: `curl http://127.0.0.1:5000/categories/2/questions`

```json
{
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }    
  ],
  "current_category": null,
  "success": true,
  "total_questions": 18
}
```


`POST '/quizzes'`

- Fetches questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions
- Request Arguments: `quiz_category` and `previous_question` 
- Returns: An object with single key `question` a question object having `question:question_string, answer:answer_text,category:category_string,difficulty:difficulty_score` key: value pairs, and the `success:True` key: value pair.
- Sample request: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\":[], \"quiz_category\":{\"id\":0} }"`

```json
{
  "questions":
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
  "success": true,
}
```


