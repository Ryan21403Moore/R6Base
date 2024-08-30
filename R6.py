from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
#  Path to the SQLite database file
db_path = 'SiegeBase.db'

# 404 error
@app.errorhandler(404)
def page_not_found(e):
    # Render the custom 404 error page
    return render_template('404.html'), 404


@app.route('/')
def home():
    #  Connect to the database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        #  Select all of the defender colums from the database.
        cursor.execute("SELECT * FROM Defenders")
        defenders = cursor.fetchall()
    #  Render the home.html template, for the defenders be shown on homepage.
    return render_template('home.html', defenders=defenders)


@app.route('/defender/<int:defender_id>')
def defender(defender_id):
    #  Connect to the database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        #  Get all of the defenders for the page.
        cursor.execute("SELECT * FROM Defenders WHERE defender_id = ?", (defender_id,))
        #  Fetch all gadgets linked to the defender and the information for them
        defender = cursor.fetchone()
        cursor.execute("""SELECT Gadgets.name, Gadgets.description FROM Gadgets 
          JOIN WeaponGadget ON Gadgets.gadget_id =
          WeaponGadget.gadget_id WHERE WeaponGadget.defender_id = ?""", (defender_id,))
        #  Fetch all gadgets linked to the defender and the information
        gadgets = cursor.fetchall()
        cursor.execute("""SELECT Weapons.name, Weapons.description FROM Weapons JOIN WeaponGadget
        ON Weapons.weapon_id = WeaponGadget.weapon_id WHERE WeaponGadget.defender_id = ?""", (defender_id,))
        weapons = cursor.fetchall()
    #  render the defender template with the defender, gadgets, and weapons data to be displayed to the user.
    return render_template('defender.html', defender=defender, gadgets=gadgets, weapons=weapons)


if __name__ == '__main__':
    app.run(debug=True)
