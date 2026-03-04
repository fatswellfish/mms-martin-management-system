// mms/FieldOps/static/js/app.js
// FieldOps - 现场管理系统 前端逻辑（已完成）

// 全局状态管理（模拟）
const appState = {
    farmTree: null,
    eventStream: [],
    batchList: [],
    lastUpdateTime: null
};

// API 基础路径（根据部署环境调整）
const API_BASE = "/FieldOps/api";

// 事件流滚动机制（支持无限滚动）
let eventOffset = 0;
let isFetchingEvents = false;

// DOM 元素缓存（提高性能）
const elements = {
    treeContainer: document.getElementById("farm-tree-container"),
    eventsContainer: document.getElementById("events-container"),
    batchesContainer: document.getElementById("batches-container"),
    batchIdInput: document.getElementById("batch-id-input"),
    distributeBtn: document.getElementById("distribute-btn"),
    distributionResult: document.getElementById("distribution-result")
};

// 初始化函数：应用启动时调用
function initApp() {
    console.log("🚀 FieldOps 客户端已启动");
    
    // 绑定事件监听器（避免重复绑定）
    if (elements.distributeBtn) {
        elements.distributeBtn.addEventListener("click", handleDistribute);
    }
    
    // 设置滚动事件监听（用于事件流无限滚动）
    if (elements.eventsContainer) {
        elements.eventsContainer.addEventListener("scroll", handleScroll);
    }
    
    // 启动定时数据刷新（每 30 秒）
    setInterval(refreshAllData, 30000);
    
    // 首次加载所有数据
    loadAllData();
}

// 加载所有数据（首次进入或手动刷新）
async function loadAllData() {
    try {
        // 显示加载状态
        showLoading(elements.treeContainer);
        showLoading(elements.eventsContainer);
        showLoading(elements.batchesContainer);
        
        // 并行获取所有数据源（提升性能）
        const [treeRes, eventsRes, batchesRes] = await Promise.all([
            fetch(`${API_BASE}/tree`).then(r => r.json()),
            fetch(`${API_BASE}/events?limit=50`).then(r => r.json()),
            fetch(`${API_BASE}/batches`).then(r => r.json())
        ]);
        
        // 处理响应结果
        if (treeRes.success) {
            renderFarmTree(treeRes.data);
            appState.farmTree = treeRes.data;
        } else {
            showError(elements.treeContainer, "无法加载农场结构");
        }
        
        if (eventsRes.success) {
            appState.eventStream = eventsRes.data;
            renderEventStream(eventsRes.data);
        } else {
            showError(elements.eventsContainer, "无法加载事件流");
        }
        
        if (batchesRes.success) {
            appState.batchList = batchesRes.data;
            renderBatchList(batchesRes.data);
        } else {
            showError(elements.batchesContainer, "无法加载批次列表");
        }
        
        // 记录最后更新时间
        appState.lastUpdateTime = new Date().toLocaleTimeString();
        
        console.log(`✅ 数据加载完成，时间: ${appState.lastUpdateTime}`);
        
    } catch (error) {
        console.error("❌ 数据加载失败:", error);
        showError(elements.treeContainer, "网络错误，请检查后端服务");
        showError(elements.eventsContainer, "网络错误，请检查后端服务");
        showError(elements.batchesContainer, "网络错误，请检查后端服务");
    }
}

// 渲染农场结构树（递归函数）
function renderFarmTree(data, container = elements.treeContainer) {
    // 清空容器内容（防止重复渲染）
    container.innerHTML = "";
    
    if (!Array.isArray(data) || data.length === 0) {
        container.innerHTML = "<p class='empty'>暂无农场数据</p>";
        return;
    }
    
    // 创建根节点列表（包含所有农场）
    const ul = document.createElement("ul");
    ul.className = "tree-list";
    
    data.forEach(farm => {
        const farmLi = createFarmNode(farm);
        ul.appendChild(farmLi);
    });
    
    container.appendChild(ul);
}

