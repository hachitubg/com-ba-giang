import { API_CONFIG } from '../../config/api.js'
const API_BASE_URL = API_CONFIG.BASE_URL

export default {
  name: 'HomePage',
  data() {
    return {
      // UI State
      showUserMenu: false,
      
      // Menu Data
      today: '',
      deadline: '',
      menuItems: [],
      availableToppings: '',
      
      // Auth Data
      isLoggedIn: false,
      showRegister: false,
      currentUser: { 
        name: '', 
        identifier: '', 
        groups: [] 
      },
      loginData: { 
        identifier: '', 
        password: '' 
      },
      registerData: { 
        name: '', 
        identifier: '', 
        password: '', 
        address: '' 
      },

      // User Info Modal
      showUserInfoModal: false,
      userInfoData: {
        name: '',
        address: '',
        created_at: '',
      },
      isUpdatingUserInfo: false,
      
      // Modal States
      showOrderModal: false,
      showGroupModal: false,
      groupTab: 'join',
      orderType: 'personal',
      mealType: '',
      quantity: 1,
      note: '',
      
      // Group Data
      joinGroupCode: '',
      newGroup: { 
        name: '', 
        address: '', 
        description: '' 
      },

      // Order History
      showOrderHistory: false,
      orderHistory: [],
      filteredOrderHistory: [],
      historyTimeFilter: 'all',
      historyStatusFilter: 'all',

      // Payment Summary
      showPaymentSummary: false,
      paymentSummary: {
        period: 'Tất cả thời gian',
        total_orders: 0,
        meal_summary: {},
        total_amount: 0,
        paid_amount: 0,
        remaining_amount: 0,
        selected_period: 'all'
      },
      paymentPeriod: 'all',
      selectedPaymentPeriod: 'all',
      showMealDetails: false,
      qrCodeGenerated: false,

      // Feedback
      showFeedbackModal: false,
      feedbackData: {
        text: '',
        rating: 0,
        category: 'general'
      },
      hoverRating: 0,

      // Edit Order
      showEditOrderModal: false,
      editingOrder: {},
      editOrderData: {
        meal_type: '',
        quantity: 1,
        note: ''
      },

      // PayOS Payment
      showPayOSModal: false,
      payosPaymentData: {
        transaction_id: null,
        order_code: null,
        checkout_url: '',
        qr_code: '',
        amount: 0,
        description: '',
        user_name: '',
        expires_at: '',
        status: 'PENDING'
      },
      payosStatusCheckInterval: null,
      payosCountdownInterval: null,
      payosTimeRemaining: 0,
      isLoadingPayOS: false,
      showQRCode: true,

      // PayOS Config
      payosConfig: {
        provider: "payos",
        supports: ["banking", "e_wallet", "qr_code", "payment_link"],
        timeout_minutes: 30
      },
      
      // System Notification
      systemNotification: {
        show: false,
        message: '',
        type: 'info',
        timestamp: 0
      }
    }
  },
  
  computed: {
    totalAmount() {
      const selectedItem = this.menuItems.find(item => item.name === this.mealType);
      const price = selectedItem ? selectedItem.price : 0;
      return price * this.quantity;
    }
  },

  methods: {
    // ============ HELPER METHODS ============
    getItemHeaderClass(index) {
      const colors = ['bg-blue-50', 'bg-green-50', 'bg-purple-50'];
      return colors[index % colors.length];
    },
    
    getItemPriceClass(index) {
      const colors = ['text-blue-600', 'text-green-600', 'text-purple-600'];
      return colors[index % colors.length];
    },

    getItemGradientClass(index) {
      const gradients = [
        'bg-gradient-to-br from-blue-500 to-indigo-600',
        'bg-gradient-to-br from-green-500 to-emerald-600', 
        'bg-gradient-to-br from-purple-500 to-violet-600',
        'bg-gradient-to-br from-orange-500 to-red-600',
        'bg-gradient-to-br from-pink-500 to-rose-600'
      ];
      return gradients[index % gradients.length];
    },

    getItemButtonClass(index) {
      const classes = [
        'bg-blue-500 hover:bg-blue-600 text-white',
        'bg-green-500 hover:bg-green-600 text-white',
        'bg-purple-500 hover:bg-purple-600 text-white', 
        'bg-orange-500 hover:bg-orange-600 text-white',
        'bg-pink-500 hover:bg-pink-600 text-white'
      ];
      return classes[index % classes.length];
    },
    
    formatPrice(price) {
      if (!price) return '0đ';
      return price.toLocaleString() + 'đ';
    },

    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('vi-VN', {
        weekday: 'short',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    },

    getStatusText(status) {
      const statusMap = {
        'pending': 'Đã đặt',
        'preparing': 'Đang giao', 
        'completed': 'Hoàn thành',
        'cancelled': 'Đã hủy'
      };
      return statusMap[status] || status;
    },

    getOrderStatusClass(status) {
      switch(status) {
        case 'pending': return 'bg-yellow-50 border-yellow-200';
        case 'preparing': return 'bg-blue-50 border-blue-200';
        case 'completed': return 'bg-green-50 border-green-200';
        case 'cancelled': return 'bg-red-50 border-red-200';
        default: return 'bg-gray-50 border-gray-200';
      }
    },

    getPeriodText(period) {
      const now = new Date();
      const currentMonth = now.getMonth() + 1;
      const currentYear = now.getFullYear();
      const lastMonth = currentMonth === 1 ? 12 : currentMonth - 1;
      const lastYear = currentMonth === 1 ? currentYear - 1 : currentYear;

      const periodMap = {
        'current_week': 'Tuần này',
        'current_month': `Tháng ${currentMonth}/${currentYear}`,
        'last_month': `Tháng ${lastMonth}/${lastYear}`,
        'all': 'Tất cả thời gian'
      };
      return periodMap[period] || 'Không xác định';
    },

    formatPayOSCountdown(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },

    // ============ MENU & DATA LOADING ============
    async loadTodayMenu() {
      try {
        const response = await fetch(`${API_BASE_URL}/menu/today`);
        const menu = await response.json();
        
        this.today = new Date(menu.date).toLocaleDateString('vi-VN', {
          weekday: 'long',
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        });
        this.deadline = menu.deadline;
        this.menuItems = menu.menu_items || [];
        this.availableToppings = menu.toppings;
        
        if (this.menuItems.length > 0) {
          this.mealType = this.menuItems[0].name;
        }
      } catch (error) {
        console.error('Load menu error:', error);
        this.today = new Date().toLocaleDateString('vi-VN');
        this.deadline = '10:00';
        this.menuItems = [
          { name: 'Suất tiêu chuẩn', price: 35000, description: 'Đang cập nhật menu...' },
          { name: 'Suất cao cấp', price: 40000, description: 'Đang cập nhật menu...' }
        ];
        this.availableToppings = 'Đang cập nhật...';
        this.mealType = this.menuItems[0].name;
      }
    },

    async refreshUserData() {
      if (!this.currentUser.id) return;
      
      try {
        const response = await fetch(`http://127.0.0.1:8000/users/${this.currentUser.id}/groups`);
        const result = await response.json();
        
        this.currentUser.groups = result.groups;
        
        const userDataToSave = {
          ...this.currentUser,
          loginTime: new Date().getTime()
        };
        localStorage.setItem('combagiang_user', JSON.stringify(userDataToSave));
      } catch (error) {
        console.error('Refresh user data error:', error);
      }
    },

    async loadUserInfoFromServer() {
      if (!this.currentUser.id) return;

      try {
        const response = await fetch(`http://127.0.0.1:8000/users/${this.currentUser.id}/info`);
        const result = await response.json();

        if (result.success) {
          this.currentUser = {
            ...this.currentUser,
            ...result.user
          };

          const userDataToSave = {
            ...this.currentUser,
            loginTime: new Date().getTime()
          };
          localStorage.setItem('combagiang_user', JSON.stringify(userDataToSave));
        }
      } catch (error) {
        console.error('Load user info error:', error);
      }
    },

    async loadPayOSConfig() {
      try {
        const response = await fetch(`${API_BASE_URL}/payments/payos-config`);
        const config = await response.json();
        this.payosConfig = config;
      } catch (error) {
        this.payosConfig = {
          provider: "payos",
          supports: ["banking", "e_wallet", "qr_code", "payment_link"],
          timeout_minutes: 30
        };
      }
    },

    // ============ AUTHENTICATION ============
    async login() {
      if (!this.loginData.identifier || !this.loginData.password) {
        this.showSystemNotification('Vui lòng nhập đầy đủ thông tin!', 'info');
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.loginData)
        });

        const result = await response.json();
        
        if (result.success) {
          this.currentUser = result.user;
          this.isLoggedIn = true;
          
          const userDataToSave = {
            ...result.user,
            loginTime: new Date().getTime()
          };
          localStorage.setItem('combagiang_user', JSON.stringify(userDataToSave));
        } else {
          this.showSystemNotification(result.message || 'Đăng nhập thất bại!', 'error');
        }
      } catch (error) {
        console.error('Login error:', error);
        this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
      }
    },

    async register() {
      if (!this.registerData.name || !this.registerData.identifier || !this.registerData.password) {
        this.showSystemNotification('Vui lòng nhập đầy đủ thông tin bắt buộc!', 'info');
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.registerData.name,
            identifier: this.registerData.identifier,
            password: this.registerData.password,
            address: this.registerData.address
          })
        });

        const result = await response.json();
        
        if (result.success) {
          this.showSystemNotification('Đăng ký thành công! Vui lòng đăng nhập.', 'success');
          this.showRegister = false;
          this.registerData = { name: '', identifier: '', password: '', address: '' };
        } else {
          this.showSystemNotification(result.message || 'Đăng ký thất bại!', 'error');
        }
      } catch (error) {
        console.error('Register error:', error);
        this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
      }
    },

    logout() {
      this.isLoggedIn = false;
      this.currentUser = { name: '', identifier: '', groups: [] };
      this.loginData = { identifier: '', password: '' };
      localStorage.removeItem('combagiang_user');
    },

    loadUserFromStorage() {
      try {
        const savedUser = localStorage.getItem('combagiang_user');
        
        if (savedUser) {
          const userData = JSON.parse(savedUser);
          
          const loginTime = userData.loginTime || 0;
          const now = new Date().getTime();
          const daysPassed = (now - loginTime) / (1000 * 60 * 60 * 24);
          
          if (daysPassed < 7) {
            this.currentUser = {
              id: userData.id,
              name: userData.name,
              identifier: userData.identifier,
              address: userData.address || "",
              groups: userData.groups || []
            };
            this.isLoggedIn = true;
          } else {
            localStorage.removeItem('combagiang_user');
          }
        }
      } catch (error) {
        console.error('Error loading user from localStorage:', error);
        localStorage.removeItem('combagiang_user');
      }
    },

    // ============ MODAL & UI CONTROLS ============
    openOrderModal() {
      this.showOrderModal = true;
    },

    closeOrderModal() {
      this.showOrderModal = false;
    },

    openGroupModal() {
      this.showGroupModal = true;
    },

    closeGroupModal() {
      this.showGroupModal = false;
    },

    openFeedbackModal() {
      this.showFeedbackModal = true;
    },

    closeFeedbackModal() {
      this.showFeedbackModal = false;
      this.feedbackData = {
        text: '',
        rating: 0,
        category: 'general'
      };
    },

    openUserInfoModal() {
      this.userInfoData = {
        name: this.currentUser.name,
        address: this.currentUser.address || '',
        created_at: this.currentUser.created_at || ''
      };
      this.showUserInfoModal = true;
    },

    closeUserInfoModal() {
      this.showUserInfoModal = false;
      this.userInfoData = {
        name: '',
        address: '',
        created_at: ''
      };
      this.isUpdatingUserInfo = false;
    },

    closeEditOrderModal() {
      this.showEditOrderModal = false;
      this.editingOrder = {};
      this.editOrderData = {
        meal_type: '',
        quantity: 1,
        note: ''
      };
    },

    closeOrderHistory() {
      this.showOrderHistory = false;
      this.orderHistory = [];
      this.filteredOrderHistory = [];
      this.historyTimeFilter = 'all';
      this.historyStatusFilter = 'all';
    },

    closePaymentSummary() {
      if (this.showPayOSModal) {
        this.closePayOSModal();
      }
      this.showPaymentSummary = false;
    },

    increaseQuantity() {
      this.quantity++;
    },

    decreaseQuantity() {
      if (this.quantity > 1) {
        this.quantity--;
      }
    },

    increaseEditQuantity() {
      this.editOrderData.quantity++;
    },

    decreaseEditQuantity() {
      if (this.editOrderData.quantity > 1) {
        this.editOrderData.quantity--;
      }
    },

    quickOrder(item) {
      this.mealType = item.name;
      this.quantity = 1;
      this.note = '';
      this.orderType = 'personal';
      this.openOrderModal();
    },

    setRating(stars) {
      this.feedbackData.rating = stars;
    },

    // ============ GROUP MANAGEMENT ============
    async joinGroup() {
      if (!this.joinGroupCode.trim()) {
        this.showSystemNotification('Vui lòng nhập mã nhóm!', 'info');
        return;
      }

      if (!this.currentUser.id) {
        this.showSystemNotification('Lỗi: Không tìm thấy thông tin người dùng. Vui lòng đăng nhập lại.', 'error');
        return;
      }

      try {
        const requestData = { 
          code: this.joinGroupCode,
          user_id: parseInt(this.currentUser.id)
        };
        
        const response = await fetch(`${API_BASE_URL}/groups/join`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        });

        const result = await response.json();
        
        if (result.success) {
          this.showSystemNotification('Tham gia nhóm thành công!', 'success');
          this.joinGroupCode = '';
          await this.refreshUserData();
        } else {
          this.showSystemNotification(result.message || 'Tham gia nhóm thất bại!', 'error');
        }
      } catch (error) {
        console.error('❌ Join group error:', error);
        this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
      }
    },

    async createGroup() {
      if (!this.newGroup.name || !this.newGroup.address) {
        this.showSystemNotification('Vui lòng nhập tên nhóm và địa chỉ giao hàng!', 'warning');
        return;
      }

      if (!this.currentUser.id) {
        this.showSystemNotification('Lỗi: Không tìm thấy thông tin người dùng. Vui lòng đăng nhập lại.', 'error');
        return;
      }

      try {
        const groupData = {
          user_id: parseInt(this.currentUser.id),
          name: this.newGroup.name,
          address: this.newGroup.address,
          description: this.newGroup.description
        };

        const response = await fetch(`${API_BASE_URL}/groups/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(groupData)
        });

        const result = await response.json();
        
        if (result.success) {
          this.showSystemNotification('Tạo nhóm thành công!\nMã nhóm: ${result.code}\nChia sẻ mã này với đồng nghiệp!', 'success');
          
          this.newGroup = { name: '', address: '', description: '' };
          this.closeGroupModal();
          await this.refreshUserData();
        } else {
          this.showSystemNotification(result.message || 'Tạo nhóm thất bại!', 'error');
        }
      } catch (error) {
        console.error('Create group error:', error);
        this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
      }
    },

    copyGroupCode(code) {
      navigator.clipboard.writeText(code).then(() => {
        this.showSystemNotification('Đã copy mã nhóm!', 'success');
      }).catch(() => {
        const textArea = document.createElement('textarea');
        textArea.value = code;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        this.showSystemNotification('Đã copy mã nhóm!', 'success');
      });
    },

    leaveGroup(groupName) {
      if (confirm(`Bạn có chắc muốn rời nhóm "${groupName}"?`)) {
        this.currentUser.groups = this.currentUser.groups.filter(g => g.name !== groupName);
        this.showSystemNotification('Rời nhóm thành công!', 'success');
      }
    },

    async goToGroupManagement(group) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/groups/${encodeURIComponent(group.name)}/members`);
        const result = await response.json();
        
        let actualGroupId = null;
        let groupInfo = { ...group };
        
        if (result.success && result.group_info) {
          actualGroupId = result.group_info.id;
          groupInfo = {
            id: actualGroupId,
            name: result.group_info.name,
            code: result.group_info.code,
            members: result.group_info.member_count || 0,
            totalOrders: 0,
            isLeader: group.isLeader || false,
            leaderName: this.currentUser.name
          };
        } else {
          actualGroupId = group.id || null;
          groupInfo.id = actualGroupId;
        }
        
        const groupManagementData = {
          groupInfo: groupInfo,
          groupId: actualGroupId,
          group_id: actualGroupId,
          userId: this.currentUser.id,
          user_id: this.currentUser.id,
          userName: this.currentUser.name,
          timestamp: new Date().getTime()
        };
        
        localStorage.setItem('group_management_data', JSON.stringify(groupManagementData));
        window.location.href = '/group-management';
        
      } catch (error) {
        console.error('❌ Error finding Group ID:', error);
        
        const fallbackData = {
          groupInfo: {
            id: group.id || null,
            name: group.name,
            code: group.code,
            members: 0,
            totalOrders: 0,
            isLeader: group.isLeader || false,
            leaderName: this.currentUser.name
          },
          groupId: group.id || null,
          userId: this.currentUser.id,
          userName: this.currentUser.name,
          timestamp: new Date().getTime()
        };
        
        localStorage.setItem('group_management_data', JSON.stringify(fallbackData));
        window.location.href = '/group-management';
      }
    },
    // ============ ORDER MANAGEMENT ============
    async submitOrder() {
      if (!this.currentUser.id) {
        this.showSystemNotification('Lỗi: Không tìm thấy thông tin người dùng. Vui lòng đăng nhập lại.', 'error');
        return;
      }

      if (!this.mealType) {
        this.showSystemNotification('Vui lòng chọn loại cơm!', 'warning');
        return;
      }

      try {
        const orderData = {
          user_id: parseInt(this.currentUser.id),
          group_id: this.orderType === 'personal' ? 'personal' : this.orderType,
          meal_type: this.mealType,
          quantity: this.quantity,
          note: this.note
        };

        const response = await fetch(`${API_BASE_URL}/orders/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(orderData)
        });

        const result = await response.json();
        
        if (result.success) {
          this.showSystemNotification('Đã đặt cơm, vui lòng kiểm tra trong Lịch sử!', 'success');
          this.closeOrderModal();
          this.quantity = 1;
          this.note = '';
          this.orderType = 'personal';
        } else {
          this.showSystemNotification(result.message || 'Đặt cơm thất bại!', 'error');
        }
      } catch (error) {
        console.error('Order error:', error);
        this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
      }
    },

    async viewOrderHistory() {
      if (!this.currentUser.id) {
        this.showSystemNotification('Vui lòng đăng nhập!', 'warning');
        return;
      }
      
      try {
        const response = await fetch(`http://127.0.0.1:8000/orders/history/${this.currentUser.id}`);
        const result = await response.json();
        
        this.orderHistory = result.orders || [];
        this.filteredOrderHistory = [...this.orderHistory];
        this.showOrderHistory = true;
      } catch (error) {
        console.error('Load order history error:', error);
        this.showSystemNotification('Không thể tải lịch sử đặt cơm!', 'error');
      }
    },

    filterOrderHistory() {
      let filtered = [...this.orderHistory];
      
      if (this.historyTimeFilter !== 'all') {
        const now = new Date();
        const today = now.toISOString().split('T')[0];
        
        filtered = filtered.filter(order => {
          const orderDate = new Date(order.date);
          
          switch (this.historyTimeFilter) {
            case 'today':
              return order.date === today;
            case 'week':
              const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
              return orderDate >= weekAgo;
            case 'month':
              const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
              return orderDate >= monthAgo;
            default:
              return true;
          }
        });
      }
      
      if (this.historyStatusFilter !== 'all') {
        filtered = filtered.filter(order => order.status === this.historyStatusFilter);
      }
      
      this.filteredOrderHistory = filtered;
    },
    // ============ ORDER EDIT & CANCEL ============
    editOrder(order) {
      this.editingOrder = { ...order };
      this.editOrderData = {
        meal_type: order.meal_type,
        quantity: order.quantity,
        note: order.note || ''
      };
      this.showEditOrderModal = true;
    },

    calculateEditOrderTotal() {
      const selectedItem = this.menuItems.find(item => item.name === this.editOrderData.meal_type);
      const price = selectedItem ? selectedItem.price : 0;
      return price * this.editOrderData.quantity;
    },

    async saveEditOrder() {
      if (!this.editOrderData.meal_type) {
        this.showSystemNotification('Vui lòng chọn loại cơm!', 'warning');
        return;
      }

      const hasChanges = (
        this.editOrderData.meal_type !== this.editingOrder.meal_type ||
        this.editOrderData.quantity !== this.editingOrder.quantity ||
        this.editOrderData.note !== (this.editingOrder.note || '')
      );

      if (!hasChanges) {
        this.showSystemNotification('Không có thay đổi nào để lưu!', 'warning');
        return;
      }

      if (confirm('Xác nhận lưu thay đổi đơn hàng?')) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/orders/${this.editingOrder.id}/edit`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_id: this.currentUser.id,
              date: this.editingOrder.date,
              meal_type: this.editOrderData.meal_type,
              quantity: this.editOrderData.quantity,
              note: this.editOrderData.note
            })
          });

          const result = await response.json();

          if (result.success) {
            const orderInHistory = this.orderHistory.find(o => o.id === this.editingOrder.id && o.date === this.editingOrder.date);
            if (orderInHistory) {
              orderInHistory.meal_type = this.editOrderData.meal_type;
              orderInHistory.quantity = this.editOrderData.quantity;
              orderInHistory.note = this.editOrderData.note;
              orderInHistory.total_amount = result.new_total_amount;
            }

            this.filterOrderHistory();
            this.closeEditOrderModal();
            this.showSystemNotification('Cập nhật thành công, vui lòng kiểm tra trong Lịch sử!', 'success');
          } else {
            this.showSystemNotification(result.message || 'Sửa đơn thất bại!', 'error');
          }
        } catch (error) {
          console.error('Edit order error:', error);
            this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
        }
      }
    },

    async cancelOrder(order) {
      if (confirm(`Bạn có chắc muốn hủy đơn #${order.id}?`)) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/orders/${order.id}/cancel`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_id: this.currentUser.id,
              date: order.date
            })
          });

          const result = await response.json();

          if (result.success) {
            const orderInHistory = this.orderHistory.find(o => o.id === order.id && o.date === order.date);
            if (orderInHistory) {
              orderInHistory.status = 'cancelled';
            }

            this.filterOrderHistory();
            this.showSystemNotification('Hủy xuất cơm thành công!.', 'success');
          } else {
            this.showSystemNotification(result.message || 'Hủy đơn thất bại!', 'error');
          }
        } catch (error) {
          console.error('Cancel order error:', error);
          this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
        }
      }
    },

    // ============ PAYMENT SUMMARY ============
    async viewPaymentSummary() {
      if (!this.currentUser.id) {
        this.showSystemNotification('Vui lòng đăng nhập!', 'warning');
        return;
      }
      
      this.paymentPeriod = 'all';
      this.selectedPaymentPeriod = 'all';
      
      await this.loadPaymentSummary();
      this.showPaymentSummary = true;
    },

    async loadPaymentSummary() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/payments/summary/${this.currentUser.id}?period=${this.paymentPeriod}`);
        const result = await response.json();
        
        this.paymentSummary = {
          period: result.period || this.getPeriodText(this.paymentPeriod),
          total_orders: result.total_orders || 0,
          meal_summary: result.meal_summary || {},
          total_amount: result.total_amount || 0,
          paid_amount: result.paid_amount || 0,
          remaining_amount: result.remaining_amount || 0,
          selected_period: this.paymentPeriod
        };
        
        this.selectedPaymentPeriod = this.paymentPeriod;
      } catch (error) {
        console.error('Load payment summary error:', error);
        this.paymentSummary = {
          period: this.getPeriodText(this.paymentPeriod),
          total_orders: 0,
          meal_summary: {},
          total_amount: 0,
          paid_amount: 0,
          remaining_amount: 0,
          selected_period: this.paymentPeriod
        };
      }
    },

    async markPaymentPaid() {
      if (this.paymentSummary.remaining_amount <= 0) {
        this.showSystemNotification('Bạn đã thanh toán hết rồi!', 'info');
        return;
      }
      
      const usePayOS = confirm(
        `🎯 Chọn phương thức thanh toán:\n\n` +
        `✅ OK = PayOS (QR + Link) - ${this.paymentSummary.remaining_amount.toLocaleString()} VNĐ\n` +
        `❌ Cancel = Đánh dấu đã thanh toán thủ công\n\n` +
        `💡 PayOS hỗ trợ: Banking, MoMo, ZaloPay, ViettelPay`
      );

      if (usePayOS) {
        await this.createPayOSPayment();
      } else {
        if (confirm(`Xác nhận đã thanh toán ${this.paymentSummary.remaining_amount.toLocaleString()} VNĐ bằng cách khác?`)) {
          try {
            const response = await fetch(`http://127.0.0.1:8000/payments/mark-paid/${this.currentUser.id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ amount: this.paymentSummary.remaining_amount })
            });
            
            const result = await response.json();
            
            if (result.success) {
              this.showSystemNotification('Đã đánh dấu thanh toán thành công!', 'success');
              await this.loadPaymentSummary();
            } else {
              this.showSystemNotification(result.message || 'Đánh dấu thanh toán thất bại!', 'error');
            }
          } catch (error) {
            console.error('Mark payment error:', error);
            this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
          }
        }
      }
    },

    async markManualPayment() {
      if (confirm(`Xác nhận đã thanh toán ${this.paymentSummary.remaining_amount.toLocaleString()} VNĐ cho ${this.paymentSummary.period}?`)) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/payments/mark-paid/${this.currentUser.id}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
              amount: this.paymentSummary.remaining_amount,
              payment_period: this.selectedPaymentPeriod
            })
          });
          
          const result = await response.json();
          
          if (result.success) {
            this.showSystemNotification('Đánh dấu thanh toán thành công!', 'success');
            await this.loadPaymentSummary();
          } else {
            this.showSystemNotification(result.message || 'Đánh dấu thanh toán thất bại!', 'error');
          }
        } catch (error) {
          console.error('Mark payment error:', error);
          this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
        }
      }
    },

    // ============ PAYOS PAYMENT ============
    async createPayOSPayment() {
      if (!this.currentUser.id) {
        this.showSystemNotification('Vui lòng đăng nhập!', 'warning');
        return;
      }

      if (this.paymentSummary.remaining_amount <= 0) {
        this.showSystemNotification('Không có công nợ cần thanh toán!', 'info');
        return;
      }

      this.isLoadingPayOS = true;
      this.qrCodeGenerated = false;

      try {
        const requestData = {
          user_id: this.currentUser.id,
          payment_period: this.selectedPaymentPeriod
        };
        
        const response = await fetch(`${API_BASE_URL}/payments/create-payos`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.success) {
          if (!result.order_code) {
            throw new Error('Missing order_code in response');
          }
          
          if (!result.amount) {
            throw new Error('Missing amount in response');
          }

          this.payosPaymentData = {
            transaction_id: result.transaction_id,
            order_code: result.order_code,
            checkout_url: result.checkout_url || '',
            qr_code: result.qr_code || '',
            amount: result.amount,
            description: result.description || '',
            user_name: result.user_name || '',
            expires_at: result.expires_at || '',
            status: 'PENDING'
          };

          this.showPayOSModal = true;
          this.showQRCode = true;
          
          this.startPayOSStatusChecking();
          this.startPayOSCountdown();
          
          this.showSystemNotification('Tạo thanh toán PayOS thành công!', 'success');

        } else {
          this.showSystemNotification((result.message || 'Không thể tạo thanh toán PayOS'), 'error');
        }
      } catch (error) {
        this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
      } finally {
        this.isLoadingPayOS = false;
      }
    },

    closePayOSModal() {
      this.stopPayOSIntervals();
      this.showPayOSModal = false;
      this.payosPaymentData = {
        transaction_id: null,
        order_code: null,
        checkout_url: '',
        qr_code: '',
        amount: 0,
        description: '',
        user_name: '',
        expires_at: '',
        status: 'PENDING'
      };
      this.payosTimeRemaining = 0;
      this.showQRCode = true;
    },

    async startPayOSPayment() {
      await this.createPayOSPayment();
    },

    async retryPayOSPayment() {
      this.showSystemNotification('Đang tạo thanh toán mới...', 'info');
      this.closePayOSModal();
      
      setTimeout(async () => {
        await this.createPayOSPayment();
      }, 500);
    },

    async cancelPayOSPayment() {
      if (!this.payosPaymentData.order_code) {
        this.showSystemNotification('Không có thanh toán để hủy', 'warning');
        return;
      }

      if (confirm('Bạn có chắc muốn hủy thanh toán này?')) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/payments/cancel-payos/${this.payosPaymentData.order_code}?user_id=${this.currentUser.id}`, {
            method: 'POST'
          });

          const result = await response.json();

          if (result.success) {
            this.showSystemNotification('Đã hủy thanh toán', 'success');
            this.closePayOSModal();
          } else {
            this.showSystemNotification(result.message || 'Không thể hủy thanh toán', 'error');
          }
        } catch (error) {
          console.error('Cancel PayOS payment error:', error);
          this.showSystemNotification('Lỗi kết nối khi hủy thanh toán', 'error');
        }
      }
    },

    // ============ PAYOS STATUS & COUNTDOWN ============
    startPayOSStatusChecking() {
      if (this.payosStatusCheckInterval) {
        clearInterval(this.payosStatusCheckInterval);
      }
      
      this.payosStatusCheckInterval = setInterval(async () => {
        try {
          const response = await fetch(`http://127.0.0.1:8000/payments/payos-status/${this.payosPaymentData.order_code}`);
          const result = await response.json();

          if (result.success) {
            const newStatus = result.status;
            const oldStatus = this.payosPaymentData.status;
            
            this.payosPaymentData.status = newStatus;

            if (newStatus !== oldStatus) {
              this.handlePaymentStatusChange(newStatus, oldStatus);
            }
            
            if (['PAID', 'FAILED', 'EXPIRED', 'CANCELLED'].includes(newStatus)) {
              this.stopPayOSIntervals();
            }
          } else {
            console.error('❌ Status check failed:', result.message);
          }
        } catch (error) {
          console.error('💥 PayOS status check error:', error);
        }
      }, 3000);
    },

    handlePaymentStatusChange(newStatus, oldStatus) {
      switch (newStatus) {
        case 'PAID':
          this.onPayOSPaymentSuccess();
          break;
        case 'FAILED':
          this.onPayOSPaymentFailed();
          break;
        case 'EXPIRED':
          this.onPayOSPaymentExpired();
          break;
        case 'CANCELLED':
          this.onPayOSPaymentCancelled();
          break;
        default:
          console.log(`Status update: ${newStatus}`);
      }
    },

    startPayOSCountdown() {
      const expiresAt = new Date(this.payosPaymentData.expires_at);
      
      this.payosCountdownInterval = setInterval(() => {
        const now = new Date();
        const timeLeft = expiresAt - now;

        if (timeLeft <= 0) {
          this.payosTimeRemaining = 0;
          this.onPayOSPaymentExpired();
        } else {
          this.payosTimeRemaining = Math.floor(timeLeft / 1000);
        }
      }, 1000);
    },

    onPayOSPaymentSuccess() {
      this.stopPayOSIntervals();
      
      this.showSystemNotification(
        `Thanh toán thành công!\nSố tiền: ${this.payosPaymentData.amount.toLocaleString()} VNĐ`,
        'success'
      );
      
      this.loadPaymentSummary();
      
      setTimeout(() => {
        this.closePayOSModal();
      }, 3000);
    },

    onPayOSPaymentExpired() {
      this.stopPayOSIntervals();
      this.showSystemNotification('Thanh toán đã hết hạn. Vui lòng tạo thanh toán mới.', 'warning');
    },

    onPayOSPaymentFailed() {
      this.stopPayOSIntervals();
      this.showSystemNotification('Thanh toán thất bại. Vui lòng thử lại.', 'error');
    },

    onPayOSPaymentCancelled() {
      this.stopPayOSIntervals();
      this.showSystemNotification('Thanh toán đã bị hủy.', 'info');
    },

    stopPayOSIntervals() {
      if (this.payosStatusCheckInterval) {
        clearInterval(this.payosStatusCheckInterval);
        this.payosStatusCheckInterval = null;
      }
      if (this.payosCountdownInterval) {
        clearInterval(this.payosCountdownInterval);
        this.payosCountdownInterval = null;
      }
    },

    // ============ PAYOS UTILITIES ============
    async copyPayOSOrderCode() {
      const orderCode = this.payosPaymentData.order_code;
      
      try {
        await navigator.clipboard.writeText(orderCode.toString());
        this.showSystemNotification(`Đã copy mã đơn hàng: ${orderCode}`, 'success');
      } catch (error) {
        const textArea = document.createElement('textarea');
        textArea.value = orderCode.toString();
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        this.showSystemNotification(`Đã copy mã đơn hàng: ${orderCode}`, 'success');
      }
    },

    openPaymentLink() {
      if (!this.payosPaymentData.checkout_url) {
        this.showSystemNotification('Không có link thanh toán', 'error');
        return;
      }
      
      try {
        window.open(this.payosPaymentData.checkout_url, '_blank');
      } catch (error) {
        console.error('Error opening payment link:', error);
      }
    },

    togglePaymentView() {
      this.showQRCode = !this.showQRCode;
    },

    generateVietQRImageUrl(qrData) {
      if (!qrData) {
        return '';
      }

      try {
        const encodedData = encodeURIComponent(qrData);
        const imageUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodedData}&format=png&margin=10`;
        return imageUrl;
      } catch (error) {
        console.error('❌ DEBUG: Error generating QR image URL:', error);
        return '';
      }
    },

    handleQRError(event) {
      this.showSystemNotification('Không thể hiển thị QR code. Vui lòng sử dụng link thanh toán.', 'warning');
    },

    async loadPayOSHistory() {
      if (!this.currentUser.id) return;

      try {
        const response = await fetch(`http://127.0.0.1:8000/payments/payos-history/${this.currentUser.id}`);
        const result = await response.json();

        if (result.success) {
          return result.transactions;
        }
      } catch (error) {
        console.error('Load PayOS history error:', error);
      }
      return [];
    },

    // ============ USER INFO MANAGEMENT ============
    async updateUserInfo() {
      if (!this.userInfoData.name.trim()) {
        this.showSystemNotification('Vui lòng nhập họ tên!', 'warning');
        return;
      }

      this.isUpdatingUserInfo = true;

      try {
        const response = await fetch(`http://127.0.0.1:8000/users/${this.currentUser.id}/info`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.userInfoData.name.trim(),
            address: this.userInfoData.address.trim()
          })
        });

        const result = await response.json();

        if (result.success) {
          this.currentUser.name = result.user.name;
          this.currentUser.address = result.user.address;

          const userDataToSave = {
            ...this.currentUser,
            loginTime: new Date().getTime()
          };
          localStorage.setItem('combagiang_user', JSON.stringify(userDataToSave));

          this.showSystemNotification('Cập nhật thông tin thành công!', 'success');
          this.closeUserInfoModal();
        } else {
          this.showSystemNotification(result.message || 'Cập nhật thất bại!', 'error');
        }
      } catch (error) {
        console.error('Update user info error:', error);
        this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
      } finally {
        this.isUpdatingUserInfo = false;
      }
    },

    // ============ FEEDBACK SYSTEM ============
    async submitFeedback() {
      if (!this.feedbackData.text.trim()) {
        this.showSystemNotification('Vui lòng nhập nội dung góp ý!', 'warning');
        return;
      }
      
      if (this.feedbackData.text.length > 500) {
        this.showSystemNotification('Nội dung góp ý không được vượt quá 500 ký tự!', 'warning');
        return;
      }
      
      try {
        const response = await fetch(`${API_BASE_URL}/feedback/submit`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            feedback_text: this.feedbackData.text.trim(),
            rating: this.feedbackData.rating || null,
            category: this.feedbackData.category
          })
        });
        
        const result = await response.json();
        
        if (result.success) {
          this.showSystemNotification(result.message, 'success');
          this.closeFeedbackModal();
        } else {
          this.showSystemNotification(result.message || 'Gửi góp ý thất bại!', 'error');
        }
      } catch (error) {
        console.error('Submit feedback error:', error);
        this.showSystemNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
      }
    },

    // ============ NOTIFICATION SYSTEM ============
    showSystemNotification(message, type = 'info') {
      this.systemNotification = {
        show: true,
        message: message,
        type: type,
        timestamp: new Date().getTime()
      };
      
      setTimeout(() => {
        this.hideSystemNotification();
      }, 5000);
    },

    hideSystemNotification() {
      this.systemNotification.show = false;
    },

  }, // Kết thúc methods

  // ============ LIFECYCLE HOOKS ============
  async mounted() {
    // Load user from storage first
    this.loadUserFromStorage();
    
    // Always load menu (for both logged and non-logged users)
    await this.loadTodayMenu();
    
    // Load PayOS configuration
    await this.loadPayOSConfig();

    // Load additional user data if logged in
    if (this.isLoggedIn && this.currentUser.id) {
      await this.refreshUserData();
      await this.loadUserInfoFromServer();
    }
  }, 

  beforeUnmount() {
    // Clean up PayOS intervals
    this.stopPayOSIntervals();
  }

}
