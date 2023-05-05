import time
from firebase_admin import firestore
from api.api_v1.endpoints.project_model import *
from fastapi import APIRouter, Body, Request, Response, HTTPException, status


class ProjectDataManagement:

    @staticmethod
    def get_projects(user_id, db):
        relations = [doc.to_dict() for doc in db.collection(
            u'relations').where(u'user_id', u'==', user_id).stream()]
        if relations == []:
            return None
        project_ids = set(relation['project_id'] for relation in relations)
        projects = [ProjectDataManagement.get_project(
            project_id, db) for project_id in project_ids]
        # except AttributeError as e:
        #     # You can log the error if needed
        #     print(f"Error: {e}")
        #     raise HTTPException(
        #         status_code=500, detail="Internal Server Error")
        # except Exception as e:
        #     print(f"Error: {e}")
        #     raise HTTPException(status_code=400, detail=str(e))
        return projects, project_ids

    @staticmethod
    def create_invitation(sender_id, project_id, receiver_email, role, db):
        invite = {
            'sender_id': sender_id,
            'project_id': project_id,
            'receiver_mail': receiver_email,
            'user_role': role,
            'accepted': False,
            'rejected': False,
            'id': '',
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        doc_ref = db.collection(u'invites').add(invite)
        doc_id = doc_ref[1].id
        db.collection(u'invites').document(doc_id).update({'id': doc_id})
        return True

    @staticmethod
    def create_relation(user_id, project_id, role, is_admin, db):
        relation = {
            'user_id': user_id,
            'project_id': project_id,
            'role': role,
            'is_admin': is_admin,
        }
        doc_ref = db.collection('relations').add(relation)
        record = db.collection('relations').document(doc_ref[1].id)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })
        return True

    @staticmethod
    def create_project(project, db):
        project_obj = {
            'creator_id': project.creator_id,
            'general_info': dict(project.general_info),
            'client': dict(project.client_info),
        }
        doc_ref = db.collection('projects').add(project_obj)
        record = db.collection('projects').document(doc_ref[1].id)
        record.update({
            'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })

        ProjectDataManagement.create_invitation(
            project.creator_id, doc_ref[1].id, project.client_info.email, 'client', db)
        ProjectDataManagement.create_relation(
            project.creator_id, doc_ref[1].id, 'creator', True, db)
        return True

    @staticmethod
    def create_quote(quote, db):
        quote_obj = {
            u'creator_id': quote.creator_id,
            u'quote_description': quote.quote_description,
            u'project_id': quote.project_id,
            u'quote_name': quote.quote_name,
            u'quote_type': quote.quote_type,
            u'quote_validity': quote.quote_validity,
            u'quote_status': quote.quote_status,
            u'accepted': quote.accepted,
        }

        doc_ref = db.collection('quotes').add(quote_obj)
        record = db.collection('quotes').document(doc_ref[1].id)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })
        for i in range(len(quote.items)):
            quote.items[i].quote_id = doc_ref[1].id
            ProjectDataManagement.create_item(
                quote.items[i], doc_ref[1].id, db)
        return True

    @staticmethod
    def create_item(item, quote_id, db):
        item_obj = {
            u'quote_id': quote_id,
            u'item_name': item.item_name,
            u'item_type': item,
            u'item_description': item.item_description,
            u'item_unit': item.item_unit,
            u'item_number': item.item_number,
            u'item_unit_price': item.item_unit_price,
            u'item_completion': item.item_completion,
        }
        doc_ref = db.collection('items').add(item_obj)
        record = db.collection('items').document(doc_ref[1].id)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })
        return True

    @staticmethod
    def get_project_invitations(id, db):
        users = []
        invites = []
        projects = []
        for doc in db.collection(u'users').where(u'auth_id', u'==', id).stream():
            users.append(doc.to_dict())

        if not users:
            raise Exception("No user found with the given id in the database")

        for doc in db.collection(u'invites').where(u'receiver_mail', u'==', users[0]['mail']).where(u'accepted', u'==', False).where(u'rejected', u'==', False).stream():
            invites.append(doc.to_dict())

        for i in range(len(invites)):
            for doc in db.collection(u'projects').where(u'id', u'==', invites[i]['project_id']).stream():
                proj_dict = doc.to_dict()
                proj_dict['role'] = invites[i]['user_role']
                proj_dict['invitation_id'] = invites[i]['id']
                projects.append(proj_dict)

        for i in range(len(projects)):
            for doc in db.collection(u'users').where(u'auth_id', u'==', projects[i]['creator_id']).stream():
                projects[i]['creator_info'] = doc.to_dict()

        return projects

    @staticmethod
    def accept_invitation(invite_id, id, db):
        invites = []
        invite = {}
        for doc in db.collection(u'invites').where(u'id', u'==', invite_id).stream():
            invites.append(doc)
            invite = doc.to_dict()

        if not invites:
            raise Exception(
                "No invitation found with the given id in the database")

        record = db.collection('invites').document(invites[0].id)
        record.update({
            'accepted': True,
        })

        ProjectDataManagement.create_relation(
            user_id=id, project_id=invite['project_id'], role=invite['user_role'], is_admin=False, db=db)
        return True

    @staticmethod
    def reject_invitation(invite_id, id, db):
        invite_doc = db.collection(u'invites').document(invite_id).get()
        if not invite_doc.exists:
            raise Exception(
                "No invitation found with the given id in the database")

        invite = invite_doc.to_dict()
        db.collection('invites').document(invite_id).update({
            'rejected': True,
        })

        ProjectDataManagement.create_relation(
            user_id=id, project_id=invite['project_id'], role=invite['user_role'], is_admin=False, db=db)
        return True

    @staticmethod
    def get_items(quote_id, db):
        items_docs = db.collection(u'items').where(
            u'quote_id', u'==', quote_id).stream()
        items = [doc.to_dict() for doc in items_docs]
        return items

    @staticmethod
    def get_project(project_id, db):
        project_ref = db.collection(u'projects').document(project_id)
        project_doc = project_ref.get()
        if not project_doc.exists:
            return None

        project = project_doc.to_dict()

        creator_id = project['creator_id']
        creator_doc = db.collection(u'users').where(
            u'auth_id', u'==', creator_id).limit(1).get()
        if creator_doc:  # Change this line
            project['creator_info'] = creator_doc[0].to_dict()

        quotes = ProjectDataManagement.get_quotes(project_id, db)
        project['quotations'] = [
            quote for quote in quotes if quote['quote_type'] == 'quotation']
        project['variation_orders'] = [
            quote for quote in quotes if quote['quote_type'] == 'variation_order']
        project['change_orders'] = [
            quote for quote in quotes if quote['quote_type'] == 'change_order']

        quote_ids = [quote['id'] for quote in quotes]
        items = ProjectDataManagement.get_items_for_quotes(quote_ids, db)
        for quote in quotes:
            quote_items = items.get(quote['id'], [])
            quote['items'] = quote_items

        total = sum(float(quote['total_price']) for quote in quotes if quote['quote_type'] in [
                    'quotation', 'variation_order', 'change_order'])
        project['total'] = total
        return project

    @staticmethod
    def get_quotes(project_id, db):
        quotes_docs = db.collection(u'quotes').where(
            u'project_id', u'==', project_id).stream()
        quotes = [doc.to_dict() for doc in quotes_docs]
        if not quotes:
            return quotes

        for quote in quotes:

            items = ProjectDataManagement.get_items(quote['id'], db)
            total_price = sum(map(lambda item: float(item['item_unit_price']) * float(
                item['item_number']) if 'item_unit_price' in item else 0, items))

            quote['total_price'] = total_price

        return quotes

    @staticmethod
    def get_items_for_quotes(quote_ids, db):
        if not quote_ids:
            return []

        items_docs = db.collection(u'items').where(
            u'quote_id', u'in', quote_ids).stream()
        items = [doc.to_dict() for doc in items_docs]

        items_by_quote = {}
        for item in items:
            quote_id = item['quote_id']
            if quote_id not in items_by_quote:
                items_by_quote[quote_id] = []
            items_by_quote[quote_id].append(item)

        return items_by_quote

    @staticmethod
    def get_quote_by_id(quote_id, db):
        # Recupera il documento della quotazione in base all'ID
        quote_doc = db.collection(u'quotes').document(quote_id).get()

        # Se il documento non esiste, restituisci None
        if not quote_doc.exists:
            return None

        # Converte il documento in un dizionario
        quote = quote_doc.to_dict()

        # Recupera gli elementi associati alla quotazione
        items = ProjectDataManagement.get_items(quote['id'], db)

        # Calcola il prezzo totale
        total_price = sum(float(item.get('item_unit_price', 0))
                          * float(item.get('item_number', 0)) for item in items)

        # Aggiungi il prezzo totale e gli elementi al dizionario della quotazione
        quote['total_price'] = total_price
        quote['items'] = items

        return quote

    @staticmethod
    def create_completion_request(complition_request: CompletionRequest, db):
        # Use .dict() instead of .to_dict()
        complition_request_obj = complition_request.dict()
        doc_ref = db.collection('complition_request').add(
            complition_request_obj)
        record = db.collection('complition_request').document(doc_ref[1].id)
        record.update({
            u'id': doc_ref[1].id,
            u'timestamp': time.time_ns(),
        })
        for item in complition_request.quote.items:
            item_ref = db.collection('items').document(item.id)
            item_ref.update({
                'item_completion': item.item_completion
            })
        return True

    @staticmethod
    def get_completion_requests(completion_request_id, db):
        comp_req_doc = db.collection(u'complition_request').document(
            completion_request_id).get()
        if not comp_req_doc.exists:
            return None
        project = comp_req_doc.to_dict()

    @staticmethod
    def get_completion_requests_by_project_id(project_id, db):
        comp_req_doc = db.collection(u'complition_request').document().get()
        if not comp_req_doc.exists:
            return None
        project = comp_req_doc.to_dict()

    @staticmethod
    def accept_completion_request(comp_req__id: str, user_id, db):
        relations_doc = db.collection(
            u'relations').document(comp_req__id).stream()
        relations = [doc.to_dict() for doc in relations_doc]
        auth = False
        for rel in relations:
            if rel['user_id'] == user_id and rel['role'] == 'client':
                auth = True
        if not auth:
            raise HTTPException(status_code=401, detail="Not authorized")
        record = db.collection('complition_request').document(comp_req__id)
        record.update({
            u'accepted': True,
        })
        comp_req = record.get()
        complition_request = CompletionRequest(comp_req.to_dict())
        for item in complition_request.quote.items:
            item_ref = db.collection('items').document(item.id)
            item_ref.update({
                'item_completion': item.item_completion
            })
        return True

    @staticmethod
    def reject_completion_request(project_id: str, user_id: str, db):
        complition_requests_objs = db.collection(u'complition_request').where(
            u'project_id', u'==', project_id).stream()
        complition_requests = [doc.to_dict()
                               for doc in complition_requests_objs]
        comp_reqs
        auth = False
        for rel in relations:
            if rel['user_id'] == user_id and rel['role'] == 'client':
                auth = True
        if not auth:
            raise HTTPException(status_code=401, detail="Not authorized")
        record = db.collection('complition_request').document(comp_req__id)
        record.update({
            u'rejected': True,
        })
        return True
