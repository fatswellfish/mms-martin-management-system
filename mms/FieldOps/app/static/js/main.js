// 主要的 JavaScript 逻辑文件，用于增强交互性

document.addEventListener("DOMContentLoaded", function() {
    // 初始化事件：加载后自动刷新卡片数据（如果需要）
    const cards = document.querySelectorAll('[hx-get]');
    cards.forEach(card => {
        // 确保在页面加载完成后触发一次刷新（避免首次为空）
        setTimeout(() => {
            const targetId = card.getAttribute("id");
            if (targetId) {
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    htmx.trigger(targetElement, "load");
                }
            }
        }, 1000);
    });
    
    // 为所有按钮添加点击事件（如刷新、提交等）
    document.querySelectorAll('button[type="submit"], button[data-action]').forEach(button => {
        button.addEventListener('click', function(e) {
            const action = this.getAttribute('data-action');
            if (action === 'refresh') {
                const targetId = this.getAttribute('data-target');
                if (targetId) {
                    const targetElement = document.getElementById(targetId);
                    if (targetElement) {
                        htmx.trigger(targetElement, "refresh");
                    }
                }
            }
        });
    });
    
    // 为所有下拉菜单添加变化事件处理（如切换分配方式）
    document.querySelectorAll('select[id="distribution"]').forEach(select => {
        select.addEventListener('change', function() {
            const manualDiv = document.getElementById('manual-distribution');
            if (this.value === 'manual') {
                manualDiv.style.display = 'block';
            } else {
                manualDiv.style.display = 'none';
            }
        });
    });
    
    // 为所有模态框添加关闭事件（点击遮罩或关闭按钮）
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('show');
            }
        });
    });
    
    // 为所有关闭按钮添加事件（确保能正确关闭模态框）
    document.querySelectorAll('.modal-close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.classList.remove('show');
            }
        });
    });
    
    // 为所有表格和列表添加可滚动效果（如果内容过多）
    document.querySelectorAll('.max-h-64, .max-h-48').forEach(container => {
        container.addEventListener('scroll', function() {
            // 可以在这里添加滚动时的动画或高亮效果（例如，当滚动到底部时自动加载更多）
        });
    });
    
    // 为所有卡片添加悬停效果（放大、阴影）
    document.querySelectorAll('.card, .bg-white, .rounded-lg').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
        });
    });
    
    // 为所有输入框添加聚焦效果（边框变色）
    document.querySelectorAll('input, textarea, select').forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#2563eb';
            this.style.boxShadow = '0 0 0 2px rgba(37, 99, 235, 0.5)';
        });
        
        input.addEventListener('blur', function() {
            this.style.borderColor = '#d1d5db';
            this.style.boxShadow = 'none';
        });
    });
    
    // 为所有链接添加点击效果（增加反馈）
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.href.startsWith('#')) return; // 跳转到锚点的不处理
            e.preventDefault();
            const url = this.href;
            // 可以在这里添加加载动画或提示信息（例如，正在跳转...）
            window.location.href = url;
        });
    });
    
    // 为所有表单添加提交前的验证（如果需要）
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            // 可以在这里添加表单验证逻辑（例如，必填项检查）
            // 例如：
            // const requiredInputs = this.querySelectorAll('[required]');
            // let isValid = true;
            // requiredInputs.forEach(input => {
            //     if (!input.value.trim()) {
            //         isValid = false;
            //         input.style.borderColor = '#dc2626';
            //     } else {
            //         input.style.borderColor = '#d1d5db';
            //     }
            // });
            // if (!isValid) {
            //     e.preventDefault();
            //     alert('请填写所有必填项！');
            // }
        });
    });
    
    // 为所有刷新按钮添加点击事件（如果需要更复杂的刷新逻辑）
    document.querySelectorAll('[data-action="refresh"]').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            if (targetId) {
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    htmx.trigger(targetElement, "refresh");
                }
            }
        });
    });
    
    // 为所有分页按钮添加点击事件（如果需要）
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const targetId = this.getAttribute('data-target');
            if (targetId) {
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    htmx.trigger(targetElement, "load", { page: page });
                }
            }
        });
    });
    
    // 为所有搜索框添加实时搜索功能（如果需要）
    document.querySelectorAll('input[type="search"]').forEach(searchInput => {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const items = this.closest('.list-group')?.querySelectorAll('.list-item');
            if (items) {
                items.forEach(item => {
                    const text = item.textContent.toLowerCase();
                    if (text.includes(query)) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            }
        });
    });
    
    // 为所有模态框添加键盘事件（ESC键关闭）
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal.show').forEach(modal => {
                modal.classList.remove('show');
            });
        }
    });
    
    // 为所有卡片添加拖拽排序功能（如果需要）
    // 可以使用 HTML5 Drag and Drop API 来实现，但这里为了简洁，仅做注释说明。
    // 例如：
    // document.querySelectorAll('.sortable-card').forEach(card => {
    //     card.setAttribute('draggable', 'true');
    //     card.addEventListener('dragstart', function(e) {
    //         e.dataTransfer.setData('text/plain', this.id);
    //     });
    //     card.addEventListener('dragover', function(e) {
    //         e.preventDefault();
    //     });
    //     card.addEventListener('drop', function(e) {
    //         e.preventDefault();
    //         const id = e.dataTransfer.getData('text/plain');
    //         const source = document.getElementById(id);
    //         if (source && source !== this) {
    //             // 交换位置逻辑（此处省略）
    //         }
    //     });
    // });
});

