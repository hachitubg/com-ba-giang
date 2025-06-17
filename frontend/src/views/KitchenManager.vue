<template>
  <!-- Simple Admin Login Screen -->
  <div v-if="!isAdminAuthenticated" class="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-pink-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl max-w-sm w-full p-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-gradient-to-r from-red-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
        </div>
        <h1 class="text-xl font-bold text-gray-800">Admin Panel</h1>
        <p class="text-sm text-gray-600">Cơm Bà Giang</p>
      </div>

      <!-- Error message -->
      <div v-if="adminAuthError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-sm text-red-700">{{ adminAuthError }}</p>
      </div>

      <!-- Admin Code Input -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Mã Admin</label>
        <input v-model="adminPassword" 
               type="password" 
               placeholder="Nhập mã admin"
               @keyup.enter="authenticateAdmin"
               :disabled="isCheckingAdmin"
               class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 disabled:bg-gray-100">
      </div>

      <!-- Login Button -->
      <button @click="authenticateAdmin" 
              :disabled="!adminPassword.trim() || isCheckingAdmin"
              :class="['w-full py-3 rounded-lg font-medium transition-colors',
                      (!adminPassword.trim() || isCheckingAdmin) ? 
                      'bg-gray-300 text-gray-500 cursor-not-allowed' : 
                      'bg-red-500 hover:bg-red-600 text-white']">
        <span v-if="isCheckingAdmin">Đang kiểm tra...</span>
        <span v-else>Truy cập</span>
      </button>

      <!-- Back to User Site -->
      <div class="text-center mt-4">
        <button @click="goToUserSite" class="text-sm text-blue-500 hover:text-blue-600">
          ← Quay lại trang chính
        </button>
      </div>
    </div>
  </div>

  <div v-else class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 pb-20">
    <!-- Fixed Header -->
    <header class="fixed top-0 left-0 right-0 z-40 bg-white shadow-lg border-b border-gray-100">
      <div class="px-4 py-4">
        <div class="flex justify-between items-center">
          <div class="flex-1">
            <div class="flex items-center mb-1">
              <div class="w-8 h-8 bg-gradient-to-r from-orange-400 to-red-500 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
              </div>
              <div>
                <h1 class="text-lg font-bold bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
                  Admin - Cơm Bà Giang
                </h1>
                <p class="text-xs text-gray-500">Quản lý đơn hàng và menu</p>
              </div>
            </div>
          </div>
          
          <div class="text-right">
            <p class="text-xs text-gray-600 mb-1">{{ today }}</p>
            <button @click="goToUserSite" 
                    class="text-xs bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded-full transition-colors">
              <svg class="w-3 h-3 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Fixed Bottom Tab Navigation -->
    <div class="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-2xl">
      <div class="grid grid-cols-5 h-16">
        <button @click="activeTab = 'orders'" 
                :class="['flex flex-col items-center justify-center p-2 transition-colors',
                         activeTab === 'orders' ? 'text-blue-600 bg-blue-50' : 'text-gray-500 hover:text-gray-700']">
          <svg class="w-5 h-5 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <span class="text-xs font-medium">Đơn hàng</span>
        </button>
        
        <button @click="activeTab = 'menu'" 
                :class="['flex flex-col items-center justify-center p-2 transition-colors',
                         activeTab === 'menu' ? 'text-green-600 bg-green-50' : 'text-gray-500 hover:text-gray-700']">
          <svg class="w-5 h-5 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
          <span class="text-xs font-medium">Menu</span>
        </button>
        
        <button @click="activeTab = 'payments'" 
                :class="['flex flex-col items-center justify-center p-2 transition-colors',
                         activeTab === 'payments' ? 'text-purple-600 bg-purple-50' : 'text-gray-500 hover:text-gray-700']">
          <svg class="w-5 h-5 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
          </svg>
          <span class="text-xs font-medium">Thanh toán</span>
        </button>
        
        <button @click="activeTab = 'groups'" 
                :class="['flex flex-col items-center justify-center p-2 transition-colors',
                         activeTab === 'groups' ? 'text-indigo-600 bg-indigo-50' : 'text-gray-500 hover:text-gray-700']">
          <svg class="w-5 h-5 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          <span class="text-xs font-medium">Nhóm</span>
        </button>
        
        <button @click="activeTab = 'feedback'" 
                :class="['flex flex-col items-center justify-center p-2 transition-colors',
                         activeTab === 'feedback' ? 'text-orange-600 bg-orange-50' : 'text-gray-500 hover:text-gray-700']">
          <svg class="w-5 h-5 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          <span class="text-xs font-medium">Góp ý</span>
        </button>
      </div>
    </div>

    <!-- Main Content with padding for fixed header/footer -->
    <div class="pt-20 px-4">
      <!-- Orders Tab -->
      <div v-if="activeTab === 'orders'">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-gray-900 flex items-center">
            <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            Quản lý đơn hàng
          </h3>
          <div class="text-right">
            <div class="text-sm font-bold text-gray-900">{{ filteredOrders.length }} đơn</div>
            <div class="text-xs text-gray-500">Mới nhất lên đầu</div>
          </div>
        </div>

        <!-- Quick Filters -->
        <div class="mb-4">
          <div class="flex space-x-2 overflow-x-auto pb-2">
            <button @click="orderQuickFilter = 'today'; applyOrderQuickFilter()" 
                    :class="['flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors',
                             orderQuickFilter === 'today' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200']">
              Hôm nay
            </button>
            <button @click="orderQuickFilter = 'week'; applyOrderQuickFilter()" 
                    :class="['flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors',
                             orderQuickFilter === 'week' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200']">
              Tuần này
            </button>
            <button @click="orderQuickFilter = 'month'; applyOrderQuickFilter()" 
                    :class="['flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors',
                             orderQuickFilter === 'month' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200']">
              Tháng này
            </button>
            <button @click="loadOrders()" 
                    class="flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium bg-green-100 text-green-700 hover:bg-green-200 transition-colors">
              <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Status Stats -->
        <div class="grid grid-cols-4 gap-2 mb-4">
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-yellow-800">{{ orderStats.pending }}</div>
            <div class="text-xs text-yellow-600">Đã đặt</div>
          </div>
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-blue-800">{{ orderStats.preparing }}</div>
            <div class="text-xs text-blue-600">Đang giao</div>
          </div>
          <div class="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-green-800">{{ orderStats.completed }}</div>
            <div class="text-xs text-green-600">Hoàn thành</div>
          </div>
          <div class="bg-red-50 border border-red-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-red-800">{{ orderStats.cancelled }}</div>
            <div class="text-xs text-red-600">Đã hủy</div>
          </div>
        </div>

        <!-- Advanced Filters (Collapsible) -->
        <div class="mb-4">
          <button @click="showAdvancedFilters = !showAdvancedFilters" 
                  class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center">
            <svg :class="['w-4 h-4 mr-2 transition-transform', showAdvancedFilters ? 'rotate-180' : '']" 
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
            Bộ lọc nâng cao
          </button>
          
          <div v-if="showAdvancedFilters" class="mt-3 space-y-3 bg-gray-50 rounded-lg p-4">
            <div class="grid grid-cols-2 gap-3">
              <select v-model="orderStatusFilter" @change="filterOrders" 
                      class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="all">Tất cả trạng thái</option>
                <option value="pending">Đã đặt</option>
                <option value="preparing">Đang giao</option>
                <option value="completed">Hoàn thành</option>
                <option value="cancelled">Đã hủy</option>
              </select>
              
              <select v-model="orderGroupFilter" @change="filterOrders" 
                      class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="all">Tất cả nhóm</option>
                <option value="personal">Đơn cá nhân</option>
                <option v-for="group in groups" :key="group.id" :value="group.name">
                  {{ group.name }}
                </option>
              </select>
            </div>
            
            <div v-if="orderQuickFilter === 'custom'" class="grid grid-cols-2 gap-3">
              <input v-model="orderStartDate" type="date" 
                     class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <input v-model="orderEndDate" type="date" 
                     class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
            </div>
          </div>
        </div>

        <!-- Orders List -->
        <div class="space-y-3">
          <div v-for="order in paginatedOrders" :key="`${order.date}-${order.id}`"
              :class="['rounded-xl border p-4 shadow-sm',
                        order.status === 'cancelled' ? 'bg-red-50 border-red-200' : 
                        order.quantity > 1 ? 'bg-amber-50 border-amber-200' :
                        order.note ? 'bg-blue-50 border-blue-200' :
                        'bg-white border-gray-200']">                  
            
            <!-- Order Header -->
            <div class="flex justify-between items-start mb-3">
              <div class="flex-1">
                <div class="flex items-center space-x-2 mb-2">
                  <span class="font-bold text-gray-900">Số: {{ order.sequentialNumber }}</span>
                  <span :class="['px-2 py-1 rounded-full text-xs font-medium',
                                order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                                order.status === 'preparing' ? 'bg-blue-100 text-blue-800' :
                                order.status === 'completed' ? 'bg-green-100 text-green-800' :
                                'bg-red-100 text-red-800']">
                    {{ getStatusText(order.status) }}
                  </span>
                </div>
                
                <!-- Essential Info: Customer Name - Group -->
                <div class="text-sm">
                  <span class="font-semibold text-gray-900">{{ order.user_name }}</span>
                  <span class="text-gray-500 mx-2">-</span>
                  <span class="font-medium text-blue-600">{{ order.group_name || 'Cá nhân' }}</span>
                </div>
              </div>
              
              <!-- Price + Quantity + Expand Button -->
              <div class="text-right ml-4">
                <div :class="['text-lg font-bold mb-2',
                              order.status === 'cancelled' ? 'text-red-600 line-through' : 'text-blue-600']">
                  {{ order.quantity }} suất - {{ order.total_amount.toLocaleString() }}đ
                </div>
                <button @click="toggleOrderDetails(order)" 
                        class="text-xs text-gray-500 hover:text-blue-600 transition-colors flex items-center">
                  <svg :class="['w-4 h-4 mr-1 transition-transform', 
                                isOrderExpanded(order) ? 'rotate-180' : '']" 
                      fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                  {{ isOrderExpanded(order) ? 'Ẩn' : 'Chi tiết' }}
                </button>
              </div>
            </div>
            

            
            <!-- Note Section - Always visible if exists -->
            <div v-if="order.note" class="mb-3 bg-amber-50 border-l-4 border-amber-400 p-3 rounded-r-lg">
              <div class="flex items-start space-x-2">
                <svg class="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
                <div class="flex-1">
                  <p class="text-xs font-semibold text-amber-800 mb-1">📝 Ghi chú:</p>
                  <p class="text-sm text-amber-700 font-medium leading-relaxed">{{ order.note }}</p>
                </div>
              </div>
            </div>
            
            <!-- Expandable Details - CLEAN & SIMPLE -->
            <div v-if="isOrderExpanded(order)" class="mb-3 bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h5 class="text-sm font-semibold text-gray-800 mb-3">Chi tiết đơn hàng</h5>
              
              <div class="space-y-3 text-sm">
                <!-- Số điện thoại -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Số điện thoại:</span>
                  <span class="font-medium">{{ order.user_phone || 'Chưa có số điện thoại' }}</span>
                </div>
                
                <!-- Tổng tiền -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Tổng tiền:</span>
                  <span class="font-medium">{{ order.quantity }} x {{ order.meal_type }}</span>
                </div>
                
                <!-- Giờ đặt -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Giờ đặt:</span>
                  <span class="font-medium">{{ order.created_at }}</span>
                </div>
                
                <!-- Ngày đặt -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Ngày đặt:</span>
                  <span class="font-medium">{{ formatOrderDate(order.date) }}</span>
                </div>
                
                <!-- Nhóm -->
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Nhóm:</span>
                  <span class="font-medium">{{ order.group_name || 'Cá nhân' }}</span>
                </div>
                
                <!-- Địa chỉ -->
                <div class="flex justify-between items-start">
                  <span class="text-gray-600">Địa chỉ:</span>
                  <span class="font-medium text-right max-w-xs">
                    {{ order.group_name ? (order.group_address || 'Chưa có địa chỉ nhóm') : (order.user_address || 'Chưa có địa chỉ cá nhân') }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Status Update -->
            <div v-if="order.status !== 'cancelled'" class="mt-3 pt-3 border-t border-gray-100">
              <select @change="updateOrderStatus(order, $event.target.value)"
                      :value="order.status"
                      class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="pending">Đã đặt</option>
                <option value="preparing">Đang giao</option>
                <option value="completed">Hoàn thành</option>
              </select>
            </div>
            
          </div>

          <!-- Empty State -->
          <div v-if="filteredOrders.length === 0" class="text-center py-8">
            <div class="text-4xl mb-2">📭</div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Không có đơn hàng</h3>
            <p class="text-gray-500">Chưa có đơn hàng nào trong khoảng thời gian đã chọn</p>
          </div>

          <!-- Pagination -->
          <div v-if="filteredOrders.length > ordersPerPage" class="flex justify-center items-center space-x-2 mt-4">
            <button @click="currentOrdersPage = Math.max(1, currentOrdersPage - 1)"
                    :disabled="currentOrdersPage === 1"
                    class="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50">
              ‹ Trước
            </button>
            <span class="px-3 py-2 text-sm bg-blue-500 text-white rounded-lg">
              {{ currentOrdersPage }} / {{ totalOrdersPages }}
            </span>
            <button @click="currentOrdersPage = Math.min(totalOrdersPages, currentOrdersPage + 1)"
                    :disabled="currentOrdersPage === totalOrdersPages"
                    class="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50">
              Sau ›
            </button>
          </div>
        </div>

      </div>

      <!-- Menu Tab -->
      <div v-if="activeTab === 'menu'">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-gray-900 flex items-center">
            <svg class="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
            Quản lý menu
          </h3>
          <button @click="openMenuItemModal()" 
                  class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            Thêm món
          </button>
        </div>
        
        <!-- Date & Deadline -->
        <div class="bg-white rounded-xl p-4 mb-4 shadow-sm border border-gray-200">
          <h4 class="font-semibold text-gray-800 mb-3 flex items-center">
            <svg class="w-4 h-4 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z"/>
            </svg>
            Thiết lập menu
          </h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Ngày</label>
              <input v-model="menuForm.date" type="date" 
                     class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Deadline</label>
              <input v-model="menuForm.deadline" type="time" 
                     class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
          </div>
        </div>

        <!-- Menu Items List -->
        <div class="mb-4">
          <h4 class="font-semibold text-gray-800 mb-3 flex items-center">
            <svg class="w-4 h-4 mr-2 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
            </svg>
            Danh sách món ăn
          </h4>
          
          <div class="space-y-3">
            <div v-for="(item, index) in menuForm.menu_items" :key="index" 
                 class="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h5 class="font-semibold text-gray-800 text-lg">{{ item.name || 'Chưa đặt tên' }}</h5>
                  <p class="text-2xl font-bold text-blue-600 my-1">{{ formatPrice(item.price) }}</p>
                  <p class="text-sm text-gray-600 whitespace-pre-line leading-relaxed">{{ item.description || 'Chưa có mô tả' }}</p>
                </div>
                
                <div class="flex space-x-2 ml-4">
                  <button @click="openMenuItemModal(item, index)" 
                          class="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-lg">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button @click="removeMenuItem(index)" 
                          v-if="menuForm.menu_items.length > 1"
                          class="bg-red-500 hover:bg-red-600 text-white p-2 rounded-lg">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            
            <div v-if="menuForm.menu_items.length === 0" class="text-center py-8 text-gray-500">
              <div class="text-4xl mb-2">🍽️</div>
              <p>Chưa có món ăn nào. Nhấn "Thêm món" để bắt đầu.</p>
            </div>
          </div>
        </div>

        <!-- Toppings -->
        <div class="bg-white rounded-xl p-4 mb-4 shadow-sm border border-gray-200">
          <h4 class="font-semibold text-gray-800 mb-3 flex items-center">
            <svg class="w-4 h-4 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"/>
            </svg>
            Topping có sẵn
          </h4>
          <textarea v-model="menuForm.toppings" 
                    placeholder="VD: Trứng ốp la (+5k), Chả cá thêm (+3k), Rau củ tươi (free)"
                    rows="3"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"></textarea>
        </div>

        <!-- Actions -->
        <div class="flex space-x-3">
          <button @click="saveMenu" 
                  class="flex-1 bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-lg transition-colors">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
            </svg>
            Lưu menu
          </button>
          <button @click="loadTodayMenu" 
                  class="flex-1 bg-gray-500 hover:bg-gray-600 text-white font-semibold py-3 rounded-lg transition-colors">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Tải menu
          </button>
        </div>
      </div>
      <!-- Payments Tab -->
      <div v-if="activeTab === 'payments'">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-gray-900 flex items-center">
            <svg class="w-5 h-5 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
            </svg>
            Thanh toán
          </h3>
          <button @click="refreshPayments" 
                  class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Tải lại
          </button>
        </div>

        <!-- Filters -->
        <div class="mb-4">
          <div class="flex space-x-2 overflow-x-auto pb-2">
            <select v-model="paymentFilter" @change="refreshPayments" 
                    class="flex-shrink-0 border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="current">Tháng này</option>
              <option value="last">Tháng trước</option>
              <option value="all">Tất cả</option>
            </select>
            
            <select v-model="paymentGroupFilter" @change="filterPayments" 
                    class="flex-shrink-0 border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="all">Tất cả nhóm</option>
              <option value="personal">Khách lẻ</option>
              <option v-for="group in groups" :key="group.id" :value="group.name">
                {{ group.name }}
              </option>
            </select>
            
            <select v-model="paymentStatusFilter" @change="filterPayments" 
                    class="flex-shrink-0 border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="all">Tất cả</option>
              <option value="paid">Đã thanh toán</option>
              <option value="pending">Chưa thanh toán</option>
            </select>
          </div>
        </div>

        <!-- Payment Summary -->
        <div class="grid grid-cols-3 gap-3 mb-4">
          <div class="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-green-800">{{ (paymentStats.paid || 0).toLocaleString() }}k</div>
            <div class="text-xs text-green-600">Đã thu</div>
          </div>
          
          <div class="bg-red-50 border border-red-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-red-800">{{ (paymentStats.pending || 0).toLocaleString() }}k</div>
            <div class="text-xs text-red-600">Chưa thu</div>
          </div>
          
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-blue-800">{{ (paymentStats.total || 0).toLocaleString() }}k</div>
            <div class="text-xs text-blue-600">Tổng</div>
          </div>
        </div>

        <!-- Payments List -->
        <div class="space-y-3">
          <div v-for="payment in filteredPayments" :key="payment.user_id" 
               class="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
            
            <!-- Header -->
            <div class="flex justify-between items-center mb-3">
              <div>
                <h5 class="font-semibold text-gray-900">{{ payment.user_name }}</h5>
                <span :class="['px-2 py-1 rounded-full text-xs font-medium',
                               payment.group_name ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600']">
                  {{ payment.group_name || 'Cá nhân' }}
                </span>
              </div>
              <div class="text-right">
                <div class="text-lg font-bold text-gray-900">{{ payment.total_amount.toLocaleString() }}k</div>
                <div class="text-xs text-gray-600">{{ payment.total_orders }} đơn</div>
              </div>
            </div>
            
            <!-- Payment Status -->
            <div class="grid grid-cols-2 gap-3 mb-3">
              <div class="bg-green-50 rounded-lg p-2 text-center">
                <div class="text-sm font-bold text-green-800">{{ payment.paid_amount.toLocaleString() }}k</div>
                <div class="text-xs text-green-600">Đã thanh toán</div>
              </div>
              
              <div :class="['rounded-lg p-2 text-center',
                            payment.remaining_amount > 0 ? 'bg-red-50' : 'bg-green-50']">
                <div :class="['text-sm font-bold',
                              payment.remaining_amount > 0 ? 'text-red-800' : 'text-green-800']">
                  {{ payment.remaining_amount.toLocaleString() }}k
                </div>
                <div :class="['text-xs',
                              payment.remaining_amount > 0 ? 'text-red-600' : 'text-green-600']">
                  {{ payment.remaining_amount > 0 ? 'Còn lại' : 'Hoàn thành' }}
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="flex space-x-2">
              <button v-if="payment.remaining_amount > 0" 
                      @click="markAsPaid(payment.user_id, payment.remaining_amount)"
                      class="flex-1 bg-green-500 hover:bg-green-600 text-white py-2 rounded-lg text-sm font-medium">
                Đã thanh toán
              </button>
              <button @click="viewPaymentHistory(payment.user_id)"
                      class="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg text-sm font-medium">
                Lịch sử
              </button>
            </div>
          </div>

          <div v-if="filteredPayments.length === 0" class="text-center py-8 text-gray-500">
            <div class="text-4xl mb-2">💳</div>
            <p>Không có dữ liệu thanh toán</p>
          </div>
        </div>
      </div>

      <!-- Groups Tab -->
      <div v-if="activeTab === 'groups'">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-gray-900 flex items-center">
            <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
            Quản lý nhóm
          </h3>
          <button @click="refreshGroups" 
                  class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Tải lại
          </button>
        </div>

        <!-- Groups List -->
        <div class="space-y-3">
          <div v-for="group in allGroups" :key="group.id" 
               class="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
            
            <!-- Group Header -->
            <div class="flex justify-between items-start mb-3">
              <div class="flex-1">
                <h5 class="font-bold text-gray-900 text-lg">{{ group.name }}</h5>
                <div class="text-sm text-gray-600 mt-1">
                  <p><strong>Mã:</strong> <span class="font-mono bg-gray-100 px-2 py-1 rounded">{{ group.code }}</span></p>
                  <p><strong>Trưởng nhóm:</strong> {{ group.leader_name }}</p>
                </div>
              </div>
              
              <div class="text-right">
                <div class="text-lg font-bold text-indigo-600">{{ group.member_count }}</div>
                <div class="text-xs text-gray-600">thành viên</div>
              </div>
            </div>
            
            <!-- Group Address -->
            <div class="bg-gray-50 rounded-lg p-3 mb-3">
              <p class="text-sm text-gray-700">
                <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                {{ group.address }}
              </p>
            </div>
            
            <!-- Actions -->
            <div class="flex space-x-2">
              <button @click="viewGroupDetails(group.id)"
                      class="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg text-sm font-medium">
                Chi tiết
              </button>
              <button @click="deleteGroup(group.id)"
                      class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>

          <div v-if="allGroups.length === 0" class="text-center py-8 text-gray-500">
            <div class="text-4xl mb-2">👥</div>
            <p>Chưa có nhóm nào trong hệ thống</p>
          </div>
        </div>
      </div>

      <!-- Feedback Tab -->
      <div v-if="activeTab === 'feedback'">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-gray-900 flex items-center">
            <svg class="w-5 h-5 mr-2 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
            Góp ý
          </h3>
          <button @click="refreshFeedback" 
                  class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Tải lại
          </button>
        </div>

        <!-- Feedback Summary -->
        <div class="grid grid-cols-4 gap-2 mb-4">
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-blue-800">{{ feedbackStats.total }}</div>
            <div class="text-xs text-blue-600">Tổng</div>
          </div>
          
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-yellow-800">{{ feedbackStats.avgRating }}</div>
            <div class="text-xs text-yellow-600">Đánh giá TB</div>
          </div>
          
          <div class="bg-red-50 border border-red-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-red-800">{{ feedbackStats.unread }}</div>
            <div class="text-xs text-red-600">Chưa đọc</div>
          </div>
          
          <div class="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
            <div class="text-lg font-bold text-green-800">{{ feedbackStats.resolved }}</div>
            <div class="text-xs text-green-600">Đã xử lý</div>
          </div>
        </div>

        <!-- Filters -->
        <div class="mb-4">
          <div class="flex space-x-2 overflow-x-auto pb-2">
            <select v-model="feedbackCategoryFilter" @change="filterFeedback" 
                    class="flex-shrink-0 border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="all">Tất cả loại</option>
              <option value="general">Chung</option>
              <option value="food">Món ăn</option>
              <option value="service">Dịch vụ</option>
              <option value="delivery">Giao hàng</option>
              <option value="price">Giá cả</option>
            </select>
            
            <select v-model="feedbackRatingFilter" @change="filterFeedback" 
                    class="flex-shrink-0 border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="all">Tất cả đánh giá</option>
              <option value="5">5 sao</option>
              <option value="4">4 sao</option>
              <option value="3">3 sao</option>
              <option value="2">2 sao</option>
              <option value="1">1 sao</option>
              <option value="0">Chưa đánh giá</option>
            </select>
            
            <select v-model="feedbackStatusFilter" @change="filterFeedback" 
                    class="flex-shrink-0 border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="all">Tất cả trạng thái</option>
              <option value="new">Mới</option>
              <option value="read">Đã đọc</option>
              <option value="resolved">Đã xử lý</option>
            </select>
          </div>
        </div>
        <!-- Feedback List -->
        <div class="space-y-4">
          <div v-for="feedback in filteredFeedback" :key="feedback.id" 
               :class="['bg-white rounded-xl border p-4 shadow-sm',
                        feedback.status === 'new' ? 'border-red-200 bg-red-50' : 
                        feedback.status === 'read' ? 'border-yellow-200 bg-yellow-50' : 
                        'border-green-200 bg-green-50']">
            
            <!-- Feedback Header -->
            <div class="flex justify-between items-start mb-3">
              <div class="flex items-center space-x-2">
                <span class="font-bold text-gray-900">#{{ feedback.id }}</span>
                <span :class="['px-2 py-1 rounded-full text-xs font-medium',
                              getCategoryClass(feedback.category)]">
                  {{ getCategoryText(feedback.category) }}
                </span>
                <span :class="['px-2 py-1 rounded-full text-xs font-medium',
                              getStatusClass(feedback.status)]">
                  {{ getFeedbackStatusText(feedback.status) }}
                </span>
              </div>
              
              <div v-if="feedback.rating" class="flex">
                <span v-for="star in 5" :key="star" 
                      :class="star <= feedback.rating ? 'text-yellow-400' : 'text-gray-300'">
                  ⭐
                </span>
              </div>
            </div>
            
            <!-- Feedback Content -->
            <div class="mb-3">
              <p class="text-gray-800 leading-relaxed">{{ feedback.feedback_text }}</p>
            </div>
            
            <!-- Footer -->
            <div class="flex justify-between items-center text-sm text-gray-500 mb-3">
              <span>{{ formatDate(feedback.created_at) }}</span>
            </div>

            <!-- Actions -->
            <div class="flex space-x-2">
              <button v-if="feedback.status === 'new'" 
                      @click="markFeedbackAsRead(feedback.id)"
                      class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded-lg text-sm font-medium">
                Đánh dấu đã đọc
              </button>
              <button v-if="feedback.status !== 'resolved'" 
                      @click="markFeedbackAsResolved(feedback.id)"
                      class="bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded-lg text-sm font-medium">
                Đã xử lý
              </button>
              <button @click="deleteFeedback(feedback.id)"
                      class="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded-lg text-sm font-medium">
                Xóa
              </button>
            </div>
          </div>

          <div v-if="filteredFeedback.length === 0" class="text-center py-8 text-gray-500">
            <div class="text-4xl mb-2">💬</div>
            <p>Không có góp ý nào phù hợp với bộ lọc</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Payment History Modal -->
    <div v-if="showPaymentHistory" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
      <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-2xl max-h-[90vh] overflow-hidden transform transition-all duration-300 animate-slide-up">
        <div class="relative p-6 border-b border-gray-100">
          <div class="text-center">
            <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800">Lịch sử thanh toán</h3>
            <p class="text-sm text-gray-600">{{ selectedUser.name }}</p>
          </div>
          <button @click="closePaymentHistory" 
                  class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto max-h-80">
          <div class="space-y-3">
            <div v-for="history in paymentHistory" :key="history.id" 
                 class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <div>
                <p class="font-medium text-gray-900">{{ history.amount.toLocaleString() }}k VNĐ</p>
                <p class="text-sm text-gray-600">{{ history.date }}</p>
              </div>
              <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                Đã thanh toán
              </span>
            </div>
            
            <div v-if="paymentHistory.length === 0" class="text-center text-gray-500 py-8">
              Chưa có lịch sử thanh toán
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Group Details Modal -->
    <div v-if="showGroupDetails" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
      <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-2xl max-h-[90vh] overflow-hidden transform transition-all duration-300 animate-slide-up">
        <div class="relative p-6 border-b border-gray-100">
          <div class="text-center">
            <div class="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800">Chi tiết nhóm</h3>
            <p class="text-sm text-gray-600">{{ selectedGroup.name }}</p>
          </div>
          <button @click="closeGroupDetails" 
                  class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto max-h-80">
          <div class="space-y-4">
            <!-- Group Info -->
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-gray-50 rounded-lg p-3">
                <p class="text-sm font-medium text-gray-700">Mã nhóm:</p>
                <p class="text-lg font-mono bg-gray-100 px-3 py-1 rounded mt-1">{{ selectedGroup.code }}</p>
              </div>
              <div class="bg-gray-50 rounded-lg p-3">
                <p class="text-sm font-medium text-gray-700">Trưởng nhóm:</p>
                <p class="text-lg font-semibold mt-1">{{ selectedGroup.leader_name }}</p>
              </div>
            </div>
            
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-sm font-medium text-gray-700">Địa chỉ giao hàng:</p>
              <p class="text-gray-900 mt-1">{{ selectedGroup.address }}</p>
            </div>
            
            <div v-if="selectedGroup.description" class="bg-gray-50 rounded-lg p-3">
              <p class="text-sm font-medium text-gray-700">Mô tả:</p>
              <p class="text-gray-900 mt-1">{{ selectedGroup.description }}</p>
            </div>
            
            <!-- Members List -->
            <div>
              <p class="text-sm font-medium text-gray-700 mb-2">Thành viên ({{ selectedGroup.members.length }}):</p>
              <div class="space-y-2">
                <div v-for="member in selectedGroup.members" :key="member.id" 
                     class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p class="font-medium text-gray-900">{{ member.name }}</p>
                    <p class="text-sm text-gray-600">{{ member.identifier }}</p>
                  </div>
                  <span v-if="member.is_leader" class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                    Trưởng nhóm
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Menu Item Modal -->
    <div v-if="showMenuItemModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
      <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-md max-h-[90vh] overflow-hidden transform transition-all duration-300 animate-slide-up">
        <div class="relative p-6 border-b border-gray-100">
          <div class="text-center">
            <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800">
              {{ editingMenuItemIndex >= 0 ? 'Sửa món ăn' : 'Thêm món ăn' }}
            </h3>
          </div>
          <button @click="closeMenuItemModal" 
                  class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Tên món ăn</label>
            <input v-model="editingMenuItem.name" type="text" placeholder="VD: Suất tiêu chuẩn"
                   class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Giá (VNĐ)</label>
            <input v-model.number="editingMenuItem.price" type="number" placeholder="35000"
                   class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500">
            <div class="text-sm text-green-600 mt-1">
              Hiển thị: {{ formatPrice(editingMenuItem.price) }}
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Mô tả món ăn</label>
            <textarea v-model="editingMenuItem.description" rows="5" 
                      placeholder="VD: Cơm gà xào nấm + Canh chua + Rau luộc
                                  Món chính: Gà xào nấm đậm đà
                                  Canh: Canh chua cà chua tôm khô  
                                  Rau: Rau luộc chấm tương"
                      class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 resize-none whitespace-pre-wrap"></textarea>
          </div>
        </div>
        
        <div class="flex space-x-3 p-6 border-t border-gray-200">
          <button @click="closeMenuItemModal" 
                  class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 rounded-lg transition-colors">
            Hủy
          </button>
          <button @click="saveMenuItem" 
                  class="flex-1 bg-green-500 hover:bg-green-600 text-white font-medium py-2 rounded-lg transition-colors">
            {{ editingMenuItemIndex >= 0 ? 'Cập nhật' : 'Thêm' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
/* Smooth slide up animation */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(100%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}

/* Mobile specific improvements */
@media (max-width: 640px) {
  /* Better spacing for mobile */
  .p-6 {
    padding: 1rem;
  }
  
  /* Larger tap targets */
  .grid.grid-cols-5 button {
    min-height: 4rem;
  }
}

/* Smooth transitions for all interactive elements */
* {
  transition: all 0.2s ease;
}

/* Description formatting */
.whitespace-pre-line {
  white-space: pre-line;
}

.whitespace-pre-wrap {
  white-space: pre-wrap;
}

.menu-description {
  white-space: pre-line;
  line-height: 1.6;
  word-wrap: break-word;
}

/* Better textarea styling for multi-line input */
.description-textarea {
  white-space: pre-wrap;
  line-height: 1.5;
  font-family: inherit;
}

/* Menu card description styling */
.menu-card-description {
  white-space: pre-line;
  line-height: 1.5;
  max-height: 120px;
  overflow-y: auto;
}

/* Scrollbar cho description area */
.menu-card-description::-webkit-scrollbar {
  width: 4px;
}

.menu-card-description::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.menu-card-description::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.menu-card-description::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
</style>

<script>
import kitchenLogic from '../components/js/KitchenManager.js'

export default kitchenLogic
</script>