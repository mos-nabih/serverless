<script setup>
  import { Authenticator } from '@aws-amplify/ui-vue';
  import { reactive, onMounted } from "vue";
  import { fetchAuthSession } from 'aws-amplify/auth';
  import '@aws-amplify/ui-vue/styles.css';
  import axios from 'axios';

  const API_URL = import.meta.env.VITE_VUE_APP_API_URL || 'http://localhost:8000/api';

  const createTaskForm = reactive({ title: '' });

  const tasks = reactive({openTasks: [], closedTasks: []});

  const createTask = async () => {
    const { tokens } = await fetchAuthSession();

    const config = {headers: {Authorization: tokens.idToken.toString()}};
    await axios.post(`${API_URL}/create-task`, {title: createTaskForm.title}, config);
    createTaskForm.title = '';
    await listOpenTasks();
  }

  const listOpenTasks = async () => {
    const { tokens } = await fetchAuthSession();

    const config = {headers: {Authorization: tokens.idToken.toString()}};
    const response = await axios.get(`${API_URL}/open-tasks`, config);
    tasks.openTasks = response.data.results;
  }
  const listClosedTasks = async () => {
    const { tokens } = await fetchAuthSession();

    const config = {headers: {Authorization: tokens.idToken.toString()}};
    const response = await axios.get(`${API_URL}/closed-tasks`, config);
    tasks.closedTasks = response.data.results;
  }
  const closeTask = async (id) => {
    const { tokens } = await fetchAuthSession();

    const config = {headers: {Authorization: tokens.idToken.toString()}};
    await axios.post(`${API_URL}/close-task`, {id: id}, config);
    await listOpenTasks();
    await listClosedTasks();
  }
  onMounted(() => {
    listOpenTasks();
    listClosedTasks();
  })

</script>
<template>
  <authenticator username-alias="email" :login-mechanisms="['email']">
    <template v-slot="{ signOut }">
      <div class="app-shell">
        <el-menu
          class="top-nav"
          mode="horizontal"
          :ellipsis="false"
        >
          <el-menu-item index="brand" disabled>
            <span class="brand">
              <span class="brand-mark">F</span>
              <span>
                <strong>Fintastic</strong>
                <small>Security Remediation</small>
              </span>
            </span>
          </el-menu-item>
          <div class="flex-grow" />
          <el-menu-item index="0" @click="signOut">Sign out</el-menu-item>
        </el-menu>

        <section class="page-header">
          <div>
            <p class="intro">Track findings from scans, audits, and manual cloud reviews until each risk is remediated.</p>
          </div>
        </section>

        <el-card class="create-card">
          <el-form :model="createTaskForm" label-position="top">
            <el-form-item label="Security finding">
              <el-input
                v-model="createTaskForm.title"
                placeholder="Example: Review overly broad IAM permissions"
                size="large"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="large" @click="createTask">Add finding</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <div class="queue-grid">
          <el-row :gutter="20">
            <el-col :xs="24" :md="12">
              <el-card class="queue-card">
                <template #header>
                  <div class="card-header">
                    <span>Open findings</span>
                    <el-tag type="danger" effect="plain">{{ tasks.openTasks.length }}</el-tag>
                  </div>
                </template>
                <el-table :data="tasks.openTasks" empty-text="No open security findings">
                  <el-table-column prop="title" label="Finding" min-width="220" />
                  <el-table-column fixed="right" label="Action" width="150">
                    <template #default="scope">
                      <el-button link type="primary" size="large" @click="closeTask(scope.row.id)">Remediate</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-col>
            <el-col :xs="24" :md="12">
              <el-card class="queue-card">
                <template #header>
                  <div class="card-header">
                    <span>Remediated findings</span>
                    <el-tag type="success" effect="plain">{{ tasks.closedTasks.length }}</el-tag>
                  </div>
                </template>
                <el-table :data="tasks.closedTasks" empty-text="No remediated findings yet">
                  <el-table-column prop="title" label="Finding" />
                </el-table>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>
    </template>
  </authenticator>
</template>


<style lang="scss">
body {
  background:
    radial-gradient(circle at 14% 0%, rgba(16, 185, 129, 0.14), transparent 28rem),
    linear-gradient(135deg, #f8fffb 0%, #eefaf3 54%, #f6fbf8 100%);
}

#app {
  width: 100%;
  border-inline: 0;
  text-align: left;
}

.flex-grow {
  flex-grow: 1;
}

.app-shell {
  min-height: 100vh;
  color: #0d1f18;
}

.top-nav {
  padding: 0 24px;
  border-bottom: 1px solid #cbe8d7;
  background: rgba(255, 255, 255, 0.9);

  .brand {
    display: flex;
    align-items: center;
    gap: 12px;
    line-height: 1.15;
  }

  .brand-mark {
    display: grid;
    place-items: center;
    width: 38px;
    height: 38px;
    border-radius: 8px;
    color: #ffffff;
    font-weight: 900;
    background: linear-gradient(135deg, #059669, #34d399);
  }

  strong,
  small {
    display: block;
  }

  small {
    margin-top: 2px;
    color: #52675c;
    font-size: 0.78rem;
    font-weight: 600;
  }

  .el-menu-item.is-disabled {
    cursor: default;
    color: #0d1f18;
    font-weight: 700;
    opacity: 1;
  }
}

.page-header {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 24px 24px;

  h1 {
    margin: 4px 0 8px;
    color: #0d1f18;
    font-size: clamp(2rem, 4vw, 3.25rem);
    line-height: 1.05;
    letter-spacing: 0;
  }
}

.eyebrow {
  margin: 0;
  color: #047857;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.intro {
  max-width: 680px;
  color: #52675c;
  font-size: 1rem;
  line-height: 1.55;
}

.create-card,
.queue-grid {
  max-width: 1180px;
  margin-right: auto;
  margin-left: auto;
}

.create-card {
  margin-bottom: 20px;

  .el-card__body {
    padding: 22px 24px 4px;
  }

  .el-form-item__label {
    color: #0d1f18;
    font-weight: 700;
  }
}

.queue-grid {
  padding: 0 24px 32px;
}

.queue-card,
.create-card {
  border: 1px solid #cbe8d7;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 18px 55px rgba(15, 118, 84, 0.12);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: #0d1f18;
  font-weight: 800;
}

.el-button--primary {
  --el-button-bg-color: #059669;
  --el-button-border-color: #059669;
  --el-button-hover-bg-color: #047857;
  --el-button-hover-border-color: #047857;
}

.el-table {
  --el-table-header-text-color: #52675c;
  --el-table-text-color: #0d1f18;
}

@media (max-width: 768px) {
  .top-nav {
    padding: 0 12px;
  }

  .page-header {
    padding: 28px 16px 18px;
  }

  .create-card {
    margin-right: 16px;
    margin-left: 16px;
  }

  .queue-grid {
    padding: 0 16px 28px;
  }
}
</style>
