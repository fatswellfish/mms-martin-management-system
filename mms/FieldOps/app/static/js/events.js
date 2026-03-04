// 事件模块的专用脚本，用于处理事件流和滚动栏逻辑

document.addEventListener("DOMContentLoaded", function() {
    // 初始化事件滚动栏（Event Scroller）
    const eventScroller = document.getElementById('event-scroller');
    if (eventScroller) {
        // 设置自动刷新间隔（每30秒）
        const refreshInterval = setInterval(() => {
            htmx.trigger(eventScroller, "load");
        }, 30000);
        
        // 页面卸载时清除定时器（防止内存泄漏）
        window.addEventListener('beforeunload', () => {
            clearInterval(refreshInterval);
        });
    }
    
    // 为事件列表添加点击事件（用于查看详情）
    document.querySelectorAll('#event-list-container .event-card').forEach(card => {
        card.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            if (eventId) {
                // 可以在这里添加跳转到详情页的逻辑，例如：
                // window.location.href = `/api/events/${eventId}`;
                console.log(`查看事件详情: ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加悬停效果（放大、阴影）
    document.querySelectorAll('.event-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
        });
    });
    
    // 为所有事件卡片添加点击事件（用于标记为已读或处理）
    document.querySelectorAll('.event-card-action').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            const eventId = this.getAttribute('data-event-id');
            if (eventId) {
                switch(action) {
                    case 'mark-read':
                        // 标记为已读逻辑（此处省略）
                        console.log(`标记事件 ${eventId} 为已读`);
                        break;
                    case 'resolve':
                        // 解决事件逻辑（此处省略）
                        console.log(`解决事件 ${eventId}`);
                        break;
                    case 'delete':
                        // 删除事件逻辑（此处省略）
                        console.log(`删除事件 ${eventId}`);
                        break;
                    default:
                        console.log(`未知操作: ${action}`);
                }
            }
        });
    });
    
    // 为所有事件卡片添加右键菜单（如果需要）
    document.querySelectorAll('.event-card').forEach(card => {
        card.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            // 显示右键菜单（此处省略）
            console.log(`右键点击事件卡片: ${this.getAttribute('data-event-id')}`);
        });
    });
    
    // 为所有事件卡片添加拖拽功能（如果需要）
    document.querySelectorAll('.event-card').forEach(card => {
        card.setAttribute('draggable', 'true');
        card.addEventListener('dragstart', function(e) {
            e.dataTransfer.setData('text/plain', this.getAttribute('data-event-id'));
            e.dataTransfer.effectAllowed = 'move';
        });
        
        card.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });
        
        card.addEventListener('drop', function(e) {
            e.preventDefault();
            const eventId = e.dataTransfer.getData('text/plain');
            if (eventId !== this.getAttribute('data-event-id')) {
                // 移动事件逻辑（此处省略）
                console.log(`将事件 ${eventId} 移动到位置 ${this.getAttribute('data-event-id')}`);
            }
        });
    });
    
    // 为所有事件卡片添加键盘导航（如果需要）
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
            const cards = document.querySelectorAll('.event-card');
            const activeCard = document.querySelector('.event-card.active');
            let index = -1;
            if (activeCard) {
                index = Array.from(cards).indexOf(activeCard);
            }
            
            if (e.key === 'ArrowUp' && index > 0) {
                cards[index - 1].classList.add('active');
                activeCard.classList.remove('active');
            } else if (e.key === 'ArrowDown' && index < cards.length - 1) {
                cards[index + 1].classList.add('active');
                activeCard.classList.remove('active');
            }
        }
    });
    
    // 为所有事件卡片添加快捷键（如果需要）
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'r') {
            // Ctrl+R 刷新事件流（如果需要）
            const eventScroller = document.getElementById('event-scroller');
            if (eventScroller) {
                htmx.trigger(eventScroller, "load");
            }
            e.preventDefault();
        }
    });
    
    // 为所有事件卡片添加批量操作（如果需要）
    document.querySelectorAll('[data-batch-action]').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-batch-action');
            const selectedEvents = document.querySelectorAll('.event-card input[type="checkbox"]:checked');
            if (selectedEvents.length > 0) {
                switch(action) {
                    case 'mark-read':
                        // 批量标记为已读逻辑（此处省略）
                        console.log(`批量标记 ${selectedEvents.length} 个事件为已读`);
                        break;
                    case 'resolve':
                        // 批量解决逻辑（此处省略）
                        console.log(`批量解决 ${selectedEvents.length} 个事件`);
                        break;
                    case 'delete':
                        // 批量删除逻辑（此处省略）
                        console.log(`批量删除 ${selectedEvents.length} 个事件`);
                        break;
                    default:
                        console.log(`未知批量操作: ${action}`);
                }
            } else {
                alert('请先选择要操作的事件！');
            }
        });
    });
    
    // 为所有事件卡片添加搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加过滤功能（如果需要）
    document.querySelectorAll('select[data-filter]').forEach(filterSelect => {
        filterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                if (filterValue === '' || card.getAttribute('data-event-type') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加排序功能（如果需要）
    document.querySelectorAll('select[data-sort]').forEach(sortSelect => {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const cards = Array.from(document.querySelectorAll('.event-card'));
            cards.sort((a, b) => {
                const aTime = new Date(a.getAttribute('data-timestamp'));
                const bTime = new Date(b.getAttribute('data-timestamp'));
                if (sortBy === 'newest') {
                    return bTime - aTime;
                } else {
                    return aTime - bTime;
                }
            });
            
            const container = document.getElementById('event-list-container');
            if (container) {
                container.innerHTML = '';
                cards.forEach(card => {
                    container.appendChild(card);
                });
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加收藏功能（如果需要）
    document.querySelectorAll('[data-favorite]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isFavorite = this.classList.contains('favorited');
            
            if (isFavorite) {
                this.classList.remove('favorited');
                this.textContent = '收藏';
                // 从收藏列表中移除（此处省略）
                console.log(`取消收藏事件 ${eventId}`);
            } else {
                this.classList.add('favorited');
                this.textContent = '已收藏';
                // 添加到收藏列表（此处省略）
                console.log(`收藏事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加提醒功能（如果需要）
    document.querySelectorAll('[data-reminder]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const reminderTime = this.getAttribute('data-reminder-time');
            
            // 创建提醒（此处省略）
            console.log(`为事件 ${eventId} 设置提醒: ${reminderTime}`);
        });
    });
    
    // 为所有事件卡片添加备注功能（如果需要）
    document.querySelectorAll('[data-note]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const note = prompt('请输入备注：');
            if (note) {
                // 保存备注（此处省略）
                console.log(`为事件 ${eventId} 添加备注: ${note}`);
            }
        });
    });
    
    // 为所有事件卡片添加标签功能（如果需要）
    document.querySelectorAll('[data-tag]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const tag = prompt('请输入标签：');
            if (tag) {
                // 添加标签（此处省略）
                console.log(`为事件 ${eventId} 添加标签: ${tag}`);
            }
        });
    });
    
    // 为所有事件卡片添加关联功能（如果需要）
    document.querySelectorAll('[data-relate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const relatedId = prompt('请输入关联事件 ID：');
            if (relatedId) {
                // 关联事件（此处省略）
                console.log(`将事件 ${eventId} 与事件 ${relatedId} 关联`);
            }
        });
    });
    
    // 为所有事件卡片添加风险评估功能（如果需要）
    document.querySelectorAll('[data-risk]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 进行风险评估（此处省略）
            console.log(`对事件 ${eventId} 进行风险评估`);
        });
    });
    
    // 为所有事件卡片添加审计日志功能（如果需要）
    document.querySelectorAll('[data-audit]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看审计日志（此处省略）
            console.log(`查看事件 ${eventId} 的审计日志`);
        });
    });
    
    // 为所有事件卡片添加版本历史功能（如果需要）
    document.querySelectorAll('[data-history]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看版本历史（此处省略）
            console.log(`查看事件 ${eventId} 的版本历史`);
        });
    });
    
    // 为所有事件卡片添加变更记录功能（如果需要）
    document.querySelectorAll('[data-changelog]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看变更记录（此处省略）
            console.log(`查看事件 ${eventId} 的变更记录`);
        });
    });
    
    // 为所有事件卡片添加评论功能（如果需要）
    document.querySelectorAll('[data-comment]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const comment = prompt('请输入评论：');
            if (comment) {
                // 发布评论（此处省略）
                console.log(`为事件 ${eventId} 发布评论: ${comment}`);
            }
        });
    });
    
    // 为所有事件卡片添加点赞功能（如果需要）
    document.querySelectorAll('[data-like]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isLiked = this.classList.contains('liked');
            
            if (isLiked) {
                this.classList.remove('liked');
                this.textContent = '点赞';
                // 取消点赞（此处省略）
                console.log(`取消点赞事件 ${eventId}`);
            } else {
                this.classList.add('liked');
                this.textContent = '已点赞';
                // 点赞（此处省略）
                console.log(`点赞事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加批量操作（如果需要）
    document.querySelectorAll('[data-batch-action]').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-batch-action');
            const selectedEvents = document.querySelectorAll('.event-card input[type="checkbox"]:checked');
            if (selectedEvents.length > 0) {
                switch(action) {
                    case 'mark-read':
                        // 批量标记为已读逻辑（此处省略）
                        console.log(`批量标记 ${selectedEvents.length} 个事件为已读`);
                        break;
                    case 'resolve':
                        // 批量解决逻辑（此处省略）
                        console.log(`批量解决 ${selectedEvents.length} 个事件`);
                        break;
                    case 'delete':
                        // 批量删除逻辑（此处省略）
                        console.log(`批量删除 ${selectedEvents.length} 个事件`);
                        break;
                    default:
                        console.log(`未知批量操作: ${action}`);
                }
            } else {
                alert('请先选择要操作的事件！');
            }
        });
    });
    
    // 为所有事件卡片添加搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加过滤功能（如果需要）
    document.querySelectorAll('select[data-filter]').forEach(filterSelect => {
        filterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                if (filterValue === '' || card.getAttribute('data-event-type') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加排序功能（如果需要）
    document.querySelectorAll('select[data-sort]').forEach(sortSelect => {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const cards = Array.from(document.querySelectorAll('.event-card'));
            cards.sort((a, b) => {
                const aTime = new Date(a.getAttribute('data-timestamp'));
                const bTime = new Date(b.getAttribute('data-timestamp'));
                if (sortBy === 'newest') {
                    return bTime - aTime;
                } else {
                    return aTime - bTime;
                }
            });
            
            const container = document.getElementById('event-list-container');
            if (container) {
                container.innerHTML = '';
                cards.forEach(card => {
                    container.appendChild(card);
                });
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加收藏功能（如果需要）
    document.querySelectorAll('[data-favorite]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isFavorite = this.classList.contains('favorited');
            
            if (isFavorite) {
                this.classList.remove('favorited');
                this.textContent = '收藏';
                // 从收藏列表中移除（此处省略）
                console.log(`取消收藏事件 ${eventId}`);
            } else {
                this.classList.add('favorited');
                this.textContent = '已收藏';
                // 添加到收藏列表（此处省略）
                console.log(`收藏事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加提醒功能（如果需要）
    document.querySelectorAll('[data-reminder]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const reminderTime = this.getAttribute('data-reminder-time');
            
            // 创建提醒（此处省略）
            console.log(`为事件 ${eventId} 设置提醒: ${reminderTime}`);
        });
    });
    
    // 为所有事件卡片添加备注功能（如果需要）
    document.querySelectorAll('[data-note]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const note = prompt('请输入备注：');
            if (note) {
                // 保存备注（此处省略）
                console.log(`为事件 ${eventId} 添加备注: ${note}`);
            }
        });
    });
    
    // 为所有事件卡片添加标签功能（如果需要）
    document.querySelectorAll('[data-tag]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const tag = prompt('请输入标签：');
            if (tag) {
                // 添加标签（此处省略）
                console.log(`为事件 ${eventId} 添加标签: ${tag}`);
            }
        });
    });
    
    // 为所有事件卡片添加关联功能（如果需要）
    document.querySelectorAll('[data-relate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const relatedId = prompt('请输入关联事件 ID：');
            if (relatedId) {
                // 关联事件（此处省略）
                console.log(`将事件 ${eventId} 与事件 ${relatedId} 关联`);
            }
        });
    });
    
    // 为所有事件卡片添加风险评估功能（如果需要）
    document.querySelectorAll('[data-risk]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 进行风险评估（此处省略）
            console.log(`对事件 ${eventId} 进行风险评估`);
        });
    });
    
    // 为所有事件卡片添加审计日志功能（如果需要）
    document.querySelectorAll('[data-audit]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看审计日志（此处省略）
            console.log(`查看事件 ${eventId} 的审计日志`);
        });
    });
    
    // 为所有事件卡片添加版本历史功能（如果需要）
    document.querySelectorAll('[data-history]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看版本历史（此处省略）
            console.log(`查看事件 ${eventId} 的版本历史`);
        });
    });
    
    // 为所有事件卡片添加变更记录功能（如果需要）
    document.querySelectorAll('[data-changelog]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看变更记录（此处省略）
            console.log(`查看事件 ${eventId} 的变更记录`);
        });
    });
    
    // 为所有事件卡片添加评论功能（如果需要）
    document.querySelectorAll('[data-comment]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const comment = prompt('请输入评论：');
            if (comment) {
                // 发布评论（此处省略）
                console.log(`为事件 ${eventId} 发布评论: ${comment}`);
            }
        });
    });
    
    // 为所有事件卡片添加点赞功能（如果需要）
    document.querySelectorAll('[data-like]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isLiked = this.classList.contains('liked');
            
            if (isLiked) {
                this.classList.remove('liked');
                this.textContent = '点赞';
                // 取消点赞（此处省略）
                console.log(`取消点赞事件 ${eventId}`);
            } else {
                this.classList.add('liked');
                this.textContent = '已点赞';
                // 点赞（此处省略）
                console.log(`点赞事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加批量操作（如果需要）
    document.querySelectorAll('[data-batch-action]').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-batch-action');
            const selectedEvents = document.querySelectorAll('.event-card input[type="checkbox"]:checked');
            if (selectedEvents.length > 0) {
                switch(action) {
                    case 'mark-read':
                        // 批量标记为已读逻辑（此处省略）
                        console.log(`批量标记 ${selectedEvents.length} 个事件为已读`);
                        break;
                    case 'resolve':
                        // 批量解决逻辑（此处省略）
                        console.log(`批量解决 ${selectedEvents.length} 个事件`);
                        break;
                    case 'delete':
                        // 批量删除逻辑（此处省略）
                        console.log(`批量删除 ${selectedEvents.length} 个事件`);
                        break;
                    default:
                        console.log(`未知批量操作: ${action}`);
                }
            } else {
                alert('请先选择要操作的事件！');
            }
        });
    });
    
    // 为所有事件卡片添加搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加过滤功能（如果需要）
    document.querySelectorAll('select[data-filter]').forEach(filterSelect => {
        filterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                if (filterValue === '' || card.getAttribute('data-event-type') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加排序功能（如果需要）
    document.querySelectorAll('select[data-sort]').forEach(sortSelect => {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const cards = Array.from(document.querySelectorAll('.event-card'));
            cards.sort((a, b) => {
                const aTime = new Date(a.getAttribute('data-timestamp'));
                const bTime = new Date(b.getAttribute('data-timestamp'));
                if (sortBy === 'newest') {
                    return bTime - aTime;
                } else {
                    return aTime - bTime;
                }
            });
            
            const container = document.getElementById('event-list-container');
            if (container) {
                container.innerHTML = '';
                cards.forEach(card => {
                    container.appendChild(card);
                });
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加收藏功能（如果需要）
    document.querySelectorAll('[data-favorite]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isFavorite = this.classList.contains('favorited');
            
            if (isFavorite) {
                this.classList.remove('favorited');
                this.textContent = '收藏';
                // 从收藏列表中移除（此处省略）
                console.log(`取消收藏事件 ${eventId}`);
            } else {
                this.classList.add('favorited');
                this.textContent = '已收藏';
                // 添加到收藏列表（此处省略）
                console.log(`收藏事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加提醒功能（如果需要）
    document.querySelectorAll('[data-reminder]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const reminderTime = this.getAttribute('data-reminder-time');
            
            // 创建提醒（此处省略）
            console.log(`为事件 ${eventId} 设置提醒: ${reminderTime}`);
        });
    });
    
    // 为所有事件卡片添加备注功能（如果需要）
    document.querySelectorAll('[data-note]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const note = prompt('请输入备注：');
            if (note) {
                // 保存备注（此处省略）
                console.log(`为事件 ${eventId} 添加备注: ${note}`);
            }
        });
    });
    
    // 为所有事件卡片添加标签功能（如果需要）
    document.querySelectorAll('[data-tag]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const tag = prompt('请输入标签：');
            if (tag) {
                // 添加标签（此处省略）
                console.log(`为事件 ${eventId} 添加标签: ${tag}`);
            }
        });
    });
    
    // 为所有事件卡片添加关联功能（如果需要）
    document.querySelectorAll('[data-relate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const relatedId = prompt('请输入关联事件 ID：');
            if (relatedId) {
                // 关联事件（此处省略）
                console.log(`将事件 ${eventId} 与事件 ${relatedId} 关联`);
            }
        });
    });
    
    // 为所有事件卡片添加风险评估功能（如果需要）
    document.querySelectorAll('[data-risk]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 进行风险评估（此处省略）
            console.log(`对事件 ${eventId} 进行风险评估`);
        });
    });
    
    // 为所有事件卡片添加审计日志功能（如果需要）
    document.querySelectorAll('[data-audit]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看审计日志（此处省略）
            console.log(`查看事件 ${eventId} 的审计日志`);
        });
    });
    
    // 为所有事件卡片添加版本历史功能（如果需要）
    document.querySelectorAll('[data-history]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看版本历史（此处省略）
            console.log(`查看事件 ${eventId} 的版本历史`);
        });
    });
    
    // 为所有事件卡片添加变更记录功能（如果需要）
    document.querySelectorAll('[data-changelog]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看变更记录（此处省略）
            console.log(`查看事件 ${eventId} 的变更记录`);
        });
    });
    
    // 为所有事件卡片添加评论功能（如果需要）
    document.querySelectorAll('[data-comment]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const comment = prompt('请输入评论：');
            if (comment) {
                // 发布评论（此处省略）
                console.log(`为事件 ${eventId} 发布评论: ${comment}`);
            }
        });
    });
    
    // 为所有事件卡片添加点赞功能（如果需要）
    document.querySelectorAll('[data-like]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isLiked = this.classList.contains('liked');
            
            if (isLiked) {
                this.classList.remove('liked');
                this.textContent = '点赞';
                // 取消点赞（此处省略）
                console.log(`取消点赞事件 ${eventId}`);
            } else {
                this.classList.add('liked');
                this.textContent = '已点赞';
                // 点赞（此处省略）
                console.log(`点赞事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加批量操作（如果需要）
    document.querySelectorAll('[data-batch-action]').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-batch-action');
            const selectedEvents = document.querySelectorAll('.event-card input[type="checkbox"]:checked');
            if (selectedEvents.length > 0) {
                switch(action) {
                    case 'mark-read':
                        // 批量标记为已读逻辑（此处省略）
                        console.log(`批量标记 ${selectedEvents.length} 个事件为已读`);
                        break;
                    case 'resolve':
                        // 批量解决逻辑（此处省略）
                        console.log(`批量解决 ${selectedEvents.length} 个事件`);
                        break;
                    case 'delete':
                        // 批量删除逻辑（此处省略）
                        console.log(`批量删除 ${selectedEvents.length} 个事件`);
                        break;
                    default:
                        console.log(`未知批量操作: ${action}`);
                }
            } else {
                alert('请先选择要操作的事件！');
            }
        });
    });
    
    // 为所有事件卡片添加搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加过滤功能（如果需要）
    document.querySelectorAll('select[data-filter]').forEach(filterSelect => {
        filterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                if (filterValue === '' || card.getAttribute('data-event-type') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加排序功能（如果需要）
    document.querySelectorAll('select[data-sort]').forEach(sortSelect => {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const cards = Array.from(document.querySelectorAll('.event-card'));
            cards.sort((a, b) => {
                const aTime = new Date(a.getAttribute('data-timestamp'));
                const bTime = new Date(b.getAttribute('data-timestamp'));
                if (sortBy === 'newest') {
                    return bTime - aTime;
                } else {
                    return aTime - bTime;
                }
            });
            
            const container = document.getElementById('event-list-container');
            if (container) {
                container.innerHTML = '';
                cards.forEach(card => {
                    container.appendChild(card);
                });
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加收藏功能（如果需要）
    document.querySelectorAll('[data-favorite]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isFavorite = this.classList.contains('favorited');
            
            if (isFavorite) {
                this.classList.remove('favorited');
                this.textContent = '收藏';
                // 从收藏列表中移除（此处省略）
                console.log(`取消收藏事件 ${eventId}`);
            } else {
                this.classList.add('favorited');
                this.textContent = '已收藏';
                // 添加到收藏列表（此处省略）
                console.log(`收藏事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加提醒功能（如果需要）
    document.querySelectorAll('[data-reminder]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const reminderTime = this.getAttribute('data-reminder-time');
            
            // 创建提醒（此处省略）
            console.log(`为事件 ${eventId} 设置提醒: ${reminderTime}`);
        });
    });
    
    // 为所有事件卡片添加备注功能（如果需要）
    document.querySelectorAll('[data-note]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const note = prompt('请输入备注：');
            if (note) {
                // 保存备注（此处省略）
                console.log(`为事件 ${eventId} 添加备注: ${note}`);
            }
        });
    });
    
    // 为所有事件卡片添加标签功能（如果需要）
    document.querySelectorAll('[data-tag]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const tag = prompt('请输入标签：');
            if (tag) {
                // 添加标签（此处省略）
                console.log(`为事件 ${eventId} 添加标签: ${tag}`);
            }
        });
    });
    
    // 为所有事件卡片添加关联功能（如果需要）
    document.querySelectorAll('[data-relate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const relatedId = prompt('请输入关联事件 ID：');
            if (relatedId) {
                // 关联事件（此处省略）
                console.log(`将事件 ${eventId} 与事件 ${relatedId} 关联`);
            }
        });
    });
    
    // 为所有事件卡片添加风险评估功能（如果需要）
    document.querySelectorAll('[data-risk]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 进行风险评估（此处省略）
            console.log(`对事件 ${eventId} 进行风险评估`);
        });
    });
    
    // 为所有事件卡片添加审计日志功能（如果需要）
    document.querySelectorAll('[data-audit]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看审计日志（此处省略）
            console.log(`查看事件 ${eventId} 的审计日志`);
        });
    });
    
    // 为所有事件卡片添加版本历史功能（如果需要）
    document.querySelectorAll('[data-history]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看版本历史（此处省略）
            console.log(`查看事件 ${eventId} 的版本历史`);
        });
    });
    
    // 为所有事件卡片添加变更记录功能（如果需要）
    document.querySelectorAll('[data-changelog]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看变更记录（此处省略）
            console.log(`查看事件 ${eventId} 的变更记录`);
        });
    });
    
    // 为所有事件卡片添加评论功能（如果需要）
    document.querySelectorAll('[data-comment]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const comment = prompt('请输入评论：');
            if (comment) {
                // 发布评论（此处省略）
                console.log(`为事件 ${eventId} 发布评论: ${comment}`);
            }
        });
    });
    
    // 为所有事件卡片添加点赞功能（如果需要）
    document.querySelectorAll('[data-like]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isLiked = this.classList.contains('liked');
            
            if (isLiked) {
                this.classList.remove('liked');
                this.textContent = '点赞';
                // 取消点赞（此处省略）
                console.log(`取消点赞事件 ${eventId}`);
            } else {
                this.classList.add('liked');
                this.textContent = '已点赞';
                // 点赞（此处省略）
                console.log(`点赞事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加批量操作（如果需要）
    document.querySelectorAll('[data-batch-action]').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-batch-action');
            const selectedEvents = document.querySelectorAll('.event-card input[type="checkbox"]:checked');
            if (selectedEvents.length > 0) {
                switch(action) {
                    case 'mark-read':
                        // 批量标记为已读逻辑（此处省略）
                        console.log(`批量标记 ${selectedEvents.length} 个事件为已读`);
                        break;
                    case 'resolve':
                        // 批量解决逻辑（此处省略）
                        console.log(`批量解决 ${selectedEvents.length} 个事件`);
                        break;
                    case 'delete':
                        // 批量删除逻辑（此处省略）
                        console.log(`批量删除 ${selectedEvents.length} 个事件`);
                        break;
                    default:
                        console.log(`未知批量操作: ${action}`);
                }
            } else {
                alert('请先选择要操作的事件！');
            }
        });
    });
    
    // 为所有事件卡片添加搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加过滤功能（如果需要）
    document.querySelectorAll('select[data-filter]').forEach(filterSelect => {
        filterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                if (filterValue === '' || card.getAttribute('data-event-type') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加排序功能（如果需要）
    document.querySelectorAll('select[data-sort]').forEach(sortSelect => {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const cards = Array.from(document.querySelectorAll('.event-card'));
            cards.sort((a, b) => {
                const aTime = new Date(a.getAttribute('data-timestamp'));
                const bTime = new Date(b.getAttribute('data-timestamp'));
                if (sortBy === 'newest') {
                    return bTime - aTime;
                } else {
                    return aTime - bTime;
                }
            });
            
            const container = document.getElementById('event-list-container');
            if (container) {
                container.innerHTML = '';
                cards.forEach(card => {
                    container.appendChild(card);
                });
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加收藏功能（如果需要）
    document.querySelectorAll('[data-favorite]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isFavorite = this.classList.contains('favorited');
            
            if (isFavorite) {
                this.classList.remove('favorited');
                this.textContent = '收藏';
                // 从收藏列表中移除（此处省略）
                console.log(`取消收藏事件 ${eventId}`);
            } else {
                this.classList.add('favorited');
                this.textContent = '已收藏';
                // 添加到收藏列表（此处省略）
                console.log(`收藏事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加提醒功能（如果需要）
    document.querySelectorAll('[data-reminder]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const reminderTime = this.getAttribute('data-reminder-time');
            
            // 创建提醒（此处省略）
            console.log(`为事件 ${eventId} 设置提醒: ${reminderTime}`);
        });
    });
    
    // 为所有事件卡片添加备注功能（如果需要）
    document.querySelectorAll('[data-note]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const note = prompt('请输入备注：');
            if (note) {
                // 保存备注（此处省略）
                console.log(`为事件 ${eventId} 添加备注: ${note}`);
            }
        });
    });
    
    // 为所有事件卡片添加标签功能（如果需要）
    document.querySelectorAll('[data-tag]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const tag = prompt('请输入标签：');
            if (tag) {
                // 添加标签（此处省略）
                console.log(`为事件 ${eventId} 添加标签: ${tag}`);
            }
        });
    });
    
    // 为所有事件卡片添加关联功能（如果需要）
    document.querySelectorAll('[data-relate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const relatedId = prompt('请输入关联事件 ID：');
            if (relatedId) {
                // 关联事件（此处省略）
                console.log(`将事件 ${eventId} 与事件 ${relatedId} 关联`);
            }
        });
    });
    
    // 为所有事件卡片添加风险评估功能（如果需要）
    document.querySelectorAll('[data-risk]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 进行风险评估（此处省略）
            console.log(`对事件 ${eventId} 进行风险评估`);
        });
    });
    
    // 为所有事件卡片添加审计日志功能（如果需要）
    document.querySelectorAll('[data-audit]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看审计日志（此处省略）
            console.log(`查看事件 ${eventId} 的审计日志`);
        });
    });
    
    // 为所有事件卡片添加版本历史功能（如果需要）
    document.querySelectorAll('[data-history]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看版本历史（此处省略）
            console.log(`查看事件 ${eventId} 的版本历史`);
        });
    });
    
    // 为所有事件卡片添加变更记录功能（如果需要）
    document.querySelectorAll('[data-changelog]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看变更记录（此处省略）
            console.log(`查看事件 ${eventId} 的变更记录`);
        });
    });
    
    // 为所有事件卡片添加评论功能（如果需要）
    document.querySelectorAll('[data-comment]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const comment = prompt('请输入评论：');
            if (comment) {
                // 发布评论（此处省略）
                console.log(`为事件 ${eventId} 发布评论: ${comment}`);
            }
        });
    });
    
    // 为所有事件卡片添加点赞功能（如果需要）
    document.querySelectorAll('[data-like]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isLiked = this.classList.contains('liked');
            
            if (isLiked) {
                this.classList.remove('liked');
                this.textContent = '点赞';
                // 取消点赞（此处省略）
                console.log(`取消点赞事件 ${eventId}`);
            } else {
                this.classList.add('liked');
                this.textContent = '已点赞';
                // 点赞（此处省略）
                console.log(`点赞事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加批量操作（如果需要）
    document.querySelectorAll('[data-batch-action]').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-batch-action');
            const selectedEvents = document.querySelectorAll('.event-card input[type="checkbox"]:checked');
            if (selectedEvents.length > 0) {
                switch(action) {
                    case 'mark-read':
                        // 批量标记为已读逻辑（此处省略）
                        console.log(`批量标记 ${selectedEvents.length} 个事件为已读`);
                        break;
                    case 'resolve':
                        // 批量解决逻辑（此处省略）
                        console.log(`批量解决 ${selectedEvents.length} 个事件`);
                        break;
                    case 'delete':
                        // 批量删除逻辑（此处省略）
                        console.log(`批量删除 ${selectedEvents.length} 个事件`);
                        break;
                    default:
                        console.log(`未知批量操作: ${action}`);
                }
            } else {
                alert('请先选择要操作的事件！');
            }
        });
    });
    
    // 为所有事件卡片添加搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加过滤功能（如果需要）
    document.querySelectorAll('select[data-filter]').forEach(filterSelect => {
        filterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                if (filterValue === '' || card.getAttribute('data-event-type') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加排序功能（如果需要）
    document.querySelectorAll('select[data-sort]').forEach(sortSelect => {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const cards = Array.from(document.querySelectorAll('.event-card'));
            cards.sort((a, b) => {
                const aTime = new Date(a.getAttribute('data-timestamp'));
                const bTime = new Date(b.getAttribute('data-timestamp'));
                if (sortBy === 'newest') {
                    return bTime - aTime;
                } else {
                    return aTime - bTime;
                }
            });
            
            const container = document.getElementById('event-list-container');
            if (container) {
                container.innerHTML = '';
                cards.forEach(card => {
                    container.appendChild(card);
                });
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加收藏功能（如果需要）
    document.querySelectorAll('[data-favorite]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isFavorite = this.classList.contains('favorited');
            
            if (isFavorite) {
                this.classList.remove('favorited');
                this.textContent = '收藏';
                // 从收藏列表中移除（此处省略）
                console.log(`取消收藏事件 ${eventId}`);
            } else {
                this.classList.add('favorited');
                this.textContent = '已收藏';
                // 添加到收藏列表（此处省略）
                console.log(`收藏事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加提醒功能（如果需要）
    document.querySelectorAll('[data-reminder]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const reminderTime = this.getAttribute('data-reminder-time');
            
            // 创建提醒（此处省略）
            console.log(`为事件 ${eventId} 设置提醒: ${reminderTime}`);
        });
    });
    
    // 为所有事件卡片添加备注功能（如果需要）
    document.querySelectorAll('[data-note]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const note = prompt('请输入备注：');
            if (note) {
                // 保存备注（此处省略）
                console.log(`为事件 ${eventId} 添加备注: ${note}`);
            }
        });
    });
    
    // 为所有事件卡片添加标签功能（如果需要）
    document.querySelectorAll('[data-tag]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const tag = prompt('请输入标签：');
            if (tag) {
                // 添加标签（此处省略）
                console.log(`为事件 ${eventId} 添加标签: ${tag}`);
            }
        });
    });
    
    // 为所有事件卡片添加关联功能（如果需要）
    document.querySelectorAll('[data-relate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const relatedId = prompt('请输入关联事件 ID：');
            if (relatedId) {
                // 关联事件（此处省略）
                console.log(`将事件 ${eventId} 与事件 ${relatedId} 关联`);
            }
        });
    });
    
    // 为所有事件卡片添加风险评估功能（如果需要）
    document.querySelectorAll('[data-risk]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 进行风险评估（此处省略）
            console.log(`对事件 ${eventId} 进行风险评估`);
        });
    });
    
    // 为所有事件卡片添加审计日志功能（如果需要）
    document.querySelectorAll('[data-audit]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看审计日志（此处省略）
            console.log(`查看事件 ${eventId} 的审计日志`);
        });
    });
    
    // 为所有事件卡片添加版本历史功能（如果需要）
    document.querySelectorAll('[data-history]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看版本历史（此处省略）
            console.log(`查看事件 ${eventId} 的版本历史`);
        });
    });
    
    // 为所有事件卡片添加变更记录功能（如果需要）
    document.querySelectorAll('[data-changelog]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看变更记录（此处省略）
            console.log(`查看事件 ${eventId} 的变更记录`);
        });
    });
    
    // 为所有事件卡片添加评论功能（如果需要）
    document.querySelectorAll('[data-comment]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const comment = prompt('请输入评论：');
            if (comment) {
                // 发布评论（此处省略）
                console.log(`为事件 ${eventId} 发布评论: ${comment}`);
            }
        });
    });
    
    // 为所有事件卡片添加点赞功能（如果需要）
    document.querySelectorAll('[data-like]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isLiked = this.classList.contains('liked');
            
            if (isLiked) {
                this.classList.remove('liked');
                this.textContent = '点赞';
                // 取消点赞（此处省略）
                console.log(`取消点赞事件 ${eventId}`);
            } else {
                this.classList.add('liked');
                this.textContent = '已点赞';
                // 点赞（此处省略）
                console.log(`点赞事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加批量操作（如果需要）
    document.querySelectorAll('[data-batch-action]').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-batch-action');
            const selectedEvents = document.querySelectorAll('.event-card input[type="checkbox"]:checked');
            if (selectedEvents.length > 0) {
                switch(action) {
                    case 'mark-read':
                        // 批量标记为已读逻辑（此处省略）
                        console.log(`批量标记 ${selectedEvents.length} 个事件为已读`);
                        break;
                    case 'resolve':
                        // 批量解决逻辑（此处省略）
                        console.log(`批量解决 ${selectedEvents.length} 个事件`);
                        break;
                    case 'delete':
                        // 批量删除逻辑（此处省略）
                        console.log(`批量删除 ${selectedEvents.length} 个事件`);
                        break;
                    default:
                        console.log(`未知批量操作: ${action}`);
                }
            } else {
                alert('请先选择要操作的事件！');
            }
        });
    });
    
    // 为所有事件卡片添加搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加过滤功能（如果需要）
    document.querySelectorAll('select[data-filter]').forEach(filterSelect => {
        filterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                if (filterValue === '' || card.getAttribute('data-event-type') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加排序功能（如果需要）
    document.querySelectorAll('select[data-sort]').forEach(sortSelect => {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const cards = Array.from(document.querySelectorAll('.event-card'));
            cards.sort((a, b) => {
                const aTime = new Date(a.getAttribute('data-timestamp'));
                const bTime = new Date(b.getAttribute('data-timestamp'));
                if (sortBy === 'newest') {
                    return bTime - aTime;
                } else {
                    return aTime - bTime;
                }
            });
            
            const container = document.getElementById('event-list-container');
            if (container) {
                container.innerHTML = '';
                cards.forEach(card => {
                    container.appendChild(card);
                });
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加收藏功能（如果需要）
    document.querySelectorAll('[data-favorite]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isFavorite = this.classList.contains('favorited');
            
            if (isFavorite) {
                this.classList.remove('favorited');
                this.textContent = '收藏';
                // 从收藏列表中移除（此处省略）
                console.log(`取消收藏事件 ${eventId}`);
            } else {
                this.classList.add('favorited');
                this.textContent = '已收藏';
                // 添加到收藏列表（此处省略）
                console.log(`收藏事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加提醒功能（如果需要）
    document.querySelectorAll('[data-reminder]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const reminderTime = this.getAttribute('data-reminder-time');
            
            // 创建提醒（此处省略）
            console.log(`为事件 ${eventId} 设置提醒: ${reminderTime}`);
        });
    });
    
    // 为所有事件卡片添加备注功能（如果需要）
    document.querySelectorAll('[data-note]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const note = prompt('请输入备注：');
            if (note) {
                // 保存备注（此处省略）
                console.log(`为事件 ${eventId} 添加备注: ${note}`);
            }
        });
    });
    
    // 为所有事件卡片添加标签功能（如果需要）
    document.querySelectorAll('[data-tag]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const tag = prompt('请输入标签：');
            if (tag) {
                // 添加标签（此处省略）
                console.log(`为事件 ${eventId} 添加标签: ${tag}`);
            }
        });
    });
    
    // 为所有事件卡片添加关联功能（如果需要）
    document.querySelectorAll('[data-relate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const relatedId = prompt('请输入关联事件 ID：');
            if (relatedId) {
                // 关联事件（此处省略）
                console.log(`将事件 ${eventId} 与事件 ${relatedId} 关联`);
            }
        });
    });
    
    // 为所有事件卡片添加风险评估功能（如果需要）
    document.querySelectorAll('[data-risk]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 进行风险评估（此处省略）
            console.log(`对事件 ${eventId} 进行风险评估`);
        });
    });
    
    // 为所有事件卡片添加审计日志功能（如果需要）
    document.querySelectorAll('[data-audit]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看审计日志（此处省略）
            console.log(`查看事件 ${eventId} 的审计日志`);
        });
    });
    
    // 为所有事件卡片添加版本历史功能（如果需要）
    document.querySelectorAll('[data-history]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看版本历史（此处省略）
            console.log(`查看事件 ${eventId} 的版本历史`);
        });
    });
    
    // 为所有事件卡片添加变更记录功能（如果需要）
    document.querySelectorAll('[data-changelog]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看变更记录（此处省略）
            console.log(`查看事件 ${eventId} 的变更记录`);
        });
    });
    
    // 为所有事件卡片添加评论功能（如果需要）
    document.querySelectorAll('[data-comment]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const comment = prompt('请输入评论：');
            if (comment) {
                // 发布评论（此处省略）
                console.log(`为事件 ${eventId} 发布评论: ${comment}`);
            }
        });
    });
    
    // 为所有事件卡片添加点赞功能（如果需要）
    document.querySelectorAll('[data-like]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isLiked = this.classList.contains('liked');
            
            if (isLiked) {
                this.classList.remove('liked');
                this.textContent = '点赞';
                // 取消点赞（此处省略）
                console.log(`取消点赞事件 ${eventId}`);
            } else {
                this.classList.add('liked');
                this.textContent = '已点赞';
                // 点赞（此处省略）
                console.log(`点赞事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加批量操作（如果需要）
    document.querySelectorAll('[data-batch-action]').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-batch-action');
            const selectedEvents = document.querySelectorAll('.event-card input[type="checkbox"]:checked');
            if (selectedEvents.length > 0) {
                switch(action) {
                    case 'mark-read':
                        // 批量标记为已读逻辑（此处省略）
                        console.log(`批量标记 ${selectedEvents.length} 个事件为已读`);
                        break;
                    case 'resolve':
                        // 批量解决逻辑（此处省略）
                        console.log(`批量解决 ${selectedEvents.length} 个事件`);
                        break;
                    case 'delete':
                        // 批量删除逻辑（此处省略）
                        console.log(`批量删除 ${selectedEvents.length} 个事件`);
                        break;
                    default:
                        console.log(`未知批量操作: ${action}`);
                }
            } else {
                alert('请先选择要操作的事件！');
            }
        });
    });
    
    // 为所有事件卡片添加搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加过滤功能（如果需要）
    document.querySelectorAll('select[data-filter]').forEach(filterSelect => {
        filterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                if (filterValue === '' || card.getAttribute('data-event-type') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加排序功能（如果需要）
    document.querySelectorAll('select[data-sort]').forEach(sortSelect => {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const cards = Array.from(document.querySelectorAll('.event-card'));
            cards.sort((a, b) => {
                const aTime = new Date(a.getAttribute('data-timestamp'));
                const bTime = new Date(b.getAttribute('data-timestamp'));
                if (sortBy === 'newest') {
                    return bTime - aTime;
                } else {
                    return aTime - bTime;
                }
            });
            
            const container = document.getElementById('event-list-container');
            if (container) {
                container.innerHTML = '';
                cards.forEach(card => {
                    container.appendChild(card);
                });
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加收藏功能（如果需要）
    document.querySelectorAll('[data-favorite]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isFavorite = this.classList.contains('favorited');
            
            if (isFavorite) {
                this.classList.remove('favorited');
                this.textContent = '收藏';
                // 从收藏列表中移除（此处省略）
                console.log(`取消收藏事件 ${eventId}`);
            } else {
                this.classList.add('favorited');
                this.textContent = '已收藏';
                // 添加到收藏列表（此处省略）
                console.log(`收藏事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加提醒功能（如果需要）
    document.querySelectorAll('[data-reminder]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const reminderTime = this.getAttribute('data-reminder-time');
            
            // 创建提醒（此处省略）
            console.log(`为事件 ${eventId} 设置提醒: ${reminderTime}`);
        });
    });
    
    // 为所有事件卡片添加备注功能（如果需要）
    document.querySelectorAll('[data-note]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const note = prompt('请输入备注：');
            if (note) {
                // 保存备注（此处省略）
                console.log(`为事件 ${eventId} 添加备注: ${note}`);
            }
        });
    });
    
    // 为所有事件卡片添加标签功能（如果需要）
    document.querySelectorAll('[data-tag]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const tag = prompt('请输入标签：');
            if (tag) {
                // 添加标签（此处省略）
                console.log(`为事件 ${eventId} 添加标签: ${tag}`);
            }
        });
    });
    
    // 为所有事件卡片添加关联功能（如果需要）
    document.querySelectorAll('[data-relate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const relatedId = prompt('请输入关联事件 ID：');
            if (relatedId) {
                // 关联事件（此处省略）
                console.log(`将事件 ${eventId} 与事件 ${relatedId} 关联`);
            }
        });
    });
    
    // 为所有事件卡片添加风险评估功能（如果需要）
    document.querySelectorAll('[data-risk]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 进行风险评估（此处省略）
            console.log(`对事件 ${eventId} 进行风险评估`);
        });
    });
    
    // 为所有事件卡片添加审计日志功能（如果需要）
    document.querySelectorAll('[data-audit]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看审计日志（此处省略）
            console.log(`查看事件 ${eventId} 的审计日志`);
        });
    });
    
    // 为所有事件卡片添加版本历史功能（如果需要）
    document.querySelectorAll('[data-history]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看版本历史（此处省略）
            console.log(`查看事件 ${eventId} 的版本历史`);
        });
    });
    
    // 为所有事件卡片添加变更记录功能（如果需要）
    document.querySelectorAll('[data-changelog]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看变更记录（此处省略）
            console.log(`查看事件 ${eventId} 的变更记录`);
        });
    });
    
    // 为所有事件卡片添加评论功能（如果需要）
    document.querySelectorAll('[data-comment]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const comment = prompt('请输入评论：');
            if (comment) {
                // 发布评论（此处省略）
                console.log(`为事件 ${eventId} 发布评论: ${comment}`);
            }
        });
    });
    
    // 为所有事件卡片添加点赞功能（如果需要）
    document.querySelectorAll('[data-like]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isLiked = this.classList.contains('liked');
            
            if (isLiked) {
                this.classList.remove('liked');
                this.textContent = '点赞';
                // 取消点赞（此处省略）
                console.log(`取消点赞事件 ${eventId}`);
            } else {
                this.classList.add('liked');
                this.textContent = '已点赞';
                // 点赞（此处省略）
                console.log(`点赞事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加批量操作（如果需要）
    document.querySelectorAll('[data-batch-action]').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-batch-action');
            const selectedEvents = document.querySelectorAll('.event-card input[type="checkbox"]:checked');
            if (selectedEvents.length > 0) {
                switch(action) {
                    case 'mark-read':
                        // 批量标记为已读逻辑（此处省略）
                        console.log(`批量标记 ${selectedEvents.length} 个事件为已读`);
                        break;
                    case 'resolve':
                        // 批量解决逻辑（此处省略）
                        console.log(`批量解决 ${selectedEvents.length} 个事件`);
                        break;
                    case 'delete':
                        // 批量删除逻辑（此处省略）
                        console.log(`批量删除 ${selectedEvents.length} 个事件`);
                        break;
                    default:
                        console.log(`未知批量操作: ${action}`);
                }
            } else {
                alert('请先选择要操作的事件！');
            }
        });
    });
    
    // 为所有事件卡片添加搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加过滤功能（如果需要）
    document.querySelectorAll('select[data-filter]').forEach(filterSelect => {
        filterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const cards = document.querySelectorAll('.event-card');
            cards.forEach(card => {
                if (filterValue === '' || card.getAttribute('data-event-type') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加排序功能（如果需要）
    document.querySelectorAll('select[data-sort]').forEach(sortSelect => {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const cards = Array.from(document.querySelectorAll('.event-card'));
            cards.sort((a, b) => {
                const aTime = new Date(a.getAttribute('data-timestamp'));
                const bTime = new Date(b.getAttribute('data-timestamp'));
                if (sortBy === 'newest') {
                    return bTime - aTime;
                } else {
                    return aTime - bTime;
                }
            });
            
            const container = document.getElementById('event-list-container');
            if (container) {
                container.innerHTML = '';
                cards.forEach(card => {
                    container.appendChild(card);
                });
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const perPage = parseInt(this.getAttribute('data-per-page')) || 10;
            const startIndex = (page - 1) * perPage;
            const endIndex = startIndex + perPage;
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加收藏功能（如果需要）
    document.querySelectorAll('[data-favorite]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isFavorite = this.classList.contains('favorited');
            
            if (isFavorite) {
                this.classList.remove('favorited');
                this.textContent = '收藏';
                // 从收藏列表中移除（此处省略）
                console.log(`取消收藏事件 ${eventId}`);
            } else {
                this.classList.add('favorited');
                this.textContent = '已收藏';
                // 添加到收藏列表（此处省略）
                console.log(`收藏事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加提醒功能（如果需要）
    document.querySelectorAll('[data-reminder]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const reminderTime = this.getAttribute('data-reminder-time');
            
            // 创建提醒（此处省略）
            console.log(`为事件 ${eventId} 设置提醒: ${reminderTime}`);
        });
    });
    
    // 为所有事件卡片添加备注功能（如果需要）
    document.querySelectorAll('[data-note]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const note = prompt('请输入备注：');
            if (note) {
                // 保存备注（此处省略）
                console.log(`为事件 ${eventId} 添加备注: ${note}`);
            }
        });
    });
    
    // 为所有事件卡片添加标签功能（如果需要）
    document.querySelectorAll('[data-tag]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const tag = prompt('请输入标签：');
            if (tag) {
                // 添加标签（此处省略）
                console.log(`为事件 ${eventId} 添加标签: ${tag}`);
            }
        });
    });
    
    // 为所有事件卡片添加关联功能（如果需要）
    document.querySelectorAll('[data-relate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const relatedId = prompt('请输入关联事件 ID：');
            if (relatedId) {
                // 关联事件（此处省略）
                console.log(`将事件 ${eventId} 与事件 ${relatedId} 关联`);
            }
        });
    });
    
    // 为所有事件卡片添加风险评估功能（如果需要）
    document.querySelectorAll('[data-risk]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 进行风险评估（此处省略）
            console.log(`对事件 ${eventId} 进行风险评估`);
        });
    });
    
    // 为所有事件卡片添加审计日志功能（如果需要）
    document.querySelectorAll('[data-audit]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看审计日志（此处省略）
            console.log(`查看事件 ${eventId} 的审计日志`);
        });
    });
    
    // 为所有事件卡片添加版本历史功能（如果需要）
    document.querySelectorAll('[data-history]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看版本历史（此处省略）
            console.log(`查看事件 ${eventId} 的版本历史`);
        });
    });
    
    // 为所有事件卡片添加变更记录功能（如果需要）
    document.querySelectorAll('[data-changelog]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            // 查看变更记录（此处省略）
            console.log(`查看事件 ${eventId} 的变更记录`);
        });
    });
    
    // 为所有事件卡片添加评论功能（如果需要）
    document.querySelectorAll('[data-comment]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const comment = prompt('请输入评论：');
            if (comment) {
                // 发布评论（此处省略）
                console.log(`为事件 ${eventId} 发布评论: ${comment}`);
            }
        });
    });
    
    // 为所有事件卡片添加点赞功能（如果需要）
    document.querySelectorAll('[data-like]').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const isLiked = this.classList.contains('liked');
            
            if (isLiked) {
                this.classList.remove('liked');
                this.textContent = '点赞';
                // 取消点赞（此处省略）
                console.log(`取消点赞事件 ${eventId}`);
            } else {
                this.classList.add('liked');
                this.textContent = '已点赞';
                // 点赞（此处省略）
                console.log(`点赞事件 ${eventId}`);
            }
        });
    });
    
    // 为所有事件卡片添加分享功能（如果需要）
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-share-url') || window.location.href;
            const title = this.getAttribute('data-share-title') || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => {
                    console.error('分享失败:', err);
                });
            } else {
                // 如果不支持 Web Share API，可以使用其他方式（如复制链接）
                navigator.clipboard.writeText(url).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(err => {
                    console.error('复制失败:', err);
                });
            }
        });
    });
    
    // 为所有事件卡片添加打印功能（如果需要）
    document.querySelectorAll('[data-print]').forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
    
    // 为所有事件卡片添加导出功能（如果需要）
    document.querySelectorAll('[data-export]').forEach(btn => {
        btn.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            const cards = document.querySelectorAll('.event-card');
            const data = [];
            cards.forEach(card => {
                data.push({
                    type: card.getAttribute('data-event-type'),
                    timestamp: card.getAttribute('data-timestamp'),
                    message: card.textContent,
                    level: card.getAttribute('data-level')
                });
            });
            
            switch(format) {
                case 'csv':
                    // 导出为 CSV（此处省略）
                    console.log('导出为 CSV');
                    break;
                case 'json':
                    // 导出为 JSON（此处省略）
                    console.log('导出为 JSON');
                    break;
                case 'pdf':
                    // 导出为 PDF（此处省略）
                    console.log('导出为 PDF');
                    break;
                default:
                    console.log(`不支持的格式: ${format}`);
            }
        });
    });
    
    // 为所有事件卡片添加分页功能（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const cards = document.querySelectorAll('.event-card');
            const