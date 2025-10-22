<template>
  <div>
    <div class="navbar">
      <div class="navbar-brand">StudyPoint</div>
      <div style="display: flex; align-items: center; gap: 20px;">
        <span style="font-weight: 600; color: #333;">{{ student.firstname }} {{ student.lastname }}</span>
        <button @click="logout" class="logout-btn">Шығу</button>
      </div>
    </div>

    <div v-if="!showTaskModal" class="dashboard-content">
      <!-- LEFT PANEL - Statistics -->
      <div class="left-panel">
        <div class="welcome-section">
          <div class="welcome-title">Сәлем, {{ student.firstname }}!</div>
          <div class="welcome-subtitle">{{ student.grade }}-сынып оқушысы</div>
        </div>

        <div class="stats-section">
          <div class="stats-title">Статистика</div>
          <div class="stat-item">
            <div class="stat-item-label">Барлық тапсырмалар</div>
            <div class="stat-item-value">{{ availableTasks.length }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-item-label">Орындалған</div>
            <div class="stat-item-value">{{ completedCount }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-item-label">Орындалмаған</div>
            <div class="stat-item-value">{{ pendingCount }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-item-label">Орташа баға</div>
            <div class="stat-item-value">{{ averageGrade }}%</div>
          </div>
        </div>
      </div>

      <!-- RIGHT PANEL - Tasks -->
      <div class="right-panel">
        <div class="section-header">
          <div class="section-title">Менің тапсырмаларым</div>
        </div>
        <div class="task-list">
          <div
            v-for="(task, index) in availableTasks"
            :key="task.id"
            class="task-item"
            @click="startTask(task)"
          >
          <div class="lleft"><div class="task-icon">{{ index + 1 }}</div>
            <div class="task-content">
              <div class="task-title">{{ task.title }}</div>
              <div class="task-description">{{ task.description }}</div>
            </div></div>
            <div class="rright"><div class="task-arrow">→</div></div>
            
          </div>
        </div>
      </div>
    </div>

    <!-- TASK MODAL -->
    <div v-if="showTaskModal" class="modal">
      <div class="modal-container">
        <!-- LEFT SIDEBAR -->
        <div class="left-sidebar">
          <div class="score-section">
            <div class="score-title">Жауап</div>
            <div class="score-value">{{ questionsAnswered }}</div>
          </div>

          <div class="timer-section">
            <div class="timer-title">Уақыт</div>
            <div class="timer-display">
              <div class="timer-value">{{ formattedTime }}</div>
              <div class="timer-labels">
              </div>
            </div>
          </div>

          <div class="smartscore-section">
            <div class="smartscore-title">Ұпай</div>
            <div class="smartscore-value">{{ smartScore }}</div>
            <div class="smartscore-subtitle">out of 100</div>
          </div>

          <div class="progress-section">
            <div class="progress-title">Progress</div>
            <div class="progress-items">
              <div
                v-for="(q, index) in questions"
                :key="index"
                class="progress-dot"
                :class="{
                  correct: q.answered && q.isCorrect,
                  wrong: q.answered && !q.isCorrect,
                  current: index === currentQuestion && !q.answered
                }"
              ></div>
            </div>
          </div>
        </div>

        <!-- RIGHT CONTENT -->
        <div class="right-content">
          <div class="question-header">
            <div class="question-title">{{ selectedTask.title }}</div>
            <button @click="exitTask" class="close-btn">&times;</button>
          </div>

          <div v-if="!taskCompleted" class="question-body">
            <div class="question-container">
              <div class="question-number-badge">
                 {{ currentQuestion + 1 }} / {{ totalQuestions }}
              </div>

              <div class="question-text">
                {{ questions[currentQuestion].text }}
              </div>

              <input
                type="text"
                class="answer-input"
                :class="{
                  correct: questions[currentQuestion].showFeedback && questions[currentQuestion].isCorrect,
                  wrong: questions[currentQuestion].showFeedback && !questions[currentQuestion].isCorrect
                }"
                v-model="currentAnswer"
                placeholder="Жауапты жазыңыз..."
                @keyup.enter="checkAnswer"
                :disabled="questions[currentQuestion].showFeedback"
              />

              <div
                v-if="questions[currentQuestion].showFeedback"
                class="feedback-message"
                :class="{ correct: questions[currentQuestion].isCorrect, wrong: !questions[currentQuestion].isCorrect }"
              >
                <div class="feedback-icon">{{ questions[currentQuestion].isCorrect ? '✓' : '✗' }}</div>
                <div>
                  {{ questions[currentQuestion].isCorrect ? 'Дұрыс! Керемет!' : 'Қате. Дұрыс жауап: ' + questions[currentQuestion].correctAnswer }}
                </div>
              </div>
            </div>
          </div>

          <div v-else class="question-body">
            <div class="completion-screen">
              <div class="completion-icon"></div>
              <div class="completion-title">Керемет жұмыс!</div>
              <div class="completion-score">{{ smartScore }}%</div>
              <div class="completion-desc">
                Сіз {{ correctAnswers }} / {{ totalQuestions }} сұраққа дұрыс жауап бердіңіз!<br />
                Нәтижелер сақталды және мұғалім көре алады.
              </div>
              <div class="completion-stats">
                <div class="stat-item">
                  <div class="stat-item-value">{{ questionsAnswered }}</div>
                  <div class="stat-item-label">Жауап берілді</div>
                </div>
                <div class="stat-item">
                  <div class="stat-item-value">{{ formattedTime }}</div>
                  <div class="stat-item-label">Уақыт</div>
                </div>
              </div>
              <button @click="exitTask" class="btn btn-next" style="margin-top: 40px; padding: 18px 40px; font-size: 18px;">
                Басты бетке оралу
              </button>
            </div>
          </div>

          <div v-if="!taskCompleted" class="question-footer">
            <button @click="skipQuestion" class="btn btn-skip">Өткізу</button>
            <div style="display: flex; gap: 15px;">
              <button
                v-if="!questions[currentQuestion].showFeedback"
                @click="checkAnswer"
                class="btn btn-check"
                :disabled="!currentAnswer.trim()"
              >
                Тексеру
              </button>
              <button v-else @click="nextQuestion" class="btn btn-next">
                {{ currentQuestion < totalQuestions - 1 ? 'Келесі сұрақ' : 'Аяқтау' }}
              </button>
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
  name: 'Student',
  data() {
    return {
      student: { id: null, firstname: 'Оқушы', lastname: '', grade: '–' },
      availableTasks: [],
      submissions: [],
      showTaskModal: false,
      selectedTask: null,
      currentQuestion: 0,
      currentAnswer: '',
      taskCompleted: false,
      startTime: null,
      elapsedSeconds: 0,
      timerInterval: null,
      smartScore: 0,
      questions: []
    };
  },
  computed: {
    totalQuestions() {
      return this.questions.length;
    },
    questionsAnswered() {
      return this.questions.filter(q => q.answered).length;
    },
    correctAnswers() {
      return this.questions.filter(q => q.answered && q.isCorrect).length;
    },
    completedCount() {
      return this.submissions.filter(s => s.student_id === this.student.id).length;
    },
    pendingCount() {
      return this.availableTasks.length - this.completedCount;
    },
    averageGrade() {
      const graded = this.submissions.filter(s => s.student_id === this.student.id && s.grade != null);
      if (!graded.length) return 0;
      const sum = graded.reduce((acc, s) => acc + s.grade, 0);
      return Math.round(sum / graded.length);
    },
    formattedTime() {
      const hrs = Math.floor(this.elapsedSeconds / 3600);
      const mins = Math.floor((this.elapsedSeconds % 3600) / 60);
      const secs = this.elapsedSeconds % 60;
      return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
  },
  methods: {
    normalizeTask(task) {
      if (!task) return null;
      
      return {
        id: task.id ?? task._id ?? task.taskId ?? null,
        title: task.title ?? task.name ?? '',
        description: task.description ?? task.desc ?? '',
        subject: task.subject ?? '',
        grade: task.grade ?? '',
        difficulty: task.difficulty ?? task.level ?? 'medium',
        timeLimit: task.timeLimit ?? task.time_limit ?? 15,
        fileType: (task.fileType ?? task.file_type ?? task.type ?? '').toString(),
        fileName: task.fileName ?? task.file_name ?? task.filename ?? '',
        fileContent: task.fileContent ?? task.file_content ?? task.content ?? '',
        uploadDate: task.uploadDate ?? task.upload_date ?? task.createdAt ?? ''
      };
    },

    startTask(task) {
      if (!task) return;

      console.log('=== startTask called ===');
      console.log('Task object:', task);
      console.log('Task fileType:', task.fileType);
      console.log('Task fileContent length:', task.fileContent?.length || 0);

      // preview react uploads in new window
      if (task.fileType === 'react' && task.fileContent) {
        this.openTaskInNewWindow(task);
        return;
      }

      // reset
      this.selectedTask = task;
      this.questions = [];

      // try parse json questions
      if (task.fileType === 'json' && task.fileContent) {
        try {
          console.log('Parsing JSON fileContent...');
          const parsed = JSON.parse(task.fileContent);
          console.log('Parsed structure:', parsed);
          
          if (Array.isArray(parsed.questions) && parsed.questions.length) {
            this.questions = parsed.questions.map(q => ({
              text: q.text || q.question || '',
              correctAnswer: String(q.correctAnswer ?? q.answer ?? '').trim(),
              answer: '',
              answered: false,
              isCorrect: false,
              showFeedback: false
            }));
            console.log(`✓ Successfully loaded ${this.questions.length} questions`);
          } else {
            console.warn('⚠ JSON task has no questions array or it\'s empty');
            console.warn('Parsed object:', parsed);
          }
        } catch (err) {
          console.error('✗ Failed to parse task.fileContent as JSON:', err);
          console.error('Raw fileContent:', task.fileContent?.substring(0, 200));
        }
      } else {
        console.warn('⚠ Task conditions not met for JSON parsing:', {
          fileType: task.fileType,
          expectedFileType: 'json',
          hasFileContent: !!task.fileContent,
          fileContentType: typeof task.fileContent
        });
      }

      // ensure at least one placeholder question
      if (!this.questions.length) {
        console.warn('⚠ No questions loaded, creating placeholder');
        this.questions = [{
          text: 'Сұрақ жүктелмеді. Тапсырма файлы дұрыс форматта емес немесе бос.',
          correctAnswer: '',
          answer: '',
          answered: false,
          isCorrect: false,
          showFeedback: false
        }];
      }

      // set UI state
      this.showTaskModal = true;
      this.currentQuestion = 0;
      this.currentAnswer = '';
      this.taskCompleted = false;
      this.smartScore = 0;

      // reset question flags
      this.questions.forEach(q => {
        q.answer = q.answer || '';
        q.answered = !!q.answered;
        q.isCorrect = !!q.isCorrect;
        q.showFeedback = !!q.showFeedback;
      });

      this.startTimer();
      console.log('=== startTask complete ===');
    },

    startTimer() {
      this.startTime = Date.now();
      this.elapsedSeconds = 0;
      if (this.timerInterval) clearInterval(this.timerInterval);
      this.timerInterval = setInterval(() => {
        this.elapsedSeconds = Math.floor((Date.now() - this.startTime) / 1000);
      }, 1000);
    },

    checkAnswer() {
      if (!this.currentAnswer.trim()) return;

      // if there are no real questions (edge-case), finish gracefully
      if (this.totalQuestions === 0) {
        this.finishTask();
        return;
      }

      const q = this.questions[this.currentQuestion];
      q.answer = this.currentAnswer.trim();
      q.answered = true;
      q.isCorrect = q.answer === q.correctAnswer;
      q.showFeedback = true;

      if (this.totalQuestions > 0) {
        if (q.isCorrect) this.smartScore = Math.min(100, this.smartScore + Math.floor(100 / this.totalQuestions));
        else this.smartScore = Math.max(0, this.smartScore - 5);
      }
    },

    nextQuestion() {
      if (this.currentQuestion < this.totalQuestions - 1) {
        this.currentQuestion++;
        this.currentAnswer = this.questions[this.currentQuestion].answer;
      } else this.finishTask();
    },

    skipQuestion() {
      if (this.currentQuestion < this.totalQuestions - 1) {
        this.currentQuestion++;
        this.currentAnswer = this.questions[this.currentQuestion].answer;
      }
    },

    async finishTask() {
      clearInterval(this.timerInterval);
      this.taskCompleted = true;

      const submission = {
        student_id: this.student.id,
        task_id: this.selectedTask.id,
        grade: this.smartScore,
        correct_answers: this.correctAnswers,
        total_questions: this.totalQuestions,
        time_spent: this.elapsedSeconds
      };

      try {
        const savedSubmission = await ApiService.createSubmission(submission);
        this.submissions.push(savedSubmission);
        console.log('Submission saved to API:', savedSubmission);
      } catch (e) {
        console.warn('Failed to save submission to API:', e);
        this.submissions.push({
          id: Date.now(),
          ...submission,
          submitted_at: new Date().toISOString()
        });
      }
    },

    exitTask() {
      clearInterval(this.timerInterval);
      this.showTaskModal = false;
      this.selectedTask = null;
    },

    logout() {
      if (confirm('Шығуды қалайсыз ба?')) {
        try {
          sessionStorage.removeItem('currentUser');
        } catch (e) {
          /* ignore */
        }
        window.currentUser = null;
        if (this.$router) this.$router.push('/').catch(()=>{});
        else window.location.href = '/';
      }
    },

    openTaskInNewWindow(task) {
      const w = window.open('', '_blank');
      w.document.write('<pre>' + (task.fileContent || '') + '</pre>');
      w.document.close();
    }
  },

  async mounted() {
    console.log('=== Student component mounted ===');
    
    // Load logged-in user
    let raw = null;
    try {
      raw = sessionStorage.getItem('currentUser');
    } catch (e) {
      console.warn('sessionStorage read error', e);
    }

    if (raw) {
      try {
        const u = JSON.parse(raw);
        this.student.id = u.id;
        this.student.firstname = u.firstname;
        this.student.lastname = u.lastname;
        this.student.grade = u.grade;
        console.log('✓ Loaded student from sessionStorage:', this.student);
      } catch (e) {
        console.warn('Failed to parse currentUser JSON from sessionStorage', e);
      }
    }

    // fallback to window.currentUser
    if (window.currentUser) {
      const u = window.currentUser;
      this.student.id = u.id;
      this.student.firstname = u.firstname;
      this.student.lastname = u.lastname;
      this.student.grade = u.grade;
      console.log('✓ Loaded student from window.currentUser:', this.student);
    }

    // Load tasks from API
    try {
      console.log('Loading tasks for grade:', this.student.grade);
      const rawTasks = await ApiService.getTasks(this.student.grade);
      console.log('Raw tasks from API:', rawTasks);
      
      // Normalize tasks
      const taskList = Array.isArray(rawTasks) ? rawTasks : (rawTasks?.data ?? []);
      this.availableTasks = taskList
        .map(t => this.normalizeTask(t))
        .filter(t => t !== null);
      
      console.log(`✓ Loaded ${this.availableTasks.length} tasks`);
      
      // Debug each task
      this.availableTasks.forEach((task, index) => {
        console.log(`Task ${index + 1}: "${task.title}"`);
        console.log(`  - fileType: ${task.fileType}`);
        console.log(`  - hasContent: ${!!task.fileContent}`);
        console.log(`  - contentLength: ${task.fileContent?.length || 0}`);
        if (task.fileType === 'json' && task.fileContent) {
          try {
            const parsed = JSON.parse(task.fileContent);
            console.log(`  - questions count: ${parsed.questions?.length || 0}`);
          } catch (e) {
            console.log(`  - ✗ JSON parse error: ${e.message}`);
          }
        }
      });
    } catch (e) {
      console.error('✗ Failed to load tasks from API:', e);
    }

    // Load submissions
    try {
      if (this.student.id) {
        this.submissions = await ApiService.getStudentSubmissions(this.student.id);
        console.log(`✓ Loaded ${this.submissions.length} submissions`);
      }
    } catch (e) {
      console.warn('Failed to load submissions from API:', e);
    }
    
    console.log('=== Student component mount complete ===');
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

.dashboard-content {
  display: flex;
  gap: 28px;
  width: 100%;
  padding: 28px 48px;
  min-height: calc(100vh - 72px);
  align-items: flex-start;
}

.left-panel {
  width: 360px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.welcome-section,
.stats-section {
  background: white;
  border-radius: 12px;
  padding: 26px;
  box-shadow: 0 6px 20px rgba(10, 20, 40, 0.04);
  border: 1px solid #e9eef6;
}

.welcome-title { font-size: 20px; font-weight: 700; margin-bottom: 6px; }
.welcome-subtitle { font-size: 14px; color: #5c677d; }

.stats-title {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  color: #6b7586;
  margin-bottom: 12px;
}

.stat-item { display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid #f1f4f8; }
.stat-item:last-child { border-bottom:none; }
.stat-item-label { color:#6b7586; font-size:14px; }
.stat-item-value { font-weight:800; color:#1565C0; font-size:20px; }

.right-panel { flex: 1; display:flex; flex-direction:column; gap:18px; }

.section-header { display:flex; justify-content:space-between; align-items:center; }
.section-title { font-size:26px; font-weight:800; }

.task-list { display:flex; flex-direction:column; gap:16px; }
.task-item {
  background:white;
  border-radius:12px;
  border:1px solid #e9eef6;
  padding:22px;
  display:flex;
  flex-direction: row;
  gap:20px;
  align-items:center;
  transition: transform .16s ease, box-shadow .16s ease;
  cursor:pointer;
}
.task-item:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(21,101,192,0.08); border-color:#1565C0; }
.task-icon { width:56px; height:56px; border-radius:12px; background:linear-gradient(135deg,#1565C0,#14bf96); color:white; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:20px; flex-shrink:0; }
.task-title { font-size:18px; font-weight:700; }
.task-description { font-size:14px; color:#5c677d; margin-top:4px; }
.task-arrow { font-size:24px; color:#1565C0; font-weight:700;}
.lleft { display:flex; gap:16px; align-items:center; flex:1; }

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
  display:flex;
}

.left-sidebar {
  width: 360px;
  background: white;
  border-right: 1px solid #e9eef6;
  display:flex;
  flex-direction:column;
  overflow-y:auto;
}

.score-section, .timer-section, .smartscore-section {
  border-radius:10px;
  overflow:hidden;
  border:1px solid #e9eef6;
}
.score-title, .timer-title, .smartscore-title {
  background:#1565C0; color:white; padding:10px; font-weight:700; font-size:13px; text-transform:uppercase;
}
.score-value, .smartscore-value { padding:28px; font-size:44px; font-weight:800; color:#1565C0; background:#f7f8fb; text-align:center; }

.progress-items { display:flex; gap:8px; flex-wrap:wrap; }
.progress-dot { width:20px; height:20px; border-radius:50%; border:2px solid #eef3f8; background:white; transition:all .18s; }
.progress-dot.correct { background:#14bf96; border-color:#14bf96; }
.progress-dot.wrong { background:#ee4444; border-color:#ee4444; }
.progress-dot.current { border-color:#1565C0; border-width:3px; }

.right-content { flex:1; background:#f7f8fb; display:flex; flex-direction:column;}

.question-header { background:white; padding:22px 32px; border-bottom:1px solid #e9eef6; display:flex; justify-content:space-between; align-items:center; }
.question-title { font-size:18px; font-weight:700; }
.close-btn { font-size:28px; background:none; border:none; cursor:pointer; color:#6b7586; padding:6px; border-radius:6px; }
.close-btn:hover { background:#f2f4f8; }

.question-body { flex:1; padding:46px; overflow:auto; display:flex; align-items:flex-start; justify-content:center; }
.question-container { width:100%; max-width:880px; }
.question-number-badge { background:#1565C0; color:white; padding:8px 18px; border-radius:20px; font-weight:700; display:inline-block; margin-bottom:18px; }
.question-text { font-size:24px; font-weight:600; margin-bottom:22px; color:#0a2540; }

.answer-input { width:100%; padding:16px 18px; border-radius:10px; border:2px solid #eef3f8; font-size:18px; transition:box-shadow .16s, border-color .16s; }
.answer-input:focus { outline:none; border-color:#1565C0; box-shadow:0 8px 24px rgba(21,101,192,0.12); }

.feedback-message { margin-top:18px; padding:16px 20px; border-radius:10px; display:flex; gap:12px; align-items:center; font-size:16px; }
.feedback-message.correct { background:#f0fdf9; color:#0d7a5f; border:1px solid #14bf96; }
.feedback-message.wrong { background:#fff5f5; color:#b71c1c; border:1px solid #ee4444; }

.question-footer { background:white; border-top:1px solid #e9eef6; padding:20px 36px; display:flex; justify-content:space-between; align-items:center; }
.btn { padding:12px 30px; border-radius:10px; font-weight:700; cursor:pointer; font-size:15px; border:none; transition:all .16s; }
.btn-check { background:#1565C0; color:white; }
.btn-next { background:#14bf96; color:white; }
.btn-skip { background:#f7f8fb; color:#6b7586; border:1px solid #eef3f8; }

.completion-screen { text-align:center; padding:72px 40px; }
.completion-score { font-size:64px; color:#14bf96; font-weight:900; margin:24px 0; }

@media (max-width: 1100px) {
  .left-panel { width: 300px; }
  .left-sidebar { width: 320px; }
  .question-container { max-width:700px; }
  .dashboard-content { padding: 18px; }
}

@media (max-width: 880px) {
  html, body { overflow-x: hidden; }

  .modal-container {
    flex-direction: column;
    height: 100vh;
    width: 100%;
    margin: 0;
    padding: 0;
  }

  .left-sidebar {
    display: flex !important;
    flex-direction: row !important;
    width: 100%;
    padding: 0;
    margin: 0;
    gap: 0;
  }

  .left-sidebar > .score-section,
  .left-sidebar > .timer-section,
  .left-sidebar > .smartscore-section {
    flex: 0 0 33.3333%;
    width: 33.3333%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 8px 6px;
    min-height: 72px;
    border: none;
  }

  .left-sidebar > .smartscore-section { border-right: none; }

  .left-sidebar .score-title,
  .left-sidebar .timer-title,
  .left-sidebar .smartscore-title {
    font-size: 12px;
    font-weight: 700;
    color:#155e9b;
    background-color: white;
    margin: 0;
    padding: 0;
    opacity: 0.95;
  }

  .left-sidebar .timer-value {
   font-size: 23px;
  }

  .left-sidebar .score-value {
   font-size: 23px;
  }
  
  .left-sidebar .smartscore-value {
   font-size: 23px;
  }

  .left-sidebar .timer-labels,
  .left-sidebar .smartscore-subtitle,
  .left-sidebar .progress-section { display: none !important; }

  .right-content {
    width: 100%;
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 14px;
    box-sizing: border-box;
    background: #fff;
    margin: 0;
    border-radius: 0;
    box-shadow: none;
  }

  .question-header { padding: 12px 14px; }
  .question-body { padding: 16px 14px; }
  .question-text { font-size: 20px; }

  .right-content, .modal, .modal-container, .left-sidebar, .left-sidebar > * {
    max-width: 100%;
    overflow-x: hidden;
  }
  .task-item{
    min-width: 370px;
    width: 100%;
  }
}
</style>