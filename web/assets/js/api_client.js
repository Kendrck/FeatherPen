/**
 * @file api_client.js
 * @brief FeatherPen Web API 客户端模块
 * @details 封装所有与后端RESTful API的交互逻辑。
 *          严格遵循 ACCOUNT_SPEC.md 常量对齐规则。
 *          默认端口6554，冲突时自动重新分配。
 * @version 1.0.0
 * @date 2026-07-26
 * @copyright GB/T 8567-2006 Compliant
 */

// ==========================================
// 第一部分：离线账号全局常量 (强制与后端 local_login.py 对齐)
// 来源：ACCOUNT_SPEC.md 第五章
// ==========================================
const OFFLINE_GUEST_UID = "127001";
const PRIVILEGE_UID_LIST = [
    "000000", "111111", "222222", "333333", "444444",
    "555555", "666666", "777777", "888888", "999999"
];

// ==========================================
// 第二部分：动态配置与基础请求
// ==========================================
let API_BASE_URL = 'http://127.0.0.1:6554/api/v1'; // 默认端口6554

/**
 * @brief 初始化API客户端（获取动态端口）
 * @returns {Promise<void>}
 */
async function initClient() {
    try {
        // 尝试连接默认或已知的地址
        const response = await fetch('/api/v1/status');
        if (!response.ok) throw new Error('Status check failed');
        const data = await response.json();
        if (data.code === 200) {
            // 如果后端返回了不同的端口，则更新
            if (data.data.web_port != 6554) {
                API_BASE_URL = `http://127.0.0.1:${data.data.web_port}/api/v1`;
                console.log(`[API Client] 端口冲突，已自动分配新端口: ${data.data.web_port}`);
            }
        } else {
            throw new Error('Service init error');
        }
    } catch (error) {
        console.error('[API Client] 初始化失败，将使用默认端口 6554', error);
        // 兜底策略，保持 API_BASE_URL 为默认的 6554
    }
}
// 页面加载时立即执行初始化
initClient();

/**
 * @brief 执行标准化的API请求
 * @param {string} endpoint - API端点路径
 * @param {string} method - HTTP方法
 * @param {Object|null} data - 请求体
 * @param {string|null} token - 认证Token
 * @returns {Promise<Object>}
 */
async function request(endpoint, method = 'GET', data = null, token = null) {
    // 确保基础URL已初始化
    if (!API_BASE_URL) await initClient();

    const url = `${API_BASE_URL}${endpoint}`;
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const config = { method, headers };
    if (data) config.body = JSON.stringify(data);

    try {
        const response = await fetch(url, config);
        const result = await response.json();
        
        // 统一业务错误处理 (参考 API.md 全局标准返回结构)
        if (result.code !== 200) {
            throw new Error(result.detail || 'API Error');
        }
        return result;
    } catch (error) {
        console.error(`[API Client] Request failed: ${endpoint}`, error);
        throw error;
    }
}

// ==========================================
// 第三部分：模块化API接口实现
// ==========================================

/** @namespace AccountAPI 账户用户模块 (参考 API.md 第二部分) */
const AccountAPI = {
    login: (account, password) => request('/account/login', 'POST', { account, password }),
    register: (account, password) => request('/account/register', 'POST', { account, password }),
    getInfo: (token) => request('/account/me', 'GET', null, token),
};

/** @namespace BookAPI 书籍工程模块 (参考 API.md 第三部分) */
const BookAPI = {
    create: (data, token) => request('/book/create', 'POST', data, token),
    getList: (token) => request('/book/list', 'GET', null, token),
};

/** @namespace SignAPI 签到积分模块 (参考 API.md 第四部分) */
const SignAPI = {
    checkIn: (token) => request('/sign/checkin', 'POST', null, token),
};

// 暴露全局对象
window.FeatherPenAPI = {
    Account: AccountAPI,
    Book: BookAPI,
    Sign: SignAPI,
    // 导出常量供其他模块校验使用
    Constants: { OFFLINE_GUEST_UID, PRIVILEGE_UID_LIST }
};