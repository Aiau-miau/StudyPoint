<!-- src/views/Admin.vue -->
<template>
  <div>
    <div class="navbar">
      <div class="navbar-brand">StudyPoint Admin</div>
      <div style="display: flex; align-items: center; gap: 20px;">
        <span style="font-weight: 600; color: #0a2540; font-size: 14px;">Мұғалім</span>
        <button @click="logout" class="logout-btn">Шығу</button>
      </div>
    </div>

    <div class="ddashboard-content">
      <div class="welcome-card">
        <h2>Сәлем, {{ teacherName || 'Құрметті мұғалім' }}!</h2>
        <p>React компоненттері немесе JSON файлдарын жүктеңіз</p>
      </div>

      <div v-if="successMessage" class="success-message">
        <span>✓</span>
        <span>{{ successMessage }}</span>
      </div>
      <div v-if="errorMessage" class="error-message">
        <span>✗</span>
        <span>{{ errorMessage }}</span>
      </div>

      <div class="info-box">
        <div class="info-box-title">
          <span>ℹ️</span>
          <span>Нұсқаулық</span>
        </div>
        <div class="info-box-content">
          <strong>React компоненті:</strong> .jsx, .js файлдарын жүктеңіз (интерактив тапсырмалар)<br />
          <strong>JSON конфигурация:</strong> Тапсырма параметрлері бар .json файлын жүктеңіз<br />
          <strong>Назар:</strong> Файл жүктелгеннен кейін, ол оқушыларға қолжетімді болады
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Жаңа тапсырма жүктеу</h3>
          <button @click="showUploadModal = true" class="btn-primary">+ Тапсырма қосу</button>
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
                  {{ (task.fileType === 'react' ? 'React' : (task.fileType === 'json' ? 'JSON' : task.fileType)) }}
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
              <button @click="deleteTask(task)" class="delete-btn">Жою</button>
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
              :class="{ active: uploadType === 'react' }"
              @click.prevent="setUploadType('react')"
            >
              <div class="upload-type-title">React компоненті</div>
              <div class="upload-type-desc">Интерактивті тапсырма (.jsx, .js)</div>
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
            <button type="button" class="browse-btn" @click.stop="triggerFileInput">📁 Файл таңдау</button>
            <input
              type="file"
              ref="fileInput"
              @change="handleFileSelect"
              :accept="uploadType === 'react' ? '.js,.jsx' : '.json'"
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

          <div v-if="fileContent" class="code-preview">
            {{ fileContent.substring(0, 500) }}...
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

          <button type="submit" class="submit-btn" :disabled="!uploadedFile || !newTask.title">Жүктеу және сақтау</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '../services/api.js';

