<!-- src/views/Login.vue -->
<template>
  <div id="app">
    <div class="auth-container">
      <div class="header">
        <h1>StudyPoint</h1>
        <p>НИШ • КТЛ • РФМШ</p>
      </div>

      <div class="tab-selector">
        <button
          class="tab-btn"
          :class="{ active: currentTab === 'login' }"
          @click="switchTab('login')"
        >
          Кіру
        </button>
        <button
          class="tab-btn"
          :class="{ active: currentTab === 'register' }"
          @click="switchTab('register')"
        >
          Тіркелу
        </button>
      </div>

      <!-- LOGIN FORM -->
      <div v-if="currentTab === 'login'">
        <div class="role-selector">
          <div
            class="role-btn"
            :class="{ active: selectedRole === 'student' }"
            @click="selectRole('student')"
          >
            <div class="role-text">Оқушы</div>
          </div>
          <div
            class="role-btn"
            :class="{ active: selectedRole === 'parent' }"
            @click="selectRole('parent')"
          >
            <div class="role-text">Ата-ана</div>
          </div>
          <div
            class="role-btn"
            :class="{ active: selectedRole === 'admin' }"
            @click="selectRole('admin')"
          >
            <div class="role-text">Админ</div>
          </div>
        </div>

        <div class="form-container">
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="login-username">Логин</label>
              <input
                type="text"
                id="login-username"
                v-model="loginForm.username"
                placeholder="Логиніңізді енгізіңіз"
                required
              />
            </div>

            <div class="form-group">
              <label for="login-password">Құпия сөз</label>
              <input
                type="password"
                id="login-password"
                v-model="loginForm.password"
                placeholder="Құпия сөзді енгізіңіз"
                required
              />
            </div>

            <button type="submit" class="submit-btn">
              Кіру
            </button>
          </form>
        </div>
      </div>

      <!-- REGISTER FORM -->
      <div v-else>
        <div class="role-selector">
          <div
            class="role-btn"
            :class="{ active: registerRole === 'student' }"
            @click="registerRole = 'student'"
          >
            <div class="role-text">Оқушы</div>
          </div>
          <div
            class="role-btn"
            :class="{ active: registerRole === 'parent' }"
            @click="registerRole = 'parent'"
          >
            <div class="role-text">Ата-ана</div>
          </div>
          <div
            class="role-btn"
            :class="{ active: registerRole === 'admin' }"
            @click="registerRole = 'admin'"
          >
            <div class="role-text">Админ</div>
          </div>
        </div>

        <div class="form-container">
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <div v-if="registerRole === 'parent'" class="parent-code-info">
            💡 Ата-ана болып тіркелу үшін балаңыздың жеке кодын сұраңыз
          </div>

          <!-- Show student code after successful registration -->
          <div v-if="newStudentCode" class="student-code-display">
            <h3>🎉 Тіркелу сәтті өтті!</h3>
            <div class="code">{{ newStudentCode }}</div>
            <p>Бұл кодты ата-анаға беріңіз</p>
          </div>

          <form v-if="!newStudentCode" @submit.prevent="handleRegister">
            <div class="form-row">
              <div class="form-group">
                <label for="reg-firstname">Аты</label>
                <input
                  type="text"
                  id="reg-firstname"
                  v-model="registerForm.firstname"
                  placeholder="Атыңыз"
                  required
                />
              </div>
              <div class="form-group">
                <label for="reg-lastname">Тегі</label>
                <input
                  type="text"
                  id="reg-lastname"
                  v-model="registerForm.lastname"
                  placeholder="Тегіңіз"
                  required
                />
              </div>
            </div>

            <div v-if="registerRole === 'student'">
              <div class="form-group">
                <label for="reg-grade">Сынып</label>
                <select id="reg-grade" v-model="registerForm.grade" required>
                  <option value="">Сыныпты таңдаңыз</option>
                  <option value="4">4 сынып</option>
                  <option value="5">5 сынып</option>
                  <option value="6">6 сынып</option>
                </select>
              </div>
            </div>

            <div v-if="registerRole === 'parent'">
              <div class="form-group">
                <label for="reg-studentcode">Бала коды</label>
                <input
                  type="text"
                  id="reg-studentcode"
                  v-model="registerForm.studentCode"
                  placeholder="Балаңыздың жеке коды"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="reg-phone">Телефон</label>
              <input
                type="tel"
                id="reg-phone"
                v-model="registerForm.phone"
                placeholder="+7 (___) ___-__-__"
                required
              />
            </div>

            <div class="form-group">
              <label for="reg-username">Логин</label>
              <input
                type="text"
                id="reg-username"
                v-model="registerForm.username"
                placeholder="Логин ойлап табыңыз"
                required
                minlength="4"
              />
            </div>

            <div class="form-group">
              <label for="reg-password">Құпия сөз</label>
              <input
                type="password"
                id="reg-password"
                v-model="registerForm.password"
                placeholder="Құпия сөз (кемінде 6 таңба)"
                required
                minlength="6"
              />
            </div>

            <div class="form-group">
              <label for="reg-confirm">Құпия сөзді қайталаңыз</label>
              <input
                type="password"
                id="reg-confirm"
                v-model="registerForm.confirmPassword"
                placeholder="Құпия сөзді қайталаңыз"
                required
              />
            </div>

            <button type="submit" class="submit-btn" :disabled="isRegistering">
              {{ isRegistering ? 'Тіркелуде...' : 'Тіркелу' }}
            </button>
          </form>

          <div v-if="newStudentCode" style="margin-top: 20px;">
            <button @click="goToLogin" class="submit-btn">Кіру бетіне өту</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '../services/api.js'

