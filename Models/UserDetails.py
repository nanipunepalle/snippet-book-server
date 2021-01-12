# @app.route('/add', methods=['POST'])
# def add_user():
#     user = User(name=request.form.get('name'),
#                 email=request.form.get('email'))
#     try:
#         user.save()
#     except :
#         return "error"
    
#     return user.to_json()

# @app.route('/get', methods=["GET"])
# def get_user():
#     user = User.objects(email="lalith@gmail.com")
#     if not user:
#         return jsonify({'error': 'data not found'})
#     else:
#         return user.to_json()