"""
Base model, the other models should inherit it
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import or_, and_
import os
from collections import namedtuple
from dotenv import load_dotenv

load_dotenv()

db = os.getenv('DB_PATH')
print('db %s' % db)

engine = create_engine(db, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import webapp.models.models

    Base.metadata.create_all(bind=engine)


class DataTablesServer:
    def __init__( self, request, columns, index, model):
        self.columns = columns
        self.index = index
        self.model = model

        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values

        # results from the db
        self.result_data = None

        # total in the table after filtering
        self.cardinality_filtered = 0

        # total in the table unfiltered
        self.cadinality = 0

        self.run_queries()

    def output_result(self):
        output = {}
        output['sEcho'] = str(int(self.request_values['sEcho']))
        output['iTotalRecords'] = str(self.cardinality)
        output['iTotalDisplayRecords'] = str(self.cardinality_filtered)
        aaData_rows = []

        for row in self.result_data:
            aaData_rows.append(row.to_dict())

        output['aaData'] = aaData_rows
        return output

    def run_queries(self):
        # pages has 'start' and 'length' attributes
        pages = self.paging()

        # the term you entered into the datatable search
        filter = self.filtering()

        # the document field you chose to sort
        sorting = self.sorting()

        # get result from db
        query = self.model.query.filter(filter).order_by(sorting)
        items = query.offset((pages.start-1)*pages.length).limit(pages.length).all()
        total_count = self.model.query.filter(filter).count()

        self.result_data = items
        self.cardinality_filtered = total_count
        self.cardinality = self.model.query.count()

    def filtering(self):
        # build your filter spec
        s_filter = or_()
        if ( self.request_values.has_key('sSearch') ) and ( self.request_values['sSearch'] != "" ):
            search_values = (self.request_values['sSearch']).split()
            s_filter = and_(*[or_(*[getattr(self.model, column).contains(search_value) for column in self.columns]) for search_value in search_values])

        return s_filter

    def sorting(self):
        order = [('index',1)]
        order_dict = {'asc': 1, 'desc': -1}

        if ( int(self.request_values['iSortCol_0']) > 0 ) and ( int(self.request_values['iSortingCols']) > 0 ):
            order = []
            for i in range( int(self.request_values['iSortingCols']) ):
                order.append((self.columns[ int(self.request_values['iSortCol_'+str(i)]) - 1 ], order_dict[self.request_values['sSortDir_'+str(i)]]))

        if order[0][1] == 1:
            sorting = getattr(self.model, order[0][0])
        else:
            sorting = getattr(self.model, order[0][0]).desc()

        return sorting

    def paging(self):
        pages = namedtuple('pages', ['start', 'length'])
        if (self.request_values['iDisplayStart'] != "" ) and (self.request_values['iDisplayLength'] != -1 ):
            pages.length = int(self.request_values['iDisplayLength'])
            pages.start = int(self.request_values['iDisplayStart']) / pages.length + 1

        return pages
