<!-- src/views/Parent.vue -->
<template>
  <div>
    <div class="navbar">
      <div class="navbar-brand">StudyPoint</div>
      <div style="display: flex; align-items: center; gap: 20px;">
        <span style="font-weight: 600; color: #333;">{{ parent.firstname }} {{ parent.lastname }}</span>
        <button @click="logout" class="logout-btn">Шығу</button>
      </div>
    </div>
    
    <div v-if="!showDetailModal" class="dashboard-content">
      <!-- LEFT PANEL - Child Info & Statistics -->
      <div class="left-panel">
        <div class="welcome-section">
          <div class="welcome-title">Сәлем, {{ parent.firstname }}!</div>
          <div class="welcome-subtitle">Балаңыздың оқу үлгерімін бақылаңыз</div>
        </div>

        <div class="child-card">
          <div class="child-header">
            <div class="child-avatar">👨‍🎓</div>
            <div class="child-info">
              <div class="child-name">{{ child.firstname }} {{ child.lastname }}</div>
              <div class="child-meta">{{ child.grade }} сынып • Код: {{ child.studentCode }}</div>
            </div>
          </div>
        </div>

        <div class="stats-section">
          <div class="stats-title">Статистика</div>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-item-label">Барлық тапсырмалар</div>
              <div class="stat-item-value">{{ allTasks.length }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-item-label">Орындалған</div>
              <div class="stat-item-value">{{ completedTasks }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-item-label">Орындалмаған</div>
              <div class="stat-item-value">{{ pendingTasks }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-item-label">Орташа баға</div>
              <div class="stat-item-value">{{ averageGrade }}%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT PANEL - Tasks -->
      <div class="right-panel">
        <div class="section-header">
          <div class="section-title">Баланың тапсырмалары</div>
        </div>

        <div v-if="allTasks.length === 0" class="empty-state">
          <div class="empty-icon">🔭</div>
          <div class="empty-text">Әзірше тапсырмалар жоқ</div>
        </div>

        <div v-else class="task-list">
          <div
            v-for="(task, index) in allTasks"
            :key="task.id"
            class="task-item"
            @click="viewTaskDetail(task)"
          >
            <div class="lleft">
              <div class="task-icon">{{ index + 1 }}</div>
              <div class="task-content">
                <div class="task-title">{{ task.title }}</div>
                <div class="task-description">{{ task.description }}</div>
                <div class="task-meta">
                  📚 {{ getSubjectName(task.subject) }} • ⏱️ {{ task.timeLimit }} минут
                </div>
              </div>
            </div>
            <div class="rright">
              <span :class="'task-status status-' + getTaskStatus(task.id)">
                {{ getStatusText(getTaskStatus(task.id)) }}
              </span>
              <div v-if="getTaskGrade(task.id)" class="task-grade">
                🏆 {{ getTaskGrade(task.id) }}%
              </div>
              <div class="task-arrow">→</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- DETAIL MODAL -->
    <div v-if="showDetailModal" class="modal">
      <div class="modal-container">
        <!-- LEFT SIDEBAR -->
        <div class="left-sidebar">
          <div class="score-section">
            <div class="score-title">Questions answered</div>
            <div class="score-value">{{ selectedSubmission ? selectedSubmission.correctAnswers : 0 }}</div>
          </div>

          <div class="timer-section">
            <div class="timer-title">Time spent</div>
            <div class="timer-display">
              <div class="timer-value">{{ formatTimeSpent(selectedSubmission ? selectedSubmission.timeSpent : 0) }}</div>
            </div>
          </div>

          <div class="smartscore-section">
            <div class="smartscore-title">SmartScore</div>
            <div class="smartscore-value">{{ selectedSubmission ? selectedSubmission.grade : 0 }}</div>
            <div class="smartscore-subtitle">out of 100</div>
          </div>

          <div class="progress-section" v-if="selectedSubmission">
            <div class="progress-title">Progress</div>
            <div class="progress-items">
              <div
                v-for="n in (selectedSubmission ? selectedSubmission.totalQuestions : 0)"
                :key="n"
                class="progress-dot"
                :class="{ correct: n <= (selectedSubmission ? selectedSubmission.correctAnswers : 0) }"
              ></div>
            </div>
          </div>
        </div>

        <!-- RIGHT CONTENT -->
        <div class="right-content">
          <div class="detail-header">
            <div class="detail-title">{{ selectedTask ? selectedTask.title : '' }}</div>
            <button @click="closeDetailModal" class="close-btn">&times;</button>
          </div>

          <div class="detail-body">
            <div class="detail-container">
              <div v-if="selectedSubmission" class="grade-display">
                <div class="grade-display-label">Балаңыздың бағасы</div>
                <div class="grade-display-value">{{ selectedSubmission.grade }}%</div>
                <div class="grade-display-subtitle">
                  {{ selectedSubmission.correctAnswers }} / {{ selectedSubmission.totalQuestions }} дұрыс жауап
                </div>
              </div>

              <div class="detail-section">
                <h3>📋 Тапсырма туралы</h3>
                <div class="detail-row">
                  <span class="detail-label">Атауы</span>
                  <span class="detail-value">{{ selectedTask ? selectedTask.title : '' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Пәні</span>
                  <span class="detail-value">{{ selectedTask ? getSubjectName(selectedTask.subject) : '' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Қиындық деңгейі</span>
                  <span class="detail-value">{{ selectedTask ? getDifficultyText(selectedTask.difficulty) : '' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Уақыт</span>
                  <span class="detail-value">{{ selectedTask ? selectedTask.timeLimit + ' минут' : '' }}</span>
                </div>
              </div>

              <div class="detail-section" v-if="selectedSubmission">
                <h3>📊 Статистика</h3>
                <div class="detail-row">
                  <span class="detail-label">Жіберілген күні</span>
                  <span class="detail-value">{{ formatDateTime(selectedSubmission.submittedAt) }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Жауап берілді</span>
                  <span class="detail-value">{{ selectedSubmission.correctAnswers }} / {{ selectedSubmission.totalQuestions }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Дұрыс жауаптар</span>
                  <span class="detail-value" style="color: #14bf96;">{{ selectedSubmission.correctAnswers }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Қате жауаптар</span>
                  <span class="detail-value" style="color: #ee4444;">{{ (selectedSubmission.totalQuestions || 0) - (selectedSubmission.correctAnswers || 0) }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Жұмсалған уақыт</span>
                  <span class="detail-value">{{ formatTimeSpent(selectedSubmission.timeSpent) }}</span>
                </div>
              </div>

              <div v-else class="detail-section" style="text-align: center; padding: 40px;">
                <div style="font-size: 48px; margin-bottom: 15px;">⏳</div>
                <div style="font-size: 18px; color: #666; margin-bottom: 10px;">Әзірше орындалмаған</div>
                <div style="font-size: 14px; color: #999;">Балаңыз бұл тапсырманы әлі орындаған жоқ</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '../services/api.js'

export default {
  name: 'Parent',
  data() {
    return {
      parent: {
        firstname: 'Гүлнар',
        lastname: 'Нұрланова'
      },
      child: {
        id: 1,
        firstname: 'Айдос',
        lastname: 'Нұрланов',
        grade: '4',
        studentCode: '123456'
      },
      tasks: [],
      submissions: [],
      showDetailModal: false,
      selectedTask: null,
      selectedSubmission: null
    };
  },
  computed: {
    allTasks() {
      return this.tasks.filter(t => {
        if (!t) return false;
        if (!t.grade || String(t.grade) === 'undefined' || t.grade === '') return true;
        return String(t.grade) === String(this.child.grade);
      });
    },
    completedTasks() {
      return this.submissions.filter(s => s.student_id === this.child.id && s.grade != null).length;
    },
    pendingTasks() {
      const submittedIds = this.submissions.filter(s => s.student_id === this.child.id).map(s => s.task_id);
      return this.allTasks.filter(t => !submittedIds.includes(t.id)).length;
    },
    averageGrade() {
      const graded = this.submissions.filter(s => s.student_id === this.child.id && s.grade != null);
      if (graded.length === 0) return 0;
      const sum = graded.reduce((acc, s) => acc + s.grade, 0);
      return Math.round(sum / graded.length);
    }
  },
  methods: {
    async loadData() {
      try {
        // Load tasks from API
        this.tasks = await ApiService.getTasks();
        console.log('Loaded tasks from API:', this.tasks);
      } catch (e) {
        console.warn('Failed to load tasks from API', e);
        this.tasks = [];
      }

      try {
        // Get the child's info using the student code
        if (this.child.studentCode) {
          const childInfo = await ApiService.getStudentByCode(this.child.studentCode);
          this.child.id = childInfo.id;
          this.child.firstname = childInfo.firstname;
          this.child.lastname = childInfo.lastname;
          this.child.grade = childInfo.grade;
          console.log('Loaded child info:', this.child);

          // Load submissions from API
          this.submissions = await ApiService.getStudentSubmissions(this.child.id);
          console.log('Loaded submissions from API:', this.submissions);
        }
      } catch (e) {
        console.warn('Failed to load child data from API', e);
        this.submissions = [];
      }
    },
    viewTaskDetail(task) {
      this.selectedTask = task;
      this.selectedSubmission = this.submissions.find(s => s.student_id === this.child.id && s.task_id === task.id) || null;
      this.showDetailModal = true;
    },
    closeDetailModal() {
      this.showDetailModal = false;
      this.selectedTask = null;
      this.selectedSubmission = null;
    },
    getTaskStatus(taskId) {
      const submission = this.submissions.find(s => s.student_id === this.child.id && s.task_id === taskId);
      return submission ? 'completed' : 'pending';
    },
    getTaskGrade(taskId) {
      const submission = this.submissions.find(s => s.student_id === this.child.id && s.task_id === taskId);
      return submission?.grade || null;
    },
    getStatusText(status) {
      return { pending: 'Орындалмаған', completed: 'Орындалған' }[status] || status;
    },
    getSubjectName(subject) {
      const map = {
        math: 'Математика',
        kazakh: 'Қазақ тілі',
        russian: 'Орыс тілі',
        english: 'Ағылшын тілі',
        science: 'Жаратылыстану'
      };
      return map[subject] || subject;
    },
    getDifficultyText(difficulty) {
      return { easy: 'Оңай', medium: 'Орташа', hard: 'Қиын' }[difficulty] || difficulty;
    },
    formatTimeSpent(seconds) {
      const hrs = Math.floor(seconds / 3600);
      const mins = Math.floor((seconds % 3600) / 60);
      const secs = seconds % 60;
      return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    },
    formatDateTime(date) {
      const d = new Date(date);
      return d.toLocaleDateString('kk-KZ') + ' ' + d.toLocaleTimeString('kk-KZ', { hour: '2-digit', minute: '2-digit' });
    },
    logout() {
      if (confirm('Шығуды қалайсыз ба?')) {
        if (this.$router) {
          this.$router.push('/').catch(() => {});
        } else {
          window.location.href = '/';
        }
      }
    }
  },
  async mounted() {
    // Load user info
    let raw = null;
    try {
      raw = sessionStorage.getItem('currentUser');
    } catch (e) {
      console.warn('sessionStorage read error', e);
    }

    if (raw) {
      try {
        const u = JSON.parse(raw);
        this.parent.firstname = u.firstname;
        this.parent.lastname = u.lastname;
        if (u.parent_student_code) {
          this.child.studentCode = u.parent_student_code;
        }
      } catch (e) {
        console.warn('Failed to parse currentUser JSON from sessionStorage', e);
      }
    }

    // Load data from API
    await this.loadData();
  }
};
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, #app {
  height: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
  background: #f5f7fb;
  color: #0a2540;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.4;
}

/* NAVBAR */
.navbar {
  width: 100%;
  background: white;
  padding: 14px 40px;
  border-bottom: 1px solid #e0e6ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 40;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

.navbar-brand {
  font-size: 22px;
  font-weight: 700;
  color: #1565C0;
}

.logout-btn {
  padding: 8px 18px;
  background: white;
  color: #1565C0;
  border: 1.5px solid #1565C0;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: 0.18s;
}
.logout-btn:hover { background: #1565C0; color: white; }

/* DASHBOARD */
.dashboard-content {
  display: flex;
  gap: 28px;
  width: 100%;
  padding: 28px 48px;
  min-height: calc(100vh - 72px);
  align-items: flex-start;
}

/* LEFT PANEL */
.left-panel {
  width: 360px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.welcome-section,
.child-card,
.stats-section {
  background: white;
  border-radius: 12px;
  padding: 26px;
  box-shadow: 0 6px 20px rgba(10, 20, 40, 0.04);
  border: 1px solid #e9eef6;
}

.welcome-title { font-size: 20px; font-weight: 700; margin-bottom: 6px; }
.welcome-subtitle { font-size: 14px; color: #5c677d; }

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
}

.stat-card {
  padding: 0;
  background: transparent;
}

.child-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.child-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1565C0, #14bf96);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.child-info {
  flex: 1;
}

.child-name {
  font-size: 18px;
  font-weight: 700;
  color: #0a2540;
  margin-bottom: 4px;
}

.child-meta {
  font-size: 14px;
  color: #5c677d;
}

.stats-title {
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  color: #9ca3af;
  margin-bottom: 24px;
  letter-spacing: 0.5px;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
}

.stat-card {
  padding: 20px 0;
  background: transparent;
  border-bottom: 1px solid #f1f4f8;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-card:last-child {
  border-bottom: none;
}

.stat-item-label { 
  color: #6b7586; 
  font-size: 15px;
  font-weight: 400;
}

.stat-item-value { 
  font-weight: 700; 
  color: #1565C0; 
  font-size: 28px;
}

/* RIGHT PANEL */
.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 26px;
  font-weight: 800;
}

/* EMPTY STATE */
.empty-state {
  background: white;
  border-radius: 12px;
  padding: 60px 40px;
  text-align: center;
  border: 1px solid #e9eef6;
  box-shadow: 0 6px 20px rgba(10, 20, 40, 0.04);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-text {
  font-size: 18px;
  color: #6b7586;
}

/* TASK LIST */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.task-item {
  background: white;
  border-radius: 12px;
  border: 1px solid #e9eef6;
  padding: 22px;
  display: flex;
  gap: 20px;
  align-items: center;
  justify-content: space-between;
  transition: transform .16s ease, box-shadow .16s ease;
  cursor: pointer;
}

.task-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(21,101,192,0.08);
  border-color: #1565C0;
}

.task-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: linear-gradient(135deg, #1565C0, #14bf96);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 20px;
  flex-shrink: 0;
}

.lleft {
  display: flex;
  gap: 16px;
  align-items: center;
  flex: 1;
}

.task-content {
  flex: 1;
}

.task-header-inline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 6px;
}

.task-title {
  font-size: 18px;
  font-weight: 700;
  color: #0a2540;
}

.task-description {
  font-size: 14px;
  color: #5c677d;
  margin-bottom: 10px;
}

.task-footer-inline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.task-meta {
  font-size: 13px;
  color: #6b7586;
}

.rright {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.task-status {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-completed {
  background: #d4edda;
  color: #155724;
}

.task-grade {
  font-size: 13px;
  color: #14bf96;
  font-weight: 700;
  white-space: nowrap;
}

.task-arrow {
  font-size: 24px;
  color: #1565C0;
  font-weight: 700;
  margin-left: 8px;
}

/* MODAL */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(4,8,16,0.6);
  z-index: 90;
  display: flex;
  align-items: stretch;
  justify-content: center;
}

.modal-container {
  width: 100%;
  height: 100vh;
  display: flex;
}

/* LEFT SIDEBAR */
.left-sidebar {
  width: 360px;
  background: white;
  padding: 28px;
  border-right: 1px solid #e9eef6;
  display: flex;
  flex-direction: column;
  gap: 22px;
  overflow-y: auto;
}

.score-section, .timer-section, .smartscore-section {
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e9eef6;
}

.score-title, .timer-title, .smartscore-title {
  background: #1565C0;
  color: white;
  padding: 10px;
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
}

.score-value, .smartscore-value {
  padding: 28px;
  font-size: 44px;
  font-weight: 800;
  color: #1565C0;
  background: #f7f8fb;
  text-align: center;
}

.timer-display {
  background: #f7f8fb;
  padding: 28px;
  text-align: center;
}

.timer-value {
  font-size: 32px;
  font-weight: 800;
  color: #1565C0;
  font-family: 'Courier New', monospace;
}

.smartscore-subtitle {
  padding: 10px;
  background: #f7f8fb;
  color: #6b7586;
  font-size: 12px;
  text-align: center;
}

.progress-section {
  padding: 20px;
  background: white;
  border-radius: 10px;
  border: 1px solid #e9eef6;
}

.progress-title {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  color: #6b7586;
  margin-bottom: 12px;
}

.progress-items {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.progress-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #eef3f8;
  background: white;
  transition: all .18s;
}

.progress-dot.correct {
  background: #14bf96;
  border-color: #14bf96;
}

/* RIGHT CONTENT */
.right-content {
  flex: 1;
  background: #f7f8fb;
  display: flex;
  flex-direction: column;
}

.detail-header {
  background: white;
  padding: 22px 32px;
  border-bottom: 1px solid #e9eef6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-title {
  font-size: 18px;
  font-weight: 700;
}

.close-btn {
  font-size: 28px;
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7586;
  padding: 6px;
  border-radius: 6px;
}

.close-btn:hover {
  background: #f2f4f8;
}

.detail-body {
  flex: 1;
  padding: 46px;
  overflow: auto;
}

.detail-container {
  max-width: 880px;
  margin: 0 auto;
}

.grade-display {
  background: linear-gradient(135deg, #1565C0, #14bf96);
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  margin-bottom: 24px;
}

.grade-display-label {
  color: white;
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 12px;
}

.grade-display-value {
  color: white;
  font-size: 64px;
  font-weight: 900;
}

.grade-display-subtitle {
  color: white;
  font-size: 16px;
  opacity: 0.9;
  margin-top: 12px;
}

.detail-section {
  background: white;
  border-radius: 12px;
  padding: 28px;
  margin-bottom: 20px;
  border: 1px solid #e9eef6;
}

.detail-section h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1565C0;
  margin-bottom: 20px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid #f1f4f8;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  color: #6b7586;
  font-size: 14px;
}

.detail-value {
  color: #0a2540;
  font-weight: 600;
  font-size: 14px;
}

/* RESPONSIVE */
@media (max-width: 1100px) {
  .left-panel { width: 300px; }
  .left-sidebar { width: 320px; }
  .dashboard-content { padding: 18px; }
}

@media (max-width: 880px) {
  .dashboard-content { flex-direction: column; padding: 12px; }
  .left-panel { width: 100%; order: 2; }
  .right-panel { order: 1; }
  .modal-container { flex-direction: column; }
  .left-sidebar { width: 100%; border-right: none; border-bottom: 1px solid #e9eef6; }
  .right-content { width: 100%; }
}
</style>