export default {
  name: 'Login',
  data() {
    return {
      currentTab: 'login',
      selectedRole: 'student',
      registerRole: 'student',
      errorMessage: '',
      successMessage: '',
      isRegistering: false,
      newStudentCode: '',
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        firstname: '',
        lastname: '',
        grade: '',
        school: '',
        studentCode: '',
        phone: '',
        username: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  mounted() {
    // No need to load users from localStorage anymore
  },
  methods: {

    selectRole(role) {
      this.selectedRole = role
      this.errorMessage = ''
    },

    switchTab(tab) {
      this.currentTab = tab
      this.errorMessage = ''
      this.successMessage = ''
      this.newStudentCode = ''
    },

    generateStudentCode() {
      const code = Math.floor(100000 + Math.random() * 900000).toString()
      const exists = this.users.some(u => u.studentCode === code)
      if (exists) {
        return this.generateStudentCode()
      }
      return code
    },

    async handleLogin() {
      this.errorMessage = ''

      if (!this.loginForm.username || !this.loginForm.password) {
        this.errorMessage = 'Барлық өрістерді толтырыңыз'
        return
      }

      try {
        // Login via API - this will store the JWT token
        const tokenResponse = await ApiService.login(
          this.loginForm.username,
          this.loginForm.password,
          this.selectedRole
        )

        // Get user info using the token
        const user = await ApiService.getCurrentUser()

        // Save user to session storage
        try {
          sessionStorage.setItem('currentUser', JSON.stringify(user))
        } catch (e) {
          console.warn('Could not save currentUser to sessionStorage:', e)
          window.currentUser = user
        }

        window.currentUser = user

        // Redirect based on role
        if (this.$router) {
          if (user.role === 'student') {
            this.$router.push('/student').catch(() => {})
          } else if (user.role === 'admin') {
            this.$router.push('/admin').catch(() => {})
          } else if (user.role === 'parent') {
            this.$router.push('/parent').catch(() => {})
          }
        }
      } catch (error) {
        this.errorMessage = error.message || 'Қате логин немесе құпия сөз'
      }
    },

    async handleRegister() {
      this.errorMessage = ''
      this.successMessage = ''

      // Validation
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.errorMessage = 'Құпия сөздер сәйкес емес'
        return
      }

      if (this.registerForm.password.length < 6) {
        this.errorMessage = 'Құпия сөз кемінде 6 таңбадан тұруы керек'
        return
      }

      if (this.registerForm.username.length < 4) {
        this.errorMessage = 'Логин кемінде 4 таңбадан тұруы керек'
        return
      }

      if (this.registerRole === 'student' && !this.registerForm.grade) {
        this.errorMessage = 'Сыныпты таңдаңыз'
        return
      }

      this.isRegistering = true

      try {
        // Prepare registration data
        const userData = {
          username: this.registerForm.username,
          password: this.registerForm.password,
          role: this.registerRole,
          firstname: this.registerForm.firstname,
          lastname: this.registerForm.lastname,
          phone: this.registerForm.phone
        }

        if (this.registerRole === 'student') {
          userData.grade = this.registerForm.grade
          userData.school = this.registerForm.school
        } else if (this.registerRole === 'parent') {
          userData.parent_student_code = this.registerForm.studentCode
        }

        // Register via API
        const newUser = await ApiService.register(userData)

        if (this.registerRole === 'student' && newUser.student_code) {
          this.newStudentCode = newUser.student_code
          this.successMessage = `Тіркелу сәтті өтті! Сіздің кодыңыз: ${newUser.student_code}`
        } else {
          this.successMessage = 'Тіркелу сәтті өтті! Енді кіре аласыз'
          setTimeout(() => {
            this.goToLogin()
          }, 2000)
        }

        // Reset form
        this.registerForm = {
          firstname: '',
          lastname: '',
          grade: '',
          school: '',
          studentCode: '',
          phone: '',
          username: '',
          password: '',
          confirmPassword: ''
        }
      } catch (error) {
        this.errorMessage = error.message || 'Тіркелу кезінде қате орын алды'
      } finally {
        this.isRegistering = false
      }
    },

    goToLogin() {
      this.currentTab = 'login'
      this.newStudentCode = ''
      this.successMessage = ''
      this.errorMessage = ''
    },

    getRoleName(role) {
      const names = {
        student: 'Оқушы',
        parent: 'Ата-ана',
        admin: 'Әкімші'
      }
      return names[role] || role
    }
  }
}
</script>

<style>
/* (copied original styles from your login.html) */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

#app {
  width: 100%;
  
}

