from flask_restful import Resource
from flask import jsonify,request,send_file
from views.financetest.financetest import FinanceTest,FinanceTestDetail

class FinanceTestListApi(Resource):
    def get(self):
        finance = FinanceTest()
        result = finance.getList()
        return jsonify(result)
    
class FinanceTestDetailListApi(Resource):
    def get(self,customer_id):
        finance = FinanceTestDetail(customer_id)
        financeDetail = finance.getDetailList()
        financePaid = finance.getByDatePaids()
        data = {
            'financeDetail':financeDetail,
            'financePaid':financePaid
            
        }
        return jsonify(data)
    
class FinanceTestListExcelApi(Resource):
    def post(self):
        data = request.get_json()
        finance = FinanceTest()
        status = finance.getExcelList(data)
        return {'status':status}
    
    def get(self):
        
        excel_path = 'resource_api/finans/konteyner_islem/dosyalar/finans_test_list.xlsx'

        return send_file(excel_path,as_attachment=True)
        
        
    
