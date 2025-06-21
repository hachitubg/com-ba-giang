import { API_CONFIG } from '../../config/api.js'
const API_BASE_URL = API_CONFIG.BASE_URL

export default {
  name: 'GroupManagement',
  data() {
    return {
      // UI State
      activeTab: 'members',
      
      // Group Information
      groupInfo: {
        name: '',
        code: '',
        id: null,
        members: 0,
        totalOrders: 0
      },
      
      // Current User Info
      currentUser: {
        id: null,
        name: '',
        isLeader: false
      },
      
      // Group Statistics
      groupStats: {
        memberCount: 0,
        totalOrders: 0
      },
      
      // Notification System
      notification: {
        show: false,
        message: '',
        type: 'info'
      },
      
      // Members Management
      members: [],
      isLoadingMembers: false,
      
      // Delete Member Modal
      showDeleteModal: false,
      memberToDelete: {
        id: null,
        name: ''
      },
      isDeleting: false,
      
      // Orders Management
      orders: [],
      filteredOrders: [],
      orderFilter: 'today',
      isLoadingOrders: false,
      
      // Payments Management
      payments: [],
      filteredPayments: [],
      paymentFilter: 'current',
      paymentSummary: {
        totalAmount: 0,
        paidAmount: 0,
        remainingAmount: 0
      },
      isLoadingPayments: false
    }
  },
  methods: {
    // ============ NAVIGATION ============
    goBack() {
      window.location.href = '/';
    },
    
    // ============ NOTIFICATION SYSTEM ============
    showNotification(message, type = 'info') {
      this.notification = {
        show: true,
        message: message,
        type: type
      };
      
      setTimeout(() => {
        this.hideNotification();
      }, 5000);
    },
    
    hideNotification() {
      this.notification.show = false;
    },

    // ============ DATA LOADING & STORAGE ============
    loadGroupDataFromStorage() {
      try {
        const storedData = localStorage.getItem('group_management_data');
        
        if (storedData) {
          const data = JSON.parse(storedData);
          const now = new Date().getTime();
          const timeDiff = now - data.timestamp;
          
          if (timeDiff < 3600000) {
            // Ưu tiên lấy ID từ nhiều nguồn khác nhau
            let groupId = data.groupInfo?.id || data.groupId || data.group_id;
            
            this.groupInfo = {
              name: data.groupInfo?.name || data.groupName || data.group_name,
              code: data.groupInfo?.code || data.groupCode || data.group_code,
              id: groupId, // Ưu tiên ID
              members: data.groupInfo?.members || 0,
              totalOrders: data.groupInfo?.totalOrders || 0
            };
            
            this.currentUser = {
              id: data.userId || data.user_id,
              name: data.groupInfo?.leaderName || data.userName || 'Unknown',
              isLeader: data.groupInfo?.isLeader !== undefined ? data.groupInfo.isLeader : true
            };
            
            // QUAN TRỌNG: Phải có ID, name chỉ là fallback
            if (!this.groupInfo.id) {
              this.showNotification('Thiếu Group ID. Không thể quản lý nhóm an toàn.', 'error');
              
              setTimeout(() => {
                this.goBack();
              }, 3000);
              return false;
            }
            
            return true;
          } else {
            localStorage.removeItem('group_management_data');
          }
        }
        
        this.showNotification('Không tìm thấy thông tin nhóm. Đang chuyển về trang chính...', 'error');
        setTimeout(() => {
          this.goBack();
        }, 2000);
        return false;
        
      } catch (error) {
        this.showNotification('Lỗi tải thông tin nhóm. Đang chuyển về trang chính...', 'error');
        setTimeout(() => {
          this.goBack();
        }, 2000);
        return false;
      }
    },
    
    async loadAllData() {
      if (!this.loadGroupDataFromStorage()) {
        return;
      }
      
      await Promise.all([
        this.loadMembers(),
        this.loadOrders(),
        this.loadPayments()
      ]);
      
      this.calculateGroupStats();
    },
    
    calculateGroupStats() {
      // Calculate today's orders count
      const today = new Date().toISOString().split('T')[0];
      const todayOrders = this.orders.filter(order => order.date === today);
      
      this.groupStats = {
        memberCount: this.members.length,
        totalOrders: todayOrders.length
      };
    },

    // ============ MEMBERS MANAGEMENT ============
    async loadMembers() {
      this.isLoadingMembers = true;
      
      try {
        // LUÔN LUÔN dùng ID trước, chỉ fallback name khi thực sự cần
        if (!this.groupInfo.id) {
          this.showNotification('Thiếu Group ID để tải thành viên', 'error');
          return;
        }
        const url = `${API_BASE_URL}/groups/${this.groupInfo.id}/members`;
        
        const response = await fetch(url);
        const result = await response.json();
        
        if (result.success) {
          this.members = result.members || [];
        } else {
          this.members = [];
          this.showNotification(result.message || 'Không thể tải danh sách thành viên', 'error');
        }
        
      } catch (error) {
        this.members = [];
        this.showNotification('Không thể kết nối tới server', 'error');
      } finally {
        this.isLoadingMembers = false;
      }
    },
    
    openInviteMember() {
      const groupCode = this.groupInfo.code;
      const inviteMessage = `🎉 Bạn được mời tham gia nhóm "${this.groupInfo.name}"!\n\n` +
                           `📋 Mã nhóm: ${groupCode}\n\n` +
                           `💡 Hướng dẫn:\n` +
                           `1. Mở app Cơm Bà Giang\n` +
                           `2. Chọn "Nhóm" → "Tham gia"\n` +
                           `3. Nhập mã: ${groupCode}`;
      
      navigator.clipboard.writeText(inviteMessage).then(() => {
        this.showNotification(`Đã copy thông tin mời!\nMã nhóm: ${groupCode}`, 'success');
      }).catch(() => {
        this.showNotification(`Mã nhóm: ${groupCode}`, 'info');
      });
    },
    
    async removeMember(memberId, memberName) {
      this.memberToDelete = {
        id: memberId,
        name: memberName
      };
      this.showDeleteModal = true;
    },
    
    cancelDelete() {
      this.showDeleteModal = false;
      this.memberToDelete = {
        id: null,
        name: ''
      };
    },
    
    async confirmDelete() {
      this.isDeleting = true;
      
      try {
        if (!this.groupInfo.id) {
          this.showNotification('Thiếu Group ID để xóa thành viên', 'error');
          return;
        }
        
        const response = await fetch(`${API_BASE_URL}/groups/${this.groupInfo.id}/members/${this.memberToDelete.id}`, {
          method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
          this.showNotification(`Đã loại ${this.memberToDelete.name} khỏi nhóm`, 'success');
          await this.loadMembers();
          this.calculateGroupStats();
        } else {
          this.showNotification(result.message || 'Không thể loại thành viên', 'error');
        }
        
      } catch (error) {
        this.showNotification('Không thể kết nối tới server', 'error');
      } finally {
        this.isDeleting = false;
        this.showDeleteModal = false;
        this.memberToDelete = {
          id: null,
          name: ''
        };
      }
    },

    // ============ ORDERS MANAGEMENT ============
    async loadOrders() {
      this.isLoadingOrders = true;
      
      try {
        if (!this.groupInfo.id) {
          this.showNotification('Thiếu Group ID để tải đơn hàng', 'error');
          return;
        }
        
        const response = await fetch(`${API_BASE_URL}/groups/${this.groupInfo.id}/orders`);
        const result = await response.json();
        
        if (result.success) {
          this.orders = result.orders || [];
          this.filterOrders();
        } else {
          this.orders = [];
          this.filteredOrders = [];
          this.showNotification(result.message || 'Không thể tải danh sách đơn hàng', 'error');
        }
        
      } catch (error) {
        this.orders = [];
        this.filteredOrders = [];
        this.showNotification('Không thể kết nối tới server', 'error');
      } finally {
        this.isLoadingOrders = false;
      }
    },
    
    filterOrders() {
      let filtered = [...this.orders];
      const now = new Date();
      
      switch (this.orderFilter) {
        case 'today':
          const today = now.toISOString().split('T')[0];
          filtered = filtered.filter(order => order.date === today);
          break;
          
        case 'week':
          const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
          const weekAgoStr = weekAgo.toISOString().split('T')[0];
          const todayStr = now.toISOString().split('T')[0];
          filtered = filtered.filter(order => order.date >= weekAgoStr && order.date <= todayStr);
          break;
          
        case 'month':
          const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
          const monthAgoStr = monthAgo.toISOString().split('T')[0];
          const nowStr = now.toISOString().split('T')[0];
          filtered = filtered.filter(order => order.date >= monthAgoStr && order.date <= nowStr);
          break;
      }
      
      filtered.sort((a, b) => {
        const dateTimeA = new Date(a.date + ' ' + a.time);
        const dateTimeB = new Date(b.date + ' ' + b.time);
        return dateTimeB - dateTimeA;
      });
      
      this.filteredOrders = filtered;
    },
    
    async refreshOrders() {
      await this.loadOrders();
      this.calculateGroupStats();
      this.showNotification('Đã tải lại danh sách đơn hàng', 'success');
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

    // ============ PAYMENTS MANAGEMENT ============
    async loadPayments() {
      this.isLoadingPayments = true;
      
      try {
        if (!this.groupInfo.id) {
          this.showNotification('Thiếu Group ID để tải thanh toán', 'error');
          return;
        }
        
        const response = await fetch(`${API_BASE_URL}/groups/${this.groupInfo.id}/payments?period=${this.paymentFilter}`);
        const result = await response.json();
        
        if (result.success) {
          this.payments = result.payments || [];
          this.paymentSummary = result.summary || {
            totalAmount: 0,
            paidAmount: 0,
            remainingAmount: 0
          };
          this.filterPayments();
        } else {
          this.payments = [];
          this.filteredPayments = [];
          this.paymentSummary = {
            totalAmount: 0,
            paidAmount: 0,
            remainingAmount: 0
          };
          this.showNotification(result.message || 'Không thể tải thông tin thanh toán', 'error');
        }
        
      } catch (error) {
        this.payments = [];
        this.filteredPayments = [];
        this.paymentSummary = {
          totalAmount: 0,
          paidAmount: 0,
          remainingAmount: 0
        };
        this.showNotification('Không thể kết nối tới server', 'error');
      } finally {
        this.isLoadingPayments = false;
      }
    },
    
    filterPayments() {
      this.filteredPayments = [...this.payments];
      this.filteredPayments.sort((a, b) => b.remainingAmount - a.remainingAmount);
    },
    
    async refreshPayments() {
      await this.loadPayments();
      this.showNotification('Đã tải lại thông tin thanh toán', 'success');
    }
    
  }, // Kết thúc methods
  
  // ============ LIFECYCLE HOOKS ============
  async mounted() {
    if (window.location.hash) {
      const tab = window.location.hash.substring(1);
      if (['members', 'orders', 'payments'].includes(tab)) {
        this.activeTab = tab;
      }
    }
    
    await this.loadAllData();
  },
  
  watch: {
    activeTab(newTab) {
      window.location.hash = newTab;
    }
  }

}