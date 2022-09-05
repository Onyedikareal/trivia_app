import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate(request, questions):
        page = request.args.get('page', 1, type=int)
        
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formated_questions = [question.format() for question in questions]
        return formated_questions[start: end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def get_categories(): 
        error = False
       
        categories = Category.query.all()
        if len(categories) != 0:
            formatted_categories = {category.id: category.type for category in categories}
        else:
            abort(404)
        
        
        return jsonify({
        'success':True,
        'categories':formatted_categories,
        'total_categories':len(formatted_categories)})


        


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def get_questions(): 
       
        questions = Question.query.all()
        
        
        page_questions = paginate(request, questions) 
        if len(page_questions) == 0:
            abort(404)
        categories = Category.query.all()

        formatted_categories = {category.id: category.type for category in categories}
    
        return jsonify({
        'success':True,
        'questions':page_questions,
        'current_category':None,
        'categories': formatted_categories,
        'total_questions':len(questions)})




        

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        error = False
        try: 
            db.session.delete(question)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        if error:
            abort(500)
        else:
            return jsonify({
            'success':True})

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def submit_question():
        request_body = request.get_json()
        question_body = request_body.get('question')
        answer = request_body.get('answer')
        difficulty = request_body.get('difficulty')
        category = request_body.get('category')
        if not question_body or not answer or not difficulty or not category:
            abort(400)
        

        question = Question(question=question_body, answer=answer, difficulty=difficulty,category= category)
        
        error = False
        try: 
            db.session.add(question)
            db.session.commit()
            questions = Question.query.order_by(Question.id).all()
            formatted_questions = paginate(request, questions) 
        except Exception as e:
            print(e)
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        if error:
            abort(500)
        else:
            return jsonify({
            'success':True,
            'questions':formatted_questions,
            'total_questions':len(questions)
            })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        
        request_body = request.get_json()
        search_term = request_body.get('searchTerm','')
        
        questions = Question.query.filter(Question.question.ilike('%'+search_term+'%'))
        formatted_questions = [question.format()
                                   for question in questions]
        
        
        return jsonify({
            'success':True,
            'questions':formatted_questions,
            'current_category':None,
            'total_questions':len(formatted_questions)})

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_category(category_id):

        
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        questions = Question.query.filter(Question.category == category_id).all()
        formatted_questions = [question.format()
                                   for question in questions]
        return jsonify({
            'success':True,
            'questions':formatted_questions,
            'current_category':category.id,
            'total_questions':len(questions)})

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        request_body = request.get_json()
        quiz_category = request_body.get('quiz_category')
        previous_questions = request_body.get('previous_questions')
        if not quiz_category:
            abort(400)

        category_id = quiz_category['id'] 
        
        if category_id == 0:
            question = Question.query.filter(
                Question.id.notin_((previous_questions))).first()
            
        else:
            question = Question.query.filter_by(category=category_id).filter(
                Question.id.notin_((previous_questions))).first()

        if question:
            formatted_question = question.format()
        else:
            formatted_question = question
        
                                   
        
        return jsonify({
            'success':True,
            'question':formatted_question})


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(405)
    def not_allowed_error(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405
    
        
    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable error"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    
    

    return app

