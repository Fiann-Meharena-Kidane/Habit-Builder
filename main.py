from website import create_app, db


app=create_app()

# with app.app_context():
#     db.drop_all(app=app)
#     db.create_all(app=app)


if __name__=='__main__':
    app.run(debug=True)