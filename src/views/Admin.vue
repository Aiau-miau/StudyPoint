<!-- src/views/Admin.vue -->
<template>
  <div>
    <div class="navbar">
      <div class="navbar-brand">StudyPoint Admin</div>
      <div style="display: flex; align-items: center; gap: 20px;">
        <span style="font-weight: 600; color: #0a2540; font-size: 14px;">{{ teacherName || 'Мұғалім' }}</span>
        <button @click="logout" class="logout-btn">Шығу</button>
      </div>
    </div>

    <div class="ddashboard-content">
      <div class="welcome-card">
        <h2>Сәлем, {{ teacherName || 'Құрметті мұғалім' }}!</h2>
      </div>

      <div v-if="!isAuthenticated" class="warning-message">
        <span>⚠️</span>
        <span>Аутентификация жоқ! Жүйеге кіруіңіз керек.</span>
        <button @click="redirectToLogin" class="btn-primary" style="margin-left: auto;">Кіру</button>
      </div>

      <div v-if="successMessage" class="success-message">
        <span>✔</span>
        <span>{{ successMessage }}</span>
      </div>
      <div v-if="errorMessage" class="error-message">
        <span>✗</span>
        <span>{{ errorMessage }}</span>
      </div>

      <div class="info-box">
        <div class="info-box-title">
          <span>Нұсқаулық</span>
        </div>
        <div class="info-box-content">
          <strong>Word файлдары:</strong> .docx файлдарын жүктеңіз (сұрақтар нөмірленуі керек: 1., 2., 3.)<br />
          <strong>JSON конфигурация:</strong> Тапсырма параметрлері бар .json файлын жүктеңіз<br />
          <strong>Назар:</strong> Файл жүктелгеннен кейін, ол оқушыларға қолжетімді болады
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Жаңа тапсырма жүктеу</h3>
          <button @click="openUploadModal" class="btn-primary" :disabled="!isAuthenticated">
            + Тапсырма қосу
          </button>
        </div>

        <div v-if="tasks.length === 0" class="empty-state">
          <div class="empty-state-text">Әзірше жүктелген тапсырмалар жоқ</div>
        </div>

        <div v-else class="task-grid">
          <div v-for="task in tasks" :key="task.id || task._id" class="task-card">
            <div class="task-card-header">
              <div class="task-card-title">{{ task.title }}</div>
              <div>
                <span :class="'task-badge badge-' + (task.fileType || 'json')">
                  {{ (task.fileType === 'word' ? 'Word' : (task.fileType === 'json' ? 'JSON' : task.fileType)) }}
                </span>
                <span class="task-badge badge-grade">{{ task.grade }} сынып</span>
              </div>
            </div>
            <div class="task-card-desc">{{ task.description }}</div>
            <div class="task-card-footer">
              <div class="task-meta">
                📄 {{ task.fileName }}<br />
                📅 {{ task.uploadDate }}
              </div>
              <button @click="deleteTask(task)" class="delete-btn" :disabled="!isAuthenticated">Жою</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Modal -->
    <div v-if="showUploadModal" @click.self="closeUploadModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">Жаңа тапсырма жүктеу</h3>
          <button @click="closeUploadModal" class="close-btn">&times;</button>
        </div>

        <form @submit.prevent="uploadTask">
          <div class="upload-type-selector">
            <div
              class="upload-type-btn"
              :class="{ active: uploadType === 'word' }"
              @click.prevent="setUploadType('word')"
            >
              <div class="upload-type-title">Word документ</div>
              <div class="upload-type-desc">Сұрақтары бар .docx файл</div>
            </div>
            <div
              class="upload-type-btn"
              :class="{ active: uploadType === 'json' }"
              @click.prevent="setUploadType('json')"
            >
              <div class="upload-type-title">JSON файл</div>
              <div class="upload-type-desc">Конфигурация файлы (.json)</div>
            </div>
          </div>

          <div
            class="file-upload-area"
            :class="{ dragover: isDragging }"
            @click="triggerFileInput"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleFileDrop"
          >
            <div class="upload-text">Файлды осы жерге апарыңыз</div>
            <div class="upload-subtext">немесе компьютерден таңдаңыз</div>
            <button type="button" class="browse-btn" @click.stop="triggerFileInput">🔍 Файл таңдау</button>
            <input
              type="file"
              ref="fileInput"
              @change="handleFileSelect"
              :accept="uploadType === 'word' ? '.docx' : '.json'"
              style="display: none;"
            />
          </div>

          <div v-if="uploadedFile" class="uploaded-file">
            <div class="file-info">
              <div class="file-details">
                <div class="file-name">{{ uploadedFile.name }}</div>
                <div class="file-size">{{ formatFileSize(uploadedFile.size) }}</div>
              </div>
            </div>
            <button type="button" @click="removeFile" class="remove-file-btn">Жою</button>
          </div>

          <!-- Word Preview -->
          <div v-if="uploadType === 'word' && parsedQuestions.length > 0" class="word-preview">
            <div class="preview-header">
              <strong>Табылған сұрақтар: {{ parsedQuestions.length }}</strong>
            </div>
            <div class="preview-list">
              <div v-for="(q, idx) in parsedQuestions.slice(0, 3)" :key="idx" class="preview-item">
                <div class="preview-number">{{ idx + 1 }}</div>
                <div class="preview-content">
                  <div class="preview-text">{{ q.text.substring(0, 100) }}{{ q.text.length > 100 ? '...' : '' }}</div>
                  <img v-if="q.imageUrl" :src="q.imageUrl" alt="Question image" class="preview-image" />
                </div>
                <div v-if="q.hasImage || q.imageUrl" class="preview-badge">🖼️ Сурет</div>
              </div>
              <div v-if="parsedQuestions.length > 3" class="preview-more">
                + тағы {{ parsedQuestions.length - 3 }} сұрақ
              </div>
            </div>
          </div>

          <!-- JSON Preview -->
          <div v-if="uploadType === 'json' && fileContent" class="json-preview-section">
            <div class="preview-header">
              <strong>JSON мазмұны:</strong>
            </div>
            <div class="code-preview">
              {{ fileContent.substring(0, 500) }}...
            </div>
            <div v-if="getJsonQuestions().length > 0" class="word-preview" style="margin-top: 16px;">
              <div class="preview-header">
                <strong>Сұрақтар алдын ала қарау: {{ getJsonQuestions().length }}</strong>
              </div>
              <div class="preview-list">
                <div v-for="(q, idx) in getJsonQuestions().slice(0, 3)" :key="idx" class="preview-item">
                  <div class="preview-number">{{ idx + 1 }}</div>
                  <div class="preview-content">
                    <div class="preview-text">{{ q.text.substring(0, 100) }}{{ q.text.length > 100 ? '...' : '' }}</div>
                    <img v-if="q.imageUrl" :src="q.imageUrl" alt="Question image" class="preview-image" />
                  </div>
                  <div v-if="q.imageUrl" class="preview-badge">🖼️ Сурет</div>
                </div>
                <div v-if="getJsonQuestions().length > 3" class="preview-more">
                  + тағы {{ getJsonQuestions().length - 3 }} сұрақ
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>Тапсырма атауы</label>
            <input type="text" v-model="newTask.title" placeholder="Мысалы: Айырманы бағалау" required />
          </div>

          <div class="form-group">
            <label>Сипаттама</label>
            <textarea v-model="newTask.description" placeholder="Тапсырманың қысқаша сипаттамасы" required></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Пән</label>
              <select v-model="newTask.subject" required>
                <option value="">Таңдаңыз</option>
                <option value="math">Математика</option>
                <option value="kazakh">Қазақ тілі</option>
                <option value="russian">Орыс тілі</option>
                <option value="english">Ағылшын тілі</option>
                <option value="science">Жаратылыстану</option>
              </select>
            </div>
            <div class="form-group">
              <label>Сынып</label>
              <select v-model="newTask.grade" required>
                <option value="">Таңдаңыз</option>
                <option value="4">4 сынып</option>
                <option value="5">5 сынып</option>
                <option value="6">6 сынып</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Қиындық деңгейі</label>
              <select v-model="newTask.difficulty" required>
                <option value="easy">Оңай</option>
                <option value="medium">Орташа</option>
                <option value="hard">Қиын</option>
              </select>
            </div>
            <div class="form-group">
              <label>Уақыты (минут)</label>
              <input type="number" v-model.number="newTask.timeLimit" min="5" value="15" />
            </div>
          </div>

          <button type="submit" class="submit-btn" :disabled="!uploadedFile || !newTask.title || !isAuthenticated || isProcessing">
            {{ isProcessing ? 'Өңделуде...' : 'Жүктеу және сақтау' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
// Mammoth.js will be loaded globally from index.html
import ApiService from '../services/api.js';

export default {
  name: 'Admin',
  data() {
    return {
      showUploadModal: false,
      uploadType: 'word',
      uploadedFile: null,
      fileContent: '',
      parsedQuestions: [],
      isDragging: false,
      successMessage: '',
      errorMessage: '',
      teacherName: '',
      rawUser: null,
      isAuthenticated: false,
      isProcessing: false,
      newTask: {
        title: '',
        description: '',
        subject: '',
        grade: '',
        difficulty: 'medium',
        timeLimit: 15
      },
      tasks: []
    };
  },
  methods: {
    checkAuthentication() {
      const token = ApiService.getToken()
      this.isAuthenticated = !!token
      console.log('Authentication status:', this.isAuthenticated ? '✓ Authenticated' : '✗ Not authenticated')
      
      if (!this.isAuthenticated) {
        this.showError('Аутентификация жоқ! Жүйеге кіруіңіз керек.')
      }
      
      return this.isAuthenticated
    },

    redirectToLogin() {
      if (this.$router) {
        this.$router.push('/').catch(() => {})
      } else {
        window.location.href = '/'
      }
    },

    openUploadModal() {
      if (!this.checkAuthentication()) {
        this.showError('Тапсырма жүктеу үшін жүйеге кіруіңіз керек!')
        return
      }
      this.showUploadModal = true
    },

    normalizeTask(serverTask = {}) {
      return {
        id: serverTask.id ?? serverTask._id ?? serverTask.taskId ?? null,
        title: serverTask.title ?? serverTask.name ?? '',
        description: serverTask.description ?? serverTask.desc ?? '',
        subject: serverTask.subject ?? '',
        grade: serverTask.grade ?? '',
        difficulty: serverTask.difficulty ?? serverTask.level ?? 'medium',
        timeLimit: serverTask.timeLimit ?? serverTask.time_limit ?? 15,
        fileType: (serverTask.fileType ?? serverTask.file_type ?? serverTask.type ?? '').toString(),
        fileName: serverTask.fileName ?? serverTask.file_name ?? serverTask.filename ?? '',
        fileContent: serverTask.fileContent ?? serverTask.file_content ?? '',
        uploadDate: serverTask.uploadDate ?? serverTask.upload_date ?? serverTask.createdAt ?? ''
      };
    },

    setUploadType(type) {
      if (this.uploadType !== type) {
        this.uploadType = type;
        this.removeFile();
      }
    },

    triggerFileInput() {
      if (this.$refs.fileInput) this.$refs.fileInput.click();
    },

    handleFileSelect(e) {
      if (e.target && e.target.files && e.target.files[0]) {
        this.processFile(e.target.files[0]);
      }
    },

    handleFileDrop(e) {
      this.isDragging = false;
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
        this.processFile(e.dataTransfer.files[0]);
      }
    },

    async processFile(file) {
      console.log('processFile called, uploadType:', this.uploadType, 'file:', file);
      
      if (this.uploadType === 'word') {
        const validExtensions = ['.docx'];
        const fileExt = '.' + file.name.split('.').pop().toLowerCase();
        if (!validExtensions.includes(fileExt)) {
          this.showError('Қате файл түрі! .docx файлдарын жүктеңіз');
          return;
        }
        
        this.uploadedFile = file;
        this.isProcessing = true;
        
        try {
          await this.parseWordFile(file);
          this.showSuccess(`${this.parsedQuestions.length} сұрақ табылды!`);
        } catch (error) {
          console.error('Word parse error:', error);
          this.showError('Word файлын оқу кезінде қате орын алды: ' + error.message);
          this.removeFile();
        } finally {
          this.isProcessing = false;
        }
      } else {
        // JSON file
        const validExtensions = ['.json'];
        const fileExt = '.' + file.name.split('.').pop().toLowerCase();
        if (!validExtensions.includes(fileExt)) {
          this.showError('Қате файл түрі! .json файлдарын жүктеңіз');
          return;
        }
        
        this.uploadedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => { 
          this.fileContent = e.target.result || ''; 
        };
        reader.readAsText(file);
      }
    },

    async parseWordFile(file) {
      const arrayBuffer = await file.arrayBuffer();
      const result = await mammoth.convertToHtml({ arrayBuffer: arrayBuffer });
      
      const parser = new DOMParser();
      const doc = parser.parseFromString(result.value, 'text/html');
      
      this.parsedQuestions = this.extractQuestions(doc);
      
      if (this.parsedQuestions.length === 0) {
        throw new Error('Файлда сұрақтар табылмады. Сұрақтар нөмірленгенін тексеріңіз (1., 2., 3.)');
      }
      
      // Convert to JSON format for storage
      const jsonContent = {
        questions: this.parsedQuestions.map(q => ({
          text: q.text,
          imageUrl: q.imageUrl || null,
          type: q.type,
          choices: q.choices,
          correctAnswer: q.correctAnswer
        }))
      };
      
      this.fileContent = JSON.stringify(jsonContent, null, 2);
    },

    extractQuestions(doc) {
      const questions = [];
      
      // Get all paragraphs from the document
      const paragraphs = Array.from(doc.querySelectorAll('p'));
      
      let currentQuestion = null;
      let currentChoices = [];
      let correctAnswer = '';
      
      for (let i = 0; i < paragraphs.length; i++) {
        const text = paragraphs[i].textContent.trim();
        if (!text) continue;
        
        console.log('Processing line:', text);
        
        // Check if line starts with number (e.g., "1.", "2.", "10.")
        const questionMatch = text.match(/^(\d+)\.\s*(.+)/);
        
        if (questionMatch) {
          // Save previous question if exists
          if (currentQuestion) {
            questions.push({
              text: currentQuestion,
              type: currentChoices.length >= 2 ? 'multiple-choice' : 'text-input',
              choices: currentChoices.length >= 2 ? currentChoices : null,
              correctAnswer: correctAnswer,
              hasImage: false
            });
            console.log('Saved question:', currentQuestion, 'with', currentChoices.length, 'choices');
          }
          
          // Start new question
          currentQuestion = questionMatch[2].trim();
          currentChoices = [];
          correctAnswer = '';
          console.log('New question found:', currentQuestion);
          continue;
        }
        
        // Check for choices (A), B), C), D))
        const choiceMatch = text.match(/^([A-DАБВГД])\)\s*(.+)/i);
        if (choiceMatch && currentQuestion) {
          const choiceText = choiceMatch[2].trim();
          currentChoices.push(choiceText);
          console.log('Choice found:', choiceText);
          continue;
        }
        
        // Check for correct answer - try multiple patterns
        const correctPatterns = [
          /Дұрыс жауап:\s*([A-DАБВГД])/i,
          /дұрыс жауап:\s*([A-DАБВГД])/i,
          /Жауап:\s*([A-DАБВГД])/i,
          /жауап:\s*([A-DАБВГД])/i
        ];
        
        let foundCorrect = false;
        for (const pattern of correctPatterns) {
          const correctMatch = text.match(pattern);
          if (correctMatch && currentQuestion) {
            const correctLetter = correctMatch[1].toUpperCase();
            const correctIndex = correctLetter.charCodeAt(0) - 65; // A=0, B=1, etc
            if (correctIndex >= 0 && correctIndex < currentChoices.length) {
              correctAnswer = currentChoices[correctIndex];
              console.log('Correct answer found:', correctLetter, '=', correctAnswer);
            }
            foundCorrect = true;
            break;
          }
        }
        
        if (foundCorrect) continue;
        
        // If not a special line and we have a current question, append to question text
        if (currentQuestion && 
            !text.match(/^[A-DАБВГД]\)/i) && 
            !text.match(/Дұрыс жауап/i) &&
            !text.match(/дұрыс жауап/i)) {
          currentQuestion += ' ' + text;
          console.log('Appending to question:', text);
        }
      }
      
      // Don't forget the last question
      if (currentQuestion) {
        questions.push({
          text: currentQuestion,
          type: currentChoices.length >= 2 ? 'multiple-choice' : 'text-input',
          choices: currentChoices.length >= 2 ? currentChoices : null,
          correctAnswer: correctAnswer,
          hasImage: false
        });
        console.log('Saved last question:', currentQuestion);
      }
      
      console.log('Total questions extracted:', questions.length);
      
      // Try to detect images
      const images = doc.querySelectorAll('img');
      if (images.length > 0) {
        images.forEach((img, index) => {
          if (questions[index]) {
            questions[index].hasImage = true;
            questions[index].imageUrl = img.src;
          }
        });
      }
      
      return questions;
    },

    removeFile() {
      this.uploadedFile = null;
      this.fileContent = '';
      this.parsedQuestions = [];
      if (this.$refs.fileInput) {
        try { this.$refs.fileInput.value = ''; } catch (e) { /* ignore */ }
      }
    },

    formatFileSize(bytes) {
      if (!bytes) return '0 B';
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    },

    async uploadTask() {
      if (!this.checkAuthentication()) {
        this.showError('Тапсырма жүктеу үшін жүйеге кіруіңіз керек!');
        return;
      }

      if (!this.uploadedFile || !this.newTask.title) {
        this.showError('Барлық міндетті өрістерді толтырыңыз!');
        return;
      }

      this.isProcessing = true;

      const payloadJson = {
        ...this.newTask,
        file_name: this.uploadedFile.name,
        file_type: this.uploadType === 'word' ? 'json' : this.uploadType, // Store as JSON
        file_content: this.fileContent,
        upload_date: new Date().toLocaleDateString('kk-KZ')
      };

      console.log('Attempting createTask with JSON payload:', payloadJson);
      try {
        let res = await ApiService.createTask(payloadJson);
        const created = res?.data ?? res;
        if (!created) throw new Error('No task returned from API');

        const normalized = this.normalizeTask(created);
        this.tasks.push(normalized);
        this.showSuccess('Тапсырма сәтті жүктелді!');
        this.closeUploadModal();
      } catch (err) {
        console.error('Task creation failed:', err);
        
        if (err.message && err.message.includes('Authentication')) {
          this.isAuthenticated = false;
          this.showError('Сессия аяқталды. Қайта кіруіңіз керек!');
          setTimeout(() => this.redirectToLogin(), 2000);
          return;
        }
        
        this.showError('Тапсырма жүктеу кезінде қате орын алды: ' + (err?.message || err));
      } finally {
        this.isProcessing = false;
      }
    },

    async deleteTask(taskOrId) {
      if (!this.checkAuthentication()) {
        this.showError('Тапсырма жою үшін жүйеге кіруіңіз керек!');
        return;
      }

      const task = typeof taskOrId === 'object' ? taskOrId : null;
      const id = task ? (task.id ?? task._id ?? task.taskId) : taskOrId;

      if (!id) {
        this.showError('Жою үшін жарамды идентификатор табылмады.');
        return;
      }
      if (!confirm('Тапсырманы жойуды қалайсыз ба?')) return;

      try {
        console.log('Deleting task id:', id);
        await ApiService.deleteTask(id);
        this.tasks = this.tasks.filter(t => (t.id ?? t._id ?? t.taskId) !== id);
        this.showSuccess('Тапсырма жойылды');
      } catch (error) {
        console.error('Delete error:', error);
        
        if (error.message && error.message.includes('Authentication')) {
          this.isAuthenticated = false;
          this.showError('Сессия аяқталды. Қайта кіруіңіз керек!');
          setTimeout(() => this.redirectToLogin(), 2000);
          return;
        }
        
        this.showError('Тапсырма жою кезінде қате орын алды: ' + (error?.message || error));
      }
    },

    closeUploadModal() {
      this.showUploadModal = false;
      this.removeFile();
      this.newTask = { title: '', description: '', subject: '', grade: '', difficulty: 'medium', timeLimit: 15 };
    },

    showSuccess(message) {
      this.successMessage = message;
      this.errorMessage = '';
      setTimeout(() => this.successMessage = '', 3000);
    },

    showError(message) {
      this.errorMessage = message;
      this.successMessage = '';
      setTimeout(() => this.errorMessage = '', 5000);
    },

    logout() {
      if (confirm('Шығуды қалайсыз ба?')) {
        ApiService.clearToken();
        this.isAuthenticated = false;
        if (this.$router) this.$router.push('/').catch(()=>{}); else window.location.href = '/';
      }
    },

    getJsonQuestions() {
      if (!this.fileContent) return [];
      try {
        const parsed = JSON.parse(this.fileContent);
        return parsed.questions || [];
      } catch (e) {
        return [];
      }
    }
  },

  async mounted() {
    console.log('=== Admin component mounted ===');
    
    this.checkAuthentication();

    try {
      const sessionRaw = sessionStorage.getItem('currentUser');
      if (sessionRaw) this.rawUser = JSON.parse(sessionRaw);
    } catch (e) { console.warn('sessionStorage read failed:', e); }

    if (!this.rawUser && window.currentUser) this.rawUser = window.currentUser;
    if (this.rawUser) {
      const u = this.rawUser;
      const name = ((u.firstname || '') + ' ' + (u.lastname || '')).trim() || (u.username || '') || (u.name || '');
      this.teacherName = name;
    }

    if (this.isAuthenticated) {
      try {
        const raw = await ApiService.getTasks();
        const list = Array.isArray(raw) ? raw : (raw?.data ?? []);
        this.tasks = list.map(t => this.normalizeTask(t));
        console.log('✓ Loaded tasks from API:', this.tasks.length);
      } catch (e) {
        console.error('✗ Failed to load tasks from API:', e);
        
        if (e.message && e.message.includes('Authentication')) {
          this.isAuthenticated = false;
          this.showError('Сессия аяқталды. Қайта кіруіңіз керек!');
        } else {
          this.showError('Тапсырмаларды жүктеу кезінде қате орын алды');
        }
      }
    } else {
      this.showError('Тапсырмаларды көру үшін жүйеге кіруіңіз керек!');
    }
    
    console.log('=== Admin component mount complete ===');
  }
};
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: #f7f8fa; min-height: 100vh; }
.navbar { background: white; padding: 12px 24px; border-bottom: 1px solid #e5e5e5; display: flex; justify-content: space-between; align-items: center; }
.navbar-brand { font-size: 20px; font-weight: 700; color: #1565C0; display: flex; align-items: center; gap: 8px; }
.logout-btn { padding: 8px 16px; background: white; color: #1565C0; border: 1px solid #1565C0; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 14px; transition: all 0.2s; }
.logout-btn:hover { background: #1865f2; color: white; }
.ddashboard-content { padding: 24px; max-width: 1400px; margin: 0 auto; }
.welcome-card { background: white; padding: 32px; border-radius: 8px; border: 1px solid #e5e5e5; margin-bottom: 24px; }
.welcome-card h2 { font-size: 28px; font-weight: 700; color: #0a2540; margin-bottom: 8px; }
.welcome-card p { font-size: 15px; color: #697386; }
.card { background: white; padding: 24px; border-radius: 8px; border: 1px solid #e5e5e5; margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.card-title { font-size: 20px; font-weight: 700; color: #0a2540; }
.btn-primary { background: #1565C0; color: white; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 14px; transition: all 0.2s; }
.btn-primary:hover:not(:disabled) { background: #0d47a1; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(24, 101, 242, 0.3); }
.btn-primary:disabled { background: #ccc; cursor: not-allowed; opacity: 0.6; }
.modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; padding: 20px; }
.modal-content { background: white; padding: 32px; border-radius: 12px; max-width: 800px; width: 100%; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e5e5e5; }
.modal-title { font-size: 24px; font-weight: 700; color: #0a2540; }
.close-btn { font-size: 24px; background: none; border: none; cursor: pointer; color: #697386; padding: 0; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 4px; transition: all 0.2s; }
.close-btn:hover { background: #f0f0f0; }
.upload-type-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 24px; }
.upload-type-btn { padding: 20px; border: 2px solid #e5e5e5; border-radius: 8px; cursor: pointer; text-align: center; transition: all 0.2s; background: white; }
.upload-type-btn:hover { border-color: #1565C0; background: #f7f8fa; }
.upload-type-btn.active { border-color: #1565C0; background: #f0f4ff; }
.upload-type-title { font-weight: 600; color: #0a2540; margin-bottom: 4px; font-size: 15px; }
.upload-type-desc { font-size: 13px; color: #697386; }
.file-upload-area { border: 2px dashed #1565C0; border-radius: 8px; padding: 40px 30px; text-align: center; cursor: pointer; background: #f7f9fc; margin-bottom: 20px; transition: all 0.2s; }
.file-upload-area:hover { background: #f0f4ff; border-color: #0d47a1; }
.file-upload-area.dragover { background: #e8f0ff; border-color: #1565C0; transform: scale(1.01); }
.upload-text { font-size: 16px; font-weight: 600; color: #0a2540; margin-bottom: 8px; }
.upload-subtext { color: #697386; font-size: 14px; margin-bottom: 16px; }
.browse-btn { background: #1565C0; color: white; padding: 10px 24px; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 14px; transition: all 0.2s; }
.browse-btn:hover { background: #0d47a1; }
.uploaded-file { background: #f0f4ff; padding: 16px 20px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border: 2px solid #1565C0; }
.file-info { display: flex; align-items: center; gap: 12px; flex: 1; }
.file-details { flex: 1; }
.file-name { font-weight: 600; color: #0a2540; margin-bottom: 4px; font-size: 14px; }
.file-size { font-size: 12px; color: #697386; }
.remove-file-btn { background: #ee4444; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; transition: all 0.2s; }
.remove-file-btn:hover { background: #cc3333; }
.word-preview { background: #f7f9fc; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #e5e5e5; }
.preview-header { font-size: 15px; color: #0a2540; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #e5e5e5; }
.preview-list { display: flex; flex-direction: column; gap: 12px; }
.preview-item { display: flex; gap: 12px; align-items: flex-start; padding: 12px; background: white; border-radius: 6px; border: 1px solid #e5e5e5; }
.preview-number { width: 32px; height: 32px; border-radius: 50%; background: #1565C0; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }
.preview-content { flex: 1; display: flex; flex-direction: column; gap: 8px; }
.preview-text { font-size: 14px; color: #0a2540; line-height: 1.5; }
.preview-image { max-width: 100%; height: auto; max-height: 200px; border-radius: 6px; border: 1px solid #e5e5e5; object-fit: contain; margin-top: 8px; }
.preview-badge { background: #14bf96; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; white-space: nowrap; align-self: flex-start; }
.preview-more { text-align: center; padding: 12px; color: #697386; font-size: 14px; font-style: italic; }
.json-preview-section { margin-bottom: 20px; }
.code-preview { background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 8px; max-height: 250px; overflow: auto; font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.6; margin-bottom: 20px; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; color: #0a2540; font-weight: 600; font-size: 14px; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 12px; border: 2px solid #e5e5e5; border-radius: 6px; font-size: 14px; font-family: inherit; transition: border-color 0.2s; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #1565C0; box-shadow: 0 0 0 3px rgba(24, 101, 242, 0.1); }
.form-group textarea { min-height: 100px; resize: vertical; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.submit-btn { width: 100%; padding: 14px; background: #1565C0; color: white; border: none; border-radius: 6px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.submit-btn:hover:not(:disabled) { background: #0d47a1; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(24, 101, 242, 0.3); }
.submit-btn:disabled { background: #ccc; cursor: not-allowed; transform: none; opacity: 0.6; }
.task-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; margin-top: 20px; }
.task-card { background: white; border: 1px solid #e5e5e5; border-radius: 8px; padding: 20px; transition: all 0.2s; }
.task-card:hover { border-color: #1865f2; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(24, 101, 242, 0.1); }
.task-card-header { margin-bottom: 12px; }
.task-card-title { font-size: 16px; font-weight: 600; color: #0a2540; margin-bottom: 8px; }
.task-badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-right: 6px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
.badge-word { background: #e3f2fd; color: #1976d2; }
.badge-json { background: #fff9c4; color: #f57f17; }
.badge-grade { background: #f0f4ff; color: #1565C0; }
.task-card-desc { color: #697386; font-size: 13px; line-height: 1.5; margin-bottom: 16px; }
.task-card-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 1px solid #f0f0f0; }
.task-meta { font-size: 11px; color: #999; }
.delete-btn { background: #ee4444; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 600; transition: all 0.2s; }
.delete-btn:hover:not(:disabled) { background: #cc3333; }
.delete-btn:disabled { background: #ccc; cursor: not-allowed; opacity: 0.6; }
.success-message { background: #e8f5e9; color: #2e7d32; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #4caf50; display: flex; align-items: center; gap: 10px; font-size: 14px; }
.error-message { background: #ffebee; color: #c62828; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #f44336; display: flex; align-items: center; gap: 10px; font-size: 14px; }
.warning-message { background: #fff3e0; color: #e65100; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #ff9800; display: flex; align-items: center; gap: 10px; font-size: 14px; }
.empty-state { text-align: center; padding: 60px 20px; color: #697386; }
.empty-state-text { font-size: 15px; }
.info-box { background: #f0f4ff; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #1565C0; }
.info-box-title { font-weight: 600; color: #0d47a1; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; font-size: 14px; }
.info-box-content { font-size: 13px; color: #555; line-height: 1.6; }
@media (max-width: 768px) {
  .modal-content { padding: 20px; }
  .upload-type-selector { grid-template-columns: 1fr; }
  .form-row { grid-template-columns: 1fr; }
  .task-grid { grid-template-columns: 1fr; }
}
</style>