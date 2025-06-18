<template>

  <!-- Notification Toast -->
  <Transition
    name="notification"
    enter-active-class="transition-all duration-300 ease-out"
    leave-active-class="transition-all duration-200 ease-in"
    enter-from-class="opacity-0 -translate-y-4 scale-95"
    enter-to-class="opacity-100 translate-y-0 scale-100"
    leave-from-class="opacity-100 translate-y-0 scale-100"
    leave-to-class="opacity-0 -translate-y-4 scale-95"
  >
    <div v-if="systemNotification.show" 
         class="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-80 max-w-[90vw]">
      <div :class="['rounded-lg shadow-lg p-3 bg-white border-l-4',
                    systemNotification.type === 'success' ? 'border-green-500' :
                    systemNotification.type === 'error' ? 'border-red-500' :
                    systemNotification.type === 'warning' ? 'border-amber-500' : 'border-blue-500']">
        <div class="flex items-center gap-3">
          <!-- Dynamic Icon -->
          <div :class="['w-5 h-5 flex-shrink-0',
                        systemNotification.type === 'success' ? 'text-green-500' :
                        systemNotification.type === 'error' ? 'text-red-500' :
                        systemNotification.type === 'warning' ? 'text-amber-500' : 'text-blue-500']">
            <!-- Success Icon -->
            <svg v-if="systemNotification.type === 'success'" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>
            </svg>
            
            <!-- Error Icon -->
            <svg v-else-if="systemNotification.type === 'error'" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"/>
            </svg>
            
            <!-- Warning Icon -->
            <svg v-else-if="systemNotification.type === 'warning'" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"/>
            </svg>
            
            <!-- Info Icon -->
            <svg v-else fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"/>
            </svg>
          </div>
          
          <!-- Message -->
          <p class="text-sm text-gray-800 font-medium flex-1 whitespace-pre-line">
            {{ systemNotification.message }}
          </p>
          
          <!-- Close Button -->
          <button @click="hideSystemNotification" 
                  class="text-gray-400 hover:text-gray-600 transition-colors shrink-0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <!-- Login Screen -->
  <div v-if="!isLoggedIn" class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl max-w-sm w-full overflow-hidden">
      
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-500 to-indigo-600 px-8 py-10 text-center">
        <div class="w-20 h-20 mx-auto mb-4 bg-white rounded-full flex items-center justify-center">
          <svg class="w-10 h-10 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-white mb-2">Cơm Bà Giang</h1>
        <p class="text-blue-100">Đặt cơm trưa ngon miệng</p>
      </div>

      <!-- Form Container -->
      <div class="p-8">
        <!-- Login Form -->
        <div v-if="!showRegister" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Số điện thoại
            </label>
            <input v-model="loginData.identifier" 
                   type="text" 
                   placeholder="0901234567"
                   class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              Mật khẩu
            </label>
            <input v-model="loginData.password" 
                   type="password" 
                   placeholder="Mật khẩu 4-6 số"
                   @keyup.enter="login"
                   class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all">
          </div>
          
          <button @click="login" 
                  :disabled="!loginData.identifier || !loginData.password"
                  :class="['w-full font-semibold py-4 rounded-xl transition-all duration-200 transform hover:scale-105 shadow-lg',
                          !loginData.identifier || !loginData.password 
                            ? 'bg-gray-300 text-gray-500 cursor-not-allowed transform-none' 
                            : 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white']">
            <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
            </svg>
            Đăng nhập
          </button>
          
          <div class="text-center">
            <button @click="showRegister = true" 
                    class="text-blue-500 hover:text-blue-600 font-medium transition-colors">
              Chưa có tài khoản? 
              <span class="underline">Đăng ký ngay</span>
            </button>
          </div>
        </div>

        <!-- Register Form -->
        <div v-else class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Họ tên
            </label>
            <input v-model="registerData.name" 
                  type="text" 
                  placeholder="Nguyễn Văn A"
                  class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              Số điện thoại
            </label>
            <input v-model="registerData.identifier" 
                  type="text" 
                  placeholder="0901234567"
                  class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              Địa chỉ nhận cơm
            </label>
            <input v-model="registerData.address" 
                  type="text" 
                  placeholder="VD: Tầng 5, Tòa nhà ABC, Công ty XYZ..."
                  class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all">
            <p class="text-xs text-gray-500 mt-1">Địa chỉ để shipper giao cơm (có thể để trống)</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              Mật khẩu (4-6 số)
            </label>
            <input v-model="registerData.password" 
                  type="password" 
                  placeholder="VD: 1234"
                  @keyup.enter="register"
                  class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all">
          </div>
          
          <button @click="register" 
                  :disabled="!registerData.name || !registerData.identifier || !registerData.password"
                  :class="['w-full font-semibold py-4 rounded-xl transition-all duration-200 transform hover:scale-105 shadow-lg',
                          !registerData.name || !registerData.identifier || !registerData.password
                            ? 'bg-gray-300 text-gray-500 cursor-not-allowed transform-none'
                            : 'bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white']">
            <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
            </svg>
            Đăng ký
          </button>
          
          <div class="text-center">
            <button @click="showRegister = false" 
                    class="text-blue-500 hover:text-blue-600 font-medium transition-colors">
              Đã có tài khoản? 
              <span class="underline">Đăng nhập</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Main App (sau khi login) -->
  <div v-else class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 pb-24">
    
    <!-- Fixed Header -->
    <header class="fixed top-0 left-0 right-0 z-40 bg-white shadow-lg border-b border-gray-100">
      <div class="px-4 py-4">
        <div class="flex justify-between items-center">
          <!-- App Logo & Title -->
          <div class="flex-1 text-center">
            <div class="flex items-center justify-center mb-1">
              <div class="w-8 h-8 bg-gradient-to-r from-orange-400 to-red-500 rounded-full flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-cooking-pot">
                  <path d="M2 12h20"/><path d="M20 12v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-8"/><path d="m4 8 16-4"/><path d="m8.86 6.78-.45-1.81a2 2 0 0 1 1.45-2.43l1.94-.48a2 2 0 0 1 2.43 1.46l.45 1.8"/>
                </svg>
              </div>
              <h1 class="text-xl font-bold bg-gradient-to-r from-orange-500 to-red-600 bg-clip-text text-transparent">
                Cơm Bà Giang
              </h1>
            </div>
            <p class="text-xs text-gray-500">Cơm trưa văn phòng ngon miệng</p>
          </div>
          
          <!-- User Menu -->
          <div class="relative">
            <button @click="showUserMenu = !showUserMenu" 
                    class="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center hover:from-blue-600 hover:to-indigo-700 transition-all duration-200 transform hover:scale-105 shadow-md">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
            </button>

            <!-- User Dropdown -->
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 scale-95"
              enter-to-class="opacity-100 scale-100"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100 scale-100"
              leave-to-class="opacity-0 scale-95"
            >
              <div v-show="showUserMenu" 
                   class="absolute right-0 top-12 bg-white border border-gray-200 rounded-xl shadow-lg min-w-48 py-2 z-50">
                
                <!-- User Info Header -->
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-sm font-semibold text-gray-800">{{ currentUser.name }}</p>
                  <p class="text-xs text-gray-500">{{ currentUser.identifier }}</p>
                </div>
                
                <!-- Menu Items -->
                <div class="py-1">
                  <button @click="openUserInfoModal(); showUserMenu = false" 
                          class="w-full flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors">
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    Chỉnh sửa thông tin
                  </button>
                  
                  <button @click="logout(); showUserMenu = false" 
                          class="w-full flex items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors">
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                    </svg>
                    Đăng xuất
                  </button>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </header>

    <!-- Backdrop for closing user menu -->
    <div v-if="showUserMenu" @click="showUserMenu = false" class="fixed inset-0 z-30"></div>

    <!-- Main Content -->
    <main class="pt-24 px-4">
      
      <!-- Today Info Card -->
      <div class="mb-8">
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="w-12 h-12 bg-gradient-to-br from-blue-400 to-blue-600 rounded-xl flex items-center justify-center mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar-check-2">
                  <path d="M8 2v4"/><path d="M16 2v4"/><path d="M21 14V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h8"/><path d="M3 10h18"/><path d="m16 20 2 2 4-4"/>
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-500">Hôm nay</p>
                <p class="font-semibold text-gray-800">{{ today }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-500">Deadline</p>
              <p class="font-semibold text-orange-600 flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                {{ deadline }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Menu Carousel -->
      <div class="mb-8">
        <div class="overflow-x-auto scrollbar-hide">
          <div class="flex space-x-3 px-4 pb-2" style="width: max-content;">
            <div v-for="(item, index) in menuItems" :key="`menu-${index}`"
                 class="flex-shrink-0 w-72 bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden flex flex-col h-64">
              
              <!-- Menu Header -->
              <div :class="['p-4 text-white', getItemGradientClass(index)]">
                <div class="flex justify-between items-center">
                  <div>
                    <h4 class="text-lg font-bold">{{ item.name }}</h4>
                    <span class="text-xl font-bold">{{ formatPrice(item.price) }}</span>
                  </div>
                  <div class="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-salad">
                      <path d="M7 21h10"/><path d="M12 21a9 9 0 0 0 9-9H3a9 9 0 0 0 9 9Z"/><path d="M11.38 12a2.4 2.4 0 0 1-.4-4.77 2.4 2.4 0 0 1 3.2-2.77 2.4 2.4 0 0 1 3.47-.63 2.4 2.4 0 0 1 3.37 3.37 2.4 2.4 0 0 1-1.1 3.7 2.51 2.51 0 0 1 .03 1.1"/><path d="m13 12 4-4"/><path d="M10.9 7.25A3.99 3.99 0 0 0 4 10c0 .73.2 1.41.54 2"/>
                    </svg>
                  </div>
                </div>
              </div>
              
              <!-- Menu Body -->
              <div class="p-4 flex flex-col flex-1 min-h-0">
                <!-- Description with fixed height and scroll -->
                <div class="text-gray-600 text-sm leading-relaxed flex-1 mb-4 min-h-0">
                  <div class="menu-card-description">{{ item.description || 'Menu ngon, bổ, rẻ hôm nay' }}</div>
                </div>
                
                <!-- Quick Order Button - Always at bottom -->
                <div class="flex-shrink-0">
                  <button @click="quickOrder(item)" 
                          :class="['w-full py-3 rounded-lg font-medium text-sm transition-all duration-200 transform hover:scale-105', getItemButtonClass(index)]">
                    <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                    </svg>
                    Đặt ngay
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Scroll Indicators -->
        <div class="flex justify-center mt-4" v-if="menuItems.length > 1">
          <div class="flex space-x-2">
            <div v-for="(item, index) in menuItems" :key="`indicator-${index}`" 
                 class="w-2 h-2 rounded-full bg-gray-300 transition-colors"></div>
          </div>
        </div>
      </div>

      <!-- Toppings Info -->
      <div class="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 rounded-2xl p-6 mb-8">
        <h4 class="font-semibold text-amber-800 mb-3 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
          Tùy chọn thêm
        </h4>
        <p class="text-amber-700 leading-relaxed whitespace-pre-line">{{ availableToppings || 'Đang cập nhật...' }}</p>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-3 mb-8 px-4">
        <button @click="openOrderModal"
                class="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-4 rounded-xl shadow-sm transition-all duration-200 transform hover:scale-105">
          <div class="flex items-center justify-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shopping-cart">
              <circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>
            </svg>
            <span>Đặt cơm</span>
          </div>
        </button>
        
        <button @click="openGroupModal"
                class="flex-1 bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white font-semibold py-3 px-4 rounded-xl shadow-sm transition-all duration-200 transform hover:scale-105">
          <div class="flex items-center justify-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><path d="M16 3.128a4 4 0 0 1 0 7.744"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/>
            </svg>
            <span>Nhóm</span>
          </div>
        </button>
      </div>
    </main>

    <!-- Fixed Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-2xl">
      <div class="grid grid-cols-4 h-20">
        <button @click="viewOrderHistory" 
                class="flex flex-col items-center justify-center p-2 hover:bg-blue-50 transition-colors active:bg-blue-100">
          <svg class="w-6 h-6 text-blue-600 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <span class="text-xs font-medium text-blue-600">Lịch sử</span>
        </button>
        
        <button @click="viewPaymentSummary"
                class="flex flex-col items-center justify-center p-2 hover:bg-green-50 transition-colors active:bg-green-100">
          <svg class="w-6 h-6 text-green-600 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
          </svg>
          <span class="text-xs font-medium text-green-600">Thanh toán</span>
        </button>
        
        <button @click="openFeedbackModal"
                class="flex flex-col items-center justify-center p-2 hover:bg-orange-50 transition-colors active:bg-orange-100">
          <svg class="w-6 h-6 text-orange-600 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          <span class="text-xs font-medium text-orange-600">Góp ý</span>
        </button>
        
        <a href="/admin" 
           class="flex flex-col items-center justify-center p-2 hover:bg-purple-50 transition-colors active:bg-purple-100">
          <svg class="w-6 h-6 text-purple-600 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          <span class="text-xs font-medium text-purple-600">Quản lý</span>
        </a>
      </div>
    </nav>
    
    <!-- Order Modal -->
    <div v-if="showOrderModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
      <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-md transform transition-all duration-300 animate-slide-up">
        <!-- Modal Header -->
        <div class="relative p-6 border-b border-gray-100">
          <div class="text-center">
            <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.5 5M7 13l-1.5-5m0 0L3 3m4 10h10M17 21a2 2 0 11-4 0 2 2 0 014 0zM9 21a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800">Đặt cơm</h3>
          </div>
          <button @click="closeOrderModal" 
                  class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <!-- Modal Body -->
        <div class="p-6 space-y-6 overflow-y-auto max-h-[60vh]">
          <!-- Dropdown chọn loại đặt -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-3">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
              Đặt cho
            </label>
            <select v-model="orderType" 
                    class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 bg-white">
              <option value="personal">Cá nhân</option>
              <option v-for="group in currentUser.groups" :key="group.name" :value="group.name">
                {{ group.name }} ({{ group.members }} người)
              </option>
            </select>
          </div>

          <!-- Tên người đặt -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-3">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Người đặt
            </label>
            <input :value="currentUser.name" disabled 
                   class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg bg-gray-50 text-gray-600">
          </div>

          <!-- Chọn suất cơm -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-3">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
              </svg>
              Loại cơm
            </label>
            <div class="space-y-3">
              <label v-for="(item, index) in menuItems" :key="index" 
                     :class="['flex items-center p-4 rounded-xl border-2 cursor-pointer transition-all',
                              mealType === item.name ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300']">
                <input v-model="mealType" type="radio" :value="item.name" class="sr-only">
                <div class="flex items-center justify-between w-full">
                  <div class="flex items-center">
                    <div :class="['w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center',
                                  mealType === item.name ? 'border-blue-500 bg-blue-500' : 'border-gray-300']">
                      <div v-if="mealType === item.name" class="w-2 h-2 bg-white rounded-full"></div>
                    </div>
                    <span class="font-medium text-gray-800">{{ item.name }}</span>
                  </div>
                  <span class="font-bold text-blue-600">{{ formatPrice(item.price) }}</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Số lượng -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-3">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 3v10a1 1 0 001 1h8a1 1 0 001-1V7M7 7h10"/>
              </svg>
              Số lượng
            </label>
            <div class="flex items-center justify-center space-x-6">
              <button @click="decreaseQuantity" 
                      class="w-12 h-12 bg-gray-200 hover:bg-gray-300 rounded-xl flex items-center justify-center text-xl font-bold transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
                </svg>
              </button>
              <span class="text-3xl font-bold text-gray-800 w-16 text-center">{{ quantity }}</span>
              <button @click="increaseQuantity" 
                      class="w-12 h-12 bg-blue-500 hover:bg-blue-600 rounded-xl flex items-center justify-center text-xl font-bold text-white transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Ghi chú -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-3">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
              Ghi chú topping
            </label>
            <textarea v-model="note" 
                      placeholder="VD: Thêm trứng, không cay..." 
                      rows="3"
                      class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg resize-none focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"></textarea>
          </div>

          <!-- Tổng tiền -->
          <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6">
            <div class="flex justify-between items-center">
              <span class="text-lg font-semibold text-blue-800">
                <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
                </svg>
                Tổng tiền:
              </span>
              <span class="text-2xl font-bold text-blue-600">{{ totalAmount.toLocaleString() }} VNĐ</span>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="p-6 bg-gray-50 rounded-b-3xl">
          <div class="flex space-x-4">
            <button @click="closeOrderModal" 
                    class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-4 rounded-xl transition-colors">
              Hủy
            </button>
            <button @click="submitOrder" 
                    class="flex-1 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-semibold py-4 rounded-xl transition-all duration-200 transform hover:scale-105">
              <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              Đặt cơm ngay
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Group Modal -->
    <div v-if="showGroupModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
      <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-lg max-h-[90vh] overflow-hidden">
        <!-- Modal Header -->
        <div class="relative p-6 border-b border-gray-100">
          <div class="text-center">
            <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800">Quản lý nhóm</h3>
          </div>
          <button @click="closeGroupModal" 
                  class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Tab Navigation -->
        <div class="flex bg-gray-50 border-b border-gray-200">
          <button @click="groupTab = 'join'" 
                  :class="['flex-1 py-4 text-sm font-semibold transition-colors',
                           groupTab === 'join' ? 'text-blue-600 bg-white border-b-2 border-blue-500' : 'text-gray-500 hover:text-gray-700']">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            Tham gia
          </button>
          <button @click="groupTab = 'create'" 
                  :class="['flex-1 py-4 text-sm font-semibold transition-colors',
                           groupTab === 'create' ? 'text-blue-600 bg-white border-b-2 border-blue-500' : 'text-gray-500 hover:text-gray-700']">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            Tạo nhóm
          </button>
          <button @click="groupTab = 'manage'" 
                  :class="['flex-1 py-4 text-sm font-semibold transition-colors',
                           groupTab === 'manage' ? 'text-blue-600 bg-white border-b-2 border-blue-500' : 'text-gray-500 hover:text-gray-700']">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            </svg>
            Quản lý
          </button>
        </div>

        <!-- Modal Content with scroll -->
        <div class="p-6 overflow-y-auto max-h-96">
          <!-- Join Group Tab -->
          <div v-if="groupTab === 'join'" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Mã nhóm</label>
              <div class="flex space-x-2">
                <input v-model="joinGroupCode" type="text" placeholder="VD: IT2025, MKT001..." 
                       class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button @click="joinGroup" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors whitespace-nowrap">
                  Tham gia
                </button>
              </div>
            </div>
            <div class="text-center text-gray-500 text-sm">
              Liên hệ trưởng nhóm để lấy mã nhóm
            </div>
          </div>

          <!-- Create Group Tab -->
          <div v-if="groupTab === 'create'" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tên nhóm</label>
              <input v-model="newGroup.name" type="text" placeholder="VD: IT Team, Marketing Team..." 
                     class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Địa chỉ giao hàng</label>
              <input v-model="newGroup.address" type="text" placeholder="VD: Tầng 5, Tòa nhà ABC..." 
                     class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>

            <!-- Benefits Info (compact) -->
            <div class="bg-green-50 border border-green-200 rounded-lg p-3">
              <h4 class="font-medium text-green-800 text-sm mb-1">💡 Lợi ích trưởng nhóm:</h4>
              <p class="text-green-700 text-xs">Giảm giá 5-10k/suất • Miễn phí khi ≥20 người • Giao hàng tập trung</p>
            </div>

            <button @click="createGroup" class="w-full bg-green-500 hover:bg-green-600 text-white font-medium py-2 rounded-lg transition-colors">
              Tạo nhóm ngay
            </button>
          </div>

          <!-- Manage Groups Tab -->
          <div v-if="groupTab === 'manage'">
            <div v-if="currentUser.groups.length === 0" class="text-center text-gray-500 py-8">
              <p class="text-sm">Bạn chưa tham gia nhóm nào</p>
              <button @click="groupTab = 'join'" class="text-blue-500 hover:text-blue-600 text-sm mt-2">
                Tham gia nhóm ngay
              </button>
            </div>
            <div v-else class="space-y-3 max-h-64 overflow-y-auto">
              <div v-for="group in currentUser.groups" :key="group.name" 
                   class="border border-gray-200 rounded-lg p-3">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h5 class="font-medium text-gray-800 text-sm">{{ group.name }}</h5>
                    <p class="text-xs text-gray-600" v-if="group.isLeader">👑 Trưởng nhóm</p>
                    <p class="text-xs text-gray-600" v-else>👤 Thành viên</p>
                  </div>
                  <!-- Hiển thị button khác nhau cho leader vs member -->
                  <button v-if="group.isLeader" 
                          @click="goToGroupManagement(group)" 
                          class="text-xs px-3 py-1">
                    Quản lý
                  </button>
                  <button v-else 
                          @click="leaveGroup(group.name)" 
                          class="text-red-500 hover:text-red-600 text-xs">
                    Rời nhóm
                  </button>
                </div>
                
                <!-- Group Code (chỉ leader) -->
                <div v-if="group.isLeader" class="bg-blue-50 rounded-lg p-2 mb-2">
                  <div class="flex justify-between items-center">
                    <div>
                      <p class="text-xs text-blue-700 font-medium">Mã: {{ group.code }}</p>
                      <p class="text-xs text-blue-600">Chia sẻ để mọi người tham gia</p>
                    </div>
                    <button @click="copyGroupCode(group.code)" 
                            class="bg-blue-500 hover:bg-blue-600 text-white text-xs px-2 py-1 rounded">
                      Copy
                    </button>
                  </div>
                </div>

                <!-- Group Stats -->
                <div class="flex justify-between text-xs text-gray-500">
                  <span>{{ group.members }} thành viên</span>
                  <span v-if="group.isLeader">{{ group.totalOrders || 0 }} đơn tuần này</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Order History Modal -->
  <div v-if="showOrderHistory" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
    <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-4xl max-h-[95vh] overflow-hidden transform transition-all duration-300 animate-slide-up">
      
      <!-- Modal Header -->
      <div class="relative p-6 border-b border-gray-100">
        <div class="text-center">
          <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-800">Lịch sử đặt cơm</h3>
        </div>
        <button @click="closeOrderHistory" 
                class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
      
      <!-- Filters -->
      <div class="p-4 bg-gray-50 border-b border-gray-200">
        <div class="flex space-x-4">
          <select v-model="historyTimeFilter" @change="filterOrderHistory" 
                  class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="all">Tất cả thời gian</option>
            <option value="today">Hôm nay</option>
            <option value="week">Tuần này</option>
            <option value="month">Tháng này</option>
          </select>
          
          <select v-model="historyStatusFilter" @change="filterOrderHistory" 
                  class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="all">Tất cả trạng thái</option>
            <option value="pending">Đã đặt</option>
            <option value="preparing">Đang giao</option>
            <option value="completed">Hoàn thành</option>
          </select>
        </div>
      </div>
      
      <!-- Order History List -->
      <div class="p-4 overflow-y-auto max-h-[70vh]">
        <div class="space-y-3">
          <div v-for="order in filteredOrderHistory" :key="`${order.date}-${order.id}`" 
              class="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
            
            <!-- Header Row -->
            <div class="flex justify-between items-center mb-3">
              <div class="flex items-center space-x-2">
                <span class="font-bold text-gray-900">#{{ order.id }}</span>
                <span :class="['px-2 py-1 rounded-full text-xs font-medium',
                              order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                              order.status === 'preparing' ? 'bg-blue-100 text-blue-800' :
                              order.status === 'completed' ? 'bg-green-100 text-green-800' :
                              'bg-red-100 text-red-800']">
                  {{ getStatusText(order.status) }}
                </span>
              </div>
              <span :class="['text-lg font-bold',
                            order.status === 'cancelled' ? 'text-red-600 line-through' : 'text-blue-600']">
                {{ order.total_amount.toLocaleString() }}đ
              </span>
            </div>
            
            <!-- Order Info -->
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">Ngày:</span>
                <span class="font-medium">{{ formatDate(order.date) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Món:</span>
                <span class="font-medium">{{ order.meal_type }} x{{ order.quantity }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Giờ đặt:</span>
                <span class="font-medium">{{ order.created_at }}</span>
              </div>
              <div v-if="order.note" class="pt-2 border-t border-gray-100">
                <span class="text-gray-600">Ghi chú:</span>
                <p class="text-gray-800 mt-1">{{ order.note }}</p>
              </div>
            </div>
            
            <!-- Actions for pending orders -->
            <div v-if="order.status === 'pending'" class="flex space-x-2 mt-3 pt-3 border-t border-gray-100">
              <button @click="editOrder(order)" 
                      class="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg text-sm font-medium">
                Sửa
              </button>
              <button @click="cancelOrder(order)" 
                      class="flex-1 bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg text-sm font-medium">
                Hủy
              </button>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="filteredOrderHistory.length === 0" class="text-center py-8">
            <div class="text-4xl mb-2">📭</div>
            <p class="text-gray-500">Không có đơn hàng nào</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Payment Summary Modal -->
  <div v-if="showPaymentSummary" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
    <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-lg max-h-[90vh] overflow-hidden transform transition-all duration-300 animate-slide-up">
      
      <!-- Modal Header -->
      <div class="relative p-6 border-b border-gray-100">
        <div class="text-center">
          <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-800">Thanh toán</h3>
          <p class="text-sm text-gray-600">{{ getPeriodText(selectedPaymentPeriod) }}</p>
        </div>
        <button @click="closePaymentSummary" 
                class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
      
      <!-- PayOS Payment Status Banner (Enhanced) -->
      <div v-if="showPayOSModal" :class="['p-4 text-white transition-all duration-500',
                                          payosPaymentData.status === 'PAID' ? 'bg-gradient-to-r from-green-500 to-green-600' :
                                          payosPaymentData.status === 'FAILED' ? 'bg-gradient-to-r from-red-500 to-red-600' :
                                          payosPaymentData.status === 'EXPIRED' ? 'bg-gradient-to-r from-orange-500 to-orange-600' :
                                          'bg-gradient-to-r from-blue-500 to-indigo-600']">
        <div class="flex items-center justify-between">
          <div>
            <div class="flex items-center mb-1">
              <!-- Dynamic Status Icon -->
              <div class="w-6 h-6 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-2">
                <!-- Success Icon -->
                <svg v-if="payosPaymentData.status === 'PAID'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <!-- Failed Icon -->
                <svg v-else-if="payosPaymentData.status === 'FAILED'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
                <!-- Expired Icon -->
                <svg v-else-if="payosPaymentData.status === 'EXPIRED'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <!-- Processing Icon (spinning) -->
                <svg v-else class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
              </div>
              
              <!-- Dynamic Status Text -->
              <span class="text-sm font-semibold">
                {{ payosPaymentData.status === 'PAID' ? '✅ Thanh toán thành công' :
                  payosPaymentData.status === 'FAILED' ? '❌ Thanh toán thất bại' :
                  payosPaymentData.status === 'EXPIRED' ? '⏰ Thanh toán hết hạn' :
                  '🔄 Đang chờ thanh toán...' }}
              </span>
            </div>
            <p class="text-xs opacity-90">Mã: #{{ payosPaymentData.order_code }}</p>
          </div>
          
          <div class="text-right">
            <div class="text-lg font-bold">{{ payosPaymentData.amount.toLocaleString() }}đ</div>
            <div v-if="payosPaymentData.status === 'PENDING'" class="text-xs opacity-90">
              ⏱️ {{ formatPayOSCountdown(payosTimeRemaining) }}
            </div>
            <div v-else-if="payosPaymentData.status === 'PAID'" class="text-xs opacity-90">
              🎉 Hoàn thành
            </div>
            <div v-else-if="['FAILED', 'EXPIRED'].includes(payosPaymentData.status)" class="text-xs opacity-90">
              💡 Có thể thử lại
            </div>
          </div>
        </div>
        
        <!-- Progress Bar for Pending Status -->
        <div v-if="payosPaymentData.status === 'PENDING'" class="mt-3">
          <div class="w-full bg-white bg-opacity-20 rounded-full h-2">
            <div class="bg-white h-2 rounded-full transition-all duration-1000 ease-linear" 
                :style="{ width: `${Math.max(0, (payosTimeRemaining / (30 * 60)) * 100)}%` }">
            </div>
          </div>
          <div class="flex justify-between text-xs opacity-75 mt-1">
            <span>Còn lại {{ formatPayOSCountdown(payosTimeRemaining) }}</span>
            <span>30:00 phút</span>
          </div>
        </div>
      </div>
      
      <div class="overflow-y-auto max-h-[70vh]">
        <!-- Period Filter -->
        <div class="p-4 bg-gray-50 border-b">
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z"/>
            </svg>
            Chọn thời gian thanh toán
          </label>
          <select v-model="paymentPeriod" @change="loadPaymentSummary" 
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
            <option value="current_week">Tuần này</option>
            <option value="current_month">Tháng này</option>
            <option value="last_month">Tháng trước</option>
            <option value="all">Tất cả thời gian</option>
          </select>
        </div>

        <!-- Payment Overview - Compact -->
        <div class="p-4">
          <!-- Quick Stats Grid -->
          <div class="grid grid-cols-3 gap-3 mb-4">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 text-center">
              <div class="text-lg font-bold text-blue-800">{{ paymentSummary.total_orders || 0 }}</div>
              <div class="text-xs text-blue-600">Suất đặt</div>
            </div>
            
            <div class="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
              <div class="text-lg font-bold text-green-800">{{ (paymentSummary.paid_amount || 0).toLocaleString() }}đ</div>
              <div class="text-xs text-green-600">Đã trả</div>
            </div>
            
            <div :class="['rounded-lg p-3 text-center border',
                          (paymentSummary.remaining_amount || 0) > 0 ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200']">
              <div :class="['text-lg font-bold',
                            (paymentSummary.remaining_amount || 0) > 0 ? 'text-red-800' : 'text-green-800']">
                {{ (paymentSummary.remaining_amount || 0).toLocaleString() }}đ
              </div>
              <div :class="['text-xs',
                            (paymentSummary.remaining_amount || 0) > 0 ? 'text-red-600' : 'text-green-600']">
                {{ (paymentSummary.remaining_amount || 0) > 0 ? 'Còn lại' : 'Xong' }}
              </div>
            </div>
          </div>

          <!-- Total Amount - Highlighted -->
          <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-4 mb-4">
            <div class="flex justify-between items-center">
              <span class="text-lg font-semibold text-blue-800">
                <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2"/>
                </svg>
                Tổng tiền:
              </span>
              <span class="text-2xl font-bold text-blue-600">{{ (paymentSummary.total_amount || 0).toLocaleString() }}đ</span>
            </div>
          </div>

          <!-- Chi tiết món ăn - Collapsible -->
          <div v-if="Object.keys(paymentSummary.meal_summary || {}).length > 0" class="mb-4">
            <button @click="showMealDetails = !showMealDetails" 
                    class="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors">
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-2 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                </svg>
                <span class="text-sm font-semibold text-gray-800">Chi tiết món ăn</span>
              </div>
              <svg :class="['w-4 h-4 text-gray-600 transition-transform', showMealDetails ? 'rotate-180' : '']" 
                  fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            
            <!-- Meal Details - Expandable -->
            <div v-if="showMealDetails" class="mt-2 space-y-2 bg-white border border-gray-200 rounded-lg p-3">
              <div v-for="(data, mealType) in paymentSummary.meal_summary" :key="mealType" 
                  class="flex justify-between items-center text-sm py-2 border-b border-gray-100 last:border-b-0">
                <div class="flex-1">
                  <span class="font-medium text-gray-700">{{ mealType }}</span>
                  <div class="text-xs text-gray-500 mt-1">
                    <!-- TODO: Thêm thời gian đặt ở đây khi có data từ backend -->
                    <span class="inline-block mr-3">{{ data.count }} suất</span>
                    <span class="text-gray-400">• Đặt từ nhiều ngày khác nhau</span>
                  </div>
                </div>
                <span class="font-semibold text-gray-900">{{ data.amount.toLocaleString() }}đ</span>
              </div>
            </div>
          </div>

          <!-- PAYMENT ACTION SECTION -->
          <div v-if="(paymentSummary.remaining_amount || 0) === 0" class="text-center p-6 bg-green-100 border-2 border-green-300 rounded-xl mb-4">
            <div class="text-4xl mb-2">🎉</div>
            <p class="text-green-800 font-semibold">{{ getPeriodText(selectedPaymentPeriod) }} đã thanh toán xong!</p>
          </div>
          
          <div v-else class="space-y-3">
            <!-- Info box về period thanh toán -->
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <div class="flex items-center">
                <svg class="w-4 h-4 text-blue-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <div>
                  <p class="text-sm font-medium text-blue-800">
                    Thanh toán cho: {{ getPeriodText(selectedPaymentPeriod) }}
                  </p>
                  <p class="text-xs text-blue-600">
                    Số tiền: {{ paymentSummary.remaining_amount.toLocaleString() }}đ
                  </p>
                </div>
              </div>
            </div>

            <!-- PayOS Payment Button -->
            <button @click="startPayOSPayment" 
                    :disabled="isLoadingPayOS || showPayOSModal"
                    :class="['w-full font-semibold py-4 rounded-xl transition-all duration-200 transform hover:scale-105 disabled:transform-none disabled:cursor-not-allowed',
                            isLoadingPayOS || showPayOSModal ? 
                            'bg-gray-400 text-gray-600' : 
                            'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white']">
              <div class="flex items-center justify-center space-x-2">
                <div v-if="isLoadingPayOS" class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"/>
                </svg>
                <span>{{ isLoadingPayOS ? 'Đang tạo...' : showPayOSModal ? 'Đang thanh toán...' : 'Thanh toán PayOS' }}</span>
              </div>
              <div class="text-xs mt-1 opacity-90">
                {{ getPeriodText(selectedPaymentPeriod) }} • {{ paymentSummary.remaining_amount.toLocaleString() }}đ
              </div>
            </button>

            <!-- Manual Payment Button -->
            <button @click="markManualPayment" 
                    class="w-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 rounded-xl transition-colors">
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              Đã thanh toán bằng cách khác
            </button>

            <p class="text-center text-xs text-gray-500">
              💡 PayOS: Tự động cập nhật • Manual: Cần xác nhận thủ công
            </p>
          </div>
        </div>

        <!-- PayOS Payment Interface (khi active) -->
        <div v-if="showPayOSModal" class="border-t border-gray-200 bg-gradient-to-br from-blue-50 to-indigo-50">
          <!-- Payment Method Toggle -->
          <div class="p-4">
            <div class="bg-white rounded-lg shadow-sm border border-blue-200 overflow-hidden">
              <div class="flex">
                <button @click="showQRCode = true" 
                        :class="['flex-1 py-3 px-4 text-sm font-medium transition-all duration-200',
                                showQRCode ? 'bg-blue-500 text-white shadow-md' : 'bg-white text-gray-600 hover:bg-blue-50']">
                  <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01"/>
                  </svg>
                  QR Code
                </button>
                <button @click="showQRCode = false" 
                        :class="['flex-1 py-3 px-4 text-sm font-medium transition-all duration-200',
                                !showQRCode ? 'bg-blue-500 text-white shadow-md' : 'bg-white text-gray-600 hover:bg-blue-50']">
                  <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-2"/>
                  </svg>
                  Trang thanh toán
                </button>
              </div>
            </div>
          </div>

          <!-- Payment Content -->
          <div class="px-4 pb-4">
            <!-- QR Code View -->
            <div v-if="showQRCode" class="bg-white rounded-lg border border-blue-200 p-6 text-center">
              <div v-if="payosPaymentData.qr_code" class="space-y-4">
                <!-- Display QR Code using VietQR data directly -->
                <div class="inline-block p-3 bg-white border-2 border-gray-300 rounded-lg shadow-sm">
                  <!-- Fallback - use online QR generator with VietQR data -->
                  <img 
                      :src="generateVietQRImageUrl(payosPaymentData.qr_code)" 
                      alt="PayOS QR Code" 
                      class="w-40 h-40 mx-auto"
                      @load="qrCodeGenerated = true"
                      @error="handleQRError">
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-700 mb-1">📱 Quét mã QR để thanh toán</p>
                  <p class="text-xs text-gray-500">Sử dụng app ngân hàng hoặc ví điện tử</p>
                </div>
              </div>
              <div v-else class="py-8 text-gray-500">
                <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5l-6.928-12c-.77-.833-2.244-.833-3.014 0l-6.928 12C-.44 16.333.52 18 2.06 18z"/>
                </svg>
                <p class="text-sm">Không có mã QR</p>
                <p class="text-xs text-gray-400 mt-1">QR Data: {{ payosPaymentData.qr_code ? 'Có' : 'Không có' }}</p>
              </div>
            </div>

            <!-- Payment Link View -->
            <div v-else class="bg-white rounded-lg border border-blue-200 p-6 text-center space-y-4">
              <div class="w-16 h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-full mx-auto flex items-center justify-center">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-2"/>
                </svg>
              </div>
              <div>
                <h4 class="text-lg font-semibold text-gray-800 mb-2">Trang thanh toán PayOS</h4>
                <p class="text-sm text-gray-600 mb-4">Click để mở trang thanh toán chính thức</p>
                <button @click="openPaymentLink" 
                        class="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold py-3 rounded-lg transition-all duration-200 transform hover:scale-105">
                  🔗 Mở trang thanh toán
                </button>
              </div>
            </div>

            <!-- Status-aware Quick Actions -->
            <div class="flex space-x-2 mt-4">
              <!-- Cancel button (chỉ khi PENDING) -->
              <button v-if="payosPaymentData.status === 'PENDING'" 
                      @click="cancelPayOSPayment" 
                      class="flex-1 bg-red-100 hover:bg-red-200 text-red-700 text-sm py-2 rounded-lg transition-colors">
                ❌ Hủy thanh toán
              </button>
              
              <!-- Copy button (luôn hiện) -->
              <button @click="copyPayOSOrderCode" 
                      class="flex-1 bg-blue-100 hover:bg-blue-200 text-blue-700 text-sm py-2 rounded-lg transition-colors">
                📋 Copy mã: #{{ payosPaymentData.order_code }}
              </button>
              
              <!-- Retry button (khi FAILED hoặc EXPIRED) -->
              <button v-if="['FAILED', 'EXPIRED'].includes(payosPaymentData.status)" 
                      @click="retryPayOSPayment" 
                      class="flex-1 bg-green-100 hover:bg-green-200 text-green-700 text-sm py-2 rounded-lg transition-colors">
                🔄 Thử lại
              </button>
              
              <!-- Close button (khi PAID) -->
              <button v-if="payosPaymentData.status === 'PAID'" 
                      @click="closePayOSModal" 
                      class="flex-1 bg-green-100 hover:bg-green-200 text-green-700 text-sm py-2 rounded-lg transition-colors">
                ✅ Đóng
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Feedback Modal -->
  <div v-if="showFeedbackModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
    <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-md max-h-[90vh] overflow-hidden transform transition-all duration-300 animate-slide-up">
      
      <div class="relative p-6 border-b border-gray-100">
        <div class="text-center">
          <div class="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-800">Góp ý cho Cơm Bà Giang</h3>
        </div>
        <button @click="closeFeedbackModal" 
                class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
      
      <div class="p-6">
        <!-- Anonymous Notice -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-6">
          <div class="flex items-center">
            <span class="text-blue-500 mr-2">🔒</span>
            <p class="text-sm text-blue-800">
              <strong>Góp ý ẩn danh:</strong> Chúng tôi không lưu thông tin cá nhân của bạn
            </p>
          </div>
        </div>

        <!-- Category Selection -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Loại góp ý</label>
          <select v-model="feedbackData.category" 
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="general">Chung</option>
            <option value="food">Về món ăn</option>
            <option value="service">Về dịch vụ</option>
            <option value="delivery">Về giao hàng</option>
            <option value="price">Về giá cả</option>
          </select>
        </div>

        <!-- Rating Stars -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Đánh giá (tùy chọn)</label>
          <div class="flex space-x-1 star-rating">
            <button v-for="star in 5" :key="star"
                    @click="setRating(star)"
                    @mouseover="hoverRating = star"
                    @mouseleave="hoverRating = 0"
                    :class="['text-3xl transition-all duration-200 transform hover:scale-110 focus:outline-none',
                            star <= (hoverRating || feedbackData.rating) ? 'text-yellow-400 drop-shadow-lg' : 'text-gray-300 hover:text-yellow-200']">
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </button>
          </div>
          <p class="text-sm text-gray-600 mt-2 font-medium">
            {{ feedbackData.rating === 0 ? 'Chưa đánh giá' : 
              feedbackData.rating === 1 ? 'Rất không hài lòng' :
              feedbackData.rating === 2 ? 'Không hài lòng' :
              feedbackData.rating === 3 ? 'Bình thường' :
              feedbackData.rating === 4 ? 'Hài lòng' : 'Rất hài lòng' }}
          </p>
        </div>

        <!-- Feedback Text -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">Nội dung góp ý</label>
          <textarea v-model="feedbackData.text" 
                    rows="4" 
                    placeholder="Chia sẻ ý kiến của bạn về cơm Bà Giang. Góp ý của bạn sẽ giúp chúng tôi cải thiện chất lượng dịch vụ..."
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"></textarea>
          <p class="text-xs text-gray-500 mt-1">
            {{ feedbackData.text.length }}/500 ký tự
          </p>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="flex space-x-3 p-6 border-t border-gray-200">
        <button @click="closeFeedbackModal" 
                class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 rounded-lg transition-colors">
          Hủy
        </button>
        <button @click="submitFeedback" 
                :disabled="!feedbackData.text.trim()"
                :class="['flex-1 font-medium py-2 rounded-lg transition-colors',
                        feedbackData.text.trim() ? 
                        'bg-blue-500 hover:bg-blue-600 text-white' : 
                        'bg-gray-300 text-gray-500 cursor-not-allowed']">
          Gửi góp ý
        </button>
      </div>
    </div>
  </div>

  <!-- Edit Order Modal -->
  <div v-if="showEditOrderModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
    <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-md max-h-[90vh] overflow-hidden transform transition-all duration-300 animate-slide-up">
      
      <!-- Modal Header -->
      <div class="relative p-6 border-b border-gray-100">
        <div class="text-center">
          <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-800">Sửa đơn hàng #{{ editingOrder.id }}</h3>
        </div>
        <button @click="closeEditOrderModal" 
                class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 space-y-6 overflow-y-auto max-h-[60vh]">
        <!-- Current Order Info -->
        <div class="bg-gradient-to-r from-gray-50 to-blue-50 border-2 border-gray-200 rounded-xl p-4">
          <h4 class="text-sm font-semibold text-gray-700 mb-3 flex items-center">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Thông tin đơn hiện tại
          </h4>
          <div class="text-sm text-gray-600 space-y-1">
            <p><strong>Ngày:</strong> {{ formatDate(editingOrder.date) }} - {{ editingOrder.created_at }}</p>
            <p><strong>Món:</strong> {{ editingOrder.meal_type }} x{{ editingOrder.quantity }}</p>
            <p v-if="editingOrder.note"><strong>Ghi chú:</strong> {{ editingOrder.note }}</p>
            <p class="font-semibold text-blue-600"><strong>Tổng tiền:</strong> {{ editingOrder.total_amount.toLocaleString() }} VNĐ</p>
          </div>
        </div>

        <!-- Chọn suất cơm -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
            Loại cơm
          </label>
          <div class="space-y-3">
            <label v-for="(item, index) in menuItems" :key="index" 
                  :class="['flex items-center justify-between p-4 rounded-xl border-2 cursor-pointer transition-all',
                            editOrderData.meal_type === item.name ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300']">
              <input v-model="editOrderData.meal_type" type="radio" :value="item.name" class="sr-only">
              <div class="flex items-center">
                <div :class="['w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center',
                              editOrderData.meal_type === item.name ? 'border-blue-500 bg-blue-500' : 'border-gray-300']">
                  <div v-if="editOrderData.meal_type === item.name" class="w-2 h-2 bg-white rounded-full"></div>
                </div>
                <span class="font-medium text-gray-800">{{ item.name }}</span>
              </div>
              <span class="font-bold text-blue-600">{{ formatPrice(item.price) }}</span>
            </label>
          </div>
        </div>

        <!-- Số lượng -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 3v10a1 1 0 001 1h8a1 1 0 001-1V7M7 7h10"/>
            </svg>
            Số lượng
          </label>
          <div class="flex items-center justify-center space-x-6">
            <button @click="decreaseEditQuantity" 
                    class="w-12 h-12 bg-gray-200 hover:bg-gray-300 rounded-xl flex items-center justify-center text-xl font-bold transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
              </svg>
            </button>
            <span class="text-3xl font-bold text-gray-800 w-16 text-center">{{ editOrderData.quantity }}</span>
            <button @click="increaseEditQuantity" 
                    class="w-12 h-12 bg-blue-500 hover:bg-blue-600 rounded-xl flex items-center justify-center text-xl font-bold text-white transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Ghi chú -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            Ghi chú topping
          </label>
          <textarea v-model="editOrderData.note" 
                    placeholder="VD: Thêm trứng, không cay..." 
                    rows="3"
                    class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg resize-none focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"></textarea>
        </div>

        <!-- Tổng tiền -->
        <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6">
          <div class="flex justify-between items-center">
            <span class="text-lg font-semibold text-blue-800">
              <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
              </svg>
              Tổng tiền mới:
            </span>
            <span class="text-2xl font-bold text-blue-600">{{ calculateEditOrderTotal().toLocaleString() }} VNĐ</span>
          </div>
          <div v-if="calculateEditOrderTotal() !== editingOrder.total_amount" class="text-sm text-blue-700 mt-2 font-medium">
            Thay đổi: {{ (calculateEditOrderTotal() - editingOrder.total_amount).toLocaleString() }} VNĐ
          </div>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="flex space-x-3 p-6 border-t border-gray-200">
        <button @click="closeEditOrderModal" class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 rounded-lg transition-colors">
          Hủy
        </button>
        <button @click="saveEditOrder" 
                :disabled="!editOrderData.meal_type"
                :class="['flex-1 font-medium py-2 rounded-lg transition-colors',
                        editOrderData.meal_type ? 
                        'bg-blue-500 hover:bg-blue-600 text-white' : 
                        'bg-gray-300 text-gray-500 cursor-not-allowed']">
          Lưu thay đổi
        </button>
      </div>
    </div>
  </div>

  <!-- User Info Modal -->
  <div v-if="showUserInfoModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center z-50 p-4">
    <div class="bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl w-full sm:max-w-md max-h-[90vh] overflow-hidden transform transition-all duration-300 animate-slide-up">
      
      <!-- Modal Header -->
      <div class="relative p-6 border-b border-gray-100">
        <div class="text-center">
          <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-800">Thông tin cá nhân</h3>
        </div>
        <button @click="closeUserInfoModal" 
                class="absolute top-4 right-4 w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 space-y-6">
        <!-- Họ tên -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            Họ tên
          </label>
          <input v-model="userInfoData.name" 
                type="text" 
                placeholder="Nhập họ tên"
                class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all">
        </div>

        <!-- SĐT (read-only) -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            Số điện thoại
          </label>
          <input :value="currentUser.identifier" 
                disabled 
                class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg bg-gray-50 text-gray-600 cursor-not-allowed">
          <p class="text-xs text-gray-500 mt-1">Không thể thay đổi số điện thoại</p>
        </div>

        <!-- Địa chỉ -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            Địa chỉ nhận cơm
          </label>
          <textarea v-model="userInfoData.address" 
                    rows="3"
                    placeholder="VD: Tầng 5, Tòa nhà ABC, Công ty XYZ..."
                    class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg resize-none focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"></textarea>
          <p class="text-xs text-gray-500 mt-1">Địa chỉ để shipper giao cơm</p>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="flex space-x-3 p-6 border-t border-gray-200">
        <button @click="closeUserInfoModal" 
                class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-3 rounded-xl transition-colors">
          Hủy
        </button>
        <button @click="updateUserInfo" 
                :disabled="isUpdatingUserInfo"
                :class="['flex-1 font-medium py-3 rounded-xl transition-colors',
                        isUpdatingUserInfo ? 
                        'bg-gray-400 text-gray-600 cursor-not-allowed' : 
                        'bg-blue-500 hover:bg-blue-600 text-white']">
          <div v-if="isUpdatingUserInfo" class="flex items-center justify-center">
            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
            Đang lưu...
          </div>
          <div v-else>
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            Cập nhật
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar for webkit browsers */
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

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

