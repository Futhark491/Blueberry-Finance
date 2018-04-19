from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import modules.db.masterDb as master

#Loads the database that has the user,category, and ransaction tables
def load_db():
    db_engine = create_engine('sqlite:///master.db', echo = False)
    db_session = sessionmaker(bind = db_engine)
    return(db_session())

#Pass the username, password and database to validate the authenticity of the user logging in
#Returns False if fails and True if valid
def validate_user(user_name, pass_word, db):
    query = db.query(master.User).filter(master.User.username == user_name)
    if query.count() < 1:
        return False

    user = query.first()
    if user.password == pass_word:
        return True
    else:
        return False

#Pass the username and database
#Returns a list of lists. Sublists are category id, category name, and category value
def get_categories(username, db):

    query = db.query(master.User).filter(master.User.username == username)
    user_id = query.first().id
    query = db.query(master.Category).filter(master.Category.userId == user_id)
    cats = []
    query2 = db.query(master.User).filter(master.User.username == 'master')
    if query2.count() < 1:
        add_user('master', 'Uncategorized',{'Uncategorized':'0'}, db)
    query2 = db.query(master.User).filter(master.User.username == 'master')
    user_id = query2.first().id
    query2 = db.query(master.Category).filter(master.Category.userId == user_id)
    for row in query2:
        cats.append([row.id, row.catName, row.catVal])
    for row in query:
        cats.append([row.id, row.catName, row.catVal])

    return cats

#Pass the username, password, a dictionary of starting catagories and their values, and the database
#Returns False if the user already exists
#Creates the new user and then creates their default catagories with their userID
def add_user(username, password, cats, db):

    query = db.query(master.User).filter(master.User.username.in_([username]))
    result = query.first()

    if result:
        return False

    new_user = master.User(username, password)
    db.add(new_user)

    query = db.query(master.User).filter(master.User.username.in_([username]))
    result = query.first()

    for cat in cats:
        new_cata = master.Category(result.id, cat, cats[cat])
        db.add(new_cata)

    db.commit()
    return True

#Pass the username and database
#Returns False if the user does not exist
#Otherwise deletes the user and all associate categories and transactions
def remove_user(username, db):
    query = db.query(master.User).filter(master.User.username == username)
    if query.count() < 1:
        return []
    user_id = query.first().id
    query = db.query(master.Category).filter(master.Category.userId == user_id)
    for row in query:
        remove_cat(row.id, db)
    query = db.query(master.Transaction).filter(master.Transaction.userId == user_id)
    for row in query:
        remove_trans(row.id, db)
    db.query(master.User).filter(master.User.username == username).delete()
    db.commit()

def edit_income(username, income, db):
    query = db.query(master.User).filter(master.User.username == username)
    if query.count() < 1:
        return False
    for row in query:
        row.income = income
    db.commit()
    return True

def get_income(username, db):
    query = db.query(master.User).filter(master.User.username == username)
    if query.count() < 1:
        return(-1)
    return query.first().income

#Pass the category id and database
#Otherwise deletes the desired catagory for the user and reassigns all associated transactions to 'Uncategorized'
def remove_cat(catid, db):
    query = db.query(master.Category).filter(master.Category.id == catid)
    cat = query.first()
    query = db.query(master.Transaction).filter(master.Transaction.tranCat == cat.catName)
    for row in query:
        edit_trans(row.id, 'Uncategorized', row.tranVal, row.tranDesc, row.tranDate, db)
    db.query(master.Category).filter(master.Category.id == catid).delete()
    db.commit()

#Pass the username, catagory name and value, and database
#Returns False if the user does not exist or if the Catagory already exists
#Otherwise creates the new catagory for the user
def add_cat(username, catname, catval, db):
    query = db.query(master.User).filter(master.User.username == username)
    if query.count() < 1:
        return False
    user_id = query.first().id
    query = db.query(master.Category).filter(master.Category.userId == user_id).\
        filter(master.Category.catName == catname)
    if query.count() > 0:
        return False

    new_cata = master.Category(user_id, catname, catval)
    db.add(new_cata)
    db.commit()
    return True

#Pass the category id, the new category name and value and the database
#The name or value do not have to be changed for this to work.
#Returns false if category does not exist
#Otherwise updates the desired category with the new values
def edit_cat(catid, catname, catval, db):
    query = db.query(master.Category).filter(master.Category.id == catid)
    if query.count() < 1:
        return False
    for row in query:
        row.catName = catname
        row.catVal = catval
    db.commit()
    return True

#Pass the username, category name for the transaction, the value of the transaction,
#a description of the transaction if so desired, the date of the transaction and the database
#Returns false if the user does not exist
#Otherwise adds the new transaction for the user
def add_trans(username, trancat, tranval, trandesc, trandate, db):
    query = db.query(master.User).filter(master.User.username == username)
    if query.count() < 1:
        return False
    user_id = query.first().id
    new_tran = master.Transaction(user_id, trancat, tranval, trandesc, trandate)
    db.add(new_tran)
    db.commit()
    return True

#Pass the username and the database
#Returns and empty list if the user does not exist or there are no transactions
#Otherwise returns a list of lists
#A sublist contains the transaction id, category, value, description, and date
def get_transactions(username, db):
    query = db.query(master.User).filter(master.User.username == username)
    if query.count() < 1:
        return []
    user_id = query.first().id
    query = db.query(master.Transaction).filter(master.Transaction.userId == user_id)
    if query.count() < 1:
        return []

    tran = []
    for row in query:
        tran.append([row.id, row.tranCat, row.tranVal, row.tranDesc, row.tranDate])

    return tran

#Pass the transaction id, category, value, description, date and the database
#returns false if the transaction does not exist
#Otherwise updates the transaction with the given values
def edit_trans(tranid, trancat, tranval, trandesc, trandate, db):
    query = db.query(master.Transaction).filter(master.Transaction.id == tranid)
    if query.count() < 1:
        return False
    for row in query:
        row.tranCat = trancat
        row.tranVal = tranval
        row.tranDesc = trandesc
        row.tranDate = trandate
    db.commit()
    return True

#Pass the transaction id and the database
#Deletes the transaction if it exists
def remove_trans(tranid, db):
    db.query(master.Transaction).filter(master.Transaction.id == tranid).delete()
    db.commit()
