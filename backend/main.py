from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from excel_handler import ExcelHandler
import random
import string
import json
from datetime import datetime
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ============ APP SETUP ============
app = FastAPI(title="Cơm Bà Giang API")

# Enable CORS for frontend
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production nên chỉ định domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Excel handler
excel_handler = ExcelHandler()

# ============ UTILITY FUNCTIONS ============
def generate_group_code():
    """Generate random 6-character group code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# ============ PYDANTIC MODELS ============

# Authentication Models
class AdminAuthRequest(BaseModel):
    admin_password: str

class LoginRequest(BaseModel):
    identifier: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    identifier: str
    password: str
    address: str = ""

class UpdateUserInfoRequest(BaseModel):
    name: str = None
    address: str = None

# Group Models
class CreateGroupRequest(BaseModel):
    user_id: int
    name: str
    address: str
    description: str = ""

class JoinGroupRequest(BaseModel):
    code: str
    user_id: int

# Order Models
class CreateOrderRequest(BaseModel):
    user_id: int  
    group_id: str  
    meal_type: str  
    quantity: int
    note: str = ""

class EditOrderRequest(BaseModel):
    user_id: int
    date: str
    meal_type: str
    quantity: int
    note: str = ""
    group_id: str = ""

class CancelOrderRequest(BaseModel):
    user_id: int
    date: str

# Payment Models
class MarkPaymentRequest(BaseModel):
    amount: int
    payment_period: str = "current_month"

class CreatePayOSPaymentRequest(BaseModel):
    user_id: int
    payment_period: str = "current_month"

class PayOSWebhookData(BaseModel):
    code: str
    desc: str
    success: bool
    data: dict
    signature: str

# Feedback Models
class FeedbackRequest(BaseModel):
    feedback_text: str
    rating: int = None  # 1-5 stars, optional
    category: str = "general"  # general, food, service, delivery

# ============ AUTHENTICATION ENDPOINTS ============
@app.post("/auth/login")
async def login(request: LoginRequest):
    """Login user - returns address"""
    result = excel_handler.authenticate_user(request.identifier, request.password)
    
    if result["success"]:
        user = result["user"]
        groups = excel_handler.get_user_groups(user["id"])
        
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "identifier": user["identifier"],
                "address": user["address"],
                "groups": groups
            }
        }
    else:
        return {"success": False, "message": result["message"]}

@app.post("/auth/register")
async def register(request: RegisterRequest):
    """Register new user with address"""
    result = excel_handler.create_user(
        request.identifier, 
        request.password, 
        request.name,
        request.address
    )
    return result

@app.post("/admin/auth")
async def authenticate_admin(request: AdminAuthRequest):
    """Simple admin authentication using Excel file"""
    try:
        result = excel_handler.verify_admin_code(request.admin_password)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Xác thực admin thành công"
            }
        else:
            return {
                "success": False,
                "message": result["message"]
            }
            
    except Exception as e:
        print(f"💥 Admin auth error: {e}")
        return {
            "success": False,
            "message": "Lỗi hệ thống! Vui lòng thử lại."
        }

@app.get("/admin/codes")
async def get_admin_codes():
    """Get all admin codes (for management)"""
    try:
        codes = excel_handler.get_admin_codes()
        return {"success": True, "codes": codes}
    except Exception as e:
        return {"success": False, "message": str(e)}
    
# ============ USER MANAGEMENT ENDPOINTS ============
@app.get("/users/{user_id}/info")
async def get_user_info(user_id: int):
    """Get user information by ID"""
    result = excel_handler.get_user_by_id(user_id)
    return result

@app.put("/users/{user_id}/info")
async def update_user_info(user_id: int, request: UpdateUserInfoRequest):
    """Update user information"""
    try:
        result = excel_handler.update_user_info(
            user_id=user_id,
            name=request.name,
            address=request.address
        )
        return result
    except Exception as e:
        return {"success": False, "message": f"Lỗi cập nhật thông tin: {str(e)}"}

@app.get("/users/{user_id}/groups")
async def get_user_groups(user_id: int):
    groups = excel_handler.get_user_groups(user_id)
    return {"groups": groups}

# ============ MENU ENDPOINTS ============
@app.get("/menu/today")
async def get_today_menu():
    menu = excel_handler.get_today_menu()
    return menu

@app.post("/admin/menu/save")
async def save_menu(menu_data: dict):
    """Save menu for a date"""
    result = excel_handler.save_menu(menu_data)
    return result

# ============ GROUP MANAGEMENT ENDPOINTS ============
@app.post("/groups/create")
async def create_group(request: CreateGroupRequest):
    """Create group with user_id from request"""
    try:
        user_id = request.user_id
        
        if not user_id:
            return {"success": False, "message": "Thiếu thông tin người dùng"}
        
        code = generate_group_code()
        result = excel_handler.create_group(
            request.name, code, user_id, request.address, request.description
        )
        
        return result
        
    except Exception as e:
        print(f"💥 Create group API error: {e}")
        return {"success": False, "message": "Lỗi server khi tạo nhóm"}

@app.post("/groups/join")
async def join_group(request: JoinGroupRequest):
    """Join existing group with user_id from request"""
    try:
        user_id = request.user_id
        group_code = request.code
        
        if not user_id:
            return {"success": False, "message": "Thiếu thông tin người dùng"}
        
        if not group_code:
            return {"success": False, "message": "Thiếu mã nhóm"}
        
        result = excel_handler.join_group(group_code, user_id)
        return result
        
    except Exception as e:
        print(f"💥 Join group API error: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "message": "Lỗi server khi tham gia nhóm"}

@app.get("/groups/{group_identifier}/members")
async def get_group_members(group_identifier: str):
    """Get all members of a group with their statistics - ACCEPTS NAME OR ID"""
    try:
        result = excel_handler.get_group_members_with_stats(group_identifier)
        
        print(f"📤 API: Members result - Success: {result['success']}")
        if result["success"]:
            print(f"   Found {len(result['members'])} members")
        else:
            print(f"   Error: {result['message']}")
        
        if result["success"]:
            return {
                "success": True,
                "members": result["members"],
                "group_info": result["group_info"]
            }
        else:
            return {"success": False, "message": result["message"]}
            
    except Exception as e:
        print(f"❌ Error getting group members: {e}")
        return {"success": False, "message": "Lỗi tải danh sách thành viên"}

@app.get("/groups/{group_identifier}/orders")
async def get_group_orders(group_identifier: str):
    """Get all orders for a group - ACCEPTS NAME OR ID"""
    try:
        result = excel_handler.get_group_orders(group_identifier)
        
        if result["success"]:
            print(f"   Found {len(result['orders'])} orders")
        else:
            print(f"   Error: {result['message']}")
        
        if result["success"]:
            return {
                "success": True,
                "orders": result["orders"],
                "total_orders": len(result["orders"]),
                "total_amount": sum(order["totalAmount"] for order in result["orders"])
            }
        else:
            return {"success": False, "message": result["message"]}
            
    except Exception as e:
        print(f"❌ Error getting group orders: {e}")
        return {"success": False, "message": "Lỗi tải danh sách đơn hàng"}

@app.get("/groups/{group_identifier}/payments")
async def get_group_payments(group_identifier: str, period: str = "current"):
    """Get payment information for all group members - ACCEPTS NAME OR ID"""
    try:
        result = excel_handler.get_group_payments(group_identifier, period)
        
        if result["success"]:
            print(f"   Found {len(result['payments'])} payment records")
            print(f"   Summary: {result['summary']}")
        else:
            print(f"   Error: {result['message']}")
        
        if result["success"]:
            return {
                "success": True,
                "payments": result["payments"],
                "summary": result["summary"]
            }
        else:
            return {"success": False, "message": result["message"]}
            
    except Exception as e:
        print(f"❌ Error getting group payments: {e}")
        return {"success": False, "message": "Lỗi tải thông tin thanh toán"}

@app.post("/groups/{group_id}/invite")
async def invite_member_to_group(group_id: int, invite_data: dict):
    """Send invitation to join group (future feature)"""
    try:
        phone_number = invite_data.get('phone_number')
        message = invite_data.get('message', '')
        
        result = excel_handler.get_group_invite_info(group_id)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Thông tin mời đã được tạo",
                "group_code": result["group_code"],
                "group_name": result["group_name"],
                "invite_message": f"Bạn được mời tham gia nhóm '{result['group_name']}'. Mã nhóm: {result['group_code']}"
            }
        else:
            return {"success": False, "message": result["message"]}
            
    except Exception as e:
        print(f"❌ Error creating group invitation: {e}")
        return {"success": False, "message": "Lỗi tạo lời mời nhóm"}

@app.delete("/groups/{group_id}/members/{user_id}")
async def remove_member_from_group(group_id: int, user_id: int):
    """Remove a member from group (leader only)"""
    try:
        result = excel_handler.remove_group_member(group_id, user_id)
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Đã loại thành viên khỏi nhóm"
            }
        else:
            return {"success": False, "message": result["message"]}
            
    except Exception as e:
        print(f"❌ Error removing group member: {e}")
        return {"success": False, "message": "Lỗi loại thành viên khỏi nhóm"}
    
# ============ ORDER MANAGEMENT ENDPOINTS ============
@app.post("/orders/create")
async def create_order(request: CreateOrderRequest):
    """Create order with user_id from request"""
    try:
        user_id = request.user_id
        
        if not user_id:
            return {"success": False, "message": "Thiếu thông tin người dùng"}
        
        result = excel_handler.create_order(
            user_id, request.group_id, request.meal_type, request.quantity, request.note
        )
        
        return result
        
    except Exception as e:
        print(f"💥 Create order API error: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "message": "Lỗi server khi tạo đơn hàng"}

@app.get("/orders/history/{user_id}")
async def get_user_order_history(user_id: int):
    """Get order history for a user"""
    history = excel_handler.get_user_order_history(user_id)
    return {"orders": history}

@app.put("/orders/{order_id}/edit")
async def edit_order(order_id: int, request: EditOrderRequest):
    """Edit an order"""
    try:
        result = excel_handler.edit_order(
            order_id,
            request.user_id,
            request.date,
            request.meal_type,
            request.quantity,
            request.note,
            request.group_id
        )
        return result
    except Exception as e:
        return {"success": False, "message": f"Error editing order: {str(e)}"}

@app.put("/orders/{order_id}/cancel")
async def cancel_order(order_id: int, request: CancelOrderRequest):
    """Cancel an order"""
    try:
        result = excel_handler.cancel_order(
            order_id, 
            request.user_id, 
            request.date
        )
        return result
    except Exception as e:
        return {"success": False, "message": f"Error cancelling order: {str(e)}"}

# ============ ADMIN ORDER ENDPOINTS ============
@app.get("/admin/orders")
async def get_all_orders():
    """Get all orders for today"""
    orders = excel_handler.get_today_orders()
    return {"orders": orders}

@app.get("/admin/orders/range")
async def get_orders_by_range(start_date: str = None, end_date: str = None):
    """Get orders by date range"""
    orders = excel_handler.get_orders_by_date_range(start_date, end_date)
    return {"orders": orders}

@app.put("/admin/orders/{order_id}/status")
async def update_order_status(order_id: int, status: str):
    """Update order status"""
    result = excel_handler.update_order_status(order_id, status)
    return result

@app.put("/admin/orders/{order_id}/status/{order_date}")
async def update_order_status_by_date(order_id: int, order_date: str, status_data: dict):
    """Update order status for specific date"""
    result = excel_handler.update_order_status_by_date(order_id, order_date, status_data.get('status'))
    return result

# ============ PAYMENT MANAGEMENT ENDPOINTS ============
@app.get("/payments/summary/{user_id}")
async def get_user_payment_summary(user_id: int, period: str = "all"):
    """Get payment summary for a user - ENHANCED DEBUG"""
    try:
        summary = excel_handler.get_user_payment_summary(user_id, period)
        return summary
        
    except Exception as e:
        print(f"❌ API: Error getting payment summary: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "period": excel_handler.get_period_text(period),
            "total_orders": 0,
            "meal_summary": {},
            "total_amount": 0,
            "paid_amount": 0,
            "remaining_amount": 0,
            "selected_period": period,
            "error": str(e)
        }

@app.post("/payments/mark-paid/{user_id}")
async def mark_user_payment_paid(user_id: int, request: MarkPaymentRequest):
    """Mark user payment as paid with period support"""
    try:
        period_keys = excel_handler.get_period_keys(request.payment_period)
        
        if request.payment_period == "all":
            result = excel_handler.mark_all_user_payments_paid(user_id, request.amount)
        else:
            result = excel_handler.mark_period_payments_paid(user_id, period_keys, request.amount)
        
        return result
        
    except Exception as e:
        print(f"Mark payment error: {e}")
        return {"success": False, "message": str(e)}

# ============ ADMIN PAYMENT ENDPOINTS ============
@app.get("/admin/payments")
async def get_all_payments():
    """Get payment summary for all users"""
    payments = excel_handler.get_payment_summary()
    return {"payments": payments}

@app.get("/admin/payments/period/{period}")
async def get_payments_by_period(period: str = "current"):
    """Get payment summary filtered by period"""
    payments = excel_handler.get_payment_summary_by_period(period)
    return {"payments": payments}

@app.post("/admin/payments/{user_id}/mark-paid")
async def mark_payment_as_paid(user_id: int, amount: int):
    """Mark payment as paid"""
    result = excel_handler.mark_payment_paid(user_id, amount)
    return result

@app.get("/admin/payments/{user_id}/history")
async def get_payment_history(user_id: int):
    """Get payment history for a user"""
    history = excel_handler.get_payment_history(user_id)
    return {"history": history}

# ============ PAYOS PAYMENT ENDPOINTS ============
@app.post("/payments/create-payos")
async def create_payos_payment(request: CreatePayOSPaymentRequest):
    """Tạo PayOS payment link và QR code - ENHANCED DEBUG VERSION"""
    
    try:
        # Validation
        if not request.user_id:
            return {"success": False, "message": "Missing user_id"}
        
        if not request.payment_period:
            return {"success": False, "message": "Missing payment_period"}
        
        # Call the actual method
        result = excel_handler.create_payos_payment(request.user_id, request.payment_period)
        
        if result.get('success'):
            
            # ENHANCED: Validate QR code format
            qr_code = result.get('qr_code', '')
            if qr_code:
                print(f"🔍 QR Code Analysis:")
                print(f"   Starts with: {qr_code[:20]}...")
                print(f"   Length: {len(qr_code)}")
                print(f"   Contains VietQR markers: {'00020101' in qr_code}")
                
                # Sample VietQR format check
                if qr_code.startswith('00020101'):
                    print(f"   ✅ Valid VietQR format detected")
                else:
                    print(f"   ⚠️ Unusual QR format - might not be VietQR")
            else:
                print(f"   ❌ No QR code in response!")
                
            # ENHANCED: Validate checkout URL
            checkout_url = result.get('checkout_url', '')
            if checkout_url:
                print(f"🔍 Checkout URL Analysis:")
                print(f"   URL: {checkout_url}")
                print(f"   Is HTTPS: {checkout_url.startswith('https://')}")
                print(f"   Contains payos domain: {'payos' in checkout_url.lower()}")
            else:
                print(f"   ❌ No checkout URL in response!")
                
        else:
            print(f"❌ Excel handler FAILED!")
            print(f"   Error: {result.get('message')}")
        
        print(f"📡 Returning response to frontend...")
        
        # ENHANCED: Add debug info to response for development
        if result.get('success'):
            result['debug_info'] = {
                'qr_code_length': len(result.get('qr_code', '')),
                'has_checkout_url': bool(result.get('checkout_url')),
                'qr_format_check': result.get('qr_code', '').startswith('00020101') if result.get('qr_code') else False,
                'timestamp': datetime.now().isoformat()
            }
        
        return result
        
    except Exception as e:
        print(f"💥 CRITICAL ERROR in PayOS endpoint:")
        print(f"   Exception type: {type(e).__name__}")
        print(f"   Exception message: {str(e)}")
        
        import traceback
        print(f"📋 Full traceback:")
        traceback.print_exc()
        
        return {
            "success": False, 
            "message": f"Server error: {str(e)}",
            "error_type": type(e).__name__,
            "debug_info": {
                "error_occurred": True,
                "timestamp": datetime.now().isoformat()
            }
        }
    finally:
        print(f"🏁 PayOS endpoint finished")
        print(f"="*80 + "\n")

@app.get("/payments/payos-status/{order_code}")
async def check_payos_payment_status(order_code: int):
    """Kiểm tra trạng thái thanh toán PayOS - SAFE VERSION"""
    try:
        print(f"🔍 CHECK PAYOS STATUS REQUEST:")
        print(f"   Order Code: {order_code}")
        
        # Basic validation
        if not order_code:
            return {"success": False, "message": "Missing order_code"}
        
        result = excel_handler.check_payos_payment_status(order_code)
        
        print(f"📊 STATUS CHECK RESULT: {result.get('success', False)}")
        if result.get('success'):
            print(f"   Status: {result.get('status', 'Unknown')}")
        else:
            print(f"❌ Error: {result.get('message', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"💥 CHECK STATUS ENDPOINT ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "message": "Lỗi server khi check status"}

@app.post("/webhooks/payos")
async def payos_webhook(webhook_data: PayOSWebhookData, request: Request):
    """Webhook endpoint để nhận thông báo thanh toán từ PayOS - IMPROVED"""
    start_time = datetime.now()
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        # Validate webhook data structure
        webhook_dict = webhook_data.dict()
        
        # Log webhook content (mask sensitive data)
        safe_webhook = webhook_dict.copy()
        if 'signature' in safe_webhook:
            safe_webhook['signature'] = safe_webhook['signature'][:10] + "..."
        
        # Basic validation
        if not webhook_dict.get('data'):
            return {
                "success": False, 
                "message": "Invalid webhook format - missing data",
                "timestamp": start_time.isoformat()
            }
        
        order_code = webhook_dict.get('data', {}).get('orderCode')
        if not order_code:
            return {
                "success": False, 
                "message": "Invalid webhook format - missing orderCode",
                "timestamp": start_time.isoformat()
            }
        
        # Process the webhook
        result = excel_handler.process_payos_webhook(webhook_dict)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        if result["success"]:
            # Log successful webhook to file (optional)
            try:
                log_entry = {
                    "timestamp": start_time.isoformat(),
                    "order_code": order_code,
                    "user_id": result.get('user_id'),
                    "amount": result.get('amount'),
                    "status": "success",
                    "processing_time": processing_time,
                    "client_ip": client_ip
                }
                
                # You can save this to a log file if needed
                # with open("webhook_logs.json", "a") as f:
                #     f.write(json.dumps(log_entry) + "\n")
                    
            except Exception as log_error:
                print(f"⚠️ Warning: Could not write webhook log: {log_error}")
            
        else:
            print(f"❌ WEBHOOK PROCESSING FAILED")
        
        print(f"="*80 + "\n")
        
        # PayOS yêu cầu return HTTP 200 để xác nhận nhận được webhook
        # Return success=True trong mọi trường hợp để tránh PayOS retry
        return {
            "success": True,  # Always return True to PayOS
            "message": "Webhook received and processed",
            "order_code": order_code,
            "processing_time": f"{processing_time:.2f}s",
            "timestamp": start_time.isoformat(),
            "internal_result": result["success"]  # Internal tracking
        }
        
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        
        import traceback
        traceback.print_exc()
        
        # Even on error, return 200 to PayOS to prevent infinite retries
        return {
            "success": True,  # Return True to PayOS
            "message": "Webhook received with errors",
            "error": str(e),
            "processing_time": f"{processing_time:.2f}s",
            "timestamp": start_time.isoformat()
        }

@app.get("/payments/payos-history/{user_id}")
async def get_payos_payment_history(user_id: int, limit: int = 10):
    """Lấy lịch sử thanh toán PayOS của user"""
    try:
        transactions = excel_handler.get_user_payos_transactions(user_id, limit)
        return {"success": True, "transactions": transactions}
        
    except Exception as e:
        print(f"Get PayOS payment history error: {e}")
        return {"success": False, "message": "Lỗi lấy lịch sử thanh toán"}

@app.get("/payments/payos-config")
async def get_payos_config():
    """Lấy thông tin cấu hình PayOS payment"""
    return {
        "provider": "payos",
        "supports": ["banking", "e_wallet", "qr_code", "payment_link"],
        "timeout_minutes": 30,
        "min_amount": 1000,
        "max_amount": 50000000,
        "currency": "VND",
        "features": {
            "qr_code": True,
            "payment_link": True,
            "webhook": True,
            "real_time": True
        }
    }

@app.post("/payments/cancel-payos/{order_code}")
async def cancel_payos_payment(order_code: int, user_id: int):
    """Cancel PayOS payment (mark as cancelled)"""
    try:
        payos_file = excel_handler.data_dir / "payos_transactions.xlsx"
        if not payos_file.exists():
            return {"success": False, "message": "Không tìm thấy giao dịch"}
        
        import pandas as pd
        payos_df = pd.read_excel(payos_file)
        
        # Find and update transaction
        transaction_mask = (payos_df['order_code'] == order_code) & (payos_df['user_id'] == user_id)
        transaction = payos_df[transaction_mask]
        
        if transaction.empty:
            return {"success": False, "message": "Không tìm thấy giao dịch"}
        
        if transaction.iloc[0]['status'] not in ['PENDING']:
            return {"success": False, "message": "Không thể hủy giao dịch này"}
        
        # Update status to cancelled
        payos_df.loc[transaction_mask, 'status'] = 'CANCELLED'
        payos_df.to_excel(payos_file, index=False)
        
        return {"success": True, "message": "Đã hủy thanh toán"}
        
    except Exception as e:
        print(f"❌ Cancel PayOS payment error: {e}")
        return {"success": False, "message": "Lỗi hủy thanh toán"}

@app.get("/payments/check-status/{order_code}")
async def check_payment_status_detailed(order_code: int):
    """Check detailed payment status including logs"""
    try:
        # Get từ PayOS transactions table
        result = excel_handler.check_payos_payment_status(order_code)
        
        if result["success"]:
            # Thêm thông tin chi tiết
            payos_file = excel_handler.data_dir / "payos_transactions.xlsx"
            if payos_file.exists():
                import pandas as pd
                payos_df = pd.read_excel(payos_file)
                transaction = payos_df[payos_df['order_code'] == order_code]
                
                if not transaction.empty:
                    trans_data = transaction.iloc[0]
                    result.update({
                        "user_id": int(trans_data['user_id']),
                        "payment_period": trans_data['payment_period'],
                        "description": trans_data['description'],
                        "checkout_url": trans_data['checkout_url'],
                        "has_webhook_data": pd.notna(trans_data['webhook_data']),
                        "notes": trans_data['notes'] if pd.notna(trans_data['notes']) else None
                    })
        
        return result
        
    except Exception as e:
        return {"success": False, "message": f"Error checking status: {str(e)}"}
    
# ============ ADMIN GROUP ENDPOINTS ============
@app.get("/admin/groups")
async def get_all_groups():
    """Get all groups with details"""
    groups = excel_handler.get_all_groups_details()
    return {"groups": groups}

@app.delete("/admin/groups/{group_id}")
async def delete_group(group_id: int):
    """Delete a group"""
    result = excel_handler.delete_group(group_id)
    return result

# ============ ADMIN PAYOS ENDPOINTS ============
@app.get("/admin/payos-transactions")
async def get_all_payos_transactions(limit: int = 50):
    """Admin endpoint để xem tất cả PayOS transactions"""
    try:
        import pandas as pd
        
        payos_file = excel_handler.data_dir / "payos_transactions.xlsx"
        if not payos_file.exists():
            return {"success": True, "transactions": []}
        
        payos_df = pd.read_excel(payos_file)
        
        # Get user names
        users_file = excel_handler.data_dir / "users.xlsx"
        users_df = pd.read_excel(users_file, dtype={'identifier': str})
        
        transactions = []
        for _, trans in payos_df.sort_values('created_at', ascending=False).head(limit).iterrows():
            # Get user name
            user = users_df[users_df['id'] == trans['user_id']]
            user_name = user.iloc[0]['name'] if not user.empty else 'Unknown'
            
            transactions.append({
                "id": int(trans['id']),
                "user_id": int(trans['user_id']),
                "user_name": user_name,
                "order_code": int(trans['order_code']),
                "amount": int(trans['amount']),
                "description": trans['description'],
                "status": trans['status'],
                "created_at": trans['created_at'],
                "paid_at": trans['paid_at'] if pd.notna(trans['paid_at']) else None,
                "payment_period": trans['payment_period']
            })
        
        return {"success": True, "transactions": transactions}
        
    except Exception as e:
        print(f"❌ Get all PayOS transactions error: {e}")
        return {"success": False, "message": "Lỗi lấy danh sách giao dịch"}

# ============ FEEDBACK ENDPOINTS ============
@app.post("/feedback/submit")
async def submit_feedback(request: FeedbackRequest, http_request: Request):
    """Submit anonymous feedback"""
    client_ip = http_request.client.host if http_request.client else "unknown"
    result = excel_handler.save_feedback(
        request.feedback_text, 
        request.rating, 
        request.category,
        client_ip
    )
    return result

@app.get("/admin/feedback")
async def get_all_feedback():
    """Get all feedback for admin"""
    feedback = excel_handler.get_all_feedback()
    return {"feedback": feedback}

@app.put("/admin/feedback/{feedback_id}/status")
async def update_feedback_status(feedback_id: int, status_data: dict):
    """Update feedback status"""
    result = excel_handler.update_feedback_status(feedback_id, status_data.get('status'))
    return result

@app.delete("/admin/feedback/{feedback_id}")
async def delete_feedback(feedback_id: int):
    """Delete feedback"""
    result = excel_handler.delete_feedback(feedback_id)
    return result

# ============ TEST & DEVELOPMENT ENDPOINTS ============
@app.post("/payments/test-payos-webhook")
async def test_payos_webhook(order_code: int):
    """Test endpoint để simulate PayOS webhook (chỉ dùng trong development)"""
    try:
        # Tạo fake webhook data
        fake_webhook_data = {
            "code": "00",
            "desc": "success",
            "success": True,
            "data": {
                "orderCode": order_code,
                "amount": 150000,  # Test amount
                "description": "Test payment",
                "accountNumber": "12345678",
                "reference": f"TEST{random.randint(100000, 999999)}",
                "transactionDateTime": "2025-06-01 14:30:00",
                "currency": "VND",
                "paymentLinkId": f"test_payment_link_{order_code}",
                "code": "00",
                "desc": "Thành công"
            },
            "signature": "test_signature_for_development"
        }
        
        # For now, just return success
        return {
            "success": True,
            "message": "Test webhook sent successfully",
            "webhook_data": fake_webhook_data
        }
        
    except Exception as e:
        print(f"❌ Test PayOS webhook error: {e}")
        return {"success": False, "message": "Test webhook failed"}

@app.post("/test/payos-webhook")
async def test_payos_webhook_locally(test_data: dict):
    """Test endpoint để simulate PayOS webhook locally (development only)"""
    try:
        # Get test parameters
        order_code = test_data.get('order_code')
        success = test_data.get('success', True)
        amount = test_data.get('amount', 100000)
        
        if not order_code:
            return {"success": False, "message": "Missing order_code in test data"}
        
        # Create mock webhook data
        mock_webhook = {
            "code": "00" if success else "01",
            "desc": "success" if success else "failed",
            "success": success,
            "data": {
                "orderCode": order_code,
                "amount": amount,
                "description": f"Test payment for order {order_code}",
                "accountNumber": "1234567890",
                "reference": f"TEST{random.randint(100000, 999999)}",
                "transactionDateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "currency": "VND",
                "paymentLinkId": f"test_link_{order_code}",
                "code": "00" if success else "01",
                "desc": "Thành công" if success else "Thất bại"
            },
            "signature": "test_signature_development_only"
        }
        
        # Process mock webhook
        result = excel_handler.process_payos_webhook(mock_webhook)
        
        return {
            "success": True,
            "message": "Test webhook processed",
            "mock_webhook": mock_webhook,
            "processing_result": result
        }
        
    except Exception as e:
        print(f"❌ Test webhook error: {e}")
        return {"success": False, "message": f"Test webhook failed: {str(e)}"}

@app.get("/test/payos-direct")
async def test_payos_direct():
    """Test PayOS API call trực tiếp"""
    try:
        import requests
        import json
        import hmac
        import hashlib
        
        # PayOS credentials
        client_id = excel_handler.PAYOS_CLIENT_ID
        api_key = excel_handler.PAYOS_API_KEY
        checksum_key = excel_handler.PAYOS_CHECKSUM_KEY
        
        # Create test payment request
        test_order = {
            "orderCode": 123456789,
            "amount": 50000,
            "description": "Test Payment CBG",
            "returnUrl": "https://yourdomain.com/return",
            "cancelUrl": "https://yourdomain.com/cancel"
        }
        
        # Create signature
        sorted_keys = sorted(test_order.keys())
        data_string = "&".join([f"{key}={test_order[key]}" for key in sorted_keys])
        
        signature = hmac.new(
            checksum_key.encode('utf-8'),
            data_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        test_order["signature"] = signature
        
        # Headers
        headers = {
            "x-client-id": client_id,
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        # Make request
        response = requests.post(
            "https://api-merchant.payos.vn/v2/payment-requests",
            headers=headers,
            json=test_order,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "status_code": response.status_code,
                "response": data,
                "has_qr": bool(data.get('data', {}).get('qrCode')),
                "has_url": bool(data.get('data', {}).get('checkoutUrl')),
                "qr_length": len(data.get('data', {}).get('qrCode', '')),
                "checkout_url": data.get('data', {}).get('checkoutUrl', '')
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response.text,
                "possible_issues": [
                    "Invalid credentials",
                    "Account not activated", 
                    "Wrong environment (sandbox vs production)",
                    "Invalid request format"
                ]
            }
            
    except Exception as e:
        print(f"❌ Direct test error: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
    
# ============ OPTIONS HANDLERS FOR PREFLIGHT REQUESTS ============
@app.options("/payments/create-payos")
async def options_create_payos():
    return {"message": "OK"}

@app.options("/payments/payos-status/{order_code}")
async def options_payos_status(order_code: int):
    return {"message": "OK"}

@app.options("/orders/{order_id}/edit")
async def options_edit_order(order_id: int):
    """Handle OPTIONS preflight request for edit order"""
    return {"message": "OK"}

@app.options("/orders/{order_id}/cancel")
async def options_cancel_order(order_id: int):
    """Handle OPTIONS preflight request for cancel order"""
    return {"message": "OK"}

@app.options("/admin/auth")
async def options_admin_auth():
    return {"message": "OK"}

@app.options("/users/{user_id}/info")
async def options_user_info(user_id: int):
    return {"message": "OK"}

@app.options("/groups/{group_identifier}/members")
async def options_group_members(group_identifier: str):
    return {"message": "OK"}

@app.options("/groups/{group_identifier}/orders") 
async def options_group_orders(group_identifier: str):
    return {"message": "OK"}

@app.options("/groups/{group_identifier}/payments")
async def options_group_payments(group_identifier: str):
    return {"message": "OK"}

@app.options("/groups/{group_id}/invite")
async def options_group_invite(group_id: int):
    return {"message": "OK"}

# =============
# SERVE FRONTEND STATIC FILES
# =============
static_dir = Path(__file__).parent / "static"

if static_dir.exists() and (static_dir / "index.html").exists():
    # Mount assets folder
    assets_dir = static_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
    
    # Root route - serve index.html
    @app.get("/")
    async def serve_frontend_root():
        return FileResponse(str(static_dir / "index.html"))
    
    # Catch-all route cho SPA routing
    @app.get("/{full_path:path}")
    async def serve_frontend_catchall(full_path: str):
        # Skip API routes
        if full_path.startswith("api/"):
            return {"error": "API endpoint not found"}
        
        # Serve index.html cho tất cả routes khác
        return FileResponse(str(static_dir / "index.html"))
else:
    @app.get("/")
    async def no_frontend():
        return {
            "error": "Static files not found", 
            "message": "Check build process",
            "static_dir": str(static_dir),
            "exists": static_dir.exists()
        }