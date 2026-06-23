const TRANSLATIONS = {
    uz: {
        searchPlaceholder: "Taom qidirish...",
        allCategories: "Barchasi",
        noResults: "Hech narsa topilmadi",
        noResultsHint: "Boshqa so'z bilan qidirib ko'ring",
        orderBtn: "Buyurtma berish",
        orderText: "Buyurtma berish — Telegram orqali",
        priceNote: "* Narxlar o'zgarishi mumkin",
        footerCopy: "© 2026 Shirin Kafe. Barcha huquqlar himoyalangan.",
        categories: {
            salads: "Salatlar",
            soups: "Sho'rvalar",
            main: "Taomlar",
            kebab: "Shashliklar",
            extras: "Qo'shimcha",
            drinks: "Ichimliklar"
        },
        catIcons: {
            salads: "🥗", soups: "🍜", main: "🥘", kebab: "🍢", extras: "🫓", drinks: "🥤"
        }
    },
    krill: {
        searchPlaceholder: "Таом қидириш...",
        allCategories: "Барчаси",
        noResults: "Ҳеч нарса топилмади",
        noResultsHint: "Бошқа сўз билан қидириб кўринг",
        orderBtn: "Буюртма бериш",
        orderText: "Буюртма бериш — Telegram орқали",
        priceNote: "* Нархлар ўзгариши мумкин",
        footerCopy: "© 2026 Ширин Кафе. Барча ҳуқуқлар ҳимояланган.",
        categories: {
            salads: "Салатлар",
            soups: "Шўрвалар",
            main: "Таомлар",
            kebab: "Шашликлар",
            extras: "Қўшимча",
            drinks: "Ичимликлар"
        },
        catIcons: {
            salads: "🥗", soups: "🍜", main: "🥘", kebab: "🍢", extras: "🫓", drinks: "🥤"
        }
    },
    ru: {
        searchPlaceholder: "Поиск блюд...",
        allCategories: "Все",
        noResults: "Ничего не найдено",
        noResultsHint: "Попробуйте другое слово",
        orderBtn: "Заказать",
        orderText: "Заказать — через Telegram",
        priceNote: "* Цены могут измениться",
        footerCopy: "© 2026 Shirin Кафе. Все права защищены.",
        categories: {
            salads: "Салаты",
            soups: "Супы",
            main: "Блюда",
            kebab: "Шашлыки",
            extras: "Дополнительно",
            drinks: "Напитки"
        },
        catIcons: {
            salads: "🥗", soups: "🍜", main: "🥘", kebab: "🍢", extras: "🫓", drinks: "🥤"
        }
    }
};

