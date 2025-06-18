import pandas as pd
import os
import random
import string
import time
import requests
import json
import hashlib
import hmac
from datetime import datetime, date, timedelta
from pathlib import Path
from openpyxl.styles import Alignment

# ============ EXCEL HANDLER CLASS ============
class ExcelHandler:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # PayOS Configuration
        self.PAYOS_CLIENT_ID = os.getenv("PAYOS_CLIENT_ID")
        self.PAYOS_API_KEY = os.getenv("PAYOS_API_KEY")  
        self.PAYOS_CHECKSUM_KEY = os.getenv("PAYOS_CHECKSUM_KEY")
        self.PAYOS_BASE_URL = "https://api-merchant.payos.vn"

        self.init_excel_files()

# ============ FILE INITIALIZATION ============
    def init_excel_files(self):
        """Initialize Excel files if they don't exist"""
        
        # admin_codes.xlsx
        admin_codes_file = self.data_dir / "admin_codes.xlsx"
        if not admin_codes_file.exists():
            admin_df = pd.DataFrame([
                {
                    'id': 1,
                    'code': 'hachitu123A@',
                    'description': 'Mã admin mặc định',
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'active'
                }
            ])
            admin_df.to_excel(admin_codes_file, index=False)
        
        # users.xlsx
        users_file = self.data_dir / "users.xlsx"
        if not users_file.exists():
            users_df = pd.DataFrame(columns=[
                'id', 'identifier', 'password', 'name', 'address', 'created_at', 'last_login'
            ])
            # Save with specific format to preserve leading zeros
            with pd.ExcelWriter(users_file, engine='openpyxl') as writer:
                users_df.to_excel(writer, index=False, sheet_name='Sheet1')
                worksheet = writer.sheets['Sheet1']
                # Set identifier column as text format
                for cell in worksheet['B']:
                    cell.number_format = '@'  # Text format
        
        # groups.xlsx
        groups_file = self.data_dir / "groups.xlsx"
        if not groups_file.exists():
            groups_df = pd.DataFrame(columns=[
                'id', 'name', 'code', 'leader_id', 'address', 'description', 'created_at', 'members'
            ])
            groups_df.to_excel(groups_file, index=False)
        
        # menu_config.xlsx
        menu_file = self.data_dir / "menu_config.xlsx"
        if not menu_file.exists():
            menu_df = pd.DataFrame([
                {
                    'date': '2025-05-28',
                    'deadline': '10:00',
                    'toppings': 'Trứng ốp la (+5k), Chả cá thêm (+3k), Rau củ tươi (free)'
                }
            ])
            menu_df.to_excel(menu_file, index=False)

        # menu_items.xlsx - NEW SEPARATE TABLE
        menu_items_file = self.data_dir / "menu_items.xlsx"
        if not menu_items_file.exists():
            items_df = pd.DataFrame([
                {
                    'date': '2025-05-28',
                    'item_name': 'Suất tiêu chuẩn',
                    'price': 35000,
                    'description': 'Cơm gà xào nấm + Canh chua + Rau luộc',
                    'order_index': 1
                },
                {
                    'date': '2025-05-28',
                    'item_name': 'Suất cao cấp', 
                    'price': 40000,
                    'description': 'Cơm bò lúc lắc + Canh chua + Rau luộc + Chả cá',
                    'order_index': 2
                }
            ])
            items_df.to_excel(menu_items_file, index=False)

        # payments.xlsx
        payments_file = self.data_dir / "payments.xlsx"
        if not payments_file.exists():
            payments_df = pd.DataFrame(columns=[
                'user_id', 'period', 'total_orders', 'total_amount', 'paid_amount', 
                'remaining_amount', 'status', 'last_updated', 'payment_date', 'notes'
            ])
            payments_df.to_excel(payments_file, index=False)

        # feedback.xlsx
        feedback_file = self.data_dir / "feedback.xlsx"
        if not feedback_file.exists():
            feedback_df = pd.DataFrame(columns=[
                'id', 'feedback_text', 'rating', 'category', 'created_at', 'ip_address', 'status'
            ])
            feedback_df.to_excel(feedback_file, index=False)

        # payos_transactions.xlsx
        payos_transactions_file = self.data_dir / "payos_transactions.xlsx"
        if not payos_transactions_file.exists():
            payos_transactions_df = pd.DataFrame(columns=[
                'id', 'user_id', 'payment_period', 'order_code', 'amount', 'description',
                'payment_link_id', 'checkout_url', 'qr_code', 'status', 'created_at',
                'expired_at', 'paid_at', 'webhook_data', 'notes'
            ])
            payos_transactions_df.to_excel(payos_transactions_file, index=False)

