// API service for connecting frontend to backend with JWT authentication
const API_BASE_URL = 'http://localhost:8000/api'

class ApiService {
  constructor() {
    this.token = null
    this.loadToken()
    console.log('ApiService initialized, token:', this.token ? 'exists' : 'missing')
  }

  loadToken() {
    // Try multiple storage locations
    try {
      // First try localStorage
      this.token = localStorage.getItem('access_token')
      if (this.token) {
        console.log('✓ Token loaded from localStorage')
        return
      }

      // Then try sessionStorage
      this.token = sessionStorage.getItem('access_token')
      if (this.token) {
        console.log('✓ Token loaded from sessionStorage')
        return
      }

      console.warn('⚠ No token found in storage')
    } catch (e) {
      console.error('Error loading token:', e)
    }
  }

  setToken(token) {
    this.token = token
    if (token) {
      try {
        localStorage.setItem('access_token', token)
        sessionStorage.setItem('access_token', token)
        console.log('✓ Token saved to storage')
      } catch (e) {
        console.error('Error saving token:', e)
      }
    } else {
      this.clearToken()
    }
  }

  clearToken() {
    this.token = null
    try {
      localStorage.removeItem('access_token')
      sessionStorage.removeItem('access_token')
      console.log('✓ Token cleared from storage')
    } catch (e) {
      console.error('Error clearing token:', e)
    }
  }

  getToken() {
    if (!this.token) {
      this.loadToken()
    }
    return this.token
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const token = this.getToken()
    
    const config = {
      headers: {
        ...options.headers
      },
      ...options
    }

    // Don't set Content-Type for FormData (browser will set it with boundary)
    if (!options.isFormData) {
      config.headers['Content-Type'] = 'application/json'
    }

    // Add JWT token if available
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
      console.log(`✓ API Request: ${options.method || 'GET'} ${endpoint} (with auth)`)
    } else {
      console.warn(`⚠ API Request: ${options.method || 'GET'} ${endpoint} (NO AUTH TOKEN!)`)
    }

    console.log('Request config:', {
      url,
      method: options.method || 'GET',
      hasAuth: !!token,
      headers: config.headers
    })

    try {
      const response = await fetch(url, config)
      
      console.log(`Response status: ${response.status} ${response.statusText}`)

      // Handle 401 Unauthorized
      if (response.status === 401) {
        console.error('✗ 401 Unauthorized - Token invalid or expired')
        this.clearToken()
        
        // Don't redirect if it's a login attempt
        if (!endpoint.includes('/login')) {
          alert('Session expired. Please login again.')
          window.location.href = '/'
        }
        
        throw new Error('Unauthorized - please login again')
      }

      // Handle 403 Forbidden
      if (response.status === 403) {
        console.error('✗ 403 Forbidden - Access denied')
        const errorData = await response.json().catch(() => ({ detail: 'Access denied' }))
        console.error('403 Error details:', errorData)
        throw new Error(errorData.detail || 'Access denied')
      }
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Network error' }))
        console.error(`✗ API Error ${response.status}:`, errorData)
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }
      
      const data = await response.json()
      console.log(`✓ API Response success:`, data)
      return data
    } catch (error) {
      console.error('✗ API request failed:', error)
      throw error
    }
  }

  // User authentication
  async register(userData) {
    return this.request('/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  }

  async login(username, password, role) {
    console.log('Attempting login:', { username, role })
    
    const response = await this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password, role })
    })
    
    console.log('Login response:', response)
    
    // Store the token
    if (response.access_token) {
      this.setToken(response.access_token)
      console.log('✓ Login successful, token saved')
    } else {
      console.warn('⚠ Login response missing access_token')
    }
    
    return response
  }

  async getCurrentUser() {
    return this.request('/me')
  }

  async getUsers() {
    return this.request('/users')
  }

  async getStudentByCode(studentCode) {
    return this.request(`/users/student/${studentCode}`)
  }

  // Tasks
  async getTasks(grade = null) {
    const url = grade ? `/tasks?grade=${grade}` : '/tasks'
    return this.request(url)
  }

  async createTask(taskData, options = {}) {
    console.log('Creating task with data:', taskData)
    console.log('Options:', options)
    
    // Check if we have authentication
    const token = this.getToken()
    if (!token) {
      console.error('✗ Cannot create task: No authentication token!')
      throw new Error('Authentication required. Please login again.')
    }

    // Handle FormData
    if (options.isForm || taskData instanceof FormData) {
      console.log('Sending FormData...')
      return this.request('/tasks', {
        method: 'POST',
        body: taskData,
        isFormData: true
      })
    }

    // Handle JSON
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData)
    })
  }

  async deleteTask(taskId) {
    console.log('Deleting task:', taskId)
    
    // Check if we have authentication
    const token = this.getToken()
    if (!token) {
      console.error('✗ Cannot delete task: No authentication token!')
      throw new Error('Authentication required. Please login again.')
    }

    return this.request(`/tasks/${taskId}`, {
      method: 'DELETE'
    })
  }

  // Submissions
  async createSubmission(submissionData) {
    return this.request('/submissions', {
      method: 'POST',
      body: JSON.stringify(submissionData)
    })
  }

  async getSubmissions(studentId = null) {
    const url = studentId ? `/submissions?student_id=${studentId}` : '/submissions'
    return this.request(url)
  }

  async getStudentSubmissions(studentId) {
    return this.request(`/submissions/student/${studentId}`)
  }
}

export default new ApiService()