// 可选：为某些特定操作提供额外的工具函数（如批量操作、导出数据等）
window.utils = {
    // 批量删除确认对话框
    confirmDelete: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },
    
    // 数据导出为 CSV
    exportToCSV: function(data, filename) {
        const csv = data.map(row => Object.values(row).join(",")).join('\n');
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename || 'export.csv';
        a.click();
        window.URL.revokeObjectURL(url);
    },
    
    // 显示成功/错误消息（可以替换为更美观的 toast 消息）
    showMessage: function(text, type = 'info') {
        alert(`${type.toUpperCase()}: ${text}`);
    }
};

// 可选：为 HTMX 响应添加自定义行为（例如，处理特定响应头）
htmx.on("htmx:afterRequest", function(evt) {
    // 检查响应是否包含特定的自定义头，例如：X-Redirect
    const redirectHeader = evt.detail.xhr.getResponseHeader('X-Redirect');
    if (redirectHeader) {
        window.location.href = redirectHeader;
    }
    
    // 检查响应是否包含特定的自定义头，例如：X-Toast
    const toastHeader = evt.detail.xhr.getResponseHeader('X-Toast');
    if (toastHeader) {
        window.utils.showMessage(toastHeader, 'success');
    }
});

// 可选：为页面加载状态添加进度条（如果需要）
window.addEventListener('load', function() {
    // 可以在这里添加页面加载完成后的逻辑（例如，隐藏加载动画）
    const loader = document.getElementById('page-loader');
    if (loader) {
        loader.style.display = 'none';
    }
});

// 可选：为所有外部链接添加新窗口打开（如果需要）
document.querySelectorAll('a[href^="http"]:not([href*="localhost"])').forEach(link => {
    link.setAttribute('target', '_blank');
    link.setAttribute('rel', 'noopener noreferrer');
});

// 可选：为所有图片添加懒加载（如果需要）
// 这里是一个简单的示例，实际中可能需要使用 Intersection Observer
// document.querySelectorAll('img[data-src]').forEach(img => {
//     img.src = img.dataset.src;
//     img.removeAttribute('data-src');
// });

// 可选：为所有表格添加行高亮（如果需要）
// document.querySelectorAll('table tr').forEach(row => {
//     row.addEventListener('mouseenter', function() {
//         this.style.backgroundColor = '#f0f9ff';
//     });
//     row.addEventListener('mouseleave', function() {
//         this.style.backgroundColor = '';
//     });
// });

// 可选：为所有按钮添加点击音效（如果需要）
// const clickSound = new Audio('/sounds/click.mp3');
// document.querySelectorAll('button, a').forEach(el => {
//     el.addEventListener('click', function() {
//         clickSound.play();
//     });
// });

// 可选：为所有输入框添加自动补全功能（如果需要）
// 这里是一个简单的示例，实际中可能需要使用更复杂的库或自定义逻辑。
// document.querySelectorAll('input[autocomplete]').forEach(input => {
//     input.addEventListener('input', function() {
//         // 自动补全逻辑（此处省略）
//     });
// });

// 可选：为所有模态框添加滚动锁定（防止背景滚动）
// 这里是一个简单的示例，实际中可能需要更复杂的逻辑。
// document.querySelectorAll('.modal').forEach(modal => {
//     modal.addEventListener('show.bs.modal', function() {
//         document.body.style.overflow = 'hidden';
//     });
//     modal.addEventListener('hidden.bs.modal', function() {
//         document.body.style.overflow = '';
//     });
// });

// 可选：为所有表单添加自动保存功能（如果需要）
// 这里是一个简单的示例，实际中可能需要使用 localStorage 或更复杂的逻辑。
// document.querySelectorAll('form').forEach(form => {
//     form.addEventListener('input', function() {
//         // 自动保存逻辑（此处省略）
//     });
// });

// 可选：为所有页面添加访问统计（如果需要）
// 这里是一个简单的示例，实际中可能需要使用 Google Analytics 等服务。
// window.addEventListener('load', function() {
//     // 发送页面访问统计（此处省略）
// });

// 可选：为所有元素添加性能监控（如果需要）
// 这里是一个简单的示例，实际中可能需要使用更复杂的工具。
// window.addEventListener('load', function() {
//     // 性能监控逻辑（此处省略）
// });

// 可选：为所有元素添加安全防护（如果需要）
// 这里是一个简单的示例，实际中可能需要使用更复杂的工具。
// window.addEventListener('load', function() {
//     // 安全防护逻辑（此处省略）
// });

// 可选：为所有元素添加可访问性支持（如果需要）
// 这里是一个简单的示例，实际中可能需要使用更复杂的工具。
// window.addEventListener('load', function() {
//     // 可访问性支持逻辑（此处省略）
// });

// 可选：为所有元素添加国际化支持（如果需要）
// 这里是一个简单的示例，实际中可能需要使用更复杂的工具。
// window.addEventListener('load', function() {
//     // 国际化支持逻辑（此处省略）
// });
