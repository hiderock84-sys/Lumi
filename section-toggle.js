/**
 * セクション折り畳み・展開機能
 * 長いセクションを初期状態で一部のみ表示し、「もっと見る」ボタンでコンテンツを展開
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // エビデンスセクションの折り畳み
    initCollapsibleSection('evidence-section', 'evidence-cards', 3);
    
    // 理論フレームワークの折り畳み
    initCollapsibleSection('theory-section', 'theory-cards', 2);
    
    // 専門家の声の折り畳み
    initCollapsibleSection('expert-section', 'expert-quotes', 2);
    
    // メディア掲載の折り畳み
    initCollapsibleSection('media-section', 'timeline-items', 2);
    
    // アコーディオン機能（完全な折り畳み）
    initAccordionSections();
});

/**
 * セクションを部分的に表示し、「もっと見る」ボタンで展開
 * @param {string} sectionId - セクションのID
 * @param {string} itemsClass - アイテムのクラス名
 * @param {number} initialCount - 初期表示数
 */
function initCollapsibleSection(sectionId, itemsClass, initialCount) {
    const section = document.getElementById(sectionId);
    if (!section) return;
    
    const items = section.querySelectorAll(`.${itemsClass}`);
    if (items.length <= initialCount) return; // アイテム数が少ない場合は処理しない
    
    // 初期状態で一部のみ表示
    items.forEach((item, index) => {
        if (index >= initialCount) {
            item.style.display = 'none';
            item.classList.add('hidden-item');
        }
    });
    
    // 「もっと見る」ボタンを作成
    const btnContainer = document.createElement('div');
    btnContainer.className = 'toggle-btn-container';
    btnContainer.style.cssText = 'text-align: center; margin-top: 2rem;';
    
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'btn btn--outline btn--large toggle-btn';
    toggleBtn.innerHTML = `
        <span class="toggle-btn__text">もっと見る（${items.length - initialCount}件）</span>
        <span class="toggle-btn__icon">▼</span>
    `;
    toggleBtn.style.cssText = 'display: inline-flex; align-items: center; gap: 0.5rem;';
    
    let isExpanded = false;
    
    toggleBtn.addEventListener('click', function() {
        isExpanded = !isExpanded;
        
        items.forEach((item, index) => {
            if (index >= initialCount) {
                if (isExpanded) {
                    item.style.display = '';
                    item.classList.remove('hidden-item');
                    // フェードイン アニメーション
                    item.style.animation = 'fadeInUp 0.5s ease forwards';
                    item.style.animationDelay = `${(index - initialCount) * 0.1}s`;
                } else {
                    item.style.display = 'none';
                    item.classList.add('hidden-item');
                }
            }
        });
        
        // ボタンのテキストとアイコンを更新
        if (isExpanded) {
            toggleBtn.innerHTML = `
                <span class="toggle-btn__text">閉じる</span>
                <span class="toggle-btn__icon">▲</span>
            `;
        } else {
            toggleBtn.innerHTML = `
                <span class="toggle-btn__text">もっと見る（${items.length - initialCount}件）</span>
                <span class="toggle-btn__icon">▼</span>
            `;
            // 閉じるときはセクションのトップにスクロール
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
    
    btnContainer.appendChild(toggleBtn);
    
    // ボタンをセクションの最後に追加
    const container = items[0].parentElement;
    container.parentElement.appendChild(btnContainer);
}

/**
 * アコーディオン形式で完全に折り畳み可能なセクションを初期化
 */
function initAccordionSections() {
    // 大きなセクションをアコーディオン化
    const accordionSections = [
        {
            id: 'evidence-section',
            title: 'エビデンスに基づく支援',
            icon: '🔬',
            defaultOpen: false
        },
        {
            id: 'theory-section', 
            title: '競争優位性と理論的基盤',
            icon: '💎',
            defaultOpen: false
        },
        {
            id: 'expert-section',
            title: '専門性と信頼性',
            icon: '🎓',
            defaultOpen: false
        },
        {
            id: 'media-section',
            title: 'メディア掲載・社会的認知',
            icon: '📰',
            defaultOpen: false
        }
    ];
    
    accordionSections.forEach(config => {
        const section = document.querySelector(`#${config.id}`);
        if (!section) return;
        
        // セクション全体をラップ
        const wrapper = document.createElement('div');
        wrapper.className = 'accordion-section';
        section.parentNode.insertBefore(wrapper, section);
        wrapper.appendChild(section);
        
        // アコーディオンヘッダーを作成
        const header = document.createElement('div');
        header.className = 'accordion-header';
        header.innerHTML = `
            <div class="accordion-header__content">
                <span class="accordion-header__icon">${config.icon}</span>
                <h3 class="accordion-header__title">${config.title}</h3>
            </div>
            <button class="accordion-toggle" aria-label="セクションを開く・閉じる">
                <span class="accordion-toggle__icon">${config.defaultOpen ? '▲' : '▼'}</span>
            </button>
        `;
        
        wrapper.insertBefore(header, section);
        
        // 初期状態を設定
        if (!config.defaultOpen) {
            section.style.display = 'none';
            section.classList.add('accordion-collapsed');
        } else {
            section.classList.add('accordion-expanded');
        }
        
        // クリックイベント
        header.addEventListener('click', function() {
            const isCollapsed = section.classList.contains('accordion-collapsed');
            const toggleIcon = header.querySelector('.accordion-toggle__icon');
            
            if (isCollapsed) {
                // 展開
                section.style.display = 'block';
                section.classList.remove('accordion-collapsed');
                section.classList.add('accordion-expanded');
                toggleIcon.textContent = '▲';
                
                // スムーズに表示
                setTimeout(() => {
                    section.style.animation = 'accordionSlideDown 0.4s ease forwards';
                }, 10);
                
            } else {
                // 折り畳み
                section.style.animation = 'accordionSlideUp 0.3s ease forwards';
                setTimeout(() => {
                    section.style.display = 'none';
                    section.classList.remove('accordion-expanded');
                    section.classList.add('accordion-collapsed');
                }, 300);
                toggleIcon.textContent = '▼';
            }
        });
    });
}

/**
 * タブ切り替え機能（エビデンスセクションを複数タブに分割）
 */
function initTabNavigation() {
    const tabContainer = document.querySelector('.evidence-tabs');
    if (!tabContainer) return;
    
    const tabs = tabContainer.querySelectorAll('.tab-button');
    const panels = document.querySelectorAll('.tab-panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetId = this.getAttribute('data-tab');
            
            // すべてのタブとパネルを非アクティブに
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => {
                p.classList.remove('active');
                p.style.display = 'none';
            });
            
            // クリックされたタブとパネルをアクティブに
            this.classList.add('active');
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) {
                targetPanel.classList.add('active');
                targetPanel.style.display = 'block';
                targetPanel.style.animation = 'fadeIn 0.4s ease forwards';
            }
        });
    });
}

