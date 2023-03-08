import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request


@app.route('/create', methods=["POST"])
def create_contactdetails():
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _mobileNo = _json['mobileNo']
        _address = _json['address']
        if _name and _email and _mobileNo and _address and request.method == 'POST':
            sqlQuery = "INSERT INTO contactdetails(name, email, mobileNo, address) VALUES(%s, %s, %s, %s)"
            binData = (_name, _email, _mobileNo, _address)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sqlQuery, binData)
            conn.commit()
            respone = jsonify("Contact added successfully!")
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/contactdetails')
def contactdetails():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT id, name, email, mobileNo, address FROM contactdetails")
        contactdetailsRows = cursor.fetchall()
        respone = jsonify(contactdetailsRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/contactdetails/<int:contactdetails_mobileNo>')
def contactdetails_details(contactdetails_mobileNo):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT mobileNo, name, email, id, address FROM contactdetails WHERE mobileNo =%s", contactdetails_mobileNo)
        contactdetailsRow = cursor.fetchone()
        respone = jsonify(contactdetailsRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=["PUT"])
def update_contactdetails():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _mobileNo = _json['mobileNo']
        _address = _json['address']
        if _name and _email and _mobileNo and _address and _id and request.method == 'PUT':
            sqlQuery = "UPDATE contactdetails SET name=%s, email=%s, mobileNo=%s, address=%s WHERE id=%s "
            binData = (_name, _email, _mobileNo, _address, _id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, binData)
            conn.commit()
            respone = jsonify("Contacts Update Successfully")
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:mobileNo>', methods=["DELETE"])
def delete_contactdetails(mobileNo):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM contactdetails WHERE mobileNo=%s", (mobileNo,))
        conn.commit()
        respone = jsonify("Contact Delete Successfully")
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run()
