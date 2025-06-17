<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 pb-20">
    <!-- Fixed Header -->
    <header class="fixed top-0 left-0 right-0 z-40 bg-white shadow-lg border-b border-gray-100">
      <div class="px-4 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center">
            <button @click="goBack" 
                    class="w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center mr-3 transition-colors">
              <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
              </svg>
            </button>
            <div>
              <h1 class="text-lg font-bold text-gray-800">Quản lý nhóm</h1>
              <p class="text-sm text-gray-600">{{ groupInfo.name }}</p>
            </div>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-600">Mã nhóm</p>
            <p class="font-mono text-sm font-bold text-blue-600">{{ groupInfo.code }}</p>
          </div>
        </div>
      </div>
    </header>

    <!-- Notification -->
    <div v-if="notification.show" 
         class="fixed top-20 left-4 right-4 z-50 mx-auto max-w-md transform transition-all duration-300 ease-out">
      <div :class="['rounded-lg shadow-lg border-l-4 p-4 bg-white',
                    notification.type === 'success' ? 'border-green-500' :
                    notification.type === 'error' ? 'border-red-500' :
                    notification.type === 'warning' ? 'border-yellow-500' : 'border-blue-500']">
        <div class="flex items-start">
          <div :class="['flex-shrink-0 w-5 h-5 mr-3 mt-0.5',
                        notification.type === 'success' ? 'text-green-500' :
                        notification.type === 'error' ? 'text-red-500' :
                        notification.type === 'warning' ? 'text-yellow-500' : 'text-blue-500']">
            <svg v-if="notification.type === 'success'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <svg v-else-if="notification.type === 'error'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <svg v-else-if="notification.type === 'warning'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 1.371-1.24.588-1.81"/>
            </svg>
            <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="flex-1">
            <p :class="['text-sm font-medium leading-relaxed',
                        notification.type === 'success' ? 'text-green-800' :
                        notification.type === 'error' ? 'text-red-800' :
                        notification.type === 'warning' ? 'text-yellow-800' : 'text-blue-800']">
              {{ notification.message }}
            </p>
          </div>
          <button @click="hideNotification" 
                  class="flex-shrink-0 ml-3 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white rounded-xl shadow-2xl mx-4 w-full max-w-md transform transition-all">
        <div class="p-6">
          <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 1.371-1.24.588-1.81"/>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">Xác nhận loại thành viên</h3>
              <p class="text-sm text-gray-600">Thao tác này không thể hoàn tác</p>
            </div>
          </div>
          
          <div class="mb-6">
            <p class="text-gray-700">
              Bạn có chắc chắn muốn loại <span class="font-semibold text-red-600">{{ memberToDelete.name }}</span> 
              khỏi nhóm không?
            </p>
          </div>
          
          <div class="flex space-x-3">
            <button @click="cancelDelete" 
                    class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 py-3 px-4 rounded-lg font-medium transition-colors">
              Hủy bỏ
            </button>
            <button @click="confirmDelete" 
                    :disabled="isDeleting"
                    class="flex-1 bg-red-500 hover:bg-red-600 disabled:bg-red-400 text-white py-3 px-4 rounded-lg font-medium transition-colors">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Loại khỏi nhóm</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content with top padding for fixed header -->
    <main class="pt-24 px-4">
      
      <!-- Overview Cards -->
      <div class="grid grid-cols-2 gap-4 mb-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Thành viên</p>
              <p class="text-2xl font-bold text-blue-600">{{ groupStats.memberCount }}</p>
            </div>
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2664ec" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users-icon lucide-users"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><path d="M16 3.128a4 4 0 0 1 0 7.744"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/></svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Đơn hàng hôm nay</p>
              <p class="text-2xl font-bold text-green-600">{{ groupStats.totalOrders }}</p>
            </div>
            <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-clock-icon lucide-file-clock"><path d="M16 22h2a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v3"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><circle cx="8" cy="16" r="6"/><path d="M9.5 17.5 8 16.25V14"/></svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Fixed Bottom Tab Navigation -->
      <div class="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-2xl">
        <div class="grid grid-cols-3 h-16">
          <button @click="activeTab = 'members'" 
                  :class="['flex flex-col items-center justify-center p-2 transition-colors',
                           activeTab === 'members' ? 'text-blue-600 bg-blue-50' : 'text-gray-500 hover:text-gray-700']">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users-icon lucide-users"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><path d="M16 3.128a4 4 0 0 1 0 7.744"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/></svg>
            <span class="text-xs font-medium">Thành viên</span>
          </button>
          
          <button @click="activeTab = 'orders'" 
                  :class="['flex flex-col items-center justify-center p-2 transition-colors',
                           activeTab === 'orders' ? 'text-green-600 bg-green-50' : 'text-gray-500 hover:text-gray-700']">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-clock-icon lucide-file-clock"><path d="M16 22h2a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v3"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><circle cx="8" cy="16" r="6"/><path d="M9.5 17.5 8 16.25V14"/></svg>
            <span class="text-xs font-medium">Đơn hàng</span>
          </button>
          
          <button @click="activeTab = 'payments'" 
                  :class="['flex flex-col items-center justify-center p-2 transition-colors',
                           activeTab === 'payments' ? 'text-purple-600 bg-purple-50' : 'text-gray-500 hover:text-gray-700']">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-credit-card-icon lucide-credit-card"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
            <span class="text-xs font-medium">Thanh toán</span>
          </button>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="pb-20">
        
        <!-- Members Tab -->
        <div v-if="activeTab === 'members'">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-bold text-gray-900">Quản lý thành viên</h3>
            <button @click="openInviteMember" 
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
              <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              Mời thành viên
            </button>
          </div>

          <!-- Members List -->
          <div class="space-y-3">
            <div v-for="member in members" :key="member.id" 
                 class="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
              <div class="flex justify-between items-start">
                <div class="flex items-center flex-1">
                  <div class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center mr-3">
                    <span class="text-sm font-medium text-gray-600">{{ member.name.charAt(0) }}</span>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center">
                      <h4 class="font-medium text-gray-900">{{ member.name }}</h4>
                      <span v-if="member.isLeader" class="ml-2 px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
                        👑 Trưởng nhóm
                      </span>
                    </div>
                    <p class="text-sm text-gray-600">{{ member.phone }}</p>
                    <p class="text-xs text-gray-500">Tham gia: {{ member.joinedAt }}</p>
                  </div>
                </div>
                <div class="flex items-center space-x-3">
                  <div class="text-right">
                    <p class="text-sm font-medium text-gray-900">{{ member.totalOrders }} đơn</p>
                    <p class="text-xs text-gray-600">{{ member.totalAmount.toLocaleString() }}đ</p>
                  </div>
                  <button v-if="!member.isLeader && currentUser.isLeader" 
                          @click="removeMember(member.id, member.name)"
                          class="w-8 h-8 bg-red-100 hover:bg-red-200 text-red-600 rounded-full flex items-center justify-center transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="members.length === 0" class="text-center py-8">
              <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857"/>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Chưa có thành viên</h3>
              <p class="text-gray-500 mb-4">Mời thêm người vào nhóm để bắt đầu</p>
              <button @click="openInviteMember" 
                      class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm">
                Mời thành viên đầu tiên
              </button>
            </div>
          </div>
        </div>

        <!-- Orders Tab -->
        <div v-if="activeTab === 'orders'">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-bold text-gray-900">Đơn hàng nhóm</h3>
            <div class="flex space-x-2">
              <select v-model="orderFilter" @change="filterOrders" 
                      class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="today">Hôm nay</option>
                <option value="week">Tuần này</option>
                <option value="month">Tháng này</option>
                <option value="all">Tất cả</option>
              </select>
              <button @click="refreshOrders" 
                      :disabled="isLoadingOrders"
                      class="bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white px-3 py-2 rounded-lg text-sm font-medium transition-colors">
                <svg v-if="isLoadingOrders" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Orders List -->
          <div class="space-y-3">
            <div v-for="order in filteredOrders" :key="order.id" 
                 class="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <div class="flex items-center mb-1">
                    <span class="font-bold text-gray-900">#{{ order.id }}</span>
                    <span :class="['ml-2 px-2 py-1 rounded-full text-xs font-medium',
                                  order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                                  order.status === 'preparing' ? 'bg-blue-100 text-blue-800' :
                                  order.status === 'completed' ? 'bg-green-100 text-green-800' :
                                  'bg-red-100 text-red-800']">
                      {{ getStatusText(order.status) }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600">{{ order.userName }}</p>
                  <p class="text-xs text-gray-500">{{ order.date }} - {{ order.time }}</p>
                </div>
                <div class="text-right">
                  <p class="font-bold text-blue-600">{{ order.totalAmount.toLocaleString() }}đ</p>
                  <p class="text-sm text-gray-600">{{ order.quantity }} x {{ order.mealType }}</p>
                </div>
              </div>
              <div v-if="order.note" class="bg-gray-50 rounded-lg p-2 mt-2">
                <p class="text-xs text-gray-700">📝 {{ order.note }}</p>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredOrders.length === 0" class="text-center py-8">
              <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6"/>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Chưa có đơn hàng</h3>
              <p class="text-gray-500">Các đơn hàng của nhóm sẽ hiển thị ở đây</p>
            </div>
          </div>
        </div>

        <!-- Payments Tab -->
        <div v-if="activeTab === 'payments'">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-bold text-gray-900">Thanh toán nhóm</h3>
            <select v-model="paymentFilter" @change="filterPayments" 
                    class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="current">Tháng này</option>
              <option value="last">Tháng trước</option>
              <option value="all">Tất cả</option>
            </select>
          </div>

          <!-- Payment Summary -->
          <div class="bg-gradient-to-r from-purple-50 to-indigo-50 border-2 border-purple-200 rounded-xl p-4 mb-4">
            <h4 class="font-semibold text-purple-800 mb-2">Tổng quan thanh toán</h4>
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <p class="text-lg font-bold text-purple-800">{{ paymentSummary.totalAmount.toLocaleString() }}đ</p>
                <p class="text-xs text-purple-600">Tổng tiền</p>
              </div>
              <div>
                <p class="text-lg font-bold text-green-700">{{ paymentSummary.paidAmount.toLocaleString() }}đ</p>
                <p class="text-xs text-green-600">Đã thanh toán</p>
              </div>
              <div>
                <p class="text-lg font-bold text-red-700">{{ paymentSummary.remainingAmount.toLocaleString() }}đ</p>
                <p class="text-xs text-red-600">Còn lại</p>
              </div>
            </div>
          </div>

          <!-- Members Payment List -->
          <div class="space-y-3">
            <div v-for="payment in filteredPayments" :key="payment.userId" 
                 class="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h4 class="font-medium text-gray-900">{{ payment.userName }}</h4>
                  <p class="text-sm text-gray-600">{{ payment.totalOrders }} đơn hàng</p>
                </div>
                <div class="text-right">
                  <p class="font-bold text-gray-900">{{ payment.totalAmount.toLocaleString() }}đ</p>
                  <div class="flex items-center space-x-2 mt-1">
                    <div class="flex-1 bg-gray-200 rounded-full h-2">
                      <div class="bg-green-500 h-2 rounded-full" 
                           :style="{ width: `${(payment.paidAmount / payment.totalAmount) * 100}%` }"></div>
                    </div>
                    <span class="text-xs text-gray-600">
                      {{ Math.round((payment.paidAmount / payment.totalAmount) * 100) }}%
                    </span>
                  </div>
                  <p class="text-xs text-gray-500">
                    Đã trả: {{ payment.paidAmount.toLocaleString() }}đ
                  </p>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredPayments.length === 0" class="text-center py-8">
              <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1"/>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Chưa có dữ liệu thanh toán</h3>
              <p class="text-gray-500">Thông tin thanh toán sẽ hiển thị ở đây</p>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script>
import groupManagementLogic from '../components/js/GroupManagement.js'

export default groupManagementLogic
</script>

<style scoped>
/* Smooth transitions for all interactive elements */
* {
  transition: all 0.2s ease;
}

/* Mobile specific improvements */
@media (max-width: 640px) {
  .p-6 {
    padding: 1rem;
  }
  
  .grid.grid-cols-3 button {
    min-height: 4rem;
  }
}
</style>