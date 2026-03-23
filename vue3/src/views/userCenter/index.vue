<template>
  <div class="app-container">
    <!-- 加载中状态 -->
    <el-loading v-loading="loading" element-loading-text="加载中..." fullscreen />
    
    <el-row :gutter="24">
      <!-- 个人信息卡片 -->
      <el-col :span="6">
        <el-card class="box-card user-info-card">
          <template v-slot:header>
            <div class="card-header">
              <span class="card-title">个人信息</span>
            </div>
          </template>
          
          <!-- 头像区域 -->
          <div class="avatar-section">
            <div class="avatar-container">
              <el-avatar :size="80" :src="avatarUrl" class="user-avatar">
                {{ currentUser.username ? currentUser.username.charAt(0).toUpperCase() : 'U' }}
              </el-avatar>
              <el-button type="primary" size="small" class="avatar-upload-btn" @click="handleAvatarUpload">
                确认更换
              </el-button>
              <!-- 头像上传输入框 -->
              <input type="file" ref="avatarInput" style="display: none;" accept="image/*" @change="uploadAvatar">
            </div>
          </div>
          
          <!-- 个人信息列表 -->
          <ul class="info-list">
            <li class="info-item">
              <div class="info-label">
                <svg-icon icon="user" class="info-icon" />
                <span>用户名称</span>
              </div>
              <div class="info-value">{{ currentUser.username || '加载中...' }}</div>
            </li>
            <li class="info-item">
              <div class="info-label">
                <svg-icon icon="phone" class="info-icon" />
                <span>手机号码</span>
              </div>
              <div class="info-value">{{ currentUser.phonenumber || '加载中...' }}</div>
            </li>
            <li class="info-item">
              <div class="info-label">
                <svg-icon icon="email" class="info-icon" />
                <span>用户邮箱</span>
              </div>
              <div class="info-value">{{ currentUser.email || '加载中...' }}</div>
            </li>
            <li class="info-item">
              <div class="info-label">
                <svg-icon icon="peoples" class="info-icon" />
                <span>所属角色</span>
              </div>
              <div class="info-value">{{ currentUser.role || '未设置' }}</div>
            </li>
            <li class="info-item">
              <div class="info-label">
                <svg-icon icon="date" class="info-icon" />
                <span>创建日期</span>
              </div>
              <div class="info-value">{{ currentUser.login_date || '加载中...' }}</div>
            </li>
          </ul>
        </el-card>
      </el-col>
      
      <!-- 基本资料卡片 -->
      <el-col :span="18">
        <el-card class="box-card profile-card">
          <template v-slot:header>
            <div class="card-header">
              <span class="card-title">基本资料</span>
            </div>
          </template>
          
          <el-tabs v-model="activeTab" class="profile-tabs">
            <!-- 基本资料标签页 -->
            <el-tab-pane label="基本资料" name="userinfo">
              <div class="tab-content">
                <el-form :model="userForm" :rules="userFormRules" ref="userFormRef" label-position="left" label-width="120px" class="user-form">
                  <el-form-item label="手机号码" prop="phonenumber">
                    <el-input v-model="userForm.phonenumber" placeholder="请输入手机号码" />
                  </el-form-item>
                  <el-form-item label="用户邮箱" prop="email">
                    <el-input v-model="userForm.email" placeholder="请输入邮箱" />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" class="form-btn" @click="handleSaveUserInfo">保存</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>
            
            <!-- 修改密码标签页 -->
            <el-tab-pane label="修改密码" name="resetPwd">
              <div class="tab-content">
                <el-form :model="pwdForm" :rules="pwdFormRules" ref="pwdFormRef" label-position="left" label-width="120px" class="pwd-form">
                  <el-form-item label="原密码" prop="oldPassword">
                    <el-input v-model="pwdForm.oldPassword" type="password" placeholder="请输入原密码" />
                  </el-form-item>
                  <el-form-item label="新密码" prop="newPassword">
                    <el-input v-model="pwdForm.newPassword" type="password" placeholder="请输入新密码" />
                  </el-form-item>
                  <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input v-model="pwdForm.confirmPassword" type="password" placeholder="请确认新密码" />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" class="form-btn" @click="handleChangePassword">修改密码</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import request,{getServerUrl} from '@/util/request';
import { ref } from 'vue';
import { ElMessage } from 'element-plus';



