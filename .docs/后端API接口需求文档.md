# 后端API接口需求文档

本文档定义了药品管理和计划管理模块所需的后端API接口。

---

## 1. 药品管理模块 (Drugs)

### 1.1 获取药品列表

- **接口路径**: `GET /api/drugs`
- **功能描述**: 获取当前用户的药品列表，支持分页和筛选
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 页码，默认1 |
| page_size | integer | 否 | 每页数量，默认10 |
| keyword | string | 否 | 搜索关键词（药品名称） |
| usage_method | string | 否 | 用法筛选（口服/注射/外用/含服/吸入/滴入/其他） |
| source | string | 否 | 来源筛选（医疗数据库/手动输入） |

- **响应示例**:
```json
{
    "items": [
        {
            "id": 1,
            "user_id": 1,
            "name": "阿莫西林",
            "image": "base64...",
            "usage_method": "口服",
            "dosage": "2粒",
            "remaining": "24粒",
            "source": "手动输入",
            "external_id": null,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ],
    "total": 100,
    "page": 1,
    "page_size": 10
}
```

### 1.2 获取药品详情

- **接口路径**: `GET /api/drugs/{id}`
- **功能描述**: 获取指定药品的详细信息
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 药品ID |

- **响应示例**: 同1.1中的items中的单个对象

### 1.3 创建药品

- **接口路径**: `POST /api/drugs`
- **功能描述**: 添加新药品到用户药品库
- **请求体**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 药品名称 |
| image | string | 否 | 药品图片（Base64） |
| usage_method | string | 是 | 用法 |
| dosage | string | 是 | 用量 |
| remaining | string | 否 | 余量 |
| source | string | 是 | 来源（医疗数据库/手动输入） |
| external_id | integer | 否 | 外部数据库ID |

- **请求体示例**:
```json
{
    "name": "阿莫西林",
    "usage_method": "口服",
    "dosage": "2粒",
    "remaining": "24粒",
    "source": "手动输入"
}
```

- **响应**: 返回创建的药品对象

### 1.4 更新药品

- **接口路径**: `PUT /api/drugs/{id}`
- **功能描述**: 更新指定药品的信息
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 药品ID |

- **请求体**: 同1.3，所有字段均为可选
- **响应**: 返回更新后的药品对象

### 1.5 删除药品

- **接口路径**: `DELETE /api/drugs/{id}`
- **功能描述**: 删除指定药品
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 药品ID |

- **响应**: `204 No Content`

### 1.6 搜索外部药品

- **接口路径**: `GET /api/drugs/search`
- **功能描述**: 从外部医疗数据库搜索药品
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 是 | 搜索关键词 |

- **响应示例**:
```json
[
    {
        "id": 1001,
        "name": "阿莫西林胶囊",
        "image": "base64...",
        "usage_method": "口服",
        "dosage": "1粒"
    }
]
```

---

## 2. 计划管理模块 (Plans)

### 2.1 获取计划列表

- **接口路径**: `GET /api/plans`
- **功能描述**: 获取当前用户的用药计划列表，支持分页和状态筛选
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 页码，默认1 |
| page_size | integer | 否 | 每页数量，默认10 |
| status | string | 否 | 状态筛选（active/paused/completed） |
| plan_type | string | 否 | 类型筛选（长期/周期） |
| keyword | string | 否 | 搜索关键词（计划名称） |

- **响应示例**:
```json
{
    "items": [
        {
            "id": 1,
            "user_id": 1,
            "name": "每日降压药",
            "plan_type": "长期",
            "start_date": "2024-01-01T00:00:00Z",
            "end_date": null,
            "frequency_type": "daily",
            "frequency_detail": null,
            "time_points": ["08:00", "20:00"],
            "sms_enabled": true,
            "status": "active",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "drugs": [
                {
                    "id": 1,
                    "plan_id": 1,
                    "drug_id": 1,
                    "dosage": "1粒",
                    "drug": {
                        "id": 1,
                        "name": "降压药",
                        "usage_method": "口服",
                        "image": null
                    }
                }
            ]
        }
    ],
    "total": 50,
    "page": 1,
    "page_size": 10
}
```

