from flask import Flask, render_template
from flask_socketio import SocketIO,emit,send
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,logger=True, engineio_logger=True,cors_allowed_origins="*")

@socketio.on('connect')
def connect():
    emit('başarıyla bağlandı',broadcast=True)
    
#Socket IO Customer#
@socketio.on('customer_detail_update_emit')
def customer_detail_update_emit(musteriAdi):
    emit('customer_detail_update_on',musteriAdi,broadcast=True)

@socketio.on('customer_update_emit')
def customer_update_emit(userId):
    emit('customer_update_on',userId,broadcast=True)

#Socket IO Bgp#
@socketio.on('bgp_project_list_emit')
def bgp_project_list_emit(userId):
    emit('bgp_project_list_on',userId,broadcast=True)
    
@socketio.on('bgp_project_list_ayrinti_emit')
def bgp_project_list_ayrinti_emit(projectName):
    emit('bgp_project_list_ayrinti_on',projectName,broadcast=True)

#Socket IO Workmanship
@socketio.on('workmanship_update_emit')
def workmanship_update_emit(data):
    emit('workmanship_update_on',data,broadcast=True)

 #Socket IO Products
@socketio.on('products_update_emit')
def products_update_emit(productStatus):
    emit('products_update_on',productStatus,broadcast=True)

@socketio.on('products_detail_update_emit')
def products_detail_update_emit(po):
    emit('products_detail_update_on',po,broadcast=True)

#Socket IO Selection
@socketio.on('selection_update_emit')
def selection_update_emit():
    emit('selection_update_on',broadcast=True)

#Socket IO Finance
@socketio.on('finance_main_list_update_emit')
def finance_main_list_update_emit():
    emit('finance_main_list_update_on',broadcast=True)

@socketio.on('finance_detail_list_update_emit')
def finance_detail_list_update_emit(customerId):
    emit('finance_detail_list_update_on',customerId,broadcast=True)

@socketio.on('finance_detail_collection_list_update_emit')
def finance_detail_collection_list_update_emit(data):
    emit('finance_detail_collection_list_update_on',data,broadcast=True)

#Socket IO Cards
@socketio.on('cards_update_list_emit')
def cards_update_list_emit():
    emit('cards_update_list_on',broadcast=True)

#Socket IO Supplier
@socketio.on('supplier_update_list_emit')
def supplier_update_list_emit():
    emit('supplier_update_list_on',broadcast=True)
    
#Socket IO Uploading Folder
@socketio.on('uploading_folder_update_list_emit')
def uploading_folder_update_list_emit(po):
    emit('uploading_folder_update_list_on',po,broadcast=True)
    
#Socket IO Container
@socketio.on('container_update_follow_list_emit')
def container_update_follow_list_emit():
    emit('container_update_follow_list_on',broadcast=True)
    
@socketio.on('container_update_unfollow_list_emit')
def container_update_unfollow_list_emit():
    emit('container_update_unfollow_list_on',broadcast=True)
    
#Socket IO Shipping
@socketio.on('shipping_company_update_list_emit')
def shipping_company_update_list_emit():
    emit('shipping_company_update_list_on',broadcast=True)

#Socket IO Shopper
@socketio.on('shopper_update_list_emit')
def shopper_update_list_emit():
    emit('shopper_update_list_on',broadcast=True)

@socketio.on('shopper_offer_update_list_emit')
def shopper_offer_update_list_emit():
    emit('shopper_offer_update_list_on',broadcast=True)
    
@socketio.on('shopper_bgp_update_list_emit')
def shopper_bgp_update_list_emit():
    emit('shopper_bgp_update_list_on',broadcast=True)

@socketio.on('shopper_fair_update_list_emit')
def shopper_fair_update_list_emit():
    emit('shopper_fair_update_list_on',broadcast=True)

@socketio.on('shopper_selection_update_list_emit')
def shopper_selection_update_list_emit(user_id):
    emit('shopper_selection_update_list_on',user_id,broadcast=True)

#Socket IO Stock
@socketio.on('mekmer_reports_stock_prices_list_update_list_emit')
def mekmer_reports_stock_prices_list_update_list_emit(status):
    emit('mekmer_reports_stock_prices_list_update_list_on',status,broadcast=True)

#Socket IO Sample
@socketio.on('sample_stock_list_emit')
def sample_stock_list_emit():
    emit('sample_stock_list_on',broadcast=True)

#Socket IO Offer
@socketio.on('offer_list_emit')
def offer_list_emit():
    emit('offer_list_on',broadcast=True)
    
@socketio.on('offer_detail_list_emit')
def offer_detail_list_emit():
    emit('offer_detail_list_on',broadcast=True)
    
@socketio.on('offers_detail_all_list_emit')
def offers_detail_all_list_emit():
    emit('offers_detail_all_list_on',broadcast=True)
    
#Socket IO Usa
@socketio.on('usa_comment_list_emit')
def usa_comment_list_emit():
    emit('usa_comment_list_on',broadcast=True)

#Socket IO To Do
@socketio.on('to_do_list_emit')
def to_do_list_emit(userId):
    emit('to_do_list_on',userId,broadcast=True)
    
#Socket IO Cost Error
@socketio.on('cost_error_list_emit')
def cost_error_list_emit():
    emit('cost_error_list_on',broadcast=True)
    
#Socket IO Eta 
@socketio.on('eta_list_emit')
def eta_list_emit():
    emit('eta_list_on',broadcast=True)
    
#Socket IO Representative
@socketio.on('representative_list_emit')
def representative_list_emit():
    emit('representative_list_on',broadcast=True)
    
#Socket IO Finance Test
@socketio.on('finance_test_detail_payment_emit')
def finance_test_detail_payment_emit(data):
    emit('finance_test_detail_payment_on',data,broadcast=True)

@socketio.on('finance_test_detail_emit')
def finance_test_detail_emit(data):
    emit('finance_test_detail_on',data,broadcast=True)

@socketio.on('finance_test_list_emit')
def finance_test_list_emit():
    emit('finance_test_list_on',broadcast=True)

@socketio.on('finance_test_advanced_payment_list_emit')
def finance_test_advanced_payment_list_emit():
    emit('finance_test_advanced_payment_list_on',broadcast=True)

if __name__ == '__main__':
    socketio.run(app,port=5001)