export default {
  name: 'UserCenter',
  data() {
    return {
      loading: false,
      activeTab: 'userinfo',
      avatarUrl:   '', // 头像URL，可根据实际情况设置
      currentUser: {}, // 用户基本信息
      userForm: {}, // 用户表单
      pwdForm: {}, // 密码修改表单
      userFormRules: {
        phonenumber: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ]
      },
      pwdFormRules: {
        oldPassword: [
          { required: true, message: '请输入原密码', trigger: 'blur' }
        ],
        newPassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '新密码长度不能少于6个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认新密码', trigger: 'blur' },
          { validator: (rule, value, callback) => {
              if (value !== this.pwdForm.newPassword) {
                callback(new Error('两次输入的密码不一致'));
              } else {
                callback();
              }
            }, trigger: 'blur' }
        ]
      }
    };
  },
  mounted() {
    // 组件挂载时获取数据
    this.loadUserData();
  },
  methods: {
    // 加载用户数据
    async loadUserData() {
      this.loading = true;
      try {
        // 模拟API请求，实际项目中替换为真实API
        const userInfoResponse = await this.getUserInfo();
        this.currentUser = userInfoResponse.data;
        this.avatarUrl = getServerUrl()+'/media/userAvatar/'+this.currentUser.avatar || '';
        this.userForm = { ...userInfoResponse.data };
      } catch (error) {
        console.error('加载用户数据失败:', error);
        this.$message.error('加载用户数据失败');
      } finally {
        this.loading = false;
      }
    },
    
    // 获取用户基本信息
    async getUserInfo() {
      const currentUserStr = sessionStorage.getItem('currentUser');
      if (currentUserStr) {
        const userData = JSON.parse(currentUserStr);
        this.avatarUrl = getServerUrl()+'/media/userAvatar/'+userData.avatar || '';
        return { data: userData };
      } else {
        // 如果sessionStorage中没有数据，返回默认数据
        return {
          data: {
            username: 'java1234',
            phonenumber: '18862857417',
            email: 'caofeng4017@126.com',
            role: '管理员',
            login_date: '2022-08-29 22:10:52'
          }
        };
      }
    },
    
    // 处理头像上传
    handleAvatarUpload() {
      // 触发文件选择
      this.$refs.avatarInput.click();
    },
    
    // 上传头像
    async uploadAvatar(e) {
      const file = e.target.files[0];
      if (!file) return;
      
      // 检查文件类型
      if (!file.type.startsWith('image/')) {
        this.$message.error('请选择图片文件');
        return;
      }
      
      // 检查文件大小（1MB）
      if (file.size > 1024 * 1024) {
        this.$message.error('图片大小不能超过1MB');
        return;
      }
      
      this.loading = true;
      try {
        const formData = new FormData();
        formData.append('avatar', file);
        
        // 实际项目中替换为真实API
        const response = await request.post('/user/upload-avatar', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        if (response.data.code === 200) {
          // 更新头像URL
          this.avatarUrl = getServerUrl() + '/media/userAvatar/' + response.data.avatar;
          
          // 更新用户信息
          this.currentUser.avatar = response.data.avatar;
          this.userForm.avatar = response.data.avatar;
          
          // 更新sessionStorage
          sessionStorage.setItem('currentUser', JSON.stringify(this.currentUser));
          
          this.$message.success('头像上传成功');
        } else {
          this.$message.error('头像上传失败');
        }
      } catch (error) {
        console.error('头像上传失败:', error);
        this.$message.error('头像上传失败，请重试');
      } finally {
        this.loading = false;
        // 清空文件输入，以便可以重新选择同一文件
        e.target.value = '';
      }
    },
    
    // 保存用户信息
    async handleSaveUserInfo() {
      // const form = ref({
      //   id:'-1',
      //   phonenumber:'',
      //   email:''
      // })
      // const userRef = ref([])
      // form.value = props.userForm
        

      // 表单验证
      this.$refs.userFormRef.validate(async (valid) => {
        if (valid) {
          this.loading = true;
          try {
            // 实际项目中替换为真实API
            const response = await request.post('/user/update', this.userForm);
            
            if (response.data.code === 200) {
              // 更新当前用户信息
              this.currentUser = { ...this.userForm };
              
              // 更新sessionStorage
              sessionStorage.setItem('currentUser', JSON.stringify(this.currentUser));
              
              ElMessage.success('保存成功');
            } else {
              ElMessage.error('保存失败: ' + response.data.info);
            }
          } catch (error) {
            console.error('保存用户信息失败:', error);
            ElMessage.error('保存失败，请重试');
          } finally {
            this.loading = false;
          }
        } else {
          console.log('表单验证失败');
        }
      });
    },
    
    // 修改密码
    async handleChangePassword() {
      // 表单验证
      this.$refs.pwdFormRef.validate(async (valid) => {
        if (valid) {
          this.loading = true;
          try {
            // 实际项目中替换为真实API
            const response = await request.post('/user/change-password', this.pwdForm);
            
            if (response.data.code === 200) {
              this.$message.success('密码修改成功');
              this.resetPwdForm();
            } else {
              this.$message.error('密码修改失败: ' + response.data.info);
            }
          } catch (error) {
            console.error('修改密码失败:', error);
            this.$message.error('修改密码失败，请重试');
          } finally {
            this.loading = false;
          }
        } else {
          console.log('表单验证失败');
        }
      });
    },
    
    // 重置密码表单
    resetPwdForm() {
      this.pwdForm = {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      };
      if (this.$refs.pwdFormRef) {
        this.$refs.pwdFormRef.resetFields();
      }
    }
  }
};
</script>

<style scoped lang="scss">
.app-container {
  padding: 20px;
  min-height: calc(100vh - 120px);
  background-color: #f5f7fa;
}

/* 卡片样式 */
.box-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

/* 个人信息卡片 */
.user-info-card {
  margin-bottom: 24px;
}

/* 头像区域 */
.avatar-section {
  padding: 20px 0;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 16px;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  border: 3px solid #e6f7ff;
  background-color: #1890ff;
  color: white;
}

.avatar-upload-btn {
  margin-top: 8px;
  font-size: 12px;
  padding: 4px 16px;
  cursor: pointer;
  
  &:hover {
    background-color: #409eff;
    border-color: #409eff;
  }
}

/* 信息列表 */
.info-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  
  &:last-child {
    border-bottom: none;
  }
}

.info-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
  width: 100px;
}

.info-icon {
  color: #1890ff;
  font-size: 16px;
}

.info-value {
  color: #333;
  font-size: 14px;
  flex: 1;
  margin-left: 16px;
}

/* 基本资料卡片 */
.profile-card {
  min-height: 400px;
}

/* 标签页样式 */
.profile-tabs {
  margin-top: 16px;
}

.tab-content {
  padding: 20px 0;
}

/* 表单样式 */
.user-form,
.pwd-form {
  max-width: 600px;
}

.form-btn {
  cursor: pointer;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .el-col {
    &:span {
      width: 100%;
    }
  }
  
  .app-container {
    padding: 10px;
  }
  
  .user-form,
  .pwd-form {
    max-width: 100%;
  }
}
</style>