### 2.2 获取计划详情

- **接口路径**: `GET /api/plans/{id}`
- **功能描述**: 获取指定计划的详细信息，包含关联的药品
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 计划ID |

- **响应**: 同2.1中的items中的单个对象

### 2.3 创建计划

- **接口路径**: `POST /api/plans`
- **功能描述**: 创建新的用药计划
- **请求体**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 计划名称 |
| plan_type | string | 是 | 计划类型（长期/周期） |
| start_date | string | 是 | 开始日期（ISO格式） |
| end_date | string | 否 | 结束日期（周期计划必填） |
| frequency_type | string | 是 | 频率类型（daily/alternate/weekly/monthly） |
| frequency_detail | object | 否 | 频率详情 |
| time_points | array | 是 | 每日用药时间点数组 |
| sms_enabled | boolean | 否 | 是否启用短信提醒 |
| drug_ids | array | 是 | 关联药品列表 |

- **frequency_detail 结构**:

| 字段 | 适用类型 | 说明 |
|------|----------|------|
| interval_days | alternate | 间隔天数 |
| weekdays | weekly | 星期几（1-7数组） |
| days_of_month | monthly | 每月几号（1-31数组） |

- **drug_ids 结构**:
```json
[
    {"drug_id": 1, "dosage": "2粒"},
    {"drug_id": 2, "dosage": "1片"}
]
```

- **请求体示例**:
```json
{
    "name": "每日降压药",
    "plan_type": "长期",
    "start_date": "2024-01-01",
    "frequency_type": "daily",
    "time_points": ["08:00", "20:00"],
    "sms_enabled": true,
    "drug_ids": [
        {"drug_id": 1, "dosage": "1粒"}
    ]
}
```

- **响应**: 返回创建的计划对象

### 2.4 更新计划

- **接口路径**: `PUT /api/plans/{id}`
- **功能描述**: 更新指定计划的信息
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 计划ID |

- **请求体**: 同2.3，所有字段均为可选
- **响应**: 返回更新后的计划对象

### 2.5 删除计划

- **接口路径**: `DELETE /api/plans/{id}`
- **功能描述**: 删除指定计划
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 计划ID |

- **响应**: `204 No Content`

### 2.6 暂停计划

- **接口路径**: `POST /api/plans/{id}/pause`
- **功能描述**: 暂停指定计划
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 计划ID |

- **响应**: 返回更新后的计划对象（状态为paused）

### 2.7 恢复计划

- **接口路径**: `POST /api/plans/{id}/resume`
- **功能描述**: 恢复已暂停的计划
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 计划ID |

- **响应**: 返回更新后的计划对象（状态为active）

### 2.8 完成计划

- **接口路径**: `POST /api/plans/{id}/complete`
- **功能描述**: 标记计划为已完成
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 计划ID |

- **响应**: 返回更新后的计划对象（状态为completed）

### 2.9 获取今日计划

- **接口路径**: `GET /api/plans/today`
- **功能描述**: 获取今日需要执行的用药计划
- **响应示例**:
```json
{
    "date": "2024-01-15",
    "plans": [
        {
            "plan": {
                "id": 1,
                "name": "每日降压药",
                "time_points": ["08:00", "20:00"]
            },
            "time_point": "08:00",
            "drugs": [
                {
                    "id": 1,
                    "dosage": "1粒",
                    "drug": {
                        "id": 1,
                        "name": "降压药",
                        "usage_method": "口服"
                    }
                }
            ],
            "taken": false
        }
    ]
}
```

### 2.10 记录用药

- **接口路径**: `POST /api/plans/{id}/track`
- **功能描述**: 记录用户已服用药物
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 计划ID |