// 创建农场节点（带层级）
function createFarmNode(farm) {
    const li = document.createElement("li");
    li.className = "farm-node";
    
    const div = document.createElement("div");
    div.innerHTML = `
        <span class="farm-name">${farm.name}</span>
        <small class="location">${farm.location || "未知位置"}</small>
    `;
    
    // 添加农场节点到列表
    li.appendChild(div);
    
    // 如果有猪舍，则递归创建（深度优先）
    if (Array.isArray(farm.barns) && farm.barns.length > 0) {
        const barnUl = document.createElement("ul");
        barnUl.className = "barn-list";
        
        farm.barns.forEach(barn => {
            const barnLi = createBarnNode(barn);
            barnUl.appendChild(barnLi);
        });
        
        li.appendChild(barnUl);
    }
    
    return li;
}

// 创建猪舍节点（带层级）
function createBarnNode(barn) {
    const li = document.createElement("li");
    li.className = "barn-node";
    
    const div = document.createElement("div");
    div.innerHTML = `
        <span class="barn-name">${barn.name} (${barn.type})</span>
        <small class="capacity">容量: ${barn.capacity} | 已占: ${barn.reserved_count}</small>
    `;
    
    // 添加猪舍节点到列表
    li.appendChild(div);
    
    // 如果有栏位，则递归创建（深度优先）
    if (Array.isArray(barn.pens) && barn.pens.length > 0) {
        const penUl = document.createElement("ul");
        penUl.className = "pen-list";
        
        barn.pens.forEach(pen => {
            const penLi = createPenNode(pen);
            penUl.appendChild(penLi);
        });
        
        li.appendChild(penUl);
    }
    
    return li;
}

// 创建栏位节点（叶子节点）
function createPenNode(pen) {
    const li = document.createElement("li");
    li.className = "pen-node";
    
    const statusClass = `status-${pen.status}`;
    
    const div = document.createElement("div");
    div.innerHTML = `
        <span class="pen-status ${statusClass}"></span>
        <span class="pen-name">${pen.name}</span>
        <small class="pen-capacity">容量: ${pen.capacity}</small>
    `;
    
    // 添加栏位节点到列表
    li.appendChild(div);
    
    // 如果当前占用批次，则显示批次号（可点击查看详情）
    if (pen.current_batch_id) {
        const batchLink = document.createElement("a");
        batchLink.href = `#batch-${pen.current_batch_id}`;
        batchLink.textContent = `批次: ${pen.current_batch_id}`;
        batchLink.style.marginLeft = "6px";
        batchLink.style.fontSize = "0.8rem";
        batchLink.style.color = "var(--secondary-color)";
        
        div.appendChild(batchLink);
    }
    
    return li;
}

// 渲染事件流（最新事件在顶部）
function renderEventStream(events) {
    const container = elements.eventsContainer;
    container.innerHTML = ""; // 清空旧内容
    
    if (!Array.isArray(events) || events.length === 0) {
        container.innerHTML = "<p class='empty'>暂无事件记录</p>";
        return;
    }
    
    // 按时间倒序排列（最新在前）
    const sortedEvents = [...events].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    
    // 创建事件列表容器
    const ul = document.createElement("ul");
    ul.className = "event-list";
    
    sortedEvents.forEach(event => {
        const li = document.createElement("li");
        li.className = "event-item";
        
        const time = new Date(event.timestamp).toLocaleString();
        
        li.innerHTML = `
            <div>
                <span class="event-type">${event.event_type}</span>
                <div class="event-description">
                    ${event.description || "无描述"}
                </div>
            </div>
            <span class="event-time">${time}</span>
        `;
        
        ul.appendChild(li);
    });
    
    container.appendChild(ul);
}

