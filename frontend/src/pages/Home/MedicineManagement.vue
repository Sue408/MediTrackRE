<template>
    <div class="medicine-management">
        <!-- 顶部操作栏 -->
        <div class="top-bar">
            <button class="back-btn" @click="backHome">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M15.41 7.41L14 6L8 12L14 18L15.41 16.59L10.83 12L15.41 7.41Z" fill="currentColor"/>
                </svg>
            </button>
            <h3>药品管理</h3>
            <button class="add-btn" @click="openAddModal">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
                </svg>
                添加药品
            </button>
        </div>

        <!-- 搜索筛选 -->
        <div class="search-bar">
            <div class="search-input">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M15.5 14H14.71L14.43 13.73C15.41 12.59 16 11.11 16 9.5C16 5.91 13.09 3 9.5 3C5.91 3 3 5.91 3 9.5C3 13.09 5.91 16 9.5 16C11.11 16 12.59 15.41 13.73 14.43L14 14.71V15.5L19 20.49L20.49 19L15.5 14ZM9.5 14C7.01 14 5 11.99 5 9.5C5 7.01 7.01 5 9.5 5C11.99 5 14 7.01 14 9.5C14 11.99 11.99 14 9.5 14Z" fill="currentColor"/>
                </svg>
                <input type="text" v-model="searchKeyword" placeholder="搜索药品名称..." @input="handleSearch">
            </div>
            <select v-model="filterUsageMethod" @change="handleSearch" class="filter-select">
                <option value="">全部用法</option>
                <option value="口服">口服</option>
                <option value="注射">注射</option>
                <option value="外用">外用</option>
                <option value="含服">含服</option>
                <option value="吸入">吸入</option>
                <option value="滴入">滴入</option>
                <option value="其他">其他</option>
            </select>
        </div>

        <!-- 药品列表 -->
        <div class="drug-list" v-if="drugList.length > 0">
            <div class="drug-card" v-for="drug in drugList" :key="drug.id">
                <div class="drug-image">
                    <img v-if="drug.image" :src="drug.image" :alt="drug.name">
                    <div v-else class="drug-image-placeholder">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M4.22 11.29L11.29 4.22C11.68 3.83 12.32 3.83 12.71 4.22L19.78 11.29C20.17 11.68 20.17 12.32 19.78 12.71L12.71 19.78C12.32 20.17 11.68 20.17 11.29 19.78L4.22 12.71C3.83 12.32 3.83 11.68 4.22 11.29Z" fill="#999"/>
                            <circle cx="12" cy="12" r="3" fill="#999"/>
                        </svg>
                    </div>
                </div>
                <div class="drug-info">
                    <h4>{{ drug.name }}</h4>
                    <div class="drug-detail">
                        <span class="tag usage-method">{{ drug.usage_method }}</span>
                        <span class="tag dosage">{{ drug.dosage }}</span>
                    </div>
                    <div class="drug-meta">
                        <span v-if="drug.remaining" class="remaining">余量: {{ drug.remaining }}</span>
                        <span class="source">{{ drug.source === '医疗数据库' ? '数据库' : '手动' }}</span>
                    </div>
                </div>
                <div class="drug-actions">
                    <button class="action-btn edit" @click="openEditModal(drug)">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/>
                        </svg>
                    </button>
                    <button class="action-btn delete" @click="confirmDelete(drug)">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM19 4H15.5L14.5 3H9.5L8.5 4H5V6H19V4Z" fill="currentColor"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- 空状态 -->
        <div class="empty-state" v-else>
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4.22 11.29L11.29 4.22C11.68 3.83 12.32 3.83 12.71 4.22L19.78 11.29C20.17 11.68 20.17 12.32 19.78 12.71L12.71 19.78C12.32 20.17 11.68 20.17 11.29 19.78L4.22 12.71C3.83 12.32 3.83 11.68 4.22 11.29Z" fill="#ccc"/>
                <circle cx="12" cy="12" r="3" fill="#ccc"/>
            </svg>
            <p>暂无药品</p>
            <button class="add-first-btn" @click="openAddModal">添加第一个药品</button>
        </div>

        <!-- 分页 -->
        <div class="pagination" v-if="total > pageSize">
            <button :disabled="page <= 1" @click="changePage(page - 1)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M15.41 7.41L14 6L8 12L14 18L15.41 16.59L10.83 12L15.41 7.41Z" fill="currentColor"/></svg>
            </button>
            <span>{{ page }} / {{ Math.ceil(total / pageSize) }}</span>
            <button :disabled="page >= Math.ceil(total / pageSize)" @click="changePage(page + 1)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M8.59 16.59L10 18L16 12L10 6L8.59 7.41L13.17 12L8.59 16.59Z" fill="currentColor"/></svg>
            </button>
        </div>

        <!-- 添加/编辑弹窗 -->
        <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>{{ editingDrug ? '编辑药品' : '添加药品' }}</h3>
                    <button class="close-btn" @click="closeModal">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/></svg>
                    </button>
                </div>
                <form @submit.prevent="submitForm" class="drug-form">
                    <div class="form-group">
                        <label>药品名称 *</label>
                        <input type="text" v-model="formData.name" required placeholder="请输入药品名称">
                    </div>
                    <div class="form-group">
                        <label>用法 *</label>
                        <select v-model="formData.usage_method" required>
                            <option value="口服">口服</option>
                            <option value="注射">注射</option>
                            <option value="外用">外用</option>
                            <option value="含服">含服</option>
                            <option value="吸入">吸入</option>
                            <option value="滴入">滴入</option>
                            <option value="其他">其他</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>用量 *</label>
                        <input type="text" v-model="formData.dosage" required placeholder="如: 2粒、1片">
                    </div>
                    <div class="form-group">
                        <label>余量</label>
                        <input type="text" v-model="formData.remaining" placeholder="如: 24粒">
                    </div>
                    <div class="form-group">
                        <label>来源</label>
                        <select v-model="formData.source">
                            <option value="手动输入">手动输入</option>
                            <option value="医疗数据库">医疗数据库</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>药品图片</label>
                        <div class="image-upload">
                            <div class="image-preview" v-if="formData.image">
                                <img :src="formData.image" alt="药品图片">
                                <button type="button" class="remove-image" @click="formData.image = ''">×</button>
                            </div>
                            <label v-else class="upload-placeholder">
                                <input type="file" accept="image/*" @change="handleImageUpload">
                                <svg width="30" height="30" viewBox="0 0 24 24" fill="none"><path d="M21 19V5C21 3.9 20.1 3 19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19ZM8.5 13.5L11 16.51L14.5 12L19 18H5L8.5 13.5Z" fill="#999"/></svg>
                                <span>点击上传图片</span>
                            </label>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn-cancel" @click="closeModal">取消</button>
                        <button type="submit" class="btn-submit" :disabled="submitting">
                            {{ submitting ? '保存中...' : '保存' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- 删除确认弹窗 -->
        <div class="modal-overlay" v-if="showDeleteConfirm" @click.self="showDeleteConfirm = false">
            <div class="modal-content small">
                <div class="modal-header">
                    <h3>确认删除</h3>
                </div>
                <p class="confirm-text">确定要删除药品「{{ deletingDrug?.name }}」吗？此操作不可恢复。</p>
                <div class="form-actions">
                    <button class="btn-cancel" @click="showDeleteConfirm = false">取消</button>
                    <button class="btn-delete" @click="handleDelete" :disabled="deleting">
                        {{ deleting ? '删除中...' : '确认删除' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { getDrugList, createDrug, updateDrug, deleteDrug } from '@/api/drug'
    import type { Drug, CreateDrugRequest, UpdateDrugRequest } from '@/types/drugTypes'

    const router = useRouter()

    // 列表数据
    const drugList = ref<Drug[]>([])
    const total = ref(0)
    const page = ref(1)
    const pageSize = 10

    // 筛选条件
    const searchKeyword = ref('')
    const filterUsageMethod = ref('')

    // 弹窗状态
    const showModal = ref(false)
    const showDeleteConfirm = ref(false)
    const editingDrug = ref<Drug | null>(null)
    const deletingDrug = ref<Drug | null>(null)
    const submitting = ref(false)
    const deleting = ref(false)

    // 表单数据
    const formData = reactive<CreateDrugRequest>({
        name: '',
        usage_method: '口服',
        dosage: '',
        remaining: '',
        source: '手动输入',
        image: ''
    })

    // 返回首页
    const backHome = () => {
        router.replace('/')
    }

    // 加载药品列表
    const loadDrugList = async () => {
        try {
            const res = await getDrugList({
                page: page.value,
                page_size: pageSize,
                keyword: searchKeyword.value || undefined,
                usage_method: filterUsageMethod.value as any || undefined
            })
            drugList.value = res.items
            total.value = res.total
        } catch (error) {
            console.error('加载药品列表失败:', error)
        }
    }

    // 搜索
    const handleSearch = () => {
        page.value = 1
        loadDrugList()
    }

    // 翻页
    const changePage = (newPage: number) => {
        page.value = newPage
        loadDrugList()
    }

    // 打开添加弹窗
    const openAddModal = () => {
        editingDrug.value = null
        Object.assign(formData, {
            name: '',
            usage_method: '口服',
            dosage: '',
            remaining: '',
            source: '手动输入',
            image: ''
        })
        showModal.value = true
    }

    // 打开编辑弹窗
    const openEditModal = (drug: Drug) => {
        editingDrug.value = drug
        Object.assign(formData, {
            name: drug.name,
            usage_method: drug.usage_method,
            dosage: drug.dosage,
            remaining: drug.remaining || '',
            source: drug.source,
            image: drug.image || ''
        })
        showModal.value = true
    }

    // 关闭弹窗
    const closeModal = () => {
        showModal.value = false
        editingDrug.value = null
    }

    // 处理图片上传
    const handleImageUpload = (event: Event) => {
        const input = event.target as HTMLInputElement
        const file = input.files?.[0]
        if (file) {
            const reader = new FileReader()
            reader.onload = (e) => {
                formData.image = e.target?.result as string
            }
            reader.readAsDataURL(file)
        }
    }

    // 提交表单
    const submitForm = async () => {
        if (submitting.value) return
        submitting.value = true

        try {
            if (editingDrug.value) {
                const data: UpdateDrugRequest = {
                    name: formData.name,
                    usage_method: formData.usage_method,
                    dosage: formData.dosage,
                    remaining: formData.remaining || undefined,
                    source: formData.source,
                    image: formData.image || undefined
                }
                await updateDrug(editingDrug.value.id, data)
            } else {
                await createDrug(formData)
            }
            closeModal()
            loadDrugList()
        } catch (error) {
            console.error('保存药品失败:', error)
        } finally {
            submitting.value = false
        }
    }

    // 确认删除
    const confirmDelete = (drug: Drug) => {
        deletingDrug.value = drug
        showDeleteConfirm.value = true
    }

    // 执行删除
    const handleDelete = async () => {
        if (!deletingDrug.value || deleting.value) return
        deleting.value = true

        try {
            await deleteDrug(deletingDrug.value.id)
            showDeleteConfirm.value = false
            deletingDrug.value = null
            loadDrugList()
        } catch (error) {
            console.error('删除药品失败:', error)
        } finally {
            deleting.value = false
        }
    }

    onMounted(() => {
        loadDrugList()
    })
</script>

<style scoped>
    .medicine-management {
        padding: 20px;
        height: 100%;
        overflow-y: auto;
    }

    .top-bar {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }

    .back-btn {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: none;
        background: #7494ec;
        color: #fff;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .back-btn:hover {
        background: #5a7de0;
        transform: scale(1.1);
    }

    .top-bar h3 {
        flex: 1;
        color: #333;
        margin: 0;
    }

    .add-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        border: none;
        border-radius: 20px;
        background: #7494ec;
        color: #fff;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .add-btn:hover {
        background: #5a7de0;
    }

    .search-bar {
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
    }

    .search-input {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 15px;
        background: #f5f5f5;
        border-radius: 25px;
    }

    .search-input input {
        flex: 1;
        border: none;
        background: transparent;
        outline: none;
        font-size: 14px;
    }

    .search-input svg {
        color: #999;
    }

    .filter-select {
        padding: 10px 15px;
        border: 1px solid #e0e0e0;
        border-radius: 25px;
        background: #fff;
        outline: none;
        cursor: pointer;
    }

    .drug-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 15px;
    }

    .drug-card {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px;
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .drug-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(116, 148, 236, 0.2);
    }

    .drug-image {
        width: 70px;
        height: 70px;
        border-radius: 15px;
        overflow: hidden;
        flex-shrink: 0;
    }

    .drug-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .drug-image-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f5f5f5;
    }

    .drug-info {
        flex: 1;
        min-width: 0;
    }

    .drug-info h4 {
        margin: 0 0 8px 0;
        color: #333;
        font-size: 16px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .drug-detail {
        display: flex;
        gap: 8px;
        margin-bottom: 8px;
    }

    .tag {
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
    }

    .tag.usage-method {
        background: #e3edff;
        color: #7494ec;
    }

    .tag.dosage {
        background: #f0f0f0;
        color: #666;
    }

    .drug-meta {
        display: flex;
        gap: 10px;
        font-size: 12px;
        color: #999;
    }

    .drug-actions {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .action-btn {
        width: 32px;
        height: 32px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .action-btn.edit {
        background: #e3edff;
        color: #7494ec;
    }

    .action-btn.edit:hover {
        background: #7494ec;
        color: #fff;
    }

    .action-btn.delete {
        background: #ffeaea;
        color: #ff6b6b;
    }

    .action-btn.delete:hover {
        background: #ff6b6b;
        color: #fff;
    }

    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
        color: #999;
    }

    .empty-state p {
        margin: 20px 0;
        font-size: 16px;
    }

    .add-first-btn {
        padding: 12px 30px;
        border: none;
        border-radius: 25px;
        background: #7494ec;
        color: #fff;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .add-first-btn:hover {
        background: #5a7de0;
    }

    .pagination {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-top: 30px;
    }

    .pagination button {
        width: 36px;
        height: 36px;
        border: 1px solid #e0e0e0;
        border-radius: 50%;
        background: #fff;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .pagination button:hover:not(:disabled) {
        background: #7494ec;
        color: #fff;
        border-color: #7494ec;
    }

    .pagination button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .pagination span {
        color: #666;
        font-size: 14px;
    }

    /* 弹窗样式 */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 100;
    }

    .modal-content {
        width: 90%;
        max-width: 450px;
        max-height: 90vh;
        overflow-y: auto;
        background: #fff;
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }

    .modal-content.small {
        max-width: 380px;
        padding: 25px;
    }

    .modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 25px;
        border-bottom: 1px solid #f0f0f0;
    }

    .modal-header h3 {
        margin: 0;
        color: #333;
    }

    .close-btn {
        width: 32px;
        height: 32px;
        border: none;
        background: #f5f5f5;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .close-btn:hover {
        background: #e0e0e0;
    }

    .drug-form {
        padding: 25px;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-group label {
        display: block;
        margin-bottom: 8px;
        color: #666;
        font-size: 14px;
    }

    .form-group input,
    .form-group select {
        width: 100%;
        padding: 12px 15px;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        font-size: 14px;
        outline: none;
        transition: border-color 0.3s ease;
    }

    .form-group input:focus,
    .form-group select:focus {
        border-color: #7494ec;
    }

    .image-upload {
        width: 100px;
        height: 100px;
    }

    .image-preview {
        position: relative;
        width: 100%;
        height: 100%;
        border-radius: 12px;
        overflow: hidden;
    }

    .image-preview img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .remove-image {
        position: absolute;
        top: 5px;
        right: 5px;
        width: 24px;
        height: 24px;
        border: none;
        border-radius: 50%;
        background: rgba(0, 0, 0, 0.6);
        color: #fff;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .upload-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 2px dashed #e0e0e0;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .upload-placeholder:hover {
        border-color: #7494ec;
    }

    .upload-placeholder input {
        display: none;
    }

    .upload-placeholder span {
        font-size: 12px;
        color: #999;
        margin-top: 5px;
    }

    .form-actions {
        display: flex;
        gap: 15px;
        justify-content: flex-end;
        margin-top: 25px;
    }

    .btn-cancel,
    .btn-submit,
    .btn-delete {
        padding: 12px 25px;
        border: none;
        border-radius: 20px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .btn-cancel {
        background: #f5f5f5;
        color: #666;
    }

    .btn-cancel:hover {
        background: #e0e0e0;
    }

    .btn-submit {
        background: #7494ec;
        color: #fff;
    }

    .btn-submit:hover:not(:disabled) {
        background: #5a7de0;
    }

    .btn-submit:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .btn-delete {
        background: #ff6b6b;
        color: #fff;
    }

    .btn-delete:hover:not(:disabled) {
        background: #e05555;
    }

    .confirm-text {
        padding: 20px 25px;
        color: #666;
        line-height: 1.6;
    }
</style>