/* Feedback Stars Animation */
.star-rating button {
  transition: all 0.2s ease;
}

.star-rating button:hover {
  transform: scale(1.1);
}

/* Loading spinner */
.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Hover effects */
.hover-lift:hover {
  transform: translateY(-2px);
}

/* Mobile specific improvements */
@media (max-width: 640px) {
  /* Make modals slide up from bottom on mobile */
  .fixed.inset-0 .bg-white {
    max-height: 90vh;
  }
  
  /* Better spacing for mobile */
  .p-6 {
    padding: 1rem;
  }
  
  /* Larger tap targets */
  .grid.grid-cols-4 button {
    min-height: 4rem;
  }
}

/* Smooth transitions for all interactive elements */
* {
  transition: all 0.2s ease;
}

/* Custom gradient backgrounds */
.gradient-blue {
  background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
}

.gradient-green {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
}

.gradient-purple {
  background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
}

.gradient-orange {
  background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
}

.gradient-pink {
  background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%);
}

/* Feedback Stars Animation - UPDATE */
.star-rating button {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.star-rating button:hover {
  transform: scale(1.2);
  filter: drop-shadow(0 4px 8px rgba(251, 191, 36, 0.4));
}

.star-rating button:active {
  transform: scale(1.1);
}

/* Add glow effect for selected stars */
.text-yellow-400 {
  filter: drop-shadow(0 2px 4px rgba(251, 191, 36, 0.3));
}

/* Text truncation */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Slide down animation for dropdown */
@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-down {
  animation: slide-down 0.2s ease-out;
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
import appLogic from './components/js/App.js'

export default appLogic
</script>