- **请求体**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| time_point | string | 是 | 用药时间点（如"08:00"） |

- **响应**:
```json
{
    "track_id": 1,
    "created_at": "2024-01-15T08:05:00Z"
}
```

### 2.11 取消用药记录

- **接口路径**: `DELETE /api/plans/{id}/track/{track_id}`
- **功能描述**: 取消已记录的用药
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 计划ID |
| track_id | integer | 是 | 记录ID |

- **响应**: `204 No Content`

---

## 3. 用户与健康档案模块

### 3.1 获取当前用户信息

- **接口路径**: `GET /api/user/info`
- **功能描述**: 获取当前登录用户的详细信息
- **响应示例**:
```json
{
    "nickname": "用户昵称",
    "email": "user@example.com",
    "avatar": "base64...",
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 3.2 更新用户信息

- **接口路径**: `PUT /api/user/info`
- **功能描述**: 更新当前用户的昵称或头像
- **请求体**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| nickname | string | 否 | 用户昵称 |
| avatar | string | 否 | 头像（Base64编码） |

- **请求体示例**:
```json
{
    "nickname": "新昵称",
    "avatar": "base64..."
}
```

- **响应**: 返回更新后的用户信息

### 3.3 获取健康档案

- **接口路径**: `GET /api/user/profile`
- **功能描述**: 获取当前用户的健康档案信息
- **响应示例**:
```json
{
    "id": 1,
    "user_id": 1,
    "gender": "unknown",
    "height": 170,
    "weight": 65,
    "blood_type": "A",
    "allergies": [
        {"name": "青霉素", "reaction": "皮疹"}
    ],
    "diseases": [
        {"name": "高血压", "diagnosed_at": "2020-01-01", "status": "治疗中"}
    ],
    "special_status": null,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### 3.4 更新健康档案

- **接口路径**: `PUT /api/user/profile`
- **功能描述**: 更新用户的健康档案信息
- **请求体**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| gender | string | 否 | 性别（男/女/unknown） |
| height | number | 否 | 身高（cm） |
| weight | number | 否 | 体重（kg） |
| blood_type | string | 否 | 血型（A/B/AB/O/unknown） |
| allergies | array | 否 | 过敏史数组 |
| diseases | array | 否 | 疾病史数组 |
| special_status | string | 否 | 女性特殊状态（备孕/怀孕/哺乳/null） |

- **allergies 结构**:
```json
[{"name": "青霉素", "reaction": "皮疹"}]
```

- **diseases 结构**:
```json
[{"name": "高血压", "diagnosed_at": "2020-01-01", "status": "治疗中"}]
```

- **响应**: 返回更新后的健康档案

### 3.5 修改密码

- **接口路径**: `POST /api/user/change-password`
- **功能描述**: 修改当前用户的登录密码
- **请求体**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| old_password | string | 是 | 当前密码 |
| new_password | string | 是 | 新密码（至少6位） |
| confirm_password | string | 是 | 确认新密码 |

- **请求体示例**:
```json
{
    "old_password": "123456",
    "new_password": "abcdef",
    "confirm_password": "abcdef"
}
```

- **响应**: `200 OK` 或错误信息

### 3.6 错误响应格式（健康档案相关）
```json
{
    "detail": "错误信息描述"
}
```

---

## 4. 通用说明

### 4.1 认证
- 所有接口需要用户登录认证
- 使用Bearer Token进行身份验证
- Token过期时返回401，前端需刷新Token后重试

### 4.2 错误响应格式
```json
{
    "detail": "错误信息描述"
}
```

### 4.3 分页
- 默认每页10条记录
- 最大支持100条记录

### 4.4 日期时间格式
- 请求: ISO 8601格式（YYYY-MM-DD或YYYY-MM-DDTHH:MM:SSZ）
- 返回: ISO 8601格式（UTC时区）
