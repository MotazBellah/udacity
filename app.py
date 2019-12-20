from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database_setup import db
import httplib2
import json

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_nanodegrees():
    catalog_url = "https://catalog-api.udacity.com/v1/degrees"
    h = httplib2.Http()
    catalog_dict = json.loads(h.request(catalog_url, 'GET')[1])
    catalog = {}

    for degree in catalog_dict['degrees']:
        if degree['available'] and degree['open_for_enrollment']:
            img = degree['card_image']
            if img[:4] != 'http':
                img = 'https://d20vrrgs8k4bvw.cloudfront.net/images/degrees/nd027/nd-card.jpg'
            catalog[degree['title']] = [img, degree['key'], degree['short_summary']]

    return catalog


@app.route("/enrollment", methods=['GET', 'POST'])
def enrollment():
    catalogs = get_nanodegrees()
    if request.method == 'POST':
        nanodegree_key = str(request.args.get('key'))
        udacity_user_key = '1'
        # nanodegree_key = "nd0055"
        # udacity_user_key = 'test100'
        status = 'ENROLLED'
        # print(nanodegree_key)
        check_enroll = db.execute('''SELECT * FROM enrollments WHERE status = 'ENROLLED'
                                  and nanodegree_key= :key and udacity_user_key = :user_key LIMIT 1;''',
                                  {"key": nanodegree_key, "user_key": udacity_user_key}).fetchall()
        print(nanodegree_key)
        if check_enroll:
            flash("You aleardy enrolled in this program!", 'error')
            return redirect(url_for('enrollment'))

        db.execute("INSERT INTO enrollments (nanodegree_key, udacity_user_key, status) VALUES (:nanodegree_key, :udacity_user_key, :status)",
                    {"nanodegree_key": nanodegree_key, "udacity_user_key": udacity_user_key, "status": status})
        db.commit()
        flash("You have enrolled successfully", 'success')
        return redirect(url_for('enrollment'))

    return render_template('index.html', catalogs=catalogs)
    # return render_template('index2.html', catalogs=catalogs)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True, host='0.0.0.0')
