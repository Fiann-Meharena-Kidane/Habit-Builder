from website import create_app, db
import requests

app=create_app()

# code to run whenever database is altered manually

with app.app_context():
    # db.drop_all(app=app)
    db.create_all(app=app)


if __name__=='__main__':
    app.run(debug=True)