from sqlalchemy import create_engine
from sqlalchemy import sessionmaker
import loginDb, catagoriesDb

#create the User database
def load_user():
    user_engine = create_engine('sqlite:///usertable.db', echo = True)
    user_session = sessionmaker(bind = user_engine)
    return(user_session())

#create the catagory database
def load_cat():
    cat_engine = create_engine('sqlite:///cattable.db', echo = True)
    cat_session = sessionmaker(bind = cat_engine)
    return(cat_session())

#Pass the username, password and user database to validate the authenticity of the user logging in
#Returns False if fails and True if valid
def validate_user(user_name, pass_word, user_table):
    query = user_table.query(loginDb.User).filter(loginDb.User.username == user_name)
    if query.count < 1:
        return False

    user = query.first()
    if user.password == pass_word:
        return True
    else:
        return False

#Pass the username, user database and catagory database
#Returns false if the user does not exist or if they have no catagories
#Returns a dictionary of catagories and their values for the user
def get_catagories(username, user_table, cat_table):
    query = user_table.query(loginDb.User).filter(loginDb.User.username == username)
    if query.count < 1:
        return False
    user_id = query.first().id
    query = cat_table.query(catagoriesDb.Catagory).filter(catagoriesDb.Catagory.userId == user_id)
    if query.count < 1:
        return False

    cats = {}
    for row in query:
        cats[row.catName] = row.catVal

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
        new_cata = catagoriesDb.Catagory(result.id, cat, cats[cat])
        cat_table.add(new_cata)

#Pass the username and user database
#Returns False if the user does not exist
#Otherwise deletes the user
def remove_user(username, user_table):
    query =  user_table.query(loginDb.User).filter(loginDb.User.username == username)
    if query.count < 1:
        return False
    query.first().delete()
    user_table.session.commit()

#Pass the username, user and catagory databases, and the catagory to be deleted
#Returns False if the user or their catagory does not exist
#Otherwise deletes the desired catagory for the user
def remove_cat(username, user_table, cat, cat_table):
    query = user_table.query(loginDb.User).filter(loginDb.User.username == username)
    if query.count < 1:
        return False
    user_id = query.first().id
    query = cat_table.query(catagoriesDb.Catagory).filter(catagoriesDb.Catagory.userId == user_id).\
        filter(catagoriesDb.Catagory.catName == cat)
    if query.count < 1:
        return False
    for result in query:
        result.delete()
    cat_table.session.commit()

#Pass the username, catagory name and value, and the user and catagory databases
#Returns False if the user does not exist or if the Catagory already exists
#Otherwise creates the new catagory for the user
def add_cat(username, user_table, catname, catval, cat_table):
    query = user_table.query(loginDb.User).filter(loginDb.User.username == username)
    if query.count < 1:
        return False
    user_id = query.first().id
    query = cat_table.query(catagoriesDb.Catagory).filter(catagoriesDb.Catagory.userId == user_id). \
        filter(catagoriesDb.Catagory.catName == catname)
    if query.count > 0:
        return False

    new_cata = catagoriesDb.Catagory(user_id, catname, catval)
    cat_table.add(new_cata)