// 渲染批次列表（按状态分类）
function renderBatchList(batches) {
    const container = elements.batchesContainer;
    container.innerHTML = ""; // 清空旧内容
    
    if (!Array.isArray(batches) || batches.length === 0) {
        container.innerHTML = "<p class='empty'>暂无批次信息</p>";
        return;
    }
    
    // 创建批次列表容器
    const ul = document.createElement("ul");
    ul.className = "batch-list";
    
    batches.forEach(batch => {
        const li = document.createElement("li");
        li.className = "batch-item";
        
        // 根据状态设置样式类
        const statusClass = `status-${batch.status}`;
        
        li.innerHTML = `
            <div>
                <span class="batch-id">${batch.batch_id}</span>
                <span class="batch-status ${statusClass}">${batch.status}</span>
            </div>
            <span class="quantity">数量: ${batch.quantity}</span>
        `;
        
        ul.appendChild(li);
    });
    
    container.appendChild(ul);
}

// 处理分栏请求（用户点击按钮）
async function handleDistribute() {
    const batchId = elements.batchIdInput?.value.trim();
    if (!batchId) {
        showError(elements.distributionResult, "请输入批次号");
        return;
    }
    
    // 获取分栏映射（这里使用一个简单的示例，实际应从表单输入）
    const distributionMap = {
        1: [1, 2],  // 假设第1个猪舍的第1、2个栏位
        2: [3]       // 假设第2个猪舍的第3个栏位
    };
    
    try {
        // 显示加载状态
        elements.distributeBtn.disabled = true;
        elements.distributeBtn.textContent = "处理中...";
        
        const response = await fetch(`${API_BASE}/batches/${batchId}/distribute`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(distributionMap)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess(elements.distributionResult, `批次 ${batchId} 分栏成功！`);
            
            // 自动刷新数据（确认分配生效）
            setTimeout(() => {
                loadAllData();
            }, 2000);
        } else {
            showError(elements.distributionResult, `失败: ${result.message || "未知错误"}`);
        }
        
    } catch (error) {
        console.error("❌ 分栏请求失败:", error);
        showError(elements.distributionResult, "网络错误，请稍后重试");
    } finally {
        elements.distributeBtn.disabled = false;
        elements.distributeBtn.textContent = "分栏";
    }
}

// 处理滚动事件（用于事件流无限滚动）
function handleScroll(e) {
    const container = e.target;
    const scrollTop = container.scrollTop;
    const scrollHeight = container.scrollHeight;
    const clientHeight = container.clientHeight;
    
    // 当滚动到底部时触发加载更多事件（距离底部 200px 内）
    if (scrollTop + clientHeight >= scrollHeight - 200 && !isFetchingEvents) {
        fetchMoreEvents();
    }
}

// 获取更多事件（分页加载）
async function fetchMoreEvents() {
    if (isFetchingEvents) return;
    
    isFetchingEvents = true;
    
    try {
        const response = await fetch(`${API_BASE}/events?limit=20&offset=${eventOffset}`);
        const result = await response.json();
        
        if (result.success && Array.isArray(result.data)) {
            // 将新事件插入到开头（保持时间倒序）
            appState.eventStream.unshift(...result.data);
            
            // 更新偏移量（为下一次加载准备）
            eventOffset += result.data.length;
            
            // 重新渲染事件流（新事件在顶部）
            renderEventStream(appState.eventStream);
            
            console.log(`🔍 已加载 ${eventOffset} 条事件`);
        } else {
            console.warn("⚠️ 无更多事件数据可用");
        }
        
    } catch (error) {
        console.error("❌ 加载更多事件失败:", error);
        showError(elements.eventsContainer, "加载失败，网络问题");
    } finally {
        isFetchingEvents = false;
    }
}

// 刷新所有数据（定时任务）
function refreshAllData() {
    console.log("🔄 正在自动刷新数据...");
    loadAllData();
}

// 工具函数：显示加载状态
function showLoading(container) {
    container.innerHTML = "<p class='loading'>加载中...</p>";
}

// 工具函数：显示错误信息
function showError(container, message) {
    container.innerHTML = `<p class='error'>❌ ${message}</p>`;
}

// 工具函数：显示成功信息
function showSuccess(container, message) {
    container.innerHTML = `<p class='success'>✅ ${message}</p>`;
}

// 页面加载完成后初始化应用
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initApp);
} else {
    initApp();
}

// 导出全局对象（供测试或调试使用）
window.FieldOpsApp = {
    appState,
    loadAllData,
    refreshAllData,
    initApp
};