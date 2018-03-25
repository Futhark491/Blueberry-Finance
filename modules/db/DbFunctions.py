from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import modules.db.loginDb as loginDb
import modules.db.categoriesDb as categoriesDb
import modules.db.transanctionsDb as tranDb

#create the User database
def load_user():
    user_engine = create_engine('sqlite:///usertable.db', echo = False)
    user_session = sessionmaker(bind = user_engine)
    return(user_session())

#create the catagory database
def load_cat():
    cat_engine = create_engine('sqlite:///cattable.db', echo = False)
    cat_session = sessionmaker(bind = cat_engine)
    return(cat_session())

def load_tran():
    tran_engine = create_engine('sqlite:///trantable.db', echo = False)
    tran_session = sessionmaker(bind = tran_engine)
    return (tran_session())

#Pass the username, password and user database to validate the authenticity of the user logging in
#Returns False if fails and True if valid
def validate_user(user_name, pass_word, user_table):
    query = user_table.query(loginDb.User).filter(loginDb.User.username == user_name)
    if query.count() < 1:
        return False

    user = query.first()
    if user.password == pass_word:
        return True
    else:
        return False

#Pass the username, user database and catagory database
#Returns false if the user does not exist or if they have no catagories
#Returns a dictionary of catagories and their values for the user
def get_categories(username, user_table, cat_table):
    query = user_table.query(loginDb.User).filter(loginDb.User.username == username)
    if query.count() < 1:
        return []
    user_id = query.first().id
    query = cat_table.query(categoriesDb.Category).filter(categoriesDb.Category.userId == user_id)
    if query.count() < 1:
        return []

    cats = []
    for row in query:
        cats.append([row.id, row.catName, row.catVal])

    return cats


#Pass the username, password, user and catagories databases, and a dictionary of starting catagories and their values
#Returns False if the user already exists
#Creates the new user and then creates their default catagories with their userID
def add_user(username, password, user_table, cat_table, cats):
    query = user_table.query(loginDb.User).filter(loginDb.User.username.in_([username]))
    result = query.first()

    if result:
        return False

    new_user = loginDb.User(username, password)
    user_table.add(new_user)

    query = user_table.query(loginDb.User).filter(loginDb.User.username.in_([username]))
    result = query.first()

    for cat in cats:
        new_cata = categoriesDb.Category(result.id, cat, cats[cat])
        cat_table.add(new_cata)

    user_table.commit()
    cat_table.commit()
    return True

#Pass the username and user database
#Returns False if the user does not exist
#Otherwise deletes the user
def remove_user(username, user_table):
    user_table.query(loginDb.User).filter(loginDb.User.username == username).delete()
    user_table.commit()

#Pass the username, user and catagory databases, and the catagory to be deleted
#Returns False if the user or their catagory does not exist
#Otherwise deletes the desired catagory for the user
def remove_cat(catid, cat_table):
    cat_table.query(categoriesDb.Category).filter(categoriesDb.Category.id == catid).delete()
    cat_table.commit()

#Pass the username, catagory name and value, and the user and catagory databases
#Returns False if the user does not exist or if the Catagory already exists
#Otherwise creates the new catagory for the user
def add_cat(username, user_table, catname, catval, cat_table):
    query = user_table.query(loginDb.User).filter(loginDb.User.username == username)
    if query.count() < 1:
        return False
    user_id = query.first().id
    query = cat_table.query(categoriesDb.Category).filter(categoriesDb.Category.userId == user_id).\
        filter(categoriesDb.Category.catName == catname)
    if query.count() > 0:
        return False

    new_cata = categoriesDb.Category(user_id, catname, catval)
    cat_table.add(new_cata)
    cat_table.commit()
    return True

def edit_cat(catid, catname, catval, cat_table):
    query = cat_table.query(categoriesDb.Category).filter(categoriesDb.Category.id == catid)
    if query.count() < 1:
        return False
    for row in query:
        row.catName = catname
        row.catVal = catval
    cat_table.commit()
    return True

def add_trans(username, user_table, trancat, tranval, trandesc, trandate, tran_table):
    query = user_table.query(loginDb.User).filter(loginDb.User.username == username)
    if query.count() < 1:
        return False
    user_id = query.first().id
    new_tran = tranDb.Transaction(user_id, trancat, tranval, trandesc, trandate)
    tran_table.add(new_tran)
    tran_table.commit()
    return True

def get_transactions(username, user_table, tran_table):
    query = user_table.query(loginDb.User).filter(loginDb.User.username == username)
    if query.count() < 1:
        return []
    user_id = query.first().id
    query = tran_table.query(tranDb.Transaction).filter(tranDb.Transaction.userId == user_id)
    if query.count() < 1:
        return []

    tran = []
    for row in query:
        tran.append([row.id, row.tranCat, row.tranVal, row.tranDesc, row.tranDate])

    return tran

def edit_trans(tranid, trancat, tranval, trandesc, trandate, tran_table):
    query = tran_table.query(tranDb.Transaction).filter(tranDb.Transaction.id == tranid)
    if query.count() < 1:
        return False
    for row in query:
        row.tranCat = trancat
        row.tranVal = tranval
        row.tranDesc = trandesc
        row.tranDate = trandate
    tran_table.commit()
    return True

def remove_trans(tranid, tran_table):
    tran_table.query(tranDb.Transaction).filter(tranDb.Transaction.id == tranid).delete()
    tran_table.commit()