const MENU_DATA = [
    // ===== SALATLAR =====
    {
        id: 1, category: "salads", emoji: "🥗", image: "images/menu/1.jpg", price: 15000, weight: "250g", time: "tayyor", calories: "280 kkal",
        name: { uz: "Olivye", krill: "Оливье", ru: "Оливье" },
        desc: { uz: "Kartoshka, sabzi, kolbasa, no'xat, mayonez", krill: "Картошка, сабзи, колбаса, нўхат, майонез", ru: "Картофель, морковь, колбаса, горошек, майонез" }
    },
    {
        id: 2, category: "salads", emoji: "🥗", image: "images/menu/2.jpg", price: 22000, weight: "280g", time: "10 min", calories: "320 kkal", badge: "hit",
        name: { uz: "Sezar", krill: "Сезар", ru: "Цезарь" },
        desc: { uz: "Tovuq filesi, salat bargi, krutonlar, parmessan sousi", krill: "Товуқ филеси, салат барги, крутонлар, пармессан соуси", ru: "Куриное филе, салат, крутоны, соус пармезан" }
    },
    {
        id: 3, category: "salads", emoji: "🥒", image: "images/menu/3.jpg", price: 12000, weight: "220g", time: "tayyor", calories: "180 kkal",
        name: { uz: "Shopskiy", krill: "Шопский", ru: "Шопский" },
        desc: { uz: "Pomidor, bodring, bolgar qalampiri, piyoz, brynza", krill: "Помидор, бодринг, болгар қалампири, пиёз, брынза", ru: "Помидоры, огурцы, перец, лук, брынза" }
    },
    {
        id: 4, category: "salads", emoji: "🌿", image: "images/menu/4.jpg", price: 15000, weight: "230g", time: "tayyor", calories: "120 kkal",
        name: { uz: "Bahor salati", krill: "Баҳор салати", ru: "Весенний салат" },
        desc: { uz: "Yangi pomidor, bodring, ko'katlar, zaytun moyi", krill: "Янги помидор, бодринг, кўкатлар, зайтун мойи", ru: "Свежие помидоры, огурцы, зелень, оливковое масло" }
    },
    {
        id: 5, category: "salads", emoji: "🥕", image: "images/menu/5.jpg", price: 10000, weight: "200g", time: "tayyor", calories: "240 kkal",
        name: { uz: "Koreyscha salat", krill: "Корейсча салат", ru: "Корейский салат" },
        desc: { uz: "Koreyscha uslubda go'shtli salat, ziravorlar bilan", krill: "Корейсча услубда гўштли салат, зираворлар билан", ru: "Мясной салат по-корейски со специями" }
    },
    {
        id: 6, category: "salads", emoji: "🫒", image: "images/menu/6.jpg", price: 20000, weight: "260g", time: "tayyor", calories: "210 kkal",
        name: { uz: "Grecheskiy", krill: "Гречeский", ru: "Греческий" },
        desc: { uz: "Pomidor, bodring, zaytun, feta pishloq, zaytun moyi", krill: "Помидор, бодринг, зайтун, фета пишлоқ, зайтун мойи", ru: "Помидоры, огурцы, оливки, фета, оливковое масло" }
    },
    {
        id: 7, category: "salads", emoji: "🥩", image: "images/menu/7.jpg", price: 40000, weight: "300g", time: "tayyor", calories: "380 kkal", badge: "hit",
        name: { uz: "Go'sht salat", krill: "Гўшт салат", ru: "Мясной салат" },
        desc: { uz: "Mol go'shti, kartoshka, tuxum, piyoz, mayonez", krill: "Мол гўшти, картошка, тухум, пиёз, майонез", ru: "Говядина, картофель, яйцо, лук, майонез" }
    },
    {
        id: 8, category: "salads", emoji: "🍖", image: "images/menu/8.jpg", price: 35000, weight: "280g", time: "tayyor", calories: "350 kkal",
        name: { uz: "Tili salat", krill: "Тили салат", ru: "Салат из языка" },
        desc: { uz: "Mol tili, tuxum, kartoshka, piyoz, mayonez", krill: "Мол тили, тухум, картошка, пиёз, майонез", ru: "Говяжий язык, яйцо, картофель, лук, майонез" }
    },
    {
        id: 9, category: "salads", emoji: "🐟", image: "images/menu/9.jpg", price: 22000, weight: "260g", time: "tayyor", calories: "310 kkal",
        name: { uz: "Mimoza", krill: "Мимоза", ru: "Мимоза" },
        desc: { uz: "Konservalangan baliq, tuxum, kartoshka, sabzi, mayonez", krill: "Консервалangan балиқ, тухум, картошка, сабзи, майонез", ru: "Консервированная рыба, яйцо, картофель, морковь" }
    },
    {
        id: 10, category: "salads", emoji: "🍅", image: "images/menu/10.jpg", price: 6000, weight: "200g", time: "tayyor", calories: "60 kkal",
        name: { uz: "Achichuk", krill: "Ачичуқ", ru: "Ачичук" },
        desc: { uz: "Pomidor, piyoz, ko'katlar — milliy salat", krill: "Помидор, пиёз, кўкатлар — миллий салат", ru: "Помидоры, лук, зелень — национальный салат" }
    },
    {
        id: 11, category: "salads", emoji: "🥬", image: "images/menu/11.jpg", price: 8000, weight: "220g", time: "tayyor", calories: "170 kkal",
        name: { uz: "Vinegret", krill: "Винегрет", ru: "Винегрет" },
        desc: { uz: "Lavlagi, kartoshka, sabzi, bodring, no'xat", krill: "Лавлаги, картошка, сабзи, бодринг, нўхат", ru: "Свёкла, картофель, морковь, огурец, горошек" }
    },
    {
        id: 12, category: "salads", emoji: "🥕", image: "images/menu/12.jpg", price: 15000, weight: "200g", time: "tayyor", calories: "130 kkal",
        name: { uz: "Markovcha", krill: "Марковча", ru: "Морковь по-корейски" },
        desc: { uz: "Koreyscha sabzi salati, ziravorlar va sarimsoq", krill: "Корейсча сабзи салати, зираворлар ва саримсоқ", ru: "Морковь по-корейски с чесноком и специями" }
    },
    {
        id: 13, category: "salads", emoji: "🟣", image: "images/menu/13.jpg", price: 15000, weight: "200g", time: "tayyor", calories: "150 kkal",
        name: { uz: "Svekla salati", krill: "Свекла салати", ru: "Свекольный салат" },
        desc: { uz: "Lavlagi salati, yong'oq va sarimsoq bilan", krill: "Лавлаги салати, ёнғоқ ва саримсоқ билан", ru: "Салат из свёклы с орехами и чесноком" }
    },

    // ===== SHO'RVALAR =====
    {
        id: 14, category: "soups", emoji: "🍗", image: "images/menu/14.jpg", price: 32000, weight: "400ml", time: "20 min", calories: "250 kkal", badge: "hit",
        name: { uz: "Tovuq sho'rva", krill: "Товуқ шўрва", ru: "Куриный суп" },
        desc: { uz: "Tovuq go'shti, kartoshka, sabzi, ko'katlar", krill: "Товуқ гўшти, картошка, сабзи, кўкатлар", ru: "Куриное мясо, картофель, морковь, зелень" }
    },
    {
        id: 15, category: "soups", emoji: "🫘", image: "images/menu/15.jpg", price: 32000, weight: "400ml", time: "25 min", calories: "310 kkal",
        name: { uz: "No'xat sho'rva", krill: "Нўхат шўрва", ru: "Гороховый суп" },
        desc: { uz: "No'xat, go'sht, kartoshka, sabzavotlar", krill: "Нўхат, гўшт, картошка, сабзавотлар", ru: "Горох, мясо, картофель, овощи" }
    },
    {
        id: 16, category: "soups", emoji: "🍲", image: "images/menu/16.jpg", price: 32000, weight: "400ml", time: "25 min", calories: "290 kkal", badge: "hit",
        name: { uz: "Mastava", krill: "Мастава", ru: "Мастава" },
        desc: { uz: "Guruch, go'sht, sabzavotlar, qatiq bilan", krill: "Гуруч, гўшт, сабзавотлар, қатиқ билан", ru: "Рис, мясо, овощи, подаётся с кислым молоком" }
    },
    {
        id: 17, category: "soups", emoji: "🥣", image: "images/menu/17.jpg", price: 32000, weight: "450ml", time: "30 min", calories: "380 kkal", badge: "hit",
        name: { uz: "Shurpa", krill: "Шўрпа", ru: "Шурпа" },
        desc: { uz: "Qo'y go'shti, kartoshka, sabzi, piyoz, ko'katlar", krill: "Қўй гўшти, картошка, сабзи, пиёз, кўкатлар", ru: "Баранина, картофель, морковь, лук, зелень" }
    },

    // ===== ASOSIY TAOMLAR =====
    {
        id: 18, category: "main", emoji: "🍚", image: "images/menu/18.jpg", price: 32000, weight: "450g", time: "tayyor", calories: "580 kkal", badge: "hit",
        name: { uz: "Osh (Palov)", krill: "Ош (Палов)", ru: "Плов" },
        desc: { uz: "An'anaviy o'zbek oshi: guruch, go'sht, sabzi, ziravorlar", krill: "Анъанавий ўзбек оши: гуруч, гўшт, сабзи, зираворлар", ru: "Традиционный узбекский плов: рис, мясо, морковь" }
    },
    {
        id: 19, category: "main", emoji: "🥘", image: "images/menu/19.jpg", price: 35000, weight: "300g", time: "25 min", calories: "480 kkal", badge: "hit",
        name: { uz: "Qozon kabob", krill: "Қозон кабоб", ru: "Казан-кабоб" },
        desc: { uz: "Qozonda tayyorlangan go'sht, kartoshka bilan (300g)", krill: "Қозонда тайёрланган гўшт, картошка билан", ru: "Мясо в казане с картофелем (300г)" }
    },
    {
        id: 20, category: "main", emoji: "🍝", image: "images/menu/20.jpg", price: 32000, weight: "400g", time: "20 min", calories: "450 kkal",
        name: { uz: "Lag'mon (qovurilgan)", krill: "Лағмон (қовурилган)", ru: "Лагман (жареный)" },
        desc: { uz: "Qo'lda tayyorlangan qovurilgan lag'mon, go'sht va sabzavotlar", krill: "Қўлда тайёрланган қовурилган лағмон, гўшт ва сабзавотлар", ru: "Жареная лапша ручной работы с мясом и овощами" }
    },
    {
        id: 21, category: "main", emoji: "🍜", image: "images/menu/21.jpg", price: 32000, weight: "450g", time: "20 min", calories: "420 kkal",
        name: { uz: "Lag'mon (suyuq)", krill: "Лағмон (суюқ)", ru: "Лагман (суповой)" },
        desc: { uz: "Qo'lda tayyorlangan suyuq lag'mon, sho'rvali", krill: "Қўлда тайёрланган суюқ лағмон, шўрвали", ru: "Суповая лапша ручной работы с бульоном" }
    },
    {
        id: 22, category: "main", emoji: "🥟", image: "images/menu/22.jpg", price: 32000, weight: "350g", time: "25 min", calories: "380 kkal",
        name: { uz: "Chuchvara", krill: "Чучвара", ru: "Чучвара" },
        desc: { uz: "Qo'lda tayyorlangan chuchvara, sho'rvada, qatiq bilan", krill: "Қўлда тайёрланган чучвара, шўрвада, қатиқ билан", ru: "Пельмени ручной работы в бульоне с кислым молоком" }
    },
    {
        id: 23, category: "main", emoji: "🌯", image: "images/menu/23.jpg", price: 35000, weight: "350g", time: "15 min", calories: "420 kkal",
        name: { uz: "Tortilla", krill: "Тортилла", ru: "Тортилья" },
        desc: { uz: "Lavashga o'ralgan go'sht va sabzavotlar, sous bilan", krill: "Лавашга ўралган гўшт ва сабзавотлар, соус билан", ru: "Мясо и овощи в лаваше с соусом" }
    },
    {
        id: 24, category: "main", emoji: "🫕", image: "images/menu/24.jpg", price: 30000, weight: "400g", time: "25 min", calories: "460 kkal",
        name: { uz: "Dimlama", krill: "Димлама", ru: "Димлама" },
        desc: { uz: "Go'sht, kartoshka, sabzi, piyoz — dimlab pishirilgan", krill: "Гўшт, картошка, сабзи, пиёз — димлаб пиширилган", ru: "Тушёное мясо с картофелем, морковью, луком" }
    },
    {
        id: 25, category: "main", emoji: "🍲", image: "images/menu/25.jpg", price: 30000, weight: "380g", time: "20 min", calories: "400 kkal",
        name: { uz: "Kuritov", krill: "Куритов", ru: "Куритов" },
        desc: { uz: "Qo'lda yoyilgan xamir, go'sht va qatiq bilan", krill: "Қўлда ёйилган хамир, гўшт ва қатиқ билан", ru: "Тесто ручной раскатки с мясом и кислым молоком" }
    },
    {
        id: 26, category: "main", emoji: "🍗", image: "images/menu/26.jpg", price: 32000, weight: "350g", time: "20 min", calories: "380 kkal",
        name: { uz: "Jo'jali taom", krill: "Жўжали таом", ru: "Блюдо с цыплёнком" },
        desc: { uz: "Tovuq go'shti bilan tayyorlangan maxsus taom", krill: "Товуқ гўшти билан тайёрланган махсус таом", ru: "Особое блюдо с куриным мясом" }
    },
    {
        id: 27, category: "main", emoji: "🫓", image: "images/menu/27.jpg", price: 32000, weight: "350g", time: "20 min", calories: "410 kkal",
        name: { uz: "Chalpak", krill: "Чалпак", ru: "Чалпак" },
        desc: { uz: "An'anaviy chalpak, go'sht va sabzavotlar bilan", krill: "Анъанавий чалпак, гўшт ва сабзавотлар билан", ru: "Традиционный чалпак с мясом и овощами" }
    },
    {
        id: 28, category: "main", emoji: "🥩", image: "images/menu/28.jpg", price: 18000, weight: "200g", time: "tayyor", calories: "280 kkal",
        name: { uz: "Rulet (go'shtli)", krill: "Рулет (гўштли)", ru: "Рулет мясной" },
        desc: { uz: "Go'shtli rulet, tuxum va ziravorlar bilan", krill: "Гўштли рулет, тухум ва зираворлар билан", ru: "Мясной рулет с яйцом и специями" }
    },
    {
        id: 29, category: "main", emoji: "🍗", image: "images/menu/29.jpg", price: 35000, weight: "350g", time: "20 min", calories: "400 kkal",
        name: { uz: "Tovuq go'shtli taom", krill: "Товуқ гўштли таом", ru: "Блюдо из курицы" },
        desc: { uz: "Qovurilgan tovuq go'shti, yon taom bilan", krill: "Қовурилган товуқ гўшти, ён таом билан", ru: "Жареная курица с гарниром" }
    },
    {
        id: 30, category: "main", emoji: "🍜", image: "images/menu/30.jpg", price: 32000, weight: "400g", time: "20 min", calories: "370 kkal",
        name: { uz: "Ugra oshi", krill: "Угра оши", ru: "Угра" },
        desc: { uz: "Qo'lda qirqilgan ugra, go'sht sho'rvada, qatiq bilan", krill: "Қўлда қирқилган угра, гўшт шўрвада, қатиқ билан", ru: "Домашняя лапша в мясном бульоне с кислым молоком" }
    },
    {
        id: 31, category: "main", emoji: "🥟", image: "images/menu/31.jpg", price: 30000, weight: "350g", time: "20 min", calories: "320 kkal",
        name: { uz: "Tuxum barak", krill: "Тухум барак", ru: "Тухум-барак" },
        desc: { uz: "Tuxumli barak, qatiq va ko'katlar bilan", krill: "Тухумли барак, қатиқ ва кўкатлар билан", ru: "Вареники с яйцом, подаётся с кислым молоком" }
    },

    // ===== SHASHLIKLAR =====
    {
        id: 32, category: "kebab", emoji: "🍢", image: "images/menu/32.jpg", price: 210000, weight: "1 kg", time: "30 min", calories: "650 kkal", badge: "hit",
        name: { uz: "Qo'y shashlik (1 kg)", krill: "Қўй шашлик (1 кг)", ru: "Шашлык бараний (1 кг)" },
        desc: { uz: "Tuzlangan qo'y go'shti, ko'mirda pishirilgan, piyoz va lavash", krill: "Тузланган қўй гўшти, кўмирда пиширилган, пиёз ва лаваш", ru: "Маринованная баранина на углях, лук и лаваш" }
    },
    {
        id: 33, category: "kebab", emoji: "🥙", image: "images/menu/33.jpg", price: 25000, weight: "150g", time: "20 min", calories: "320 kkal",
        name: { uz: "Kabob (1 dona)", krill: "Кабоб (1 дона)", ru: "Кабоб (1 шт)" },
        desc: { uz: "Ko'mirda pishirilgan go'sht kabobi, piyoz va lavash", krill: "Кўмирда пиширилган гўшт кабоби, пиёз ва лаваш", ru: "Мясной кабоб на углях с луком и лавашом" }
    },
    {
        id: 34, category: "kebab", emoji: "🔥", image: "images/menu/34.jpg", price: 25000, weight: "150g", time: "18 min", calories: "280 kkal",
        name: { uz: "Jigar kabob", krill: "Жигар кабоб", ru: "Кабоб из печени" },
        desc: { uz: "Yangi jigar, ko'mirda pishirilgan, piyoz va lavash", krill: "Янги жигар, кўмирда пиширилган, пиёз ва лаваш", ru: "Свежая печень на углях с луком и лавашом" }
    },
    {
        id: 35, category: "kebab", emoji: "🍗", image: "images/menu/35.jpg", price: 25000, weight: "200g", time: "18 min", calories: "260 kkal",
        name: { uz: "Tovuq kabob", krill: "Товуқ кабоб", ru: "Куриный кабоб" },
        desc: { uz: "Marinadlangan tovuq filesi, ko'mirda pishirilgan", krill: "Маринадланган товуқ филеси, кўмирда пиширилган", ru: "Маринованное куриное филе на углях" }
    },
    {
        id: 36, category: "kebab", emoji: "🥙", image: "images/menu/36.jpg", price: 25000, weight: "150g", time: "18 min", calories: "340 kkal",
        name: { uz: "Lyulya kabob", krill: "Люля кабоб", ru: "Люля-кабоб" },
        desc: { uz: "Qiyma kabob, ko'mirda pishirilgan, lavash va piyoz", krill: "Қийма кабоб, кўмирда пиширилган, лаваш ва пиёз", ru: "Кабоб из фарша на углях с лавашом и луком" }
    },

    // ===== QO'SHIMCHA =====
    {
        id: 37, category: "extras", emoji: "🫓", image: "images/menu/37.jpg", price: 8000, weight: "180g", time: "tayyor", calories: "320 kkal", badge: "hit",
        name: { uz: "Somsa (1 dona)", krill: "Сомса (1 дона)", ru: "Самса (1 шт)" },
        desc: { uz: "Tandir somsasi, go'sht va piyozli, issiq holda", krill: "Тандир сомсаси, гўшт ва пиёзли, иссиқ ҳолда", ru: "Тандырная самса с мясом и луком, горячая" }
    },
    {
        id: 38, category: "extras", emoji: "🍞", image: "images/menu/38.jpg", price: 5000, weight: "250g", time: "tayyor", calories: "280 kkal",
        name: { uz: "Non", krill: "Нон", ru: "Лепёшка" },
        desc: { uz: "Tandirda pishirilgan issiq non", krill: "Тандирда пиширилган иссиқ нон", ru: "Горячая лепёшка из тандыра" }
    },
    {
        id: 39, category: "extras", emoji: "🥩", image: "images/menu/39.jpg", price: 40000, weight: "200g", time: "tayyor", calories: "420 kkal", badge: "hit",
        name: { uz: "Qazi", krill: "Қази", ru: "Казы" },
        desc: { uz: "An'anaviy ot go'shtidan tayyorlangan qazi", krill: "Анъанавий от гўштидан тайёрланган қази", ru: "Традиционная колбаса из конины" }
    },
    {
        id: 40, category: "extras", emoji: "🍳", image: "images/menu/40.jpg", price: 5000, weight: "120g", time: "5 min", calories: "180 kkal",
        name: { uz: "Tuxum", krill: "Тухум", ru: "Яичница" },
        desc: { uz: "Qovurilgan tuxum, ko'katlar bilan", krill: "Қовурилган тухум, кўкатлар билан", ru: "Жареное яйцо с зеленью" }
    },
    {
        id: 41, category: "extras", emoji: "🍋", image: "images/menu/41.jpg", price: 7000, weight: "100g", time: "tayyor", calories: "20 kkal",
        name: { uz: "Limon", krill: "Лимон", ru: "Лимон" },
        desc: { uz: "Yangi limon, tilimlab tortiladi", krill: "Янги лимон, тилимлаб тортилади", ru: "Свежий лимон, нарезанный дольками" }
    },
    {
        id: 42, category: "extras", emoji: "🥛", image: "images/menu/42.jpg", price: 6000, weight: "200ml", time: "tayyor", calories: "80 kkal",
        name: { uz: "Qatiq", krill: "Қатиқ", ru: "Кислое молоко" },
        desc: { uz: "Uy qatiqi, taomlar uchun", krill: "Уй қатиғи, таомлар учун", ru: "Домашнее кислое молоко" }
    },

    // ===== ICHIMLIKLAR =====
    {
        id: 43, category: "drinks", emoji: "🍵", image: "images/menu/43.jpg", price: 10000, weight: "1000ml", time: "10 min", calories: "5 kkal", badge: "hit",
        name: { uz: "Choy (choynek)", krill: "Чой (чойнек)", ru: "Чай (чайник)" },
        desc: { uz: "Ko'k yoki qora choy, 1 litrli choynek", krill: "Кўк ёки қора чой, 1 литрли чойнек", ru: "Зелёный или чёрный чай, чайник 1 литр" }
    },
    {
        id: 44, category: "drinks", emoji: "🍋", image: "images/menu/44.jpg", price: 10000, weight: "250ml", time: "5 min", calories: "30 kkal",
        name: { uz: "Limonli choy", krill: "Лимонли чой", ru: "Чай с лимоном" },
        desc: { uz: "Issiq choy, limon bo'laklari bilan", krill: "Иссиқ чой, лимон бўлаклари билан", ru: "Горячий чай с дольками лимона" }
    },
    {
        id: 45, category: "drinks", emoji: "🥤", image: "images/menu/45.jpg", price: 8000, weight: "300ml", time: "tayyor", calories: "60 kkal",
        name: { uz: "Kompot", krill: "Компот", ru: "Компот" },
        desc: { uz: "Uy kompoti, mevalardan tayyorlangan", krill: "Уй компоти, мевалардан тайёрланган", ru: "Домашний компот из фруктов" }
    },
    {
        id: 46, category: "drinks", emoji: "💧", image: "images/menu/46.jpg", price: 5000, weight: "500ml", time: "tayyor", calories: "0 kkal",
        name: { uz: "Mineral suv", krill: "Минерал сув", ru: "Минеральная вода" },
        desc: { uz: "Gazli yoki gazsiz suv, 0.5 litr", krill: "Газли ёки газсиз сув, 0.5 литр", ru: "Газированная или без газа, 0.5 литра" }
    },
    {
        id: 47, category: "drinks", emoji: "🥤", image: "images/menu/47.jpg", price: 10000, weight: "500ml", time: "tayyor", calories: "210 kkal",
        name: { uz: "Coca-Cola / Fanta / Sprite", krill: "Coca-Cola / Fanta / Sprite", ru: "Coca-Cola / Fanta / Sprite" },
        desc: { uz: "Gazlangan ichimlik, 0.5 litr", krill: "Газланган ичимлик, 0.5 литр", ru: "Газированный напиток, 0.5 литра" }
    },
    {
        id: 48, category: "drinks", emoji: "☕", image: "images/menu/48.jpg", price: 10000, weight: "200ml", time: "5 min", calories: "10 kkal",
        name: { uz: "Qahva", krill: "Қаҳва", ru: "Кофе" },
        desc: { uz: "Issiq qora qahva", krill: "Иссиқ қора қаҳва", ru: "Горячий чёрный кофе" }
    }
];
