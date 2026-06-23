(function () {
    "use strict";

    const FONT_SIZES = [12, 13, 14, 15, 16, 18, 20];
    const DEFAULT_FONT_INDEX = 2;

    const state = {
        lang: localStorage.getItem("shirin_lang") || "uz",
        theme: localStorage.getItem("shirin_theme") || "dark",
        layout: localStorage.getItem("shirin_layout") || "grid-2",
        fontIndex: parseInt(localStorage.getItem("shirin_font") || DEFAULT_FONT_INDEX),
        activeCategory: "all",
        searchQuery: ""
    };

    const $ = (s) => document.querySelector(s);
    const $$ = (s) => document.querySelectorAll(s);

    const splash = $("#splash");
    const searchInput = $("#searchInput");
    const searchClear = $("#searchClear");
    const searchContainer = $("#searchContainer");
    const categoryScroll = $("#categoryScroll");
    const menuContent = $("#menuContent");
    const itemModal = $("#itemModal");
    const itemClose = $("#itemClose");
    const itemModalImg = $("#itemModalImg");
    const itemModalBadge = $("#itemModalBadge");
    const itemModalName = $("#itemModalName");
    const itemWeightVal = $("#itemWeightVal");
    const itemTimeVal = $("#itemTimeVal");
    const itemModalPrice = $("#itemModalPrice");
    const orderBtn = $("#orderBtn");
    const orderBtnText = $("#orderBtnText");
    const backToTop = $("#backToTop");
    const footerCopy = $("#footerCopy");

    function t(key) {
        return TRANSLATIONS[state.lang][key] || key;
    }

    function formatPrice(p) {
        return p.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " so'm";
    }

    function getItemName(item) {
        return item.name[state.lang] || item.name.uz;
    }

    // ===== Splash =====
    setTimeout(() => {
        splash.classList.add("hide");
        setTimeout(() => splash.style.display = "none", 600);
    }, 1600);

    // ===== Font Size =====
    function applyFontSize() {
        const size = FONT_SIZES[state.fontIndex];
        document.body.style.setProperty("--font-size", size + "px");
        localStorage.setItem("shirin_font", state.fontIndex);
    }

    function changeFontSize(dir) {
        if (dir === "up" && state.fontIndex < FONT_SIZES.length - 1) {
            state.fontIndex++;
        } else if (dir === "down" && state.fontIndex > 0) {
            state.fontIndex--;
        }
        applyFontSize();
        renderMenu();
    }

    // ===== Theme =====
    function applyTheme(theme) {
        state.theme = theme;
        document.body.setAttribute("data-theme", theme);
        localStorage.setItem("shirin_theme", theme);
        $$(".theme-dot").forEach((d) => d.classList.remove("active-dot"));
        const activeBtn = $(`.theme-btn[data-theme="${theme}"] .theme-dot`);
        if (activeBtn) activeBtn.classList.add("active-dot");
    }

    // ===== Layout =====
    function applyLayout(layout) {
        state.layout = layout;
        document.body.setAttribute("data-layout", layout);
        localStorage.setItem("shirin_layout", layout);
        $$(".layout-btn").forEach((b) => b.classList.remove("active"));
        const btn = $(`.layout-btn[data-layout="${layout}"]`);
        if (btn) btn.classList.add("active");
        renderMenu();
    }

    // ===== Language =====
    function applyLang(lang) {
        state.lang = lang;
        localStorage.setItem("shirin_lang", lang);
        $$(".lang-btn").forEach((b) => b.classList.remove("active"));
        const btn = $(`.lang-btn[data-lang="${lang}"]`);
        if (btn) btn.classList.add("active");

        searchInput.placeholder = t("searchPlaceholder");
        footerCopy.textContent = t("footerCopy");

        renderCategories();
        renderMenu();
    }

    // ===== Categories =====
    function renderCategories() {
        const cats = TRANSLATIONS[state.lang].categories;
        const icons = TRANSLATIONS[state.lang].catIcons;
        let html = `<button class="category-btn ${state.activeCategory === "all" ? "active" : ""}" data-category="all">
            <span class="cat-icon">🍴</span><span class="cat-name">${t("allCategories")}</span>
        </button>`;
        Object.keys(cats).forEach((id) => {
            html += `<button class="category-btn ${state.activeCategory === id ? "active" : ""}" data-category="${id}">
                <span class="cat-icon">${icons[id]}</span><span class="cat-name">${cats[id]}</span>
            </button>`;
        });
        categoryScroll.innerHTML = html;

        $$(".category-btn").forEach((btn) => {
            btn.addEventListener("click", () => {
                $$(".category-btn").forEach((b) => b.classList.remove("active"));
                btn.classList.add("active");
                state.activeCategory = btn.dataset.category;
                renderMenu();
                btn.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
            });
        });
    }

    // ===== Search =====
    searchInput.addEventListener("input", () => {
        state.searchQuery = searchInput.value.trim();
        searchClear.classList.toggle("visible", state.searchQuery.length > 0);
        renderMenu();
    });
    searchClear.addEventListener("click", () => {
        searchInput.value = "";
        state.searchQuery = "";
        searchClear.classList.remove("visible");
        renderMenu();
        searchInput.focus();
    });

    // ===== Render Menu =====
    function getFilteredItems() {
        let items = MENU_DATA;
        if (state.activeCategory !== "all") {
            items = items.filter((i) => i.category === state.activeCategory);
        }
        if (state.searchQuery) {
            const q = state.searchQuery.toLowerCase();
            items = items.filter((i) => getItemName(i).toLowerCase().includes(q));
        }
        return items;
    }

    function groupByCategory(items) {
        const order = ["salads", "soups", "main", "kebab", "extras", "drinks"];
        const groups = {};
        items.forEach((item) => {
            if (!groups[item.category]) groups[item.category] = [];
            groups[item.category].push(item);
        });
        const sorted = {};
        order.forEach((id) => { if (groups[id]) sorted[id] = groups[id]; });
        return sorted;
    }

    function getBadgeHTML(badge) {
        if (!badge) return "";
        const labels = {
            uz: { new: "Yangi", hit: "Hit", spicy: "Achchiq" },
            krill: { new: "Янги", hit: "Хит", spicy: "Аччиқ" },
            ru: { new: "Новинка", hit: "Хит", spicy: "Острое" }
        };
        const cls = { new: "badge-new", hit: "badge-hit", spicy: "badge-spicy" };
        const label = (labels[state.lang] || labels.uz)[badge] || badge;
        return `<span class="card-badge ${cls[badge]}">${label}</span>`;
    }

    function renderMenu() {
        const items = getFilteredItems();
        const fontSize = FONT_SIZES[state.fontIndex];

        if (items.length === 0) {
            menuContent.innerHTML = `<div class="no-results">
                <div class="no-results-icon">🔍</div>
                <h3>${t("noResults")}</h3>
                <p>${t("noResultsHint")}</p>
            </div>`;
            return;
        }

        const layout = state.layout;
        const cats = TRANSLATIONS[state.lang].categories;
        const icons = TRANSLATIONS[state.lang].catIcons;

        if (state.activeCategory !== "all") {
            const catId = state.activeCategory;
            menuContent.innerHTML = `<div class="menu-section">
                <div class="section-header">
                    <span class="section-icon">${icons[catId]}</span>
                    <h2 class="section-title">${cats[catId]}</h2>
                    <span class="section-count">${items.length}</span>
                </div>
                <div class="menu-grid ${layout}">${items.map((it, i) => renderCard(it, i, layout, fontSize)).join("")}</div>
            </div>`;
        } else {
            const groups = groupByCategory(items);
            let html = "";
            Object.keys(groups).forEach((catId) => {
                const g = groups[catId];
                html += `<div class="menu-section">
                    <div class="section-header">
                        <span class="section-icon">${icons[catId]}</span>
                        <h2 class="section-title">${cats[catId]}</h2>
                        <span class="section-count">${g.length}</span>
                    </div>
                    <div class="menu-grid ${layout}">${g.map((it, i) => renderCard(it, i, layout, fontSize)).join("")}</div>
                </div>`;
            });
            menuContent.innerHTML = html;
        }

        $$(".menu-card").forEach((card) => {
            card.addEventListener("click", () => {
                openItemModal(parseInt(card.dataset.id));
            });
        });
    }

    function renderCard(item, index, layout, fontSize) {
        const name = getItemName(item);
        const price = formatPrice(item.price);
        const delay = Math.min(index * 0.04, 0.6);
        const nameSize = fontSize + "px";
        const priceSize = fontSize + "px";

        if (layout === "grid-1") {
            return `<div class="menu-card card-list" data-id="${item.id}" style="animation-delay:${delay}s">
                <div class="card-img-wrap">${getBadgeHTML(item.badge)}<div class="card-emoji">${item.emoji}</div></div>
                <div class="card-body">
                    <div class="card-name" style="font-size:${nameSize}">${name}</div>
                </div>
                <div class="card-price" style="font-size:${priceSize}">${price}</div>
            </div>`;
        }

        const tileFontName = layout === "grid-3" ? Math.max(fontSize - 2, 10) + "px" : nameSize;
        const tileFontPrice = layout === "grid-3" ? Math.max(fontSize - 2, 10) + "px" : priceSize;

        return `<div class="menu-card card-tile" data-id="${item.id}" style="animation-delay:${delay}s">
            ${getBadgeHTML(item.badge)}
            <div class="card-emoji-tile">${item.emoji}</div>
            <div class="card-name" style="font-size:${tileFontName}">${name}</div>
            <div class="card-price" style="font-size:${tileFontPrice}">${price}</div>
        </div>`;
    }

    // ===== Item Modal =====
    function openItemModal(id) {
        const item = MENU_DATA.find((i) => i.id === id);
        if (!item) return;

        itemModalImg.innerHTML = `<span style="font-size:80px">${item.emoji}</span>`;
        if (item.badge) {
            itemModalBadge.innerHTML = getBadgeHTML(item.badge);
            itemModalBadge.style.display = "";
        } else {
            itemModalBadge.style.display = "none";
        }
        itemModalName.textContent = getItemName(item);
        itemWeightVal.textContent = item.weight;
        itemTimeVal.textContent = item.time;
        itemModalPrice.textContent = formatPrice(item.price);

        orderBtnText.textContent = t("orderBtn");
        const msg = encodeURIComponent(`🍽 ${getItemName(item)} — ${formatPrice(item.price)}\n\nShirin Kafe`);
        orderBtn.href = `https://t.me/share/url?url=&text=${msg}`;

        itemModal.classList.add("active");
        document.body.style.overflow = "hidden";
    }

    function closeItemModal() {
        itemModal.classList.remove("active");
        document.body.style.overflow = "";
    }

    itemClose.addEventListener("click", closeItemModal);
    itemModal.addEventListener("click", (e) => { if (e.target === itemModal) closeItemModal(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeItemModal(); });

    // ===== Toolbar Events =====
    $$(".lang-btn").forEach((btn) => btn.addEventListener("click", () => applyLang(btn.dataset.lang)));
    $$(".layout-btn").forEach((btn) => btn.addEventListener("click", () => applyLayout(btn.dataset.layout)));
    $$(".theme-btn").forEach((btn) => btn.addEventListener("click", () => applyTheme(btn.dataset.theme)));
    $$(".font-btn").forEach((btn) => btn.addEventListener("click", () => changeFontSize(btn.dataset.font)));

    // ===== Scroll =====
    window.addEventListener("scroll", () => {
        searchContainer.classList.toggle("scrolled", window.scrollY > 100);
        backToTop.classList.toggle("visible", window.scrollY > 500);
    }, { passive: true });

    backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

    // ===== Init =====
    applyTheme(state.theme);
    applyLayout(state.layout);
    applyLang(state.lang);
    applyFontSize();
})();