.auth-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.header {
  background-color: #1565C0;
  padding: 40px 30px;
  text-align: center;
  color: white;
}

.header h1 {
  font-size: 28px;
  margin-bottom: 10px;
}

.header p {
  font-size: 14px;
  opacity: 0.9;
}

.tab-selector {
  display: flex;
  padding: 20px 30px 0;
  gap: 10px;
  border-bottom: 2px solid #f0f0f0;
}

.tab-btn {
  flex: 1;
  padding: 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: #999;
  position: relative;
  transition: color 0.3s;
}

.tab-btn:hover {
  color: #1565C0;
}

.tab-btn.active {
  color: #1565C0;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 3px;
  background-color: #1565C0;
  border-radius: 3px 3px 0 0;
}

.role-selector {
  display: flex;
  padding: 30px 30px 20px;
  gap: 15px;
}

.role-btn {
  flex: 1;
  padding: 15px 10px;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.role-btn:hover {
  border-color: #667eea;
  transform: translateY(-2px);
}

.role-btn.active {
  border-color: #667eea;
  background-color: #1565C0;
  color: white;
}

.role-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.role-text {
  font-size: 13px;
  font-weight: 600;
}

.form-container {
  padding: 0 30px 40px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 15px;
}

.form-row .form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 14px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 15px;
  transition: border-color 0.3s;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background-color: #1565C0;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.submit-btn:active {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  text-align: center;
}

.success-message {
  background: #efe;
  color: #3c3;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  text-align: center;
}

.parent-code-info {
  background: #f8f9ff;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 13px;
  color: #555;
  border-left: 3px solid #667eea;
}

.student-code-display {
  background: #f0f7ff;
  padding: 15px;
  border-radius: 10px;
  margin-top: 20px;
  text-align: center;
  border: 2px dashed #667eea;
}

.student-code-display h3 {
  color: #667eea;
  font-size: 14px;
  margin-bottom: 10px;
}

.student-code-display .code {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  letter-spacing: 2px;
  font-family: monospace;
}

.student-code-display p {
  font-size: 12px;
  color: #666;
  margin-top: 10px;
}
</style>
