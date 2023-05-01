class UserDataManagement:
    def get_user_profile(id,db):
        users = []
        for doc in db.collection(u'users').where(u'auth_id', u'==', id).stream():
            users.append(doc.to_dict())
        return users