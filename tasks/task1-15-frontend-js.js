// mms/FieldOps/static/js/app.js

class FieldOpsApp {
    constructor() {
        this.baseUrl = '/api';
        this.init();
    }

    init() {
        // 1. 加载农场结构数据（用于卡片渲染）
        this.loadFarmTree().then(() => {
            console.log('✅ 农场结构加载完成');
        }).catch(err => {
            console.error('❌ 农场结构加载失败:', err);
        });

        // 2. 加载批次数据（用于卡片展示）
        this.loadBatches().then(() => {
            console.log('✅ 批次数据加载完成');
        }).catch(err => {
            console.error('❌ 批次数据加载失败:', err);
        });

        // 3. 加载事件流（用于滚动条）
        this.loadEvents().then(() => {
            console.log('✅ 事件流加载完成');
        }).catch(err => {
            console.error('❌ 事件流加载失败:', err);
        });

        // 4. 绑定事件监听器（用于用户操作）
        this.bindEventListeners();
    }

    // 1. 从后端获取农场结构树并渲染到页面
    async loadFarmTree() {
        try {
            const response = await fetch(`${this.baseUrl}/tree`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            const container = document.getElementById('farm-container');
            
            // 清空容器（避免重复添加）
            container.innerHTML = '';
            
            // 遍历每个农场并生成卡片
            data.forEach(farm => {
                const farmCard = this.createFarmCard(farm);
                container.appendChild(farmCard);
            });
            
            // 添加淡入动画效果（可选）
            this.fadeInElements(container.querySelectorAll('.card'));
            
        } catch (error) {
            console.error('加载农场结构失败:', error);
            document.getElementById('farm-container').innerHTML = `
                <div class="card bg-red-900 text-red-200 p-6">
                    <p>⚠️ 无法加载农场结构，请检查后端服务是否正常运行。</p>
                </div>
            `;
        }
    }

    // 2. 从后端获取批次列表并渲染到页面
    async loadBatches() {
        try {
            const response = await fetch(`${this.baseUrl}/batches`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            const container = document.getElementById('batches-container');
            
            // 清空容器
            container.innerHTML = '';
            
            // 遍历每个批次并生成卡片（这里假设返回的是批次列表，实际需根据接口调整）
            data.forEach(batch => {
                const batchCard = this.createBatchCard(batch);
                container.appendChild(batchCard);
            });
            
            // 添加淡入动画效果（可选）
            this.fadeInElements(container.querySelectorAll('.card'));
            
        } catch (error) {
            console.error('加载批次数据失败:', error);
            document.getElementById('batches-container').innerHTML = `
                <div class="card bg-red-900 text-red-200 p-6">
                    <p>⚠️ 无法加载批次数据，请检查后端服务是否正常运行。</p>
                </div>
            `;
        }
    }

    // 3. 从后端获取事件流并实时更新滚动条
    async loadEvents() {
        try {
            const response = await fetch(`${this.baseUrl}/events`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            const container = document.getElementById('events-scroll');
            
            // 清空容器
            container.innerHTML = '';
            
            // 遍历每个事件并生成记录（按时间倒序）
            data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            
            data.forEach(event => {
                const eventItem = this.createEventItem(event);
                container.appendChild(eventItem);
            });
            
            // 添加淡入动画效果（可选）
            this.fadeInElements(container.querySelectorAll('.event-item'));
            
        } catch (error) {
            console.error('加载事件流失败:', error);
            document.getElementById('events-scroll').innerHTML = `
                <div class="event-item text-red-300">
                    ⚠️ 无法加载事件流，请检查后端服务是否正常运行。
                </div>
            `;
        }
    }

    // 4. 创建农场卡片（包含猪舍与栏位信息）
    createFarmCard(farm) {
        const card = document.createElement('div');
        card.className = 'card farm-card fade-in';
        
        const title = document.createElement('h3');
        title.textContent = farm.name;
        title.className = 'text-lg font-semibold mb-3 text-green-400';
        
        const content = document.createElement('div');
        content.className = 'space-y-3';
        
        // 按猪舍类型分组显示（产房、保育、育肥等）
        Object.keys(farm.barns_by_type).forEach(type => {
            const typeGroup = document.createElement('div');
            typeGroup.className = 'bg-gray-800 p-3 rounded border border-gray-600';
            
            const typeTitle = document.createElement('h4');
            typeTitle.textContent = `${type} (${farm.barns_by_type[type].length} 舍)`;
            typeTitle.className = 'font-medium text-blue-400 mb-2';
            
            const barnList = document.createElement('div');
            barnList.className = 'grid grid-cols-1 gap-2';
            
            farm.barns_by_type[type].forEach(barn => {
                const barnCard = this.createBarnCard(barn);
                barnList.appendChild(barnCard);
            });
            
            typeGroup.appendChild(typeTitle);
            typeGroup.appendChild(barnList);
            content.appendChild(typeGroup);
        });
        
        card.appendChild(title);
        card.appendChild(content);
        
        return card;
    }

    // 5. 创建猪舍卡片（包含栏位信息）
    createBarnCard(barn) {
        const card = document.createElement('div');
        card.className = 'card barn-card fade-in';
        
        const title = document.createElement('h4');
        title.textContent = barn.name;
        title.className = 'font-medium text-blue-300 mb-2';
        
        const info = document.createElement('div');
        info.className = 'text-sm text-gray-400 mb-2';
        info.innerHTML = `
            <span>容量: ${barn.capacity}</span><br>
            <span>占用: ${barn.pens.reduce((acc, pen) => acc + pen.current_quantity, 0)} / ${barn.pens.reduce((acc, pen) => acc + pen.capacity, 0)}</span>
        `;
        
        const penList = document.createElement('div');
        penList.className = 'grid grid-cols-2 gap-1 text-xs';
        
        barn.pens.forEach(pen => {
            const penCard = this.createPenCard(pen);
            penList.appendChild(penCard);
        });
        
        card.appendChild(title);
        card.appendChild(info);
        card.appendChild(penList);
        
        return card;
    }

    // 6. 创建猪栏卡片（显示当前数量与预留状态）
    createPenCard(pen) {
        const card = document.createElement('div');
        card.className = 'card pen-card fade-in';
        
        const name = document.createElement('div');
        name.textContent = pen.name;
        name.className = 'font-medium text-gray-300';
        
        const status = document.createElement('div');
        status.className = 'text-xs';
        
        if (pen.is_reserved) {
            status.textContent = '✓ 已预留';
            status.className += ' text-yellow-400';
        } else {
            status.textContent = `${pen.current_quantity}/${pen.capacity}`;
            status.className += ' text-green-400';
        }
        
        card.appendChild(name);
        card.appendChild(status);
        
        return card;
    }

    // 7. 创建批次卡片（显示批次详情）
    createBatchCard(batch) {
        const card = document.createElement('div');
        card.className = 'card fade-in';
        
        const title = document.createElement('h3');
        title.textContent = batch.batch_id;
        title.className = 'font-semibold text-lg mb-2';
        
        const info = document.createElement('div');
        info.className = 'text-sm text-gray-400 mb-2';
        info.innerHTML = `
            <span>数量: ${batch.quantity} 头</span><br>
            <span>状态: ${batch.status.replace('_', ' ')}</span>
        `;
        
        const events = document.createElement('div');
        events.className = 'text-xs text-gray-500';
        
        if (batch.recent_events && batch.recent_events.length > 0) {
            const lastEvent = batch.recent_events[0];
            events.textContent = `最近事件: ${lastEvent.event_type} (${new Date(lastEvent.timestamp).toLocaleTimeString()})`;
        } else {
            events.textContent = '暂无事件记录';
        }
        
        card.appendChild(title);
        card.appendChild(info);
        card.appendChild(events);
        
        return card;
    }

    // 8. 创建事件记录项（用于滚动条）
    createEventItem(event) {
        const item = document.createElement('div');
        item.className = `event-item ${this.getEventTypeClass(event.event_type)}`;
        
        const time = document.createElement('span');
        time.textContent = new Date(event.timestamp).toLocaleTimeString();
        time.className = 'font-mono text-xs mr-2';
        
        const type = document.createElement('span');
        type.textContent = event.event_type.toUpperCase();
        type.className = 'font-bold';
        
        const desc = document.createElement('span');
        desc.textContent = ` ${event.description || ''}`;
        
        item.appendChild(time);
        item.appendChild(type);
        item.appendChild(desc);
        
        return item;
    }

    // 9. 根据事件类型返回对应的样式类名（用于颜色区分）
    getEventTypeClass(eventType) {
        const classes = {
            'transfer': 'event-type-transfer',
            'death': 'event-type-death',
            'vaccination': 'event-type-vaccination',
            'sick': 'event-type-sick',
            'treatment': 'event-type-treatment'
        };
        return classes[eventType] || 'event-type-other';
    }

    // 10. 为元素添加淡入动画（可选）
    fadeInElements(elements) {
        elements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(10px)';
            
            setTimeout(() => {
                el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, 100);
        });
    }

    // 11. 绑定用户交互事件（如按钮点击）
    bindEventListeners() {
        // 1. 分配批次按钮事件
        const distributeBtn = document.getElementById('distributeBtn');
        if (distributeBtn) {
            distributeBtn.addEventListener('click', () => {
                const batchId = document.getElementById('batchId').value;
                const distributionMapStr = document.getElementById('distributionMap').value;
                
                if (!batchId) {
                    alert('请输入批次编号！');
                    return;
                }
                
                try {
                    const distributionMap = JSON.parse(distributionMapStr);
                    this.distributeBatch(batchId, distributionMap);
                } catch (e) {
                    alert('分配方案格式错误，请检查输入的JSON格式！');
                }
            });
        }

        // 2. 记录事件按钮事件
        const createEventBtn = document.getElementById('createEventBtn');
        if (createEventBtn) {
            createEventBtn.addEventListener('click', () => {
                const batchId = document.getElementById('batchId').value;
                const eventType = prompt('请输入事件类型（transfer, death, vaccination, sick, treatment）：');
                
                if (!batchId) {
                    alert('请输入批次编号！');
                    return;
                }
                
                if (!eventType) {
                    alert('事件类型不能为空！');
                    return;
                }
                
                const description = prompt('请输入事件描述（可选）：');
                
                this.createEvent(batchId, eventType, description);
            });
        }
    }

    // 12. 向后端发送分批请求（模拟）
    async distributeBatch(batchId, distributionMap) {
        try {
            const response = await fetch(`${this.baseUrl}/${batchId}/distribute`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(distributionMap)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || '分批失败');
            }
            
            const result = await response.json();
            alert(`✅ ${result.message}`);
            
            // 重新加载批次和事件数据以更新视图
            this.loadBatches();
            this.loadEvents();
            
        } catch (error) {
            alert(`❌ 分批失败: ${error.message}`);
        }
    }

    // 13. 向后端发送创建事件请求（模拟）
    async createEvent(batchId, eventType, description) {
        try {
            const response = await fetch(`${this.baseUrl}/${batchId}/event`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    event_type: eventType,
                    pen_id: null,  // 这里可扩展为选择具体猪栏
                    barn_id: null, // 这里可扩展为选择具体猪舍
                    description: description
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || '创建事件失败');
            }
            
            const result = await response.json();
            alert(`✅ 事件已成功记录: ${result.event_type}`);
            
            // 重新加载事件流以更新视图
            this.loadEvents();
            
        } catch (error) {
            alert(`❌ 创建事件失败: ${error.message}`);
        }
    }
}

// 初始化应用（在页面加载完成后执行）
document.addEventListener('DOMContentLoaded', () => {
    new FieldOpsApp();
});