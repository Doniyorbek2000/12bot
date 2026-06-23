(function () {
    "use strict";

    // ===== State =====
    const state = {
        cart: [],
        activeCategory: "all",
        searchQuery: "",
        currentItem: null,
        currentQty: 1
    };

    // ===== DOM Elements =====
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    const splash = $("#splash");
    const searchInput = $("#searchInput");
    const searchClear = $("#searchClear");
    const searchContainer = $("#searchContainer");
    const categoryNav = $("#categoryNav");
    const menuContent = $("#menuContent");
    const cartFab = $("#cartFab");
    const cartCount = $("#cartCount");
    const cartTotal = $("#cartTotal");
    const cartModal = $("#cartModal");
    const cartClose = $("#cartClose");
    const cartItems = $("#cartItems");
    const totalPrice = $("#totalPrice");
    const orderBtn = $("#orderBtn");
    const itemModal = $("#itemModal");
    const itemClose = $("#itemClose");
    const itemModalImg = $("#itemModalImg");
    const itemModalBadge = $("#itemModalBadge");
    const itemModalName = $("#itemModalName");
    const itemModalDesc = $("#itemModalDesc");
    const itemWeightVal = $("#itemWeightVal");
    const itemTimeVal = $("#itemTimeVal");
    const itemCalorieVal = $("#itemCalorieVal");
    const itemModalPrice = $("#itemModalPrice");
    const qtyMinus = $("#qtyMinus");
    const qtyPlus = $("#qtyPlus");
    const qtyValue = $("#qtyValue");
    const addToCartBtn = $("#addToCartBtn");
    const backToTop = $("#backToTop");

    // ===== Helpers =====
    function formatPrice(price) {
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " so'm";
    }

    function showToast(message, icon) {
        const existing = document.querySelector(".toast");
        if (existing) existing.remove();

        const toast = document.createElement("div");
        toast.className = "toast";
        toast.innerHTML = `<span>${icon || "✅"}</span> ${message}`;
        document.body.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.add("show");
        });

        setTimeout(() => {
            toast.classList.remove("show");
            setTimeout(() => toast.remove(), 400);
        }, 2000);
    }

    // ===== Splash Screen =====
    function hideSplash() {
        setTimeout(() => {
            splash.classList.add("hide");
            setTimeout(() => {
                splash.style.display = "none";
            }, 600);
        }, 1800);
    }

    // ===== Render Menu =====
    function getFilteredItems() {
        let items = MENU_DATA.items;

        if (state.activeCategory !== "all") {
            items = items.filter((i) => i.category === state.activeCategory);
        }

        if (state.searchQuery) {
            const q = state.searchQuery.toLowerCase();
            items = items.filter(
                (i) =>
                    i.name.toLowerCase().includes(q) ||
                    i.desc.toLowerCase().includes(q)
            );
        }

        return items;
    }

    function groupByCategory(items) {
        const groups = {};
        const categoryOrder = MENU_DATA.categories.map((c) => c.id);

        items.forEach((item) => {
            if (!groups[item.category]) {
                groups[item.category] = [];
            }
            groups[item.category].push(item);
        });

        const sorted = {};
        categoryOrder.forEach((catId) => {
            if (groups[catId]) {
                sorted[catId] = groups[catId];
            }
        });

        return sorted;
    }

    function getBadgeHTML(badge) {
        if (!badge) return "";
        const classes = {
            new: "badge-new",
            hit: "badge-hit",
            spicy: "badge-spicy"
        };
        const labels = {
            new: "Yangi",
            hit: "Hit",
            spicy: "Achchiq"
        };
        return `<span class="card-badge ${classes[badge]}">${labels[badge]}</span>`;
    }

    function renderMenu() {
        const items = getFilteredItems();

        if (items.length === 0) {
            menuContent.innerHTML = `
                <div class="no-results">
                    <div class="no-results-icon">🔍</div>
                    <h3>Hech narsa topilmadi</h3>
                    <p>Boshqa so'z bilan qidirib ko'ring</p>
                </div>
            `;
            return;
        }

        if (state.activeCategory !== "all") {
            const cat = MENU_DATA.categories.find(
                (c) => c.id === state.activeCategory
            );
            menuContent.innerHTML = `
                <div class="menu-section" data-category="${cat.id}">
                    <div class="section-header">
                        <span class="section-icon">${cat.icon}</span>
                        <h2 class="section-title">${cat.name}</h2>
                        <span class="section-count">${items.length} ta</span>
                    </div>
                    ${items.map((item, i) => renderCard(item, i)).join("")}
                </div>
            `;
        } else {
            const groups = groupByCategory(items);
            let html = "";

            Object.keys(groups).forEach((catId) => {
                const cat = MENU_DATA.categories.find((c) => c.id === catId);
                const catItems = groups[catId];
                html += `
                    <div class="menu-section" data-category="${catId}">
                        <div class="section-header">
                            <span class="section-icon">${cat.icon}</span>
                            <h2 class="section-title">${cat.name}</h2>
                            <span class="section-count">${catItems.length} ta</span>
                        </div>
                        ${catItems.map((item, i) => renderCard(item, i)).join("")}
                    </div>
                `;
            });

            menuContent.innerHTML = html;
        }

        attachCardListeners();
    }

    function renderCard(item, index) {
        const cartItem = state.cart.find((c) => c.id === item.id);
        const inCart = cartItem ? cartItem.qty : 0;

        return `
            <div class="menu-card" data-id="${item.id}" style="animation-delay: ${index * 0.05}s">
                <div class="card-img" data-id="${item.id}">
                    ${getBadgeHTML(item.badge)}
                    <div class="card-img-placeholder">${item.emoji}</div>
                </div>
                <div class="card-body">
                    <div>
                        <div class="card-name">${item.name}</div>
                        <div class="card-desc">${item.desc}</div>
                        <div class="card-meta">
                            <span class="card-weight">${item.weight}</span>
                        </div>
                    </div>
                    <div class="card-bottom">
                        <div>
                            <span class="card-price">${formatPrice(item.price)}</span>
                        </div>
                        <button class="card-add-btn" data-id="${item.id}" aria-label="Qo'shish">
                            ${inCart > 0 ? inCart : "+"}
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    function attachCardListeners() {
        $$(".menu-card").forEach((card) => {
            card.addEventListener("click", (e) => {
                if (e.target.closest(".card-add-btn")) return;
                const id = parseInt(card.dataset.id);
                openItemModal(id);
            });
        });

        $$(".card-add-btn").forEach((btn) => {
            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                const id = parseInt(btn.dataset.id);
                addToCart(id, 1);
                showToast("Savatga qo'shildi", "🛒");
            });
        });
    }

    // ===== Category Navigation =====
    function initCategories() {
        $$(".category-btn").forEach((btn) => {
            btn.addEventListener("click", () => {
                $$(".category-btn").forEach((b) => b.classList.remove("active"));
                btn.classList.add("active");
                state.activeCategory = btn.dataset.category;
                renderMenu();

                btn.scrollIntoView({
                    behavior: "smooth",
                    block: "nearest",
                    inline: "center"
                });
            });
        });
    }

    // ===== Search =====
    function initSearch() {
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
    }

    // ===== Cart =====
    function addToCart(id, qty) {
        const item = MENU_DATA.items.find((i) => i.id === id);
        if (!item) return;

        const existing = state.cart.find((c) => c.id === id);
        if (existing) {
            existing.qty += qty;
        } else {
            state.cart.push({ id, qty, item });
        }

        updateCartUI();
        renderMenu();
    }

    function removeFromCart(id) {
        state.cart = state.cart.filter((c) => c.id !== id);
        updateCartUI();
        renderMenu();
    }

    function updateCartQty(id, delta) {
        const cartItem = state.cart.find((c) => c.id === id);
        if (!cartItem) return;

        cartItem.qty += delta;
        if (cartItem.qty <= 0) {
            removeFromCart(id);
            return;
        }

        updateCartUI();
    }

    function getCartTotal() {
        return state.cart.reduce((sum, c) => sum + c.item.price * c.qty, 0);
    }

    function getCartCount() {
        return state.cart.reduce((sum, c) => sum + c.qty, 0);
    }

    function updateCartUI() {
        const count = getCartCount();
        const total = getCartTotal();

        cartFab.style.display = count > 0 ? "flex" : "none";
        cartCount.textContent = count;
        cartTotal.textContent = formatPrice(total);
        totalPrice.textContent = formatPrice(total);

        renderCartItems();
    }

    function renderCartItems() {
        if (state.cart.length === 0) {
            cartItems.innerHTML = `
                <div class="cart-empty">
                    <div class="cart-empty-icon">🛒</div>
                    <p>Savat bo'sh</p>
                </div>
            `;
            return;
        }

        cartItems.innerHTML = state.cart
            .map(
                (c) => `
            <div class="cart-item" data-id="${c.id}">
                <div class="cart-item-img">
                    <div class="card-img-placeholder">${c.item.emoji}</div>
                </div>
                <div class="cart-item-info">
                    <div class="cart-item-name">${c.item.name}</div>
                    <div class="cart-item-price">${formatPrice(c.item.price * c.qty)}</div>
                </div>
                <div class="cart-item-controls">
                    <button class="cart-qty-btn ${c.qty === 1 ? "delete" : ""}" data-action="minus" data-id="${c.id}">
                        ${c.qty === 1 ? "🗑" : "−"}
                    </button>
                    <span class="cart-item-qty">${c.qty}</span>
                    <button class="cart-qty-btn" data-action="plus" data-id="${c.id}">+</button>
                </div>
            </div>
        `
            )
            .join("");

        cartItems.querySelectorAll(".cart-qty-btn").forEach((btn) => {
            btn.addEventListener("click", () => {
                const id = parseInt(btn.dataset.id);
                const action = btn.dataset.action;
                if (action === "plus") {
                    updateCartQty(id, 1);
                } else {
                    updateCartQty(id, -1);
                }
            });
        });
    }

    // ===== Cart Modal =====
    function openCartModal() {
        renderCartItems();
        cartModal.classList.add("active");
        document.body.style.overflow = "hidden";
    }

    function closeCartModal() {
        cartModal.classList.remove("active");
        document.body.style.overflow = "";
    }

    // ===== Item Detail Modal =====
    function openItemModal(id) {
        const item = MENU_DATA.items.find((i) => i.id === id);
        if (!item) return;

        state.currentItem = item;
        state.currentQty = 1;

        itemModalImg.innerHTML = `<span style="font-size:80px">${item.emoji}</span>`;

        if (item.badge) {
            const labels = { new: "Yangi", hit: "Hit", spicy: "Achchiq" };
            const classes = {
                new: "badge-new",
                hit: "badge-hit",
                spicy: "badge-spicy"
            };
            itemModalBadge.innerHTML = `<span class="${classes[item.badge]}">${labels[item.badge]}</span>`;
            itemModalBadge.style.display = "";
        } else {
            itemModalBadge.style.display = "none";
        }

        itemModalName.textContent = item.name;
        itemModalDesc.textContent = item.desc;
        itemWeightVal.textContent = item.weight;
        itemTimeVal.textContent = item.time;
        itemCalorieVal.textContent = item.calories;
        itemModalPrice.textContent = formatPrice(item.price);
        qtyValue.textContent = "1";

        updateAddBtnText();

        itemModal.classList.add("active");
        document.body.style.overflow = "hidden";
    }

    function closeItemModal() {
        itemModal.classList.remove("active");
        document.body.style.overflow = "";
        state.currentItem = null;
    }

    function updateAddBtnText() {
        if (!state.currentItem) return;
        const total = state.currentItem.price * state.currentQty;
        addToCartBtn.textContent = `Savatga qo'shish — ${formatPrice(total)}`;
    }

    // ===== Order via Telegram =====
    function sendOrder() {
        if (state.cart.length === 0) return;

        let message = "🍽 *Yangi buyurtma - Oasis Restaurant*\n\n";

        state.cart.forEach((c, i) => {
            message += `${i + 1}. ${c.item.emoji} ${c.item.name} x${c.qty} — ${formatPrice(c.item.price * c.qty)}\n`;
        });

        message += `\n💰 *Jami: ${formatPrice(getCartTotal())}*`;

        const encoded = encodeURIComponent(message);
        window.open(`https://t.me/share/url?url=&text=${encoded}`, "_blank");

        showToast("Buyurtma yuborilmoqda...", "📱");
        closeCartModal();
    }

    // ===== Scroll Effects =====
    function initScrollEffects() {
        let lastScroll = 0;

        window.addEventListener(
            "scroll",
            () => {
                const scrollY = window.scrollY;

                if (scrollY > 100) {
                    searchContainer.classList.add("scrolled");
                } else {
                    searchContainer.classList.remove("scrolled");
                }

                if (scrollY > 500) {
                    backToTop.classList.add("visible");
                } else {
                    backToTop.classList.remove("visible");
                }

                lastScroll = scrollY;
            },
            { passive: true }
        );

        backToTop.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // ===== Event Listeners =====
    function initEvents() {
        // Cart FAB
        cartFab.addEventListener("click", openCartModal);
        cartClose.addEventListener("click", closeCartModal);
        cartModal.addEventListener("click", (e) => {
            if (e.target === cartModal) closeCartModal();
        });

        // Item Modal
        itemClose.addEventListener("click", closeItemModal);
        itemModal.addEventListener("click", (e) => {
            if (e.target === itemModal) closeItemModal();
        });

        // Quantity controls
        qtyMinus.addEventListener("click", () => {
            if (state.currentQty > 1) {
                state.currentQty--;
                qtyValue.textContent = state.currentQty;
                updateAddBtnText();
            }
        });

        qtyPlus.addEventListener("click", () => {
            if (state.currentQty < 20) {
                state.currentQty++;
                qtyValue.textContent = state.currentQty;
                updateAddBtnText();
            }
        });

        // Add to cart from modal
        addToCartBtn.addEventListener("click", () => {
            if (state.currentItem) {
                addToCart(state.currentItem.id, state.currentQty);
                showToast(
                    `${state.currentItem.name} — ${state.currentQty} ta qo'shildi`,
                    "🛒"
                );
                closeItemModal();
            }
        });

        // Order button
        orderBtn.addEventListener("click", sendOrder);

        // Prevent body scroll on modal
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                if (itemModal.classList.contains("active")) closeItemModal();
                else if (cartModal.classList.contains("active")) closeCartModal();
            }
        });
    }

    // ===== Initialize =====
    function init() {
        hideSplash();
        initCategories();
        initSearch();
        initScrollEffects();
        initEvents();
        renderMenu();
        updateCartUI();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