export default {
  name: 'Admin',
  data() {
    return {
      showUploadModal: false,
      uploadType: 'react',
      uploadedFile: null,
      fileContent: '',
      isDragging: false,
      successMessage: '',
      errorMessage: '',
      teacherName: '',
      rawUser: null,
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
    // Normalize server task -> client task shape
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
        // clear currently chosen file when switching type
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

    processFile(file) {
      console.log('processFile called, uploadType:', this.uploadType, 'file:', file);
      const validExtensions = this.uploadType === 'react' ? ['.js', '.jsx'] : ['.json'];
      const fileExt = '.' + file.name.split('.').pop().toLowerCase();
      if (!validExtensions.includes(fileExt)) {
        this.showError('Қате файл түрі! ' + validExtensions.join(', ') + ' файлдарын жүктеңіз');
        return;
      }
      this.uploadedFile = file;
      const reader = new FileReader();
      reader.onload = (e) => { this.fileContent = e.target.result || ''; };
      reader.readAsText(file);
    },

    removeFile() {
      this.uploadedFile = null;
      this.fileContent = '';
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

    // Try to upload JSON payload first; if server expects multipart, retry with FormData
    async uploadTask() {
      if (!this.uploadedFile || !this.newTask.title) {
        this.showError('Барлық міндетті өрістерді толтырыңыз!');
        return;
      }

      const payloadJson = {
        ...this.newTask,
        file_name: this.uploadedFile.name,
        file_type: this.uploadType,
        file_content: this.fileContent,
        upload_date: new Date().toLocaleDateString('kk-KZ')
      };

      console.log('Attempting createTask with JSON payload:', payloadJson);
      try {
        let res = await ApiService.createTask(payloadJson);
        // handle axios-like responses
        const created = res?.data ?? res;
        if (!created) throw new Error('No task returned from API');

        const normalized = this.normalizeTask(created);
        this.tasks.push(normalized);
        this.showSuccess('Тапсырма сәтті жүктелді!');
        this.closeUploadModal();
        return;
      } catch (err) {
        console.warn('createTask JSON failed, will try multipart if applicable. Error:', err);
        // If JSON failed, attempt multipart/form-data as fallback
      }

      // --- fallback to FormData upload (some backends expect real file upload) ---
      try {
        const form = new FormData();
        form.append('title', this.newTask.title);
        form.append('description', this.newTask.description);
        form.append('subject', this.newTask.subject || '');
        form.append('grade', this.newTask.grade || '');
        form.append('difficulty', this.newTask.difficulty || 'medium');
        form.append('timeLimit', this.newTask.timeLimit ?? 15);
        form.append('file_type', this.uploadType);
        form.append('file', this.uploadedFile); // send real file
        form.append('upload_date', new Date().toISOString());

        console.log('Attempting createTask with FormData, keys:', Array.from(form.keys()));
        const res2 = await ApiService.createTask(form, { isForm: true }); // note: ApiService must forward headers accordingly
        const created2 = res2?.data ?? res2;
        if (!created2) throw new Error('No task returned from API (form-data)');

        const normalized2 = this.normalizeTask(created2);
        this.tasks.push(normalized2);
        this.showSuccess('Тапсырма сәтті жүктелді!');
        this.closeUploadModal();
        return;
      } catch (err2) {
        console.error('FormData upload also failed:', err2);
        this.showError('Тапсырма жүктеу кезінде қате орын алды: ' + (err2?.message || err2));
      }
    },

    // Accept either task object or id; will delete on server and remove from UI
    async deleteTask(taskOrId) {
      const task = typeof taskOrId === 'object' ? taskOrId : null;
      const id = task ? (task.id ?? task._id ?? task.taskId) : taskOrId;

      if (!id) {
        this.showError('Жою үшін жарамды идентификатор табылмады.');
        return;
      }
      if (!confirm('Тапсырманы жоюды қалайсыз ба?')) return;

      try {
        console.log('Deleting task id:', id);
        await ApiService.deleteTask(id);
        // remove from local list by possible id fields
        this.tasks = this.tasks.filter(t => (t.id ?? t._id ?? t.taskId) !== id);
        this.showSuccess('Тапсырма жойылды');
      } catch (error) {
        console.error('Delete error:', error);
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
        if (this.$router) this.$router.push('/').catch(()=>{}); else window.location.href = '/';
      }
    }
  },

  async mounted() {
    // Load user info
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

    // Load tasks
    try {
      const raw = await ApiService.getTasks();
      const list = Array.isArray(raw) ? raw : (raw?.data ?? []);
      this.tasks = list.map(t => this.normalizeTask(t));
      console.log('Loaded tasks from API:', this.tasks);
    } catch (e) {
      console.warn('Failed to load tasks from API:', e);
      this.showError('Тапсырмаларды жүктеу кезінде қате орын алды');
    }
  }
};
</script>

<style>
/* (һ) — оригинал стильдеріңді сол қалпында қолдандым — қажет болса кейін оңтайландырсақ болады */
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
.btn-primary:hover { background: #0d47a1; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(24, 101, 242, 0.3); }
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
.code-preview { background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 8px; max-height: 250px; overflow: auto; font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.6; margin-bottom: 20px; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; color: #0a2540; font-weight: 600; font-size: 14px; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 12px; border: 2px solid #e5e5e5; border-radius: 6px; font-size: 14px; font-family: inherit; transition: border-color 0.2s; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #1565C0; box-shadow: 0 0 0 3px rgba(24, 101, 242, 0.1); }
.form-group textarea { min-height: 100px; resize: vertical; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.submit-btn { width: 100%; padding: 14px; background: #1565C0; color: white; border: none; border-radius: 6px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.submit-btn:hover { background: #0d47a1; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(24, 101, 242, 0.3); }
.submit-btn:disabled { background: #ccc; cursor: not-allowed; transform: none; opacity: 0.6; }
.task-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; margin-top: 20px; }
.task-card { background: white; border: 1px solid #e5e5e5; border-radius: 8px; padding: 20px; transition: all 0.2s; }
.task-card:hover { border-color: #1865f2; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(24, 101, 242, 0.1); }
.task-card-header { margin-bottom: 12px; }
.task-card-title { font-size: 16px; font-weight: 600; color: #0a2540; margin-bottom: 8px; }
.task-badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-right: 6px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
.badge-react { background: #e3f2fd; color: #1976d2; }
.badge-json { background: #fff9c4; color: #f57f17; }
.badge-grade { background: #f0f4ff; color: #1565C0; }
.task-card-desc { color: #697386; font-size: 13px; line-height: 1.5; margin-bottom: 16px; }
.task-card-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 1px solid #f0f0f0; }
.task-meta { font-size: 11px; color: #999; }
.delete-btn { background: #ee4444; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 600; transition: all 0.2s; }
.delete-btn:hover { background: #cc3333; }
.success-message { background: #e8f5e9; color: #2e7d32; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #4caf50; display: flex; align-items: center; gap: 10px; font-size: 14px; }
.error-message { background: #ffebee; color: #c62828; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #f44336; display: flex; align-items: center; gap: 10px; font-size: 14px; }
.empty-state { text-align: center; padding: 60px 20px; color: #697386; }
.empty-state-text { font-size: 15px; }
.info-box { background: #f0f4ff; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #1565C0; }
.info-box-title { font-weight: 600; color: #0d47a1; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; font-size: 14px; }
.info-box-content { font-size: 13px; color: #555; line-height: 1.6; }
</style>
