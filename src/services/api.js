// API service for connecting frontend to backend with JWT authentication
const API_BASE_URL = 'http://localhost:8000/api'

class ApiService {
  constructor() {
    this.token = localStorage.getItem('access_token')
  }

  setToken(token) {
    this.token = token
    localStorage.setItem('access_token', token)
  }

  clearToken() {
    this.token = null
    localStorage.removeItem('access_token')
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }

    // Add JWT token if available
    if (this.token) {
      config.headers['Authorization'] = `Bearer ${this.token}`
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Network error' }))
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
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
    const response = await this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password, role })
    })
    
    // Store the token
    if (response.access_token) {
      this.setToken(response.access_token)
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

  async createTask(taskData) {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData)
    })
  }

  async deleteTask(taskId) {
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