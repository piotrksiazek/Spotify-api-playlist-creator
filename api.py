from app import app
if __name__ == '__main__':
    print("XDDDDD")
    app.run(debug=True)
    app.debug = True
# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User}