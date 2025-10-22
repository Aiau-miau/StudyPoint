<!-- src/views/Home.vue -->
<template>
  <div class="home-page">
    <div class="container">
      <div class="left">
        <div class="left-content">
          <h1>StudyPoint</h1>
          <p>Біздің платформаға тіркеліп, оқу сапарыңызды бүгіннен бастаңыз!</p>
          <img src="/images/main_img.png" alt="Welcome Image" @error="onImgError" />
        </div>
      </div>
      <div class="right">
        <h2>Қош келдіңіз!</h2>
        <p>Жүйеге кіру немесе жаңа аккаунт жасау</p>
        <div class="button-group">
          <button id="login_but" @click="go('/login')">Кіру</button>
          <button id="register_but" @click="go('/login')">Тіркелу</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    go(path) {
      this.$router.push(path).catch(() => {});
    },
    onImgError(e) {
      e.target.src = 'https://via.placeholder.com/400x300/667eea/ffffff?text=StudyPoint';
    }
  }
}
</script>

<style scoped>
/* wrapper fills viewport, so we don't touch global body/html */
.home-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%);
  padding: 20px; /* keep some breathing room on small screens */
}

/* main container (same rules as your original container) */
.container {
  display: flex;
  width: 100%;
  max-width: 1200px;
  height: 90vh;
  max-height: 700px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.left {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 50px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
}

.left::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.left-content { position: relative; z-index: 1; text-align: center; }

.left h1 {
  font-size: 42px;
  margin-bottom: 20px;
  color: #1565C0;
  font-weight: 700;
  letter-spacing: -1px;
}

.left p {
  font-size: 18px;
  color: #555;
  line-height: 1.8;
  margin-bottom: 40px;
  max-width: 400px;
}

.left img {
  width: 40%;
  max-width: 350px;
  filter: drop-shadow(0 20px 40px rgba(102,126,234,0.3));
  animation: float 3s ease-in-out infinite;
}

@keyframes float { 0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)} }

.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 50px;
  gap: 20px;
  background: white;
}

.right h2 { font-size: 32px; color: #333; margin-bottom: 10px; }
.right p { font-size: 16px; color: #666; margin-bottom: 30px; text-align: center; }

.button-group { display:flex; flex-direction:column; gap:15px; width:100%; max-width:320px; }

button {
  padding: 18px 50px;
  font-size: 18px;
  cursor: pointer;
  border-radius: 30px;
  border: none;
  font-weight: 600;
  transition: all .3s ease;
  width: 100%;
}

#login_but { background-color:#1565C0; color:white; box-shadow: 0 10px 30px rgba(102,126,234,0.4); }
#login_but:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(102,126,234,0.6); }

#register_but { background: white; border: 1px solid #1565C0; color:#1565C0; box-shadow:0 5px 15px rgba(0,0,0,0.1); }
#register_but:hover { background:#667eea; color:white; transform: translateY(-3px); }

/* responsive tweaks */
@media (max-width: 1024px) {
  .container { height: 90vh; }
  .left h1 { font-size: 36px; }
}

@media (max-width: 768px) {
  .home-page { padding: 10px; }
  .container { flex-direction: column; width: 95vw; height: auto; min-height: 95vh; border-radius: 20px; }
  .left { padding: 40px 30px; min-height: 50vh; }
  .left h1 { font-size: 32px; }
  .left p { font-size: 15px; margin-bottom: 30px; }
  .left img { width: 25%; max-width: 250px; }
  .right { padding: 40px 30px; }
  .right h2 { font-size: 24px; }
  .button-group { max-width: 280px; }
  button { padding: 16px 40px; font-size: 16px; border-radius: 12px; }
}

@media (max-width: 480px) {
  .container { width: 100vw; min-height: 100vh; border-radius: 0; }
  .left { padding: 30px 20px; }
  .left h1 { font-size: 28px; }
  .left p { font-size: 14px; }
  .left img { width: 25%; }
  .right { padding: 30px 20px; }
  .button-group { max-width: 100%; }
  button { padding: 15px 30px; font-size: 15px; }
}
</style>
