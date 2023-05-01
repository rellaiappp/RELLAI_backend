import time

class ProjectDataManagement:


    def get_projects(user_id,db):
        relations = []
        projects = []
        for doc in db.collection(u'relations').where(u'user_id', u'==', user_id).stream():
            relations.append(doc.to_dict())
        for i in range(len(relations)):
            for doc in db.collection(u'projects').document(u'project_id', u'==', relations[i]['project_id']):
                projects.append(doc.to_dict())
        return projects

    def create_invitation(id,project_id, receiver_email, role, db):
        invite = {
            'sender_id': id,
            'project_id': project_id,
            'receiver_mail': receiver_email,
            'user_role': role,
            'accepted': False,
            'rejected': False,
        }
        doc_ref = db.collection(u'invites').add(invite)
        record = db.collection(u'invites').document(doc_ref[1].id)
        print(record)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })
        return True

    def create_relation(user_id,project_id,role,is_admin,db):
        relation = {
            'user_id': user_id,
            'project_id': project_id,
            'role': role,
            'is_admin': is_admin,
        }
        doc_ref = db.collection('relations').add(relation)
        record = db.collection('relations').document(doc_ref[1].id)
        print(record)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })
        return True
    
    def create_project(project,db):
        project_obj = {
            u'creator_id': project.creator_id,
            u'general_info': dict(project.general_info),
            u'client': dict(project.client_info),
        }
        doc_ref = db.collection('projects').add(project_obj)
        record = db.collection('projects').document(doc_ref[1].id)
        print(record)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })

        ProjectDataManagement.create_invitation(project.creator_id,doc_ref[1].id,project.client_info.email,'client',db)
        ProjectDataManagement.create_relation(project.creator_id,doc_ref[1].id,'creator',True,db)
        return True

    def create_quote(quote,db):
        quote_obj = {
            u'quote_id': quote.quote_id,
            u'creator_id': quote.creator_id,
            u'project_id': quote.project_id,
            u'quote_name': quote.quote_name,
            u'quote_type': quote.quote_type,
            u'quote_validity': quote.quote_validity,
            u'quote_type': quote.quote_type,
            u'quote_status': quote.quote_type,
            u'quote_accepted': quote.quote_type,
        }
        doc_ref = db.collection('items').add(quote_obj)
        record = db.collection('items').document(doc_ref[1].id)
        print(record)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })

        for i in range(len(quote.items)):
            ProjectDataManagement.create_item(quote.items[i],doc_ref[1].id,db)
        return True


    def create_completition_request(quote,db):
        quote_obj = {
            u'quote_id': quote.quote_id,
            u'creator_id': quote.creator_id,
            u'project_id': quote.project_id,
            u'quote_name': quote.quote_name,
            u'quote_type': quote.quote_type,
            u'quote_validity': quote.quote_validity,
            u'quote_type': quote.quote_type,
            u'quote_status': quote.quote_type,
            u'quote_accepted': quote.quote_type,
        }
        doc_ref = db.collection('items').add(quote_obj)
        record = db.collection('items').document(doc_ref[1].id)
        print(record)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })

        for i in range(len(quote.items)):
            ProjectDataManagement.create_item(quote.items[i],doc_ref[1].id,db)
        return True
    
       
    def create_item(item, quote_id ,db):
        item_obj = {
            u'quote_id': quote_id,
            u'item_name': item.item_name,
            u'item_type': item.item_type,
            u'item_description': item.item_description,
            u'item_unit': item.item_unit,
            u'item_number': item.item_number,
            u'item_unit_price:': item.item_unit_price,
            u'item_completition': item.completition,
        }
        doc_ref = db.collection('items').add(item_obj)
        record = db.collection('items').document(doc_ref[1].id)
        print(record)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })
        return True

    def get_project_invitations(id,db):
        users = []
        invites = []
        projects = []
        for doc in db.collection(u'users').where(u'auth_id', u'==', id).stream():
            users.append(doc.to_dict())
        if len(users) == 0:
            raise Exception("No user found with the given id in the databse")
        for doc in db.collection(u'invites').where(u'receiver_mail', u'==', users[0]['mail']).where(u'accepted', u'==', False).where(u'rejected', u'==', False).stream():
            invites.append(doc.to_dict())
        for i in range(len(invites)):
            for doc in db.collection(u'projects').where(u'id', u'==', invites[i]['project_id']).stream():
                proj_dict = doc.to_dict()
                proj_dict['role'] = invites[i]['user_role']
                proj_dict['invitation_id'] = invites[i]['id']
                projects.append(proj_dict)
        for i in range(len(projects)):
            for doc in db.collection(u'users').where(u'auth_id', u'==', projects[i]['creator_id'] ).stream():
                projects[i]['creator_info'] = doc.to_dict()
        return projects
    
    def accept_invitation(invite_id,id,db):
        invites = []
        invite = {}
        for doc in db.collection(u'invites').where(u'id', u'==', invite_id).stream():
            invites.append(doc)
            invite = doc.to_dict()
        if len(invites) == 0:
            raise Exception("No invitation found with the given id in the databse")
        record = db.collection('invites').document(invites[0].id)
        record.update({
            'accepted': True,
        })
        ProjectDataManagement.create_relation(user_id=id,project_id=invite['project_id'],role=invite['user_role'],is_admin=False,db=db)
        return True
    
    
    def reject_invitation(invite_id,id,db):
        invites = []
        invite = {}
        for doc in db.collection(u'invites').where(u'id', u'==', invite_id).stream():
            invites.append(doc)
            invite = doc.to_dict()
        if len(invites) == 0:
            raise Exception("No invitation found with the given id in the databse")
        record = db.collection('invites').document(invites[0].id)
        record.update({
            'rejected': True,
        })
        ProjectDataManagement.create_relation(user_id=id,project_id=invite['project_id'],role=invite['user_role'],is_admin=False,db=db)
        return True

    

