from flask import Flask, render_template, request, redirect, url_for, flash
from database_setup import db
import httplib2
import json

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# create function to connect to api and fetch the data
def get_nanodegrees():
    catalog_url = "https://catalog-api.udacity.com/v1/degrees"
    h = httplib2.Http()
    catalog_dict = json.loads(h.request(catalog_url, 'GET')[1])
    catalog = {}
    key = set()
    try:
        for degree in catalog_dict['degrees']:
            if degree['available'] and degree['open_for_enrollment']:
                img = degree['card_image']
                if img[:4] != 'http':
                    img = 'https://d20vrrgs8k4bvw.cloudfront.net/images/degrees/nd027/nd-card.jpg'
                if degree['key'][:5] not in key:
                    catalog[degree['title']] = [img, degree['key'], degree['short_summary']]
                    key.add(degree['key'][:5])
    except Exception as e:
        return {}

    return catalog


@app.route("/enrollment", methods=['GET', 'POST'])
def enrollment():
    catalogs = get_nanodegrees()
    if request.method == 'POST':
        nanodegree_key = str(request.args.get('key'))
        udacity_user_key = '14'
        status = 'ENROLLED'
        # print(nanodegree_key)
        check_enroll = db.execute('''SELECT * FROM enrollments WHERE status = 'ENROLLED'
                                  and nanodegree_key= :key and udacity_user_key = :user_key LIMIT 1;''',
                                  {"key": nanodegree_key, "user_key": udacity_user_key}).fetchall()

        if check_enroll:
            flash("You aleardy enrolled in this program!", 'error')
            return redirect(url_for('enrollment'))

        db.execute("INSERT INTO enrollments (nanodegree_key, udacity_user_key, status) VALUES (:nanodegree_key, :udacity_user_key, :status)",
                    {"nanodegree_key": nanodegree_key, "udacity_user_key": udacity_user_key, "status": status})
        db.commit()
        flash("You have enrolled successfully", 'success')
        return redirect(url_for('enrollment'))

    return render_template('index.html', catalogs=catalogs)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
