import { API_CONFIG } from '../../config/api.js'
const API_BASE_URL = API_CONFIG.BASE_URL

export default {
  name: 'KitchenManager',
  data() {
    return {
      // General Data
      today: new Date().toLocaleDateString('vi-VN'),
      activeTab: 'orders',
      
      // Authentication
      isAdminAuthenticated: false,
      adminPassword: '',
      adminAuthError: '',
      isCheckingAdmin: false,
      
      // Orders Management
      orders: [],
      filteredOrders: [],
      orderFilter: 'all',
      statusFilter: 'all',
      orderQuickFilter: 'today',
      orderStartDate: '',
      orderEndDate: '',
      orderStatusFilter: 'all',
      orderGroupFilter: 'all',
      currentOrdersPage: 1,
      ordersPerPage: 20,
      showAdvancedFilters: false,
      expandedOrders: [],
      
      // Groups Data
      groups: [],
      allGroups: [],
      showGroupDetails: false,
      selectedGroup: { 
        name: '', 
        code: '', 
        leader_name: '', 
        address: '', 
        description: '', 
        members: [] 
      },
      
      // Payment Management
      paymentFilter: 'current',
      paymentGroupFilter: 'all',
      paymentStatusFilter: 'all',
      payments: [],
      filteredPayments: [],
      paymentStats: {
        paid: 0,
        pending: 0,
        total: 0
      },
      showPaymentHistory: false,
      selectedUser: { name: '', id: null },
      paymentHistory: [],
      
      // Menu Management
      menuForm: {
        date: new Date().toISOString().split('T')[0],
        deadline: '10:00',
        menu_items: [
          { name: 'Suất tiêu chuẩn', price: 35000, description: '' },
          { name: 'Suất cao cấp', price: 40000, description: '' }
        ],
        toppings: ''
      }, 
      showMenuItemModal: false,
      editingMenuItem: { name: '', price: 0, description: '' },
      editingMenuItemIndex: -1,

      // Feedback Management
      feedbackList: [],
      filteredFeedback: [],
      feedbackCategoryFilter: 'all',
      feedbackRatingFilter: 'all',
      feedbackStatusFilter: 'all',
      feedbackStats: {
        total: 0,
        avgRating: 0,
        unread: 0,
        resolved: 0
      },
      hoverRating: 0
    }
  },

  computed: {
    paginatedOrders() {
      const start = (this.currentOrdersPage - 1) * this.ordersPerPage;
      const end = start + this.ordersPerPage;
      const orders = this.filteredOrders.slice(start, end);

      return orders.map((order, index) => ({
        ...order,
        sequentialNumber: this.filteredOrders.length - (start + index)
      }));
    },
    
    totalOrdersPages() {
      return Math.ceil(this.filteredOrders.length / this.ordersPerPage);
    },
    
    orderStats() {
      return {
        pending: this.filteredOrders.filter(o => o.status === 'pending').length,
        preparing: this.filteredOrders.filter(o => o.status === 'preparing').length,
        completed: this.filteredOrders.filter(o => o.status === 'completed').length,
        cancelled: this.filteredOrders.filter(o => o.status === 'cancelled').length
      };
    }
  },
  
  methods: {
    // ============ NAVIGATION ============
    goToUserSite() {
      this.$router.push('/');
    },

    // ============ AUTHENTICATION ============
    async authenticateAdmin() {
      if (!this.adminPassword.trim()) {
        this.adminAuthError = 'Vui lòng nhập mã admin!';
        return;
      }

      this.isCheckingAdmin = true;
      this.adminAuthError = '';

      try {
        const response = await fetch(`${API_BASE_URL}/admin/auth`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            admin_password: this.adminPassword 
          })
        });

        const result = await response.json();

        if (result.success) {
          this.isAdminAuthenticated = true;
          this.adminAuthError = '';
          this.adminPassword = '';
          
          // Load admin data
          // await this.loadAdminData();
          
        } else {
          this.adminAuthError = result.message || 'Mã admin không đúng!';
          this.adminPassword = '';
        }
      } catch (error) {
        console.error('Admin auth error:', error);
        this.adminAuthError = 'Lỗi kết nối! Vui lòng thử lại.';
      } finally {
        this.isCheckingAdmin = false;
      }
    },

    async loadAdminData() {
      try {
        await Promise.all([
          this.refreshGroupsData(),
          this.loadOrders(),
          this.loadTodayMenu(),
          this.refreshPayments(),
          this.refreshGroups(),
          this.refreshFeedback()
        ]);
        
        this.applyOrderQuickFilter();
      } catch (error) {
        console.error('Error loading admin data:', error);
      }
    },

    // ============ DATA LOADING UTILITIES ============
    async refreshGroupsData() {
      try {
        const response = await fetch(`${API_BASE_URL}/admin/groups`);
        const result = await response.json();
        
        this.groups = (result.groups || []).map(g => ({ 
          id: g.id, 
          name: g.name 
        }));
        
      } catch (error) {
        console.error('Refresh groups data error:', error);
        this.groups = [
          { id: 1, name: 'IT Team' },
          { id: 2, name: 'Marketing Team' }
        ];
      }
    },

    // ============ HELPER METHODS ============
    formatDateForInput(date) {
      return date.toISOString().split('T')[0];
    },
    
    formatOrderDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('vi-VN', {
        weekday: 'short',
        day: '2-digit',
        month: '2-digit'
      });
    },
    
    formatPrice(price) {
      if (!price) return '0đ';
      return price.toLocaleString() + 'đ';
    },
    
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    formatDescription(description) {
      if (!description) return 'Chưa có mô tả';
      
      return description
        .replace(/\r\n/g, '\n')
        .replace(/\r/g, '\n')    
        .trim();
    },

    // ============ ORDERS MANAGEMENT ============
    applyOrderQuickFilter() {
      const today = new Date();
      
      switch (this.orderQuickFilter) {
        case 'today':
          this.orderStartDate = this.orderEndDate = this.formatDateForInput(today);
          break;
        case 'week':
          const weekStart = new Date(today);
          weekStart.setDate(today.getDate() - today.getDay());
          this.orderStartDate = this.formatDateForInput(weekStart);
          this.orderEndDate = this.formatDateForInput(today);
          break;
        case 'month':
          const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
          this.orderStartDate = this.formatDateForInput(monthStart);
          this.orderEndDate = this.formatDateForInput(today);
          break;
        case 'custom':
          // Keep current dates
          break;
      }
      
      if (this.orderQuickFilter !== 'custom') {
        this.loadOrders();
      }
    },
    
    async loadOrders() {
      try {
        let url = `${API_BASE_URL}/admin/orders/range`;
        const params = new URLSearchParams();
        
        if (this.orderStartDate) params.append('start_date', this.orderStartDate);
        if (this.orderEndDate) params.append('end_date', this.orderEndDate);
        
        if (params.toString()) {
          url += '?' + params.toString();
        }
        
        const response = await fetch(url);
        const result = await response.json();
        
        this.orders = result.orders || [];
        this.filterOrders();
        
      } catch (error) {
        console.error('Error loading orders:', error);
        alert('Lỗi tải danh sách đơn hàng!');
      }
    },
    
    async refreshOrders() {
      await this.loadOrders();
    },
    
    filterOrders() {
      let filtered = [...this.orders];
  
      // Filter by group
      if (this.orderGroupFilter !== 'all') {
        if (this.orderGroupFilter === 'personal') {
          filtered = filtered.filter(order => !order.group_name);
        } else {
          filtered = filtered.filter(order => order.group_name === this.orderGroupFilter);
        }
      }
      
      // Filter by status
      if (this.orderStatusFilter !== 'all') {
        filtered = filtered.filter(order => order.status === this.orderStatusFilter);
      }
      
      // Sort by multiple criteria to ensure newest orders are at TOP
      filtered.sort((a, b) => {
        const dateA = new Date(a.date + ' ' + (a.created_at || '00:00:00')).getTime();
        const dateB = new Date(b.date + ' ' + (b.created_at || '00:00:00')).getTime();
        
        if (dateA !== dateB) {
          return dateB - dateA;
        }
        
        return b.id - a.id;
      });
      
      // Add sequential number directly to each order
      filtered = filtered.map((order, index) => ({
        ...order,
        sequentialNumber: index + 1
      }));
      
      this.filteredOrders = filtered;
      this.currentOrdersPage = 1;
    },
    
    async updateOrderStatus(order, newStatus) {
      if (order.status === 'cancelled') {
        alert('Không thể cập nhật đơn hàng đã hủy!');
        return;
      }
      
      try {
        const response = await fetch(`${API_BASE_URL}/admin/orders/${order.id}/status/${order.date}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ status: newStatus })
        });
        
        const result = await response.json();
        
        if (result.success) {
          const orderIndex = this.orders.findIndex(o => o.id === order.id && o.date === order.date);
          if (orderIndex !== -1) {
            this.orders[orderIndex].status = newStatus;
            this.filterOrders();
          }
          
          const statusText = this.getStatusText(newStatus);
          alert(`✅ Đã cập nhật trạng thái thành "${statusText}"`);
        } else {
          alert('❌ ' + (result.message || 'Cập nhật thất bại!'));
        }
      } catch (error) {
        console.error('Error updating order status:', error);
        alert('❌ Lỗi kết nối!');
      }
    },
    
    getStatusText(status) {
      const statusMap = {
        'pending': 'Đã đặt',
        'preparing': 'Đang giao', 
        'completed': 'Hoàn thành',
        'cancelled': 'Đã hủy' 
      };
      return statusMap[status] || `Không xác định (${status})`;
    },
    
    getStatusBadgeClass(status) {
      switch (status) {
        case 'pending': return 'bg-yellow-100 text-yellow-800';
        case 'preparing': return 'bg-blue-100 text-blue-800';
        case 'completed': return 'bg-green-100 text-green-800';
        case 'cancelled': return 'bg-red-100 text-red-800';
        default: return 'bg-gray-100 text-gray-800';
      }
    },

    toggleOrderDetails(order) {
      if (!this.expandedOrders) {
        this.expandedOrders = [];
      }
      const orderKey = `${order.date}-${order.id}`;
      const index = this.expandedOrders.indexOf(orderKey);
      
      if (index > -1) {
        this.expandedOrders.splice(index, 1);
      } else {
        this.expandedOrders.push(orderKey);
      }
    },

    isOrderExpanded(order) {
      if (!this.expandedOrders) {
        this.expandedOrders = [];
      }
      const orderKey = `${order.date}-${order.id}`;
      return this.expandedOrders.includes(orderKey);
    },

    // ============ MENU MANAGEMENT ============
    async loadTodayMenu() {
      try {
        const response = await fetch(`${API_BASE_URL}/menu/today`);
        const menu = await response.json();
        
        this.menuForm = {
          date: menu.date,
          deadline: menu.deadline,
          menu_items: menu.menu_items || [
            { name: 'Suất tiêu chuẩn', price: 35000, description: '' },
            { name: 'Suất cao cấp', price: 40000, description: '' }
          ],
          toppings: menu.toppings
        };
      } catch (error) {
        console.error('Load menu error:', error);
        this.menuForm.date = new Date().toISOString().split('T')[0];
      }
    },
    
    async saveMenu() {
      try {
        const response = await fetch(`${API_BASE_URL}/admin/menu/save`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.menuForm)
        });
        
        const result = await response.json();
        
        if (result.success) {
          alert('Lưu menu thành công!');
        } else {
          alert(result.message || 'Lưu menu thất bại!');
        }
      } catch (error) {
        console.error('Save menu error:', error);
        alert('Lỗi kết nối! Vui lòng thử lại.');
      }
    },
    
    // ============ MENU ITEM MODAL METHODS ============
    openMenuItemModal(item = null, index = -1) {
      if (item) {
        this.editingMenuItem = { ...item };
        this.editingMenuItemIndex = index;
      } else {
        this.editingMenuItem = { name: '', price: 0, description: '' };
        this.editingMenuItemIndex = -1;
      }
      this.showMenuItemModal = true;
    },

    closeMenuItemModal() {
      this.showMenuItemModal = false;
      this.editingMenuItem = { name: '', price: 0, description: '' };
      this.editingMenuItemIndex = -1;
    },

    async saveMenuItem() {
      if (!this.editingMenuItem.name || !this.editingMenuItem.price) {
        alert('Vui lòng nhập đầy đủ tên và giá!');
        return;
      }
      
      // Format description trước khi save
      const formattedDescription = this.formatDescription(this.editingMenuItem.description);
      
      if (this.editingMenuItemIndex >= 0) {
        // Update existing item với formatted description
        this.menuForm.menu_items[this.editingMenuItemIndex] = {
          ...this.editingMenuItem,
          description: formattedDescription
        };
      } else {
        // Add new item với formatted description  
        this.menuForm.menu_items.push({
          ...this.editingMenuItem,
          description: formattedDescription
        });
      }
      
      // AUTO SAVE TO EXCEL
      try {
        const response = await fetch(`${API_BASE_URL}/admin/menu/save`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.menuForm)
        });
        
        const result = await response.json();
        
        if (result.success) {
          alert('Đã lưu suất cơm vào hệ thống!');
        } else {
          alert('Lỗi: ' + (result.message || 'Không thể lưu'));
        }
      } catch (error) {
        console.error('Save error:', error);
        alert('Lỗi kết nối! Menu chỉ lưu tạm thời.');
      }
      
      this.closeMenuItemModal();
    },
    
    removeMenuItem(index) {
      if (confirm('Bạn có chắc muốn xóa suất cơm này?')) {
        this.menuForm.menu_items.splice(index, 1);
      }
    },

    // ============ PAYMENT MANAGEMENT ============
    async refreshPayments() {
      try {
        const endpoint = this.paymentFilter === 'all' ? 
          `${API_BASE_URL}/admin/payments` : 
          `${API_BASE_URL}/admin/payments/period/${this.paymentFilter}`;
          
        const response = await fetch(endpoint);
        const result = await response.json();
        this.payments = result.payments || [];
        this.filterPayments();
      } catch (error) {
        console.error('Refresh payments error:', error);
        this.loadDemoPayments();
      }
    },
    
    loadDemoPayments() {
      this.payments = [
        { 
          user_id: 1, 
          user_name: 'Nguyễn Văn Nam', 
          group_name: 'IT Team',
          total_orders: 10, 
          total_amount: 350, 
          paid_amount: 200, 
          remaining_amount: 150,
          status: 'partial'
        },
        { 
          user_id: 2, 
          user_name: 'Trần Thị Lan', 
          group_name: 'IT Team',
          total_orders: 8, 
          total_amount: 280, 
          paid_amount: 280, 
          remaining_amount: 0,
          status: 'paid'
        }
      ];
      this.filterPayments();
    },
    
    filterPayments() {
      let filtered = [...this.payments];
      
      // Filter by group
      if (this.paymentGroupFilter !== 'all') {
        if (this.paymentGroupFilter === 'personal') {
          filtered = filtered.filter(payment => !payment.group_name);
        } else {
          filtered = filtered.filter(payment => payment.group_name === this.paymentGroupFilter);
        }
      }
      
      // Filter by payment status
      if (this.paymentStatusFilter !== 'all') {
        if (this.paymentStatusFilter === 'paid') {
          filtered = filtered.filter(payment => payment.remaining_amount === 0);
        } else if (this.paymentStatusFilter === 'pending') {
          filtered = filtered.filter(payment => payment.remaining_amount > 0);
        }
      }
      
      this.filteredPayments = filtered;
      
      // Calculate stats from filtered data
      this.paymentStats = {
        paid: this.filteredPayments.reduce((sum, p) => sum + (p.paid_amount || 0), 0),
        pending: this.filteredPayments.reduce((sum, p) => sum + (p.remaining_amount || 0), 0),
        total: this.filteredPayments.reduce((sum, p) => sum + (p.total_amount || 0), 0)
      };
    },
    
    async markAsPaid(userId, amount) {
      if (confirm(`Xác nhận đã nhận thanh toán ${amount.toLocaleString()}k từ khách hàng?`)) {
        try {
          const response = await fetch(`${API_BASE_URL}/admin/payments/${userId}/mark-paid`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount })
          });
          
          const result = await response.json();
          
          if (result.success) {
            const payment = this.payments.find(p => p.user_id === userId);
            if (payment) {
              payment.paid_amount += payment.remaining;
              payment.remaining = 0;
            }
            this.filterPayments();
            alert('Đã cập nhật trạng thái thanh toán!');
          } else {
            alert(result.message || 'Cập nhật thất bại!');
          }
        } catch (error) {
          console.error('Mark as paid error:', error);
          alert('Lỗi kết nối! Vui lòng thử lại.');
        }
      }
    },
    
    async viewPaymentHistory(userId) {
      try {
        const response = await fetch(`${API_BASE_URL}/admin/payments/${userId}/history`);
        const result = await response.json();
        
        const user = this.payments.find(p => p.user_id === userId);
        this.selectedUser = { name: user.user_name, id: userId };
        this.paymentHistory = result.history || [];
        this.showPaymentHistory = true;
      } catch (error) {
        console.error('View payment history error:', error);
        const user = this.payments.find(p => p.user_id === userId);
        this.selectedUser = { name: user.user_name, id: userId };
        this.paymentHistory = [
          { id: 1, amount: 70, date: '25/05/2025 14:30' },
          { id: 2, amount: 105, date: '20/05/2025 12:15' }
        ];
        this.showPaymentHistory = true;
      }
    },
    
    closePaymentHistory() {
      this.showPaymentHistory = false;
      this.selectedUser = { name: '', id: null };
      this.paymentHistory = [];
    },

    // ============ GROUPS MANAGEMENT ============
    async refreshGroups() {
      try {
        const response = await fetch(`${API_BASE_URL}/admin/groups`);
        const result = await response.json();
        this.allGroups = result.groups || [];
      } catch (error) {
        console.error('Refresh groups error:', error);
        this.loadDemoGroups();
      }
    },
    
    loadDemoGroups() {
      this.allGroups = [
        {
          id: 1,
          name: 'IT Team',
          code: 'IT2025',
          leader_name: 'Nguyễn Văn Nam',
          member_count: 4,
          address: 'Tầng 5, Tòa nhà A',
          description: 'Nhóm phát triển phần mềm',
          members: [
            { id: 1, name: 'Nguyễn Văn Nam', identifier: '0901234567', is_leader: true }
          ]
        }
      ];
    },
    
    viewGroupDetails(groupId) {
      const group = this.allGroups.find(g => g.id === groupId);
      if (group) {
        this.selectedGroup = { ...group };
        this.showGroupDetails = true;
      }
    },
    
    closeGroupDetails() {
      this.showGroupDetails = false;
      this.selectedGroup = { 
        name: '', 
        code: '', 
        leader_name: '', 
        address: '', 
        description: '', 
        members: [] 
      };
    },
    
    async deleteGroup(groupId) {
      const group = this.allGroups.find(g => g.id === groupId);
      if (group && confirm(`Bạn có chắc muốn xóa nhóm "${group.name}"?\nLưu ý: Thao tác này không thể hoàn tác!`)) {
        try {
          const response = await fetch(`${API_BASE_URL}/admin/groups/${groupId}`, {
            method: 'DELETE'
          });
          
          const result = await response.json();
          
          if (result.success) {
            this.allGroups = this.allGroups.filter(g => g.id !== groupId);
            alert('Xóa nhóm thành công!');
          } else {
            alert(result.message || 'Xóa nhóm thất bại!');
          }
        } catch (error) {
          console.error('Delete group error:', error);
          alert('Lỗi kết nối! Vui lòng thử lại.');
        }
      }
    },

    // ============ FEEDBACK MANAGEMENT ============
    async refreshFeedback() {
      try {
        const response = await fetch(`${API_BASE_URL}/admin/feedback`);
        const result = await response.json();
        this.feedbackList = result.feedback || [];
        this.calculateFeedbackStats();
        this.filterFeedback();
      } catch (error) {
        console.error('Refresh feedback error:', error);
        this.loadDemoFeedback();
      }
    },

    loadDemoFeedback() {
      this.feedbackList = [
        {
          id: 1,
          feedback_text: "Cơm rất ngon, giao hàng nhanh. Rất hài lòng!",
          rating: 5,
          category: "food",
          created_at: "2025-05-28 14:30:00",
          status: "new"
        },
        {
          id: 2,
          feedback_text: "Món ăn ổn nhưng giao hàng hơi chậm",
          rating: 3,
          category: "delivery",
          created_at: "2025-05-28 12:15:00",
          status: "read"
        },
        {
          id: 3,
          feedback_text: "Giá cả hợp lý, chất lượng tốt",
          rating: 4,
          category: "price",
          created_at: "2025-05-27 18:45:00",
          status: "resolved"
        }
      ];
      this.calculateFeedbackStats();
      this.filterFeedback();
    },

    calculateFeedbackStats() {
      const total = this.feedbackList.length;
      const unread = this.feedbackList.filter(f => f.status === 'new').length;
      const resolved = this.feedbackList.filter(f => f.status === 'resolved').length;
      
      const ratedFeedback = this.feedbackList.filter(f => f.rating && f.rating > 0);
      const avgRating = ratedFeedback.length > 0 ? 
        (ratedFeedback.reduce((sum, f) => sum + f.rating, 0) / ratedFeedback.length).toFixed(1) : 0;
      
      this.feedbackStats = {
        total,
        avgRating,
        unread,
        resolved
      };
    },

    filterFeedback() {
      let filtered = [...this.feedbackList];
      
      // Filter by category
      if (this.feedbackCategoryFilter !== 'all') {
        filtered = filtered.filter(feedback => feedback.category === this.feedbackCategoryFilter);
      }
      
      // Filter by rating
      if (this.feedbackRatingFilter !== 'all') {
        const rating = parseInt(this.feedbackRatingFilter);
        if (rating === 0) {
          filtered = filtered.filter(feedback => !feedback.rating || feedback.rating === 0);
        } else {
          filtered = filtered.filter(feedback => feedback.rating === rating);
        }
      }
      
      // Filter by status
      if (this.feedbackStatusFilter !== 'all') {
        filtered = filtered.filter(feedback => feedback.status === this.feedbackStatusFilter);
      }
      
      this.filteredFeedback = filtered;
    },

    async markFeedbackAsRead(feedbackId) {
      try {
        const response = await fetch(`${API_BASE_URL}/admin/feedback/${feedbackId}/status`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ status: 'read' })
        });
        
        const result = await response.json();
        
        if (result.success) {
          const feedback = this.feedbackList.find(f => f.id === feedbackId);
          if (feedback) {
            feedback.status = 'read';
            this.calculateFeedbackStats();
            this.filterFeedback();
          }
        } else {
          alert(result.message || 'Cập nhật trạng thái thất bại!');
        }
      } catch (error) {
        console.error('Mark feedback as read error:', error);
        alert('Lỗi kết nối! Vui lòng thử lại.');
      }
    },

    async markFeedbackAsResolved(feedbackId) {
      if (confirm('Xác nhận đã xử lý góp ý này?')) {
        try {
          const response = await fetch(`${API_BASE_URL}/admin/feedback/${feedbackId}/status`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: 'resolved' })
          });
          
          const result = await response.json();
          
          if (result.success) {
            const feedback = this.feedbackList.find(f => f.id === feedbackId);
            if (feedback) {
              feedback.status = 'resolved';
              this.calculateFeedbackStats();
              this.filterFeedback();
            }
            alert('Đã đánh dấu góp ý là đã xử lý!');
          } else {
            alert(result.message || 'Cập nhật trạng thái thất bại!');
          }
        } catch (error) {
          console.error('Mark feedback as resolved error:', error);
          alert('Lỗi kết nối! Vui lòng thử lại.');
        }
      }
    },

    async deleteFeedback(feedbackId) {
      if (confirm('Bạn có chắc muốn xóa góp ý này? Thao tác này không thể hoàn tác!')) {
        try {
          const response = await fetch(`${API_BASE_URL}/admin/feedback/${feedbackId}`, {
            method: 'DELETE'
          });
          
          const result = await response.json();
          
          if (result.success) {
            this.feedbackList = this.feedbackList.filter(f => f.id !== feedbackId);
            this.calculateFeedbackStats();
            this.filterFeedback();
            alert('Đã xóa góp ý thành công!');
          } else {
            alert(result.message || 'Xóa góp ý thất bại!');
          }
        } catch (error) {
          console.error('Delete feedback error:', error);
          alert('Lỗi kết nối! Vui lòng thử lại.');
        }
      }
    },

    // ============ DISPLAY HELPER METHODS ============
    getCategoryClass(category) {
      const classes = {
        'general': 'bg-gray-100 text-gray-800',
        'food': 'bg-orange-100 text-orange-800',
        'service': 'bg-blue-100 text-blue-800',
        'delivery': 'bg-purple-100 text-purple-800',
        'price': 'bg-green-100 text-green-800'
      };
      return classes[category] || 'bg-gray-100 text-gray-800';
    },

    getCategoryText(category) {
      const texts = {
        'general': 'Chung',
        'food': 'Món ăn',
        'service': 'Dịch vụ',
        'delivery': 'Giao hàng',
        'price': 'Giá cả'
      };
      return texts[category] || 'Khác';
    },

    getStatusClass(status) {
      const classes = {
        'new': 'bg-red-100 text-red-800',
        'read': 'bg-yellow-100 text-yellow-800',
        'resolved': 'bg-green-100 text-green-800'
      };
      return classes[status] || 'bg-gray-100 text-gray-800';
    },

    getFeedbackStatusText(status) {
      const texts = {
        'new': 'Mới',
        'read': 'Đã đọc',
        'resolved': 'Đã xử lý'
      };
      return texts[status] || 'Không xác định';
    },

    }, // Kết thúc methods
  
  // ============ LIFECYCLE HOOKS ============
  mounted() {
    // Initialize paymentStats first
    this.paymentStats = {
      paid: 0,
      pending: 0,
      total: 0
    };

    // Load initial data
    this.refreshGroupsData();
    this.refreshOrders();
    this.loadTodayMenu();
    this.refreshPayments();
    this.refreshGroups();
    this.refreshFeedback();
    this.applyOrderQuickFilter();
  }

}