// CSSアニメーションをページに追加
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes accordionSlideDown {
        from {
            opacity: 0;
            max-height: 0;
            overflow: hidden;
        }
        to {
            opacity: 1;
            max-height: 5000px;
            overflow: visible;
        }
    }
    
    @keyframes accordionSlideUp {
        from {
            opacity: 1;
            max-height: 5000px;
        }
        to {
            opacity: 0;
            max-height: 0;
            overflow: hidden;
        }
    }
    
    .toggle-btn {
        transition: all 0.3s ease;
    }
    
    .toggle-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 169, 157, 0.3);
    }
    
    .toggle-btn__icon {
        transition: transform 0.3s ease;
        display: inline-block;
    }
    
    .btn--outline {
        background: transparent;
        border: 2px solid var(--color-primary);
        color: var(--color-primary);
        padding: 1rem 2rem;
        border-radius: var(--radius-full);
        font-weight: 600;
        cursor: pointer;
    }
    
    .btn--outline:hover {
        background: var(--color-primary);
        color: white;
    }
    
    /* アコーディオンスタイル */
    .accordion-section {
        margin: 2rem 0;
        border-radius: var(--radius-xl);
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .accordion-header {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
        color: white;
        padding: 1.5rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .accordion-header:hover {
        background: linear-gradient(135deg, var(--color-primary-light) 0%, var(--color-secondary-light) 100%);
        box-shadow: 0 4px 16px rgba(0, 169, 157, 0.4);
    }
    
    .accordion-header__content {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .accordion-header__icon {
        font-size: 2rem;
    }
    
    .accordion-header__title {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .accordion-toggle {
        background: rgba(255,255,255,0.2);
        border: 2px solid white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .accordion-toggle:hover {
        background: white;
        transform: scale(1.1);
    }
    
    .accordion-toggle__icon {
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        transition: transform 0.3s ease;
    }
    
    .accordion-toggle:hover .accordion-toggle__icon {
        color: var(--color-primary);
    }
    
    .accordion-collapsed {
        display: none;
    }
    
    .accordion-expanded {
        display: block;
    }
    
    @media (max-width: 768px) {
        .accordion-header {
            padding: 1rem 1.5rem;
        }
        
        .accordion-header__title {
            font-size: 1.125rem;
        }
        
        .accordion-header__icon {
            font-size: 1.5rem;
        }
        
        .accordion-toggle {
            width: 36px;
            height: 36px;
        }
    }
`;
document.head.appendChild(style);