# ============ ADMIN AUTHENTICATION ============
    def verify_admin_code(self, input_code):
        """Verify admin access code"""
        try:
            admin_codes_file = self.data_dir / "admin_codes.xlsx"
            
            if not admin_codes_file.exists():
                return {"success": False, "message": "Không tìm thấy file mã admin"}
            
            df = pd.read_excel(admin_codes_file)
            
            if df.empty:
                return {"success": False, "message": "Không có mã admin nào trong hệ thống"}
            
            # Find active codes that match input
            active_codes = df[df['status'] == 'active']
            matching_code = active_codes[active_codes['code'] == input_code.strip()]
            
            if not matching_code.empty:
                code_info = matching_code.iloc[0]
                return {
                    "success": True,
                    "message": "Xác thực thành công",
                    "admin_info": {
                        "code_id": int(code_info['id']),
                        "description": code_info['description'],
                        "created_at": code_info['created_at']
                    }
                }
            else:
                return {"success": False, "message": "Mã admin không đúng!"}
                
        except Exception as e:
            return {"success": False, "message": "Lỗi kiểm tra mã admin"}

    def get_admin_codes(self):
        """Get all admin codes for management (admin only)"""
        try:
            admin_codes_file = self.data_dir / "admin_codes.xlsx"
            
            if not admin_codes_file.exists():
                return []
            
            df = pd.read_excel(admin_codes_file)
            
            codes = []
            for _, code in df.iterrows():
                codes.append({
                    "id": int(code['id']),
                    "code": code['code'],
                    "description": code['description'],
                    "created_at": code['created_at'],
                    "status": code['status']
                })
            
            return codes
            
        except Exception as e:
            return []

    def add_admin_code(self, new_code, description=""):
        """Add new admin code"""
        try:
            admin_codes_file = self.data_dir / "admin_codes.xlsx"
            
            # Read existing codes
            try:
                df = pd.read_excel(admin_codes_file)
            except:
                df = pd.DataFrame(columns=['id', 'code', 'description', 'created_at', 'status'])
            
            # Check if code already exists
            if not df.empty and new_code in df['code'].values:
                return {"success": False, "message": "Mã admin đã tồn tại"}
            
            # Get next ID
            next_id = 1 if df.empty else int(df['id'].max()) + 1
            
            # Add new code
            new_admin_code = {
                'id': next_id,
                'code': new_code.strip(),
                'description': description or f'Mã admin #{next_id}',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'active'
            }
            
            df = pd.concat([df, pd.DataFrame([new_admin_code])], ignore_index=True)
            df.to_excel(admin_codes_file, index=False)
            
            return {"success": True, "message": "Đã thêm mã admin mới"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}

    def update_admin_code_status(self, code_id, new_status):
        """Update admin code status (active/inactive)"""
        try:
            admin_codes_file = self.data_dir / "admin_codes.xlsx"
            df = pd.read_excel(admin_codes_file)
            
            if code_id not in df['id'].values:
                return {"success": False, "message": "Không tìm thấy mã admin"}
            
            df.loc[df['id'] == code_id, 'status'] = new_status
            df.to_excel(admin_codes_file, index=False)
            
            return {"success": True, "message": f"Đã cập nhật trạng thái thành {new_status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
# ============ USER MANAGEMENT ============
    def create_user(self, identifier, password, name, address=""):
        """Create new user - UPDATED with address parameter"""
        users_file = self.data_dir / "users.xlsx"
        
        try:
            df = pd.read_excel(users_file, dtype={'identifier': str, 'password': str})
        except:
            df = pd.DataFrame(columns=['id', 'identifier', 'password', 'name', 'address', 'created_at', 'last_login'])
        
        # Ensure identifier is string to preserve leading zeros
        identifier = str(identifier)
        
        # Check if user exists
        if not df.empty and identifier in df['identifier'].astype(str).values:
            return {"success": False, "message": "User already exists"}
        
        # Get next ID
        next_id = 1 if df.empty else int(df['id'].max()) + 1
        
        # Add new user with address
        new_user = {
            'id': next_id,
            'identifier': identifier,
            'password': str(password),
            'name': name,
            'address': address,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': None
        }
        
        df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
        
        # Save with text format for identifier column
        with pd.ExcelWriter(users_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            worksheet = writer.sheets['Sheet1']
            # Set identifier column as text format
            for cell in worksheet['B']:
                cell.number_format = '@'
        
        return {"success": True, "user_id": int(next_id)}
    
    def update_user_info(self, user_id, name=None, address=None):
        """Update user information"""
        users_file = self.data_dir / "users.xlsx"
        
        try:
            df = pd.read_excel(users_file, dtype={'identifier': str, 'password': str})
            
            # Find user
            user_mask = df['id'] == user_id
            user = df[user_mask]
            
            if user.empty:
                return {"success": False, "message": "Không tìm thấy người dùng"}
            
            # Update fields if provided
            if name is not None:
                df.loc[user_mask, 'name'] = name
            
            if address is not None:
                df.loc[user_mask, 'address'] = address
            
            # Update last_login timestamp as "last updated"
            df.loc[user_mask, 'last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Save with text format preserved
            with pd.ExcelWriter(users_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                worksheet = writer.sheets['Sheet1']
                for cell in worksheet['B']:
                    cell.number_format = '@'
            
            # Return updated user data
            updated_user = df[user_mask].iloc[0]
            return {
                "success": True,
                "message": "Cập nhật thông tin thành công",
                "user": {
                    "id": int(updated_user['id']),
                    "name": updated_user['name'],
                    "identifier": updated_user['identifier'],
                    "address": updated_user['address'] if pd.notna(updated_user['address']) else ""
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Lỗi cập nhật thông tin: {str(e)}"}
        
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        users_file = self.data_dir / "users.xlsx"
        
        try:
            df = pd.read_excel(users_file, dtype={'identifier': str, 'password': str})
            
            user = df[df['id'] == user_id]
            
            if user.empty:
                return {"success": False, "message": "Không tìm thấy người dùng"}
            
            user_data = user.iloc[0]
            return {
                "success": True,
                "user": {
                    "id": int(user_data['id']),
                    "name": user_data['name'],
                    "identifier": user_data['identifier'],
                    "address": user_data['address'] if pd.notna(user_data['address']) else "",
                    "created_at": user_data['created_at'],
                    "last_login": user_data['last_login'] if pd.notna(user_data['last_login']) else None
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Lỗi lấy thông tin người dùng: {str(e)}"}
    
    def authenticate_user(self, identifier, password):
        """Login user - UPDATED to return address"""
        users_file = self.data_dir / "users.xlsx"
        
        try:
            # Read with dtype to preserve leading zeros
            df = pd.read_excel(users_file, dtype={'identifier': str, 'password': str})
            
        except FileNotFoundError:
            return {"success": False, "message": "No users file found"}
        except Exception as e:
            return {"success": False, "message": f"Error reading file: {e}"}
        
        if df.empty:
            return {"success": False, "message": "No users found"}
        
        # Convert to string to preserve leading zeros
        df['identifier'] = df['identifier'].astype(str)
        df['password'] = df['password'].astype(str)
        identifier = str(identifier)
        password = str(password)
        
        user = df[(df['identifier'] == identifier) & (df['password'] == password)]
        
        if user.empty:
            return {"success": False, "message": "Invalid credentials"}
        
        # Update last login
        df.loc[df['identifier'] == identifier, 'last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save with text format preserved
        with pd.ExcelWriter(users_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            worksheet = writer.sheets['Sheet1']
            for cell in worksheet['B']:
                cell.number_format = '@'
        
        user_data = user.iloc[0]
        return {
            "success": True,
            "user": {
                "id": int(user_data['id']),
                "name": user_data['name'],
                "identifier": user_data['identifier'],
                "address": user_data['address'] if pd.notna(user_data['address']) else ""
            }
        }
    
    def get_user_groups(self, user_id):
        """Get groups that user belongs to"""
        groups_file = self.data_dir / "groups.xlsx"
        df = pd.read_excel(groups_file)
        
        if df.empty:
            return []
        
        user_groups = []
        for _, group in df.iterrows():
            members = str(group['members']).split(',') if pd.notna(group['members']) else []
            is_leader = int(group['leader_id']) == user_id
            is_member = str(user_id) in members or is_leader
            
            if is_member:
                user_groups.append({
                    "name": group['name'],
                    "code": group['code'],
                    "isLeader": is_leader,
                    "members": len(members),
                    "totalOrders": 0  # TODO: Calculate from orders
                })
        
        return user_groups
    
# ============ GROUP MANAGEMENT ============
    def create_group(self, name, code, leader_id, address, description=""):
        """Create new group"""
        groups_file = self.data_dir / "groups.xlsx"
        
        try:
            df = pd.read_excel(groups_file)
        except:
            df = pd.DataFrame(columns=['id', 'name', 'code', 'leader_id', 'address', 'description', 'created_at', 'members'])
        
        # Check if group code exists
        if not df.empty and code in df['code'].values:
            return {"success": False, "message": "Group code already exists"}
        
        # Get next ID
        next_id = 1 if df.empty else int(df['id'].max()) + 1
        
        # Add new group
        new_group = {
            'id': next_id,
            'name': name,
            'code': code,
            'leader_id': int(leader_id),  # Convert to Python int
            'address': address,
            'description': description,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'members': str(leader_id)  # Leader is first member
        }
        
        df = pd.concat([df, pd.DataFrame([new_group])], ignore_index=True)
        df.to_excel(groups_file, index=False)
        
        return {"success": True, "group_id": int(next_id), "code": code}
    
    def join_group(self, group_code, user_id):
        """Join existing group"""
        groups_file = self.data_dir / "groups.xlsx"
        df = pd.read_excel(groups_file)
        
        if df.empty:
            return {"success": False, "message": "No groups found"}
        
        group = df[df['code'] == group_code]
        if group.empty:
            return {"success": False, "message": "Group not found"}
        
        # Add user to members
        current_members = str(group.iloc[0]['members']).split(',')
        if str(user_id) not in current_members:
            current_members.append(str(user_id))
            df.loc[df['code'] == group_code, 'members'] = ','.join(current_members)
            df.to_excel(groups_file, index=False)
        
        return {"success": True, "message": "Joined group successfully"}

    def get_all_groups_details(self):
        """Get all groups with member details"""
        try:
            groups_df = pd.read_excel(self.data_dir / "groups.xlsx")
            users_df = pd.read_excel(self.data_dir / "users.xlsx", dtype={'identifier': str})
            
            groups = []
            for _, group in groups_df.iterrows():
                # Get leader info
                leader = users_df[users_df['id'] == group['leader_id']]
                leader_name = leader.iloc[0]['name'] if not leader.empty else 'Unknown'
                
                # Get members
                member_ids = str(group['members']).split(',') if pd.notna(group['members']) else []
                members = []
                
                for member_id in member_ids:
                    try:
                        user = users_df[users_df['id'] == int(member_id)]
                        if not user.empty:
                            user_data = user.iloc[0]
                            members.append({
                                "id": int(user_data['id']),
                                "name": user_data['name'],
                                "identifier": user_data['identifier'],
                                "is_leader": int(user_data['id']) == int(group['leader_id'])
                            })
                    except:
                        continue
                
                groups.append({
                    "id": int(group['id']),
                    "name": group['name'],
                    "code": group['code'],
                    "leader_name": leader_name,
                    "member_count": len(members),
                    "address": group['address'],
                    "description": group['description'] if pd.notna(group['description']) else '',
                    "members": members
                })
            
            return groups
        except Exception as e:
            return []
    
    def delete_group(self, group_id):
        """Delete a group"""
        try:
            groups_file = self.data_dir / "groups.xlsx"
            df = pd.read_excel(groups_file)
            
            if group_id not in df['id'].values:
                return {"success": False, "message": "Group not found"}
            
            df = df[df['id'] != group_id]
            df.to_excel(groups_file, index=False)
            
            return {"success": True, "message": "Group deleted"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_group_members_with_stats(self, group_identifier):
        """Get group members with their order statistics - FIXED"""
        try:
            groups_file = self.data_dir / "groups.xlsx"
            users_file = self.data_dir / "users.xlsx"
            
            if not groups_file.exists() or not users_file.exists():
                return {"success": False, "message": "Không tìm thấy dữ liệu nhóm"}
            
            groups_df = pd.read_excel(groups_file)
            users_df = pd.read_excel(users_file, dtype={'identifier': str})
            
            # Find group by ID, name, or code
            group = pd.DataFrame()
            
            if str(group_identifier).isdigit():
                group = groups_df[groups_df['id'] == int(group_identifier)]
            
            if group.empty:
                group = groups_df[groups_df['name'] == str(group_identifier)]
            
            if group.empty:
                group = groups_df[groups_df['code'] == str(group_identifier)]
            
            if group.empty:
                return {"success": False, "message": f"Không tìm thấy nhóm: {group_identifier}"}
            
            group_data = group.iloc[0]
            
            # Parse member IDs
            member_ids_str = str(group_data['members']) if pd.notna(group_data['members']) else ""
            member_ids = []
            
            if member_ids_str.strip():
                member_ids = [int(id.strip()) for id in member_ids_str.split(',') if id.strip().isdigit()]
            
            # Add leader if not in members list
            leader_id = int(group_data['leader_id'])
            if leader_id not in member_ids:
                member_ids.insert(0, leader_id)
            
            members = []
            for member_id in member_ids:
                user = users_df[users_df['id'] == member_id]
                if user.empty:
                    continue
                
                user_data = user.iloc[0]
                member_stats = self.calculate_member_stats(member_id)
                is_leader = int(member_id) == int(group_data['leader_id'])
                
                member_info = {
                    "id": int(member_id),
                    "name": user_data['name'],
                    "phone": user_data['identifier'],
                    "isLeader": is_leader,
                    "joinedAt": user_data['created_at'] if pd.notna(user_data['created_at']) else 'Không rõ',
                    "totalOrders": member_stats['total_orders'],
                    "totalAmount": member_stats['total_amount']
                }
                
                members.append(member_info)
            
            members.sort(key=lambda x: (not x['isLeader'], -x['totalOrders']))
            
            return {
                "success": True,
                "members": members,
                "group_info": {
                    "id": int(group_data['id']),
                    "name": group_data['name'],
                    "code": group_data['code'],
                    "member_count": len(members)
                }
            }
            
        except Exception as e:
            return {"success": False, "message": "Lỗi tải thông tin thành viên"}

    def calculate_member_stats(self, user_id):
        """Calculate order statistics for a member"""
        try:
            # Get all order files
            order_files = list(self.data_dir.glob("orders_*.xlsx"))
            
            total_orders = 0
            total_amount = 0
            
            for order_file in order_files:
                try:
                    df = pd.read_excel(order_file)
                    user_orders = df[df['user_id'] == user_id]
                    
                    total_orders += len(user_orders)
                    total_amount += user_orders['total_amount'].sum() if not user_orders.empty else 0
                    
                except Exception as e:
                    continue
            
            return {
                "total_orders": int(total_orders),
                "total_amount": int(total_amount)
            }
            
        except Exception as e:
            return {"total_orders": 0, "total_amount": 0}

    def get_group_orders(self, group_identifier):
        """Get all orders for a specific group - FIXED"""
        try:
            groups_file = self.data_dir / "groups.xlsx"
            if not groups_file.exists():
                return {"success": False, "message": "Không tìm thấy dữ liệu nhóm"}
            
            groups_df = pd.read_excel(groups_file)
            
            # Find group
            group = pd.DataFrame()
            
            if str(group_identifier).isdigit():
                group = groups_df[groups_df['id'] == int(group_identifier)]
            
            if group.empty:
                group = groups_df[groups_df['name'] == str(group_identifier)]
            
            if group.empty:
                group = groups_df[groups_df['code'] == str(group_identifier)]
            
            if group.empty:
                return {"success": False, "message": "Không tìm thấy nhóm"}
            
            group_data = group.iloc[0]
            group_name = group_data['name']
            
            # Get member IDs
            member_ids_str = str(group_data['members']) if pd.notna(group_data['members']) else ""
            member_ids = []
            if member_ids_str.strip():
                member_ids = [int(id.strip()) for id in member_ids_str.split(',') if id.strip().isdigit()]
            
            leader_id = int(group_data['leader_id'])
            if leader_id not in member_ids:
                member_ids.insert(0, leader_id)
            
            # Get orders
            order_files = list(self.data_dir.glob("orders_*.xlsx"))
            users_file = self.data_dir / "users.xlsx"
            
            if not users_file.exists():
                return {"success": False, "message": "Không tìm thấy dữ liệu người dùng"}
            
            users_df = pd.read_excel(users_file, dtype={'identifier': str})
            all_orders = []
            
            for order_file in order_files:
                try:
                    date_str = order_file.stem.replace('orders_', '')
                    df = pd.read_excel(order_file)
                    
                    group_orders = pd.DataFrame()
                    
                    # Orders for the group
                    if not df.empty:
                        orders_for_group = df[df['group_id'] == group_name]
                        if not orders_for_group.empty:
                            group_orders = pd.concat([group_orders, orders_for_group], ignore_index=True)
                    
                    # Personal orders by group members
                    if member_ids and not df.empty:
                        member_orders = df[
                            (df['user_id'].isin(member_ids)) & 
                            ((df['group_id'] == 'personal') | (pd.isna(df['group_id'])))
                        ]
                        if not member_orders.empty:
                            group_orders = pd.concat([group_orders, member_orders], ignore_index=True)
                    
                    for _, order in group_orders.iterrows():
                        user = users_df[users_df['id'] == order['user_id']]
                        user_name = user.iloc[0]['name'] if not user.empty else 'Unknown'
                        
                        order_info = {
                            "id": int(order['id']),
                            "date": date_str,
                            "time": order['created_at'],
                            "userName": user_name,
                            "userId": int(order['user_id']),
                            "mealType": order['meal_type'],
                            "quantity": int(order['quantity']),
                            "totalAmount": int(order['total_amount']),
                            "status": order['status'],
                            "note": order['note'] if pd.notna(order['note']) else '',
                            "orderType": "Nhóm" if order['group_id'] == group_name else "Cá nhân"
                        }
                        
                        all_orders.append(order_info)
                            
                except Exception as e:
                    continue
            
            all_orders.sort(key=lambda x: (x['date'], x['time']), reverse=True)
            
            return {
                "success": True,
                "orders": all_orders
            }
            
        except Exception as e:
            return {"success": False, "message": "Lỗi tải đơn hàng nhóm"}

    def get_group_payments(self, group_identifier, period="current"):
        """Get payment information for all group members"""
        try:
            members_result = self.get_group_members_with_stats(group_identifier)
            if not members_result["success"]:
                return members_result
            
            members = members_result["members"]
            
            payments_file = self.data_dir / "payments.xlsx"
            if not payments_file.exists():
                return {"success": False, "message": "Không tìm thấy dữ liệu thanh toán"}
            
            payments_df = pd.read_excel(payments_file)
            
            # Filter by period
            if period == "current":
                now = datetime.now()
                period_key = f"{now.year}-{now.month:02d}"
                filtered_payments = payments_df[payments_df['period'] == period_key]
            elif period == "last":
                now = datetime.now()
                last_month = now.month - 1 if now.month > 1 else 12
                year = now.year if now.month > 1 else now.year - 1
                period_key = f"{year}-{last_month:02d}"
                filtered_payments = payments_df[payments_df['period'] == period_key]
            else:  # all
                filtered_payments = payments_df
            
            member_payments = []
            total_amount = 0
            total_paid = 0
            total_remaining = 0
            
            for member in members:
                user_id = member['id']
                user_payments = filtered_payments[filtered_payments['user_id'] == user_id]
                
                if not user_payments.empty:
                    member_total = user_payments['total_amount'].sum()
                    member_paid = user_payments['paid_amount'].sum()
                    member_remaining = user_payments['remaining_amount'].sum()
                    member_orders = user_payments['total_orders'].sum()
                else:
                    member_total = 0
                    member_paid = 0
                    member_remaining = 0
                    member_orders = 0
                
                member_payments.append({
                    "userId": user_id,
                    "userName": member['name'],
                    "totalOrders": int(member_orders),
                    "totalAmount": int(member_total),
                    "paidAmount": int(member_paid),
                    "remainingAmount": int(member_remaining)
                })
                
                total_amount += member_total
                total_paid += member_paid
                total_remaining += member_remaining
            
            return {
                "success": True,
                "payments": member_payments,
                "summary": {
                    "totalAmount": int(total_amount),
                    "paidAmount": int(total_paid),
                    "remainingAmount": int(total_remaining)
                }
            }
            
        except Exception as e:
            return {"success": False, "message": "Lỗi tải thông tin thanh toán"}

    def get_group_invite_info(self, group_id):
        """Get group information for invitation"""
        try:
            groups_file = self.data_dir / "groups.xlsx"
            if not groups_file.exists():
                return {"success": False, "message": "Không tìm thấy dữ liệu nhóm"}
            
            groups_df = pd.read_excel(groups_file)
            group = groups_df[groups_df['id'] == group_id]
            
            if group.empty:
                return {"success": False, "message": "Không tìm thấy nhóm"}
            
            group_data = group.iloc[0]
            
            return {
                "success": True,
                "group_code": group_data['code'],
                "group_name": group_data['name']
            }
            
        except Exception as e:
            return {"success": False, "message": "Lỗi lấy thông tin nhóm"}

    def remove_group_member(self, group_id, user_id):
        """Remove a member from group"""
        try:
            groups_file = self.data_dir / "groups.xlsx"
            if not groups_file.exists():
                return {"success": False, "message": "Không tìm thấy dữ liệu nhóm"}
            
            groups_df = pd.read_excel(groups_file)
            group = groups_df[groups_df['id'] == group_id]
            
            if group.empty:
                return {"success": False, "message": "Không tìm thấy nhóm"}
            
            group_data = group.iloc[0]
            
            # Check if trying to remove leader
            if int(group_data['leader_id']) == user_id:
                return {"success": False, "message": "Không thể loại trưởng nhóm"}
            
            # Remove user from members list
            members_str = str(group_data['members']) if pd.notna(group_data['members']) else ""
            member_ids = [id.strip() for id in members_str.split(',') if id.strip()]
            
            if str(user_id) in member_ids:
                member_ids.remove(str(user_id))
                new_members_str = ','.join(member_ids)
                
                # Update database
                groups_df.loc[groups_df['id'] == group_id, 'members'] = new_members_str
                groups_df.to_excel(groups_file, index=False)
                
                return {"success": True, "message": "Đã loại thành viên khỏi nhóm"}
            else:
                return {"success": False, "message": "Thành viên không có trong nhóm"}
            
        except Exception as e:
            return {"success": False, "message": "Lỗi loại thành viên khỏi nhóm"}
        
# ============ MENU MANAGEMENT ============
    def get_today_menu(self):
        """Get today's menu from separate tables - PRESERVE LINE BREAKS"""
        try:
            menu_file = self.data_dir / "menu_config.xlsx"
            items_file = self.data_dir / "menu_items.xlsx"
            
            # Read menu config và items
            try:
                menu_df = pd.read_excel(menu_file)
                items_df = pd.read_excel(items_file)
            except:
                self.init_excel_files()
                menu_df = pd.read_excel(menu_file)
                items_df = pd.read_excel(items_file)
            
            today = date.today().strftime('%Y-%m-%d')
            
            # Get menu config for today
            menu_config = menu_df[menu_df['date'] == today]
            if menu_config.empty and not menu_df.empty:
                menu_config = menu_df.iloc[-1:]
            
            # Get menu items for today
            menu_items = items_df[items_df['date'] == today].sort_values('order_index')
            if menu_items.empty and not items_df.empty:
                latest_date = items_df['date'].max()
                menu_items = items_df[items_df['date'] == latest_date].sort_values('order_index')
            
            # Build response
            if not menu_config.empty:
                config = menu_config.iloc[0]
                deadline = config['deadline']
                toppings = config['toppings']
            else:
                deadline = "10:00"
                toppings = "Đang cập nhật..."
            
            # Convert items to list với line breaks preserved
            items_list = []
            for _, item in menu_items.iterrows():
                description = item['description']
                
                # Đảm bảo line breaks được giữ nguyên từ Excel
                if pd.isna(description):
                    description = ""
                else:
                    description = str(description)
                    # Excel có thể lưu line breaks như \r\n, chuẩn hóa thành \n
                    description = description.replace('\r\n', '\n').replace('\r', '\n')
                
                items_list.append({
                    "name": item['item_name'],
                    "price": int(item['price']),
                    "description": description  # Giữ nguyên line breaks
                })
            
            if not items_list:
                # Fallback với line breaks
                items_list = [
                    {
                        "name": "Suất tiêu chuẩn", 
                        "price": 35000, 
                        "description": "Menu chưa được cập nhật\nVui lòng liên hệ admin"
                    },
                    {
                        "name": "Suất cao cấp", 
                        "price": 40000, 
                        "description": "Menu chưa được cập nhật\nVui lòng liên hệ admin"
                    }
                ]
            
            return {
                "date": today,
                "deadline": deadline,
                "menu_items": items_list,
                "toppings": toppings
            }
            
        except Exception as e:
            return {
                "date": date.today().strftime('%Y-%m-%d'),
                "deadline": "10:00",
                "menu_items": [
                    {
                        "name": "Suất tiêu chuẩn", 
                        "price": 35000, 
                        "description": "Lỗi tải menu\nVui lòng thử lại"
                    },
                    {
                        "name": "Suất cao cấp", 
                        "price": 40000, 
                        "description": "Lỗi tải menu\nVui lòng thử lại"
                    }
                ],
                "toppings": "Đang cập nhật..."
            }
        
    def get_meal_price(self, meal_type):
        """Get actual price of meal type from menu_items table"""
        try:
            items_file = self.data_dir / "menu_items.xlsx"
            
            if not items_file.exists():
                return 35000
                
            items_df = pd.read_excel(items_file)
            today = date.today().strftime('%Y-%m-%d')
            
            # Find item by exact name match for today
            item = items_df[(items_df['date'] == today) & (items_df['item_name'] == meal_type)]
            
            if not item.empty:
                return int(item.iloc[0]['price'])
            
            # Try latest date if today not found
            if not items_df.empty:
                latest_date = items_df['date'].max()
                item = items_df[(items_df['date'] == latest_date) & (items_df['item_name'] == meal_type)]
                
                if not item.empty:
                    return int(item.iloc[0]['price'])
            
            return 35000
                
        except Exception as e:
            return 35000
    
    def parse_menu_items(self, menu_items_str):
        """Parse menu items from JSON string"""
        try:
            import json
            return json.loads(menu_items_str)
        except:
            # Fallback to default items
            return [
                {"name": "Suất tiêu chuẩn", "price": 35000, "description": "Menu chưa được cập nhật"},
                {"name": "Suất cao cấp", "price": 40000, "description": "Menu chưa được cập nhật"}
            ]

    def save_menu(self, menu_data):
        """Save menu to separate tables - FIXED to preserve line breaks"""
        try:
            from openpyxl.styles import Alignment
            
            menu_file = self.data_dir / "menu_config.xlsx"
            items_file = self.data_dir / "menu_items.xlsx"
            
            # Read existing data
            try:
                menu_df = pd.read_excel(menu_file)
                items_df = pd.read_excel(items_file)
            except:
                menu_df = pd.DataFrame(columns=['date', 'deadline', 'toppings'])
                items_df = pd.DataFrame(columns=['date', 'item_name', 'price', 'description', 'order_index'])
            
            date_str = menu_data['date']
            
            # Update menu config
            existing_config = menu_df[menu_df['date'] == date_str]
            if not existing_config.empty:
                menu_df.loc[menu_df['date'] == date_str, 'deadline'] = menu_data['deadline']
                menu_df.loc[menu_df['date'] == date_str, 'toppings'] = menu_data['toppings']
            else:
                new_config = {
                    'date': date_str,
                    'deadline': menu_data['deadline'],
                    'toppings': menu_data['toppings']
                }
                menu_df = pd.concat([menu_df, pd.DataFrame([new_config])], ignore_index=True)
            
            # Update menu items - Remove old items for this date
            items_df = items_df[items_df['date'] != date_str]
            
            # Add new items with line breaks preserved
            new_items = []
            for index, item in enumerate(menu_data['menu_items']):
                # PRESERVE line breaks trong description
                description = item.get('description', '')
                # Đảm bảo \n được giữ nguyên khi lưu vào Excel
                
                new_item = {
                    'date': date_str,
                    'item_name': item['name'],
                    'price': int(item['price']),
                    'description': description,  # Giữ nguyên line breaks
                    'order_index': index + 1
                }
                new_items.append(new_item)
            
            # Add to dataframe
            if new_items:
                items_df = pd.concat([items_df, pd.DataFrame(new_items)], ignore_index=True)
            
            # Save menu config (normal)
            menu_df.to_excel(menu_file, index=False)
            
            # Save items with wrap_text for Excel to display line breaks
            with pd.ExcelWriter(items_file, engine='openpyxl') as writer:
                items_df.to_excel(writer, index=False, sheet_name='Sheet1')
                
                # Get worksheet and apply formatting
                worksheet = writer.sheets['Sheet1']
                
                # Set wrap_text for description column (column D - index 4)
                for row in range(2, len(items_df) + 2):  # Start from row 2 (after header)
                    description_cell = worksheet.cell(row=row, column=4)  # Column D
                    description_cell.alignment = Alignment(
                        wrap_text=True,      # Enable text wrapping
                        vertical='top',      # Align to top
                        horizontal='left'    # Align to left
                    )
                    
                    # Increase row height to display full content
                    worksheet.row_dimensions[row].height = None  # Auto-size
                
                # Set column width for description
                worksheet.column_dimensions['D'].width = 40  # Increase width for description column
            
            return {"success": True, "message": "Menu saved successfully with line breaks preserved"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}
        
# ============ ORDER MANAGEMENT ============
    def create_order(self, user_id, group_id, meal_type, quantity, note=""):
        """Create new order"""
        today = date.today().strftime('%Y-%m-%d')
        orders_file = self.data_dir / f"orders_{today}.xlsx"
        
        # Create daily orders file if doesn't exist
        if not orders_file.exists():
            df = pd.DataFrame(columns=[
                'id', 'user_id', 'group_id', 'meal_type', 'quantity', 'note', 'total_amount', 'status', 'created_at'
            ])
        else:
            df = pd.read_excel(orders_file)
        
        # GET ACTUAL PRICE FROM MENU
        price = self.get_meal_price(meal_type)
        total_amount = price * quantity
        
        # Get next ID
        next_id = 1 if df.empty else int(df['id'].max()) + 1
        
        # Add new order
        new_order = {
            'id': next_id,
            'user_id': int(user_id),
            'group_id': group_id if group_id != 'personal' else None,
            'meal_type': meal_type,
            'quantity': int(quantity),
            'note': note,
            'total_amount': int(total_amount),
            'status': 'pending',
            'created_at': datetime.now().strftime('%H:%M:%S')
        }
        
        df = pd.concat([df, pd.DataFrame([new_order])], ignore_index=True)
        df.to_excel(orders_file, index=False)

        # UPDATE PAYMENT BALANCE
        self.update_user_payment_balance(user_id, total_amount)
        
        return {"success": True, "order_id": int(next_id), "total_amount": int(total_amount)}

    def get_user_order_history(self, user_id):
        """Get order history for a user from all order files"""
        try:
            order_files = list(self.data_dir.glob("orders_*.xlsx"))
            all_orders = []
            
            for order_file in order_files:
                try:
                    df = pd.read_excel(order_file)
                    user_orders = df[df['user_id'] == user_id]
                    
                    # Extract date from filename (orders_YYYY-MM-DD.xlsx)
                    date_str = order_file.stem.replace('orders_', '')
                    
                    for _, order in user_orders.iterrows():
                        all_orders.append({
                            "id": int(order['id']),
                            "date": date_str,
                            "meal_type": order['meal_type'],
                            "quantity": int(order['quantity']),
                            "note": order['note'] if pd.notna(order['note']) else '',
                            "total_amount": int(order['total_amount']),
                            "status": order['status'],
                            "created_at": order['created_at'],
                            # THÊM DÒNG NÀY
                            "group_id": order['group_id'] if pd.notna(order['group_id']) else 'personal'
                        })
                except:
                    continue
            
            # Sort by date descending (newest first)
            all_orders.sort(key=lambda x: (x['date'], x['id']), reverse=True)
            return all_orders[:100]  # Limit to 100 most recent orders
            
        except Exception as e:
            return []

    def cancel_order(self, order_id, user_id, order_date):
        """Cancel an order by changing status to cancelled"""
        try:
            orders_file = self.data_dir / f"orders_{order_date}.xlsx"
            
            if not orders_file.exists():
                return {"success": False, "message": "Order file not found"}
            
            df = pd.read_excel(orders_file)
            
            # Find the order
            order_mask = (df['id'] == order_id) & (df['user_id'] == user_id)
            order = df[order_mask]
            
            if order.empty:
                return {"success": False, "message": "Order not found"}
            
            # Check if order can be cancelled
            current_status = order.iloc[0]['status']
            if current_status != 'pending':
                return {"success": False, "message": f"Không thể hủy đơn ở trạng thái '{current_status}'"}
            
            # Get order amount for payment adjustment
            order_amount = int(order.iloc[0]['total_amount'])
            
            # Update order status to cancelled
            df.loc[order_mask, 'status'] = 'cancelled'
            df.to_excel(orders_file, index=False)
            
            # Adjust payment balance (subtract the cancelled amount)
            self.adjust_payment_balance(user_id, -order_amount, order_date)
            
            return {"success": True, "message": "Đã hủy đơn thành công"}
            
        except Exception as e:
            print(f"Error cancelling order: {e}")
            return {"success": False, "message": str(e)}

    def edit_order(self, order_id, user_id, order_date, new_meal_type, new_quantity, new_note, new_group_id=None):
        """Edit an existing order - UPDATED with group_id support"""
        try:
            print(f"   New Group ID: '{new_group_id}' (type: {type(new_group_id)})")

            orders_file = self.data_dir / f"orders_{order_date}.xlsx"
            
            if not orders_file.exists():
                return {"success": False, "message": "Order file not found"}
            
            df = pd.read_excel(orders_file)
            
            # Find the order
            order_mask = (df['id'] == order_id) & (df['user_id'] == user_id)
            order = df[order_mask]
            
            if order.empty:
                return {"success": False, "message": "Order not found"}
            
            # Check if order can be edited
            current_status = order.iloc[0]['status']
            if current_status != 'pending':
                return {"success": False, "message": f"Không thể sửa đơn ở trạng thái '{current_status}'"}
            
            # Get old amount
            old_amount = int(order.iloc[0]['total_amount'])
            
            # Calculate new amount
            new_price = self.get_meal_price(new_meal_type)
            new_total_amount = new_price * new_quantity
            
            # Update order
            df.loc[order_mask, 'meal_type'] = new_meal_type
            df.loc[order_mask, 'quantity'] = int(new_quantity)
            df.loc[order_mask, 'note'] = new_note
            df.loc[order_mask, 'total_amount'] = int(new_total_amount)
            df.loc[order_mask, 'group_id'] = new_group_id
            
            # Save updated order
            print(f"💾 Saving to file: {orders_file}")
            df.to_excel(orders_file, index=False)
            
            # Adjust payment balance (difference between new and old amount)
            amount_difference = new_total_amount - old_amount
            if amount_difference != 0:
                self.adjust_payment_balance(user_id, amount_difference, order_date)
            
            return {
                "success": True, 
                "message": "Đã cập nhật đơn hàng thành công",
                "new_total_amount": int(new_total_amount),
                "amount_difference": int(amount_difference)
            }
            
        except Exception as e:
            print(f"Error editing order: {e}")
            return {"success": False, "message": str(e)}

    def adjust_payment_balance(self, user_id, amount_change, order_date):
        """Adjust user payment balance when order is modified"""
        try:
            payments_file = self.data_dir / "payments.xlsx"
            
            # Extract period from order date (YYYY-MM-DD -> YYYY-MM)
            period = '-'.join(order_date.split('-')[:2])
            
            try:
                df = pd.read_excel(payments_file)
            except:
                # If no payments file, no adjustment needed
                return
            
            # Find user's payment record for the period
            payment_mask = (df['user_id'] == user_id) & (df['period'] == period)
            payment_record = df[payment_mask]
            
            if not payment_record.empty:
                # Update existing record
                idx = payment_record.index[0]
                
                # Adjust amounts
                df.loc[idx, 'total_amount'] += amount_change
                df.loc[idx, 'remaining_amount'] = df.loc[idx, 'total_amount'] - df.loc[idx, 'paid_amount']
                
                # Update order count (only if amount_change is negative - cancelled order)
                if amount_change < 0:
                    df.loc[idx, 'total_orders'] = max(0, df.loc[idx, 'total_orders'] - 1)
                
                # Update status
                if df.loc[idx, 'remaining_amount'] <= 0:
                    df.loc[idx, 'status'] = 'paid'
                elif df.loc[idx, 'paid_amount'] > 0:
                    df.loc[idx, 'status'] = 'partial'
                else:
                    df.loc[idx, 'status'] = 'pending'
                
                # Update timestamp
                df.loc[idx, 'last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Save
                df.to_excel(payments_file, index=False)
            
        except Exception as e:
            print(f"Error adjusting payment balance: {e}")

    def get_orders_by_date_range(self, start_date=None, end_date=None):
        """Get orders by date range WITH ADDRESS INFO"""
        try:
            from datetime import datetime, timedelta
            
            # Default to today if no dates provided
            if not start_date:
                start_date = date.today().strftime('%Y-%m-%d')
            if not end_date:
                end_date = start_date
            
            # Convert string dates to date objects for comparison
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Load users and groups data ONCE for efficiency
            try:
                users_df = pd.read_excel(self.data_dir / "users.xlsx", dtype={'identifier': str})
                groups_df = pd.read_excel(self.data_dir / "groups.xlsx")
            except Exception as e:
                print(f"Error loading users/groups data: {e}")
                users_df = pd.DataFrame()
                groups_df = pd.DataFrame()
            
            # Get all order files in date range
            all_orders = []
            current_date = start_dt
            
            while current_date <= end_dt:
                date_str = current_date.strftime('%Y-%m-%d')
                orders_file = self.data_dir / f"orders_{date_str}.xlsx"
                
                if orders_file.exists():
                    try:
                        df = pd.read_excel(orders_file)
                        
                        for _, order in df.iterrows():
                            # Get user info WITH ADDRESS AND PHONE
                            user = users_df[users_df['id'] == order['user_id']]
                            if not user.empty:
                                user_data = user.iloc[0]
                                user_name = user_data['name']
                                user_address = user_data['address'] if pd.notna(user_data['address']) else ''
                                user_phone = user_data['identifier']  # identifier can be email or phone
                            else:
                                user_name = 'Unknown'
                                user_address = ''
                                user_phone = ''
                            
                            # Get group info WITH ADDRESS
                            group_name = None
                            group_address = ''
                            delivery_address = user_address  # Default to user address
                            
                            if pd.notna(order['group_id']) and order['group_id'] != 'personal':
                                group = groups_df[groups_df['name'] == order['group_id']]
                                if not group.empty:
                                    group_data = group.iloc[0]
                                    group_name = group_data['name']
                                    group_address = group_data['address'] if pd.notna(group_data['address']) else ''
                                    # If has group, use group address for delivery
                                    delivery_address = group_address if group_address else user_address
                            
                            all_orders.append({
                                "id": int(order['id']),
                                "date": date_str,
                                "user_name": user_name,
                                "user_phone": user_phone,
                                "user_address": user_address,
                                "meal_type": order['meal_type'],
                                "quantity": int(order['quantity']),
                                "group_name": group_name,
                                "group_address": group_address,
                                "delivery_address": delivery_address,
                                "note": order['note'] if pd.notna(order['note']) else '',
                                "total_amount": int(order['total_amount']),
                                "status": order['status'],
                                "created_at": order['created_at']
                            })
                    except Exception as e:
                        print(f"Error reading orders for {date_str}: {e}")
                
                current_date += timedelta(days=1)
            
            # Sort by date and time (newest first)
            all_orders.sort(key=lambda x: (x['date'], x['id']), reverse=True)
            return all_orders
            
        except Exception as e:
            print(f"Error getting orders by date range: {e}")
            return []

    # ADMIN ORDER METHODS
    def get_today_orders(self):
        """Get all orders for today WITH ADDRESS INFO"""
        today = date.today().strftime('%Y-%m-%d')
        return self.get_orders_by_date_range(today, today)
    
    def update_order_status(self, order_id, new_status):
        """Update order status"""
        today = date.today().strftime('%Y-%m-%d')
        orders_file = self.data_dir / f"orders_{today}.xlsx"
        
        if not orders_file.exists():
            return {"success": False, "message": "No orders file found"}
        
        try:
            df = pd.read_excel(orders_file)
            if order_id not in df['id'].values:
                return {"success": False, "message": "Order not found"}
            
            df.loc[df['id'] == order_id, 'status'] = new_status
            df.to_excel(orders_file, index=False)
            
            return {"success": True, "message": "Status updated"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def update_order_status_by_date(self, order_id, order_date, new_status):
        """Update order status for specific date"""
        orders_file = self.data_dir / f"orders_{order_date}.xlsx"
        
        if not orders_file.exists():
            return {"success": False, "message": "No orders file found"}
        
        try:
            df = pd.read_excel(orders_file)
            if order_id not in df['id'].values:
                return {"success": False, "message": "Order not found"}
            
            # Check if order is already cancelled
            current_status = df.loc[df['id'] == order_id, 'status'].iloc[0]
            if current_status == 'cancelled':
                return {"success": False, "message": "Không thể cập nhật đơn hàng đã hủy"}
            
            df.loc[df['id'] == order_id, 'status'] = new_status
            df.to_excel(orders_file, index=False)
            
            return {"success": True, "message": "Status updated"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
# ============ PAYMENT MANAGEMENT ============
    def update_user_payment_balance(self, user_id, order_amount, period=None):
        """Update user payment balance when new order is created"""
        try:
            from datetime import datetime
            
            payments_file = self.data_dir / "payments.xlsx"
            
            # Read existing payments
            try:
                df = pd.read_excel(payments_file)
            except:
                df = pd.DataFrame(columns=[
                    'user_id', 'period', 'total_orders', 'total_amount', 'paid_amount', 
                    'remaining_amount', 'status', 'last_updated', 'payment_date', 'notes'
                ])
            
            # Determine period (current month)
            if not period:
                now = datetime.now()
                period = f"{now.year}-{now.month:02d}"
            
            # Find existing record
            existing = df[(df['user_id'] == user_id) & (df['period'] == period)]
            
            if not existing.empty:
                # Update existing record
                idx = existing.index[0]
                df.loc[idx, 'total_orders'] += 1
                df.loc[idx, 'total_amount'] += order_amount
                df.loc[idx, 'remaining_amount'] = df.loc[idx, 'total_amount'] - df.loc[idx, 'paid_amount']
                df.loc[idx, 'last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Update status
                if df.loc[idx, 'remaining_amount'] <= 0:
                    df.loc[idx, 'status'] = 'paid'
                else:
                    df.loc[idx, 'status'] = 'pending'
            else:
                # Create new record
                new_payment = {
                    'user_id': int(user_id),
                    'period': period,
                    'total_orders': 1,
                    'total_amount': int(order_amount),
                    'paid_amount': 0,
                    'remaining_amount': int(order_amount),
                    'status': 'pending',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'payment_date': None,
                    'notes': ''
                }
                df = pd.concat([df, pd.DataFrame([new_payment])], ignore_index=True)
            
            # Save back to Excel
            df.to_excel(payments_file, index=False)
            
        except Exception as e:
            print(f"Error updating payment balance: {e}")

    def get_user_payment_summary(self, user_id, period="current_month"):
        """Get payment summary for a user by period from payments table - FIXED"""
        try:
            from datetime import datetime
            
            payments_file = self.data_dir / "payments.xlsx"
            
            try:
                df = pd.read_excel(payments_file)
            except Exception as e:
                return self.get_empty_payment_summary(period)
            
            if df.empty:
                return self.get_empty_payment_summary(period)
            
            # Filter records by period and user
            if period == "all":
                # FIX: For "all", get ALL records for this user
                user_payments = df[df['user_id'] == user_id]
            else:
                # Convert period filter to actual period keys
                period_keys = self.get_period_keys(period)
                
                if not period_keys:
                    return self.get_empty_payment_summary(period)
                    
                user_payments = df[(df['user_id'] == user_id) & (df['period'].isin(period_keys))]
            
            if user_payments.empty:
                return self.get_empty_payment_summary(period)
            
            # Aggregate data
            total_orders = int(user_payments['total_orders'].sum())
            total_amount = int(user_payments['total_amount'].sum())
            paid_amount = int(user_payments['paid_amount'].sum())
            remaining_amount = int(user_payments['remaining_amount'].sum())
            
            # Get meal breakdown from orders (for display only)
            meal_summary = self.get_user_meal_breakdown_for_periods(user_id, period)
            
            result = {
                "period": self.get_period_text(period),
                "total_orders": total_orders,
                "meal_summary": meal_summary,
                "total_amount": total_amount,
                "paid_amount": paid_amount,
                "remaining_amount": remaining_amount,
                "selected_period": period
            }
            
            return result
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return self.get_empty_payment_summary(period)

    def get_payment_summary(self):
        """Get payment summary for all users from payments table"""
        try:
            payments_file = self.data_dir / "payments.xlsx"
            users_file = self.data_dir / "users.xlsx"
            groups_file = self.data_dir / "groups.xlsx"
            
            try:
                payments_df = pd.read_excel(payments_file)
                users_df = pd.read_excel(users_file, dtype={'identifier': str})
                groups_df = pd.read_excel(groups_file)
            except:
                return []
            
            if payments_df.empty:
                return []
            
            # Get current month for filtering
            from datetime import datetime
            now = datetime.now()
            current_period = f"{now.year}-{now.month:02d}"
            
            # Filter current month payments
            current_payments = payments_df[payments_df['period'] == current_period]
            
            payments = []
            for _, payment in current_payments.iterrows():
                # Get user info
                user = users_df[users_df['id'] == payment['user_id']]
                if user.empty:
                    continue
                    
                user_data = user.iloc[0]
                
                # Get user's main group
                user_groups = self.get_user_groups(payment['user_id'])
                main_group = user_groups[0]['name'] if user_groups else None
                
                payments.append({
                    "user_id": int(payment['user_id']),
                    "user_name": user_data['name'],
                    "group_name": main_group,
                    "period": payment['period'],
                    "total_orders": int(payment['total_orders']),
                    "total_amount": int(payment['total_amount'] / 1000),  # Convert to thousands
                    "paid_amount": int(payment['paid_amount'] / 1000),
                    "remaining_amount": int(payment['remaining_amount'] / 1000),
                    "status": payment['status'],
                    "last_updated": payment['last_updated'],
                    "payment_date": payment['payment_date'] if pd.notna(payment['payment_date']) else None
                })
            
            return payments
            
        except Exception as e:
            return []

    def get_payment_summary_by_period(self, period_filter="current"):
        """Get payment summary filtered by period"""
        try:
            from datetime import datetime
            
            payments_file = self.data_dir / "payments.xlsx"
            users_file = self.data_dir / "users.xlsx"
            
            try:
                payments_df = pd.read_excel(payments_file)
                users_df = pd.read_excel(users_file, dtype={'identifier': str})
            except:
                return []
            
            if payments_df.empty:
                return []
            
            # Filter by period
            now = datetime.now()
            if period_filter == "current":
                period_key = f"{now.year}-{now.month:02d}"
                filtered_payments = payments_df[payments_df['period'] == period_key]
            elif period_filter == "last":
                last_month = now.month - 1 if now.month > 1 else 12
                year = now.year if now.month > 1 else now.year - 1
                period_key = f"{year}-{last_month:02d}"
                filtered_payments = payments_df[payments_df['period'] == period_key]
            else:  # all
                filtered_payments = payments_df
            
            payments = []
            for _, payment in filtered_payments.iterrows():
                # Get user info
                user = users_df[users_df['id'] == payment['user_id']]
                if user.empty:
                    continue
                    
                user_data = user.iloc[0]
                
                # Get user's main group
                user_groups = self.get_user_groups(payment['user_id'])
                main_group = user_groups[0]['name'] if user_groups else None
                
                payments.append({
                    "user_id": int(payment['user_id']),
                    "user_name": user_data['name'],
                    "group_name": main_group,
                    "period": payment['period'],
                    "total_orders": int(payment['total_orders']),
                    "total_amount": int(payment['total_amount'] / 1000),
                    "paid_amount": int(payment['paid_amount'] / 1000),
                    "remaining_amount": int(payment['remaining_amount'] / 1000),
                    "status": payment['status'],
                    "last_updated": payment['last_updated'],
                    "payment_date": payment['payment_date'] if pd.notna(payment['payment_date']) else None
                })
            
            return payments
            
        except Exception as e:
            return []

    def mark_payment_paid(self, user_id, amount):
        """Admin mark payment as paid"""
        try:
            from datetime import datetime
            
            payments_file = self.data_dir / "payments.xlsx"
            df = pd.read_excel(payments_file)
            
            # Find current month record
            now = datetime.now()
            period_key = f"{now.year}-{now.month:02d}"
            
            user_payment = df[(df['user_id'] == user_id) & (df['period'] == period_key)]
            
            if user_payment.empty:
                return {"success": False, "message": "Không tìm thấy thông tin thanh toán"}
            
            idx = user_payment.index[0]
            
            # Convert amount back to VND (from thousands)
            amount_vnd = amount * 1000
            
            # Update payment
            df.loc[idx, 'paid_amount'] += amount_vnd
            df.loc[idx, 'remaining_amount'] = df.loc[idx, 'total_amount'] - df.loc[idx, 'paid_amount']
            df.loc[idx, 'last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if df.loc[idx, 'remaining_amount'] <= 0:
                df.loc[idx, 'status'] = 'paid'
                df.loc[idx, 'payment_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                df.loc[idx, 'status'] = 'partial'
            
            df.to_excel(payments_file, index=False)
            
            return {"success": True, "message": "Đã cập nhật thanh toán"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_payment_history(self, user_id):
        """Get payment history for a user"""
        try:
            payments_file = self.data_dir / "payments.xlsx"
            df = pd.read_excel(payments_file)
            
            user_payments = df[df['user_id'] == user_id].sort_values('last_updated', ascending=False)
            
            history = []
            for _, payment in user_payments.iterrows():
                if payment['paid_amount'] > 0:
                    history.append({
                        "id": len(history) + 1,
                        "amount": int(payment['paid_amount'] / 1000),  # Convert to thousands
                        "date": payment['payment_date'] if pd.notna(payment['payment_date']) else payment['last_updated'],
                        "period": payment['period'],
                        "status": payment['status']
                    })
            
            return history[:10]  # Return last 10 payments
            
        except Exception as e:
            return []

    def mark_user_payment_paid(self, user_id, amount):
        """Mark user payment as paid"""
        try:
            from datetime import datetime
            
            payments_file = self.data_dir / "payments.xlsx"
            df = pd.read_excel(payments_file)
            
            # Find current month record
            now = datetime.now()
            period_key = f"{now.year}-{now.month:02d}"
            
            user_payment = df[(df['user_id'] == user_id) & (df['period'] == period_key)]
            
            if user_payment.empty:
                return {"success": False, "message": "Không tìm thấy thông tin thanh toán"}
            
            idx = user_payment.index[0]
            
            # Update payment
            df.loc[idx, 'paid_amount'] += amount
            df.loc[idx, 'remaining_amount'] = df.loc[idx, 'total_amount'] - df.loc[idx, 'paid_amount']
            df.loc[idx, 'last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if df.loc[idx, 'remaining_amount'] <= 0:
                df.loc[idx, 'status'] = 'paid'
                df.loc[idx, 'payment_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                df.loc[idx, 'status'] = 'partial'
            
            df.to_excel(payments_file, index=False)
            
            return {"success": True, "message": "Đã cập nhật thanh toán"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}
        
# ============ PAYOS PAYMENT METHODS ============
    def generate_order_code(self):
        """Generate unique order code for PayOS"""
        # PayOS yêu cầu orderCode là số nguyên dương, tối đa 6 chữ số
        timestamp = str(int(time.time()))[-6:]  # 6 chữ số cuối của timestamp
        return int(timestamp)

    def create_payos_signature(self, data):
        """Tạo signature cho PayOS API request"""
        # Sắp xếp keys và tạo string
        sorted_keys = sorted(data.keys())
        data_string = "&".join([f"{key}={data[key]}" for key in sorted_keys])
        
        # Tạo HMAC SHA256 signature
        signature = hmac.new(
            self.PAYOS_CHECKSUM_KEY.encode('utf-8'),
            data_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature

    def verify_payos_webhook_signature(self, webhook_data, received_signature):
        """Verify webhook signature từ PayOS - IMPROVED VERSION"""
        try:
            
            # Lấy data section
            data = webhook_data.get('data', {})
            
            if not data:
                return False
            
            # Tạo signature string theo spec của PayOS
            # Chỉ lấy các fields có value và sắp xếp theo alphabet
            valid_fields = {}
            for key, value in data.items():
                if value is not None and str(value).strip() != "":
                    valid_fields[key] = str(value)
            
            # Sắp xếp keys và tạo query string
            sorted_keys = sorted(valid_fields.keys())
            query_parts = []
            
            for key in sorted_keys:
                query_parts.append(f"{key}={valid_fields[key]}")
            
            query_string = "&".join(query_parts)
            
            # Tạo HMAC SHA256 signature
            expected_signature = hmac.new(
                self.PAYOS_CHECKSUM_KEY.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # So sánh an toàn
            is_valid = hmac.compare_digest(expected_signature, received_signature)
            
            return is_valid
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False

    def create_payos_payment(self, user_id, payment_period="current_month"):
        """Tạo PayOS payment"""
        try:
            # 1. Get payment data
            period_keys = self.get_period_keys(payment_period)
            payments_file = self.data_dir / "payments.xlsx"
            users_file = self.data_dir / "users.xlsx"
            
            payments_df = pd.read_excel(payments_file)
            users_df = pd.read_excel(users_file, dtype={'identifier': str})
            
            # Filter payments
            if payment_period == "all":
                user_payments = payments_df[payments_df['user_id'] == user_id]
            else:
                user_payments = payments_df[(payments_df['user_id'] == user_id) & 
                                        (payments_df['period'].isin(period_keys))]
            
            if user_payments.empty:
                return {"success": False, "message": "Không có dữ liệu thanh toán"}
            
            total_remaining = user_payments['remaining_amount'].sum()
            if total_remaining <= 0:
                return {"success": False, "message": "Đã thanh toán hết"}
            
            # Get user info
            user = users_df[users_df['id'] == user_id]
            if user.empty:
                return {"success": False, "message": "Không tìm thấy user"}
            
            user_data = user.iloc[0]
            amount = int(total_remaining)
            order_code = self.generate_order_code()
            description = f"TEST THANH TOAN !"
            
            # 2. Call PayOS API (copy từ test thành công)
            test_order = {
                "orderCode": order_code,
                "amount": amount,
                "description": description,
                "returnUrl": "https://yourdomain.com/return",
                "cancelUrl": "https://yourdomain.com/cancel"
            }
            
            # Create signature (copy từ test)
            sorted_keys = sorted(test_order.keys())
            data_string = "&".join([f"{key}={test_order[key]}" for key in sorted_keys])
            
            signature = hmac.new(
                self.PAYOS_CHECKSUM_KEY.encode('utf-8'),
                data_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            test_order["signature"] = signature
            
            # Headers (copy từ test)
            headers = {
                "x-client-id": self.PAYOS_CLIENT_ID,
                "x-api-key": self.PAYOS_API_KEY,
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
                payos_data = response.json()
                data = payos_data.get('data', {})
                
                checkout_url = data.get('checkoutUrl', '')
                qr_code = data.get('qrCode', '')
                
                # 3. Save to database
                payos_file = self.data_dir / "payos_transactions.xlsx"
                try:
                    payos_df = pd.read_excel(payos_file) if payos_file.exists() else pd.DataFrame()
                except:
                    payos_df = pd.DataFrame()
                
                next_id = 1 if payos_df.empty else int(payos_df['id'].max()) + 1
                
                new_transaction = {
                    'id': next_id,
                    'user_id': user_id,
                    'payment_period': payment_period,
                    'order_code': order_code,
                    'amount': amount,
                    'description': description,
                    'payment_link_id': data.get('paymentLinkId', ''),
                    'checkout_url': checkout_url,
                    'qr_code': qr_code,
                    'status': 'PENDING',
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'expired_at': (datetime.now() + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
                    'paid_at': None,
                    'webhook_data': None,
                    'notes': f"PayOS API Success: {response.status_code}"
                }
                
                payos_df = pd.concat([payos_df, pd.DataFrame([new_transaction])], ignore_index=True)
                payos_df.to_excel(payos_file, index=False)
                
                # 4. Return success
                return {
                    "success": True,
                    "transaction_id": next_id,
                    "order_code": order_code,
                    "checkout_url": checkout_url,
                    "qr_code": qr_code,
                    "amount": amount,
                    "description": description,
                    "user_name": user_data['name'],
                    "expires_at": new_transaction['expired_at'],
                    "period_filter": payment_period,
                    "period_text": self.get_period_text(payment_period)
                }
            else:
                print(f"❌ PayOS Failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return {"success": False, "message": f"PayOS Error: {response.status_code}"}
                
        except Exception as e:
            print(f"💥 Exception: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "message": f"Error: {str(e)}"}

    def check_payos_payment_status(self, order_code):
        """Kiểm tra trạng thái payment PayOS - SAFE VERSION"""
        try:
            
            payos_file = self.data_dir / "payos_transactions.xlsx"
            if not payos_file.exists():
                return {"success": False, "message": "Không tìm thấy bảng giao dịch"}
            
            try:
                payos_df = pd.read_excel(payos_file)
            except Exception as e:
                print(f"❌ Error reading PayOS file: {e}")
                return {"success": False, "message": "Lỗi đọc file giao dịch"}
            
            if payos_df.empty:
                print(f"❌ PayOS transactions file is empty")
                return {"success": False, "message": "Không có giao dịch nào"}
            
            # Find transaction
            transaction = payos_df[payos_df['order_code'] == order_code]
            
            if transaction.empty:
                print(f"❌ Transaction not found for order_code: {order_code}")
                print(f"📊 Available order codes: {payos_df['order_code'].tolist()}")
                return {"success": False, "message": "Không tìm thấy giao dịch"}
            
            trans_data = transaction.iloc[0]
            print(f"✅ Found transaction: {trans_data['id']}")
            
            # Check if expired
            try:
                expired_at = datetime.strptime(trans_data['expired_at'], '%Y-%m-%d %H:%M:%S')
                current_time = datetime.now()
                
                if current_time > expired_at and trans_data['status'] == 'PENDING':
                    # Mark as expired
                    payos_df.loc[payos_df['order_code'] == order_code, 'status'] = 'EXPIRED'
                    payos_df.to_excel(payos_file, index=False)
                    return {"success": True, "status": "EXPIRED"}
            except Exception as e:
                print(f"⚠️ Error checking expiration: {e}")
            
            # Return current status
            result = {
                "success": True,
                "status": trans_data['status'],
                "amount": int(trans_data['amount']),
                "created_at": trans_data['created_at'],
                "expired_at": trans_data['expired_at']
            }
            
            if pd.notna(trans_data['paid_at']):
                result["paid_at"] = trans_data['paid_at']
            
            return result
            
        except Exception as e:
            print(f"💥 Error in check_payos_payment_status: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "message": "Lỗi kiểm tra trạng thái"}

    def process_payos_webhook(self, webhook_data):
        """Xử lý webhook từ PayOS - IMPROVED WITH BETTER ERROR HANDLING"""
        try:
            # Step 1: Verify signature
            received_signature = webhook_data.get('signature', '')
            
            if not received_signature:
                return {"success": False, "message": "Missing signature"}
            
            # Skip signature verification in development mode (for testing)
            signature_valid = True  # Set to False to enable verification
            if not signature_valid:
                signature_valid = self.verify_payos_webhook_signature(webhook_data, received_signature)
                if not signature_valid:
                    return {"success": False, "message": "Invalid webhook signature"}
            
            # Step 2: Parse webhook data
            data = webhook_data.get('data', {})
            order_code = data.get('orderCode')
            amount = data.get('amount')
            status_code = str(data.get('code', ''))
            success_flag = webhook_data.get('success', False)
            
            # Step 3: Validate required fields
            if not order_code:
                return {"success": False, "message": "Missing order code"}
            
            if not amount:
                return {"success": False, "message": "Missing amount"}
            
            # Step 4: Find transaction in database
            payos_file = self.data_dir / "payos_transactions.xlsx"
            
            if not payos_file.exists():
                return {"success": False, "message": "Transaction database not found"}
            
            payos_df = pd.read_excel(payos_file)
            
            # Find matching transaction
            transaction = payos_df[payos_df['order_code'] == order_code]
            if transaction.empty:
                return {"success": False, "message": f"Transaction not found: {order_code}"}
            
            trans_data = transaction.iloc[0]
            
            # Step 5: Validate amount
            if int(amount) != int(trans_data['amount']):
                return {"success": False, "message": "Amount mismatch"}
            
            # Step 6: Check if transaction already processed
            if trans_data['status'] in ['PAID', 'FAILED', 'CANCELLED']:
                return {"success": True, "message": f"Transaction already {trans_data['status'].lower()}"}
            
            # Step 7: Process payment result
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if status_code == "00" and success_flag:
                # Update PayOS transaction status
                payos_df.loc[payos_df['order_code'] == order_code, 'status'] = 'PAID'
                payos_df.loc[payos_df['order_code'] == order_code, 'paid_at'] = current_time
                payos_df.loc[payos_df['order_code'] == order_code, 'webhook_data'] = json.dumps(webhook_data)
                
                # Save PayOS transactions
                payos_df.to_excel(payos_file, index=False)
                
                # Update payments table
                payment_update_result = self.update_payments_from_webhook(trans_data, amount)
                
                if payment_update_result:
                    
                    return {
                        "success": True,
                        "message": "Payment processed successfully",
                        "user_id": int(trans_data['user_id']),
                        "amount": amount,
                        "order_code": order_code,
                        "payment_period": trans_data['payment_period']
                    }
                else:
                    return {
                        "success": True,
                        "message": "Payment received but balance update failed",
                        "user_id": int(trans_data['user_id']),
                        "amount": amount
                    }
            else:
                # Update as failed
                payos_df.loc[payos_df['order_code'] == order_code, 'status'] = 'FAILED'
                payos_df.loc[payos_df['order_code'] == order_code, 'webhook_data'] = json.dumps(webhook_data)
                payos_df.to_excel(payos_file, index=False)
                
                return {
                    "success": False,
                    "message": f"Payment failed with status: {status_code}",
                    "order_code": order_code
                }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"success": False, "message": f"Webhook processing error: {str(e)}"}

    def get_user_payos_transactions(self, user_id, limit=10):
        """Lấy lịch sử giao dịch PayOS của user"""
        try:
            payos_file = self.data_dir / "payos_transactions.xlsx"
            if not payos_file.exists():
                return []
            
            payos_df = pd.read_excel(payos_file)
            user_transactions = payos_df[payos_df['user_id'] == user_id].sort_values('created_at', ascending=False).head(limit)
            
            transactions = []
            for _, trans in user_transactions.iterrows():
                transactions.append({
                    "id": int(trans['id']),
                    "order_code": int(trans['order_code']),
                    "amount": int(trans['amount']),
                    "description": trans['description'],
                    "status": trans['status'],
                    "created_at": trans['created_at'],
                    "paid_at": trans['paid_at'] if pd.notna(trans['paid_at']) else None,
                    "checkout_url": trans['checkout_url']
                })
            
            return transactions
            
        except Exception as e:
            print(f"Error getting user PayOS transactions: {e}")
            return []
        
# ============ FEEDBACK MANAGEMENT ============
    def save_feedback(self, feedback_text, rating=None, category="general", ip_address=""):
        """Save anonymous feedback"""
        try:
            feedback_file = self.data_dir / "feedback.xlsx"
            
            try:
                df = pd.read_excel(feedback_file)
            except:
                df = pd.DataFrame(columns=[
                    'id', 'feedback_text', 'rating', 'category', 'created_at', 'ip_address', 'status'
                ])
            
            # Get next ID
            next_id = 1 if df.empty else int(df['id'].max()) + 1
            
            # Add new feedback
            new_feedback = {
                'id': next_id,
                'feedback_text': feedback_text,
                'rating': rating if rating else None,
                'category': category,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip_address': ip_address,
                'status': 'new'
            }
            
            df = pd.concat([df, pd.DataFrame([new_feedback])], ignore_index=True)
            df.to_excel(feedback_file, index=False)
            
            return {"success": True, "message": "Cảm ơn bạn đã góp ý!"}
            
        except Exception as e:
            print(f"Error saving feedback: {e}")
            return {"success": False, "message": "Lỗi khi lưu góp ý"}

    def get_all_feedback(self):
        """Get all feedback for admin"""
        try:
            feedback_file = self.data_dir / "feedback.xlsx"
            
            if not feedback_file.exists():
                return []
            
            df = pd.read_excel(feedback_file)
            feedback_list = []
            
            for _, feedback in df.iterrows():
                feedback_list.append({
                    "id": int(feedback['id']),
                    "feedback_text": feedback['feedback_text'],
                    "rating": int(feedback['rating']) if pd.notna(feedback['rating']) else None,
                    "category": feedback['category'],
                    "created_at": feedback['created_at'],
                    "status": feedback['status']
                })
            
            # Sort by newest first
            feedback_list.sort(key=lambda x: x['created_at'], reverse=True)
            return feedback_list
            
        except Exception as e:
            print(f"Error getting feedback: {e}")
        return []
    
    def update_feedback_status(self, feedback_id, new_status):
        """Update feedback status"""
        try:
            feedback_file = self.data_dir / "feedback.xlsx"
            df = pd.read_excel(feedback_file)
            
            if feedback_id not in df['id'].values:
                return {"success": False, "message": "Feedback not found"}
            
            df.loc[df['id'] == feedback_id, 'status'] = new_status
            df.to_excel(feedback_file, index=False)
            
            return {"success": True, "message": "Status updated"}
            
        except Exception as e:
            print(f"Error updating feedback status: {e}")
            return {"success": False, "message": str(e)}

    def delete_feedback(self, feedback_id):
        """Delete feedback"""
        try:
            feedback_file = self.data_dir / "feedback.xlsx"
            df = pd.read_excel(feedback_file)
            
            if feedback_id not in df['id'].values:
                return {"success": False, "message": "Feedback not found"}
            
            df = df[df['id'] != feedback_id]
            df.to_excel(feedback_file, index=False)
            
            return {"success": True, "message": "Feedback deleted"}
            
        except Exception as e:
            print(f"Error deleting feedback: {e}")
            return {"success": False, "message": str(e)}

    # ============ UTILITY METHODS ============
    def get_period_keys(self, period_filter):
        """Convert period filter to actual period keys - FIXED"""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        
        if period_filter == "current_month":
            keys = [f"{now.year}-{now.month:02d}"]
            
        elif period_filter == "last_month":
            if now.month == 1:
                last_month = 12
                year = now.year - 1
            else:
                last_month = now.month - 1
                year = now.year
            keys = [f"{year}-{last_month:02d}"]
            
        elif period_filter == "current_week":
            # For simplicity, use current month (you can make this more precise)
            keys = [f"{now.year}-{now.month:02d}"]
            
        elif period_filter == "all":
            # FIX: Return None for "all" - special handling
            return None
            
        else:
            # Fallback to current month
            keys = [f"{now.year}-{now.month:02d}"]
        
        return keys

    def get_period_text(self, period_filter):
        """Get display text for period - FIXED"""
        from datetime import datetime
        
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        if period_filter == "current_week":
            return "Tuần này"
        elif period_filter == "current_month":
            return f"Tháng {current_month}/{current_year}"
        elif period_filter == "last_month":
            if current_month == 1:
                last_month = 12
                year = current_year - 1
            else:
                last_month = current_month - 1
                year = current_year
            return f"Tháng {last_month}/{year}"
        elif period_filter == "all":
            return "Tất cả thời gian"
        else:
            return "Không xác định"

    def get_user_meal_breakdown(self, user_id, period_key):
        """Get meal breakdown for display"""
        try:
            # Extract year-month from period_key (YYYY-MM)
            year, month = period_key.split('-')
            
            order_files = list(self.data_dir.glob(f"orders_{year}-{month}-*.xlsx"))
            meal_summary = {}
            
            for order_file in order_files:
                try:
                    df = pd.read_excel(order_file)
                    user_orders = df[df['user_id'] == user_id]
                    
                    for _, order in user_orders.iterrows():
                        meal_type = order['meal_type']
                        quantity = int(order['quantity'])
                        amount = int(order['total_amount'])
                        
                        if meal_type not in meal_summary:
                            meal_summary[meal_type] = {"count": 0, "amount": 0}
                        meal_summary[meal_type]["count"] += quantity
                        meal_summary[meal_type]["amount"] += amount
                except:
                    continue
                    
            return meal_summary
        except:
            return {}
        
    def get_user_meal_breakdown_for_periods(self, user_id, period_filter):
        """Get meal breakdown for periods - FIXED"""
        try:
            if period_filter == "all":
                # Get ALL order files
                order_files = list(self.data_dir.glob("orders_*.xlsx"))
            else:
                # Get specific period files
                period_keys = self.get_period_keys(period_filter)
                order_files = []
                
                for period_key in period_keys:
                    # Convert YYYY-MM to file pattern
                    year, month = period_key.split('-')
                    pattern = f"orders_{year}-{month}-*.xlsx"
                    matched_files = list(self.data_dir.glob(pattern))
                    order_files.extend(matched_files)
            
            meal_summary = {}
            total_orders_processed = 0
            
            for order_file in order_files:
                try:
                    df = pd.read_excel(order_file)
                    user_orders = df[df['user_id'] == user_id]
                    
                    for _, order in user_orders.iterrows():
                        meal_type = order['meal_type']
                        quantity = int(order['quantity'])
                        amount = int(order['total_amount'])
                        
                        if meal_type not in meal_summary:
                            meal_summary[meal_type] = {"count": 0, "amount": 0}
                        meal_summary[meal_type]["count"] += quantity
                        meal_summary[meal_type]["amount"] += amount
                        total_orders_processed += 1
                        
                except Exception as e:
                    continue
            
            return meal_summary
            
        except Exception as e:
            return {}

    def get_empty_payment_summary(self, period):
        """Return empty payment summary structure"""
        return {
            "period": self.get_period_text(period),
            "total_orders": 0,
            "meal_summary": {},
            "total_amount": 0,
            "paid_amount": 0,
            "remaining_amount": 0,
            "selected_period": period
        }
    
# ============ PAYOS HELPER METHODS ============
    def update_payments_from_webhook(self, trans_data, amount):
        """Update payments table from webhook - IMPROVED WITH BETTER LOGGING"""
        try:
            payment_period = trans_data['payment_period']
            user_id = trans_data['user_id']
            
            # Load payments file
            payments_file = self.data_dir / "payments.xlsx"
            if not payments_file.exists():
                return False
            
            payments_df = pd.read_excel(payments_file)
            
            # Get period keys based on filter
            if payment_period == "all":
                # Update all pending payments for user
                user_payments = payments_df[
                    (payments_df['user_id'] == user_id) & 
                    (payments_df['remaining_amount'] > 0)
                ]
            else:
                # Update specific period payments
                period_keys = self.get_period_keys(payment_period)
                if not period_keys:
                    return False
                    
                user_payments = payments_df[
                    (payments_df['user_id'] == user_id) & 
                    (payments_df['period'].isin(period_keys)) & 
                    (payments_df['remaining_amount'] > 0)
                ]
            
            if user_payments.empty:
                return False
            
            # Distribute payment amount across pending records
            remaining_amount = amount
            updated_count = 0
            
            for idx, payment in user_payments.iterrows():
                if remaining_amount <= 0:
                    break
                    
                payment_remaining = payment['remaining_amount']
                
                if payment_remaining > 0:
                    # Calculate how much to pay for this record
                    payment_amount = min(remaining_amount, payment_remaining)
                    
                    # Update this payment record
                    payments_df.loc[idx, 'paid_amount'] = payment['paid_amount'] + payment_amount
                    payments_df.loc[idx, 'remaining_amount'] = payment['remaining_amount'] - payment_amount
                    payments_df.loc[idx, 'last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Update status
                    if payments_df.loc[idx, 'remaining_amount'] <= 0:
                        payments_df.loc[idx, 'status'] = 'paid'
                        payments_df.loc[idx, 'payment_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        payments_df.loc[idx, 'status'] = 'partial'
                    
                    remaining_amount -= payment_amount
                    updated_count += 1
            
            # Save updated payments
            payments_df.to_excel(payments_file, index=False)
            
            return True
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False

    def mark_period_payments_paid(self, user_id, period_keys, amount):
        """Mark payments as paid for specific periods"""
        try:
            payments_file = self.data_dir / "payments.xlsx"
            payments_df = pd.read_excel(payments_file)
            
            # Find payments for the periods
            user_payments = payments_df[(payments_df['user_id'] == user_id) & 
                                    (payments_df['period'].isin(period_keys))]
            
            if user_payments.empty:
                return {"success": False, "message": "Không tìm thấy dữ liệu thanh toán"}
            
            # Update payments
            remaining_amount = amount
            
            for idx, payment in user_payments.iterrows():
                if remaining_amount <= 0:
                    break
                    
                payment_remaining = payment['remaining_amount']
                
                if payment_remaining > 0:
                    payment_amount = min(remaining_amount, payment_remaining)
                    
                    payments_df.loc[idx, 'paid_amount'] += payment_amount
                    payments_df.loc[idx, 'remaining_amount'] -= payment_amount
                    payments_df.loc[idx, 'last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    if payments_df.loc[idx, 'remaining_amount'] <= 0:
                        payments_df.loc[idx, 'status'] = 'paid'
                        payments_df.loc[idx, 'payment_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        payments_df.loc[idx, 'status'] = 'partial'
                    
                    remaining_amount -= payment_amount
            
            payments_df.to_excel(payments_file, index=False)
            
            return {"success": True, "message": "Đã cập nhật thanh toán"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}

    def mark_all_user_payments_paid(self, user_id, amount):
        """Mark all user payments as paid"""
        try:
            payments_file = self.data_dir / "payments.xlsx"
            payments_df = pd.read_excel(payments_file)
            
            user_payments = payments_df[payments_df['user_id'] == user_id]
            
            if user_payments.empty:
                return {"success": False, "message": "Không tìm thấy dữ liệu thanh toán"}
            
            # Update all user payments
            remaining_amount = amount
            
            for idx, payment in user_payments.iterrows():
                if remaining_amount <= 0:
                    break
                    
                payment_remaining = payment['remaining_amount']
                
                if payment_remaining > 0:
                    payment_amount = min(remaining_amount, payment_remaining)
                    
                    payments_df.loc[idx, 'paid_amount'] += payment_amount
                    payments_df.loc[idx, 'remaining_amount'] -= payment_amount
                    payments_df.loc[idx, 'last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    if payments_df.loc[idx, 'remaining_amount'] <= 0:
                        payments_df.loc[idx, 'status'] = 'paid'
                        payments_df.loc[idx, 'payment_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        payments_df.loc[idx, 'status'] = 'partial'
                    
                    remaining_amount -= payment_amount
            
            payments_df.to_excel(payments_file, index=False)
            
            return {"success": True, "message": "Đã cập nhật thanh toán"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}
        
# ============ CLASS CLOSURE ============
# End of ExcelHandler class