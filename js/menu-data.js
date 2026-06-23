const MENU_DATA = {
    categories: [
        { id: "salads", name: "Salatlar", icon: "🥗" },
        { id: "soups", name: "Sho'rvalar", icon: "🍜" },
        { id: "main", name: "Taomlar", icon: "🥘" },
        { id: "kebab", name: "Shashliklar", icon: "🍢" },
        { id: "extras", name: "Qo'shimcha", icon: "🫓" },
        { id: "drinks", name: "Ichimliklar", icon: "🥤" }
    ],

    items: [
        // ===== SALATLAR =====
        {
            id: 1,
            category: "salads",
            name: "Olivye",
            desc: "An'anaviy olivye salati: kartoshka, sabzi, kolbasa, no'xat, mayonez",
            price: 15000,
            weight: "250g",
            time: "tayyor",
            calories: "280 kkal",
            emoji: "🥗"
        },
        {
            id: 2,
            category: "salads",
            name: "Sezar",
            desc: "Tovuq filesi, salat bargi, krutonlar, parmessan, sezar sousi",
            price: 22000,
            weight: "280g",
            time: "10 min",
            calories: "320 kkal",
            emoji: "🥗",
            badge: "hit"
        },
        {
            id: 3,
            category: "salads",
            name: "Shopskiy",
            desc: "Pomidor, bodring, bolgar qalampiri, piyoz, brynza pishloq",
            price: 12000,
            weight: "220g",
            time: "tayyor",
            calories: "180 kkal",
            emoji: "🥒"
        },
        {
            id: 4,
            category: "salads",
            name: "Bahor salati",
            desc: "Yangi sabzavotlar: pomidor, bodring, ko'katlar, zaytun moyi",
            price: 15000,
            weight: "230g",
            time: "tayyor",
            calories: "120 kkal",
            emoji: "🌿"
        },
        {
            id: 5,
            category: "salads",
            name: "Koreyscha salat",
            desc: "Koreyscha uslubda tayyorlangan go'shtli salat, ziravorlar bilan",
            price: 10000,
            weight: "200g",
            time: "tayyor",
            calories: "240 kkal",
            emoji: "🥕"
        },
        {
            id: 6,
            category: "salads",
            name: "Grecheskiy",
            desc: "Pomidor, bodring, zaytun, feta pishloq, bolgar qalampiri, zaytun moyi",
            price: 20000,
            weight: "260g",
            time: "tayyor",
            calories: "210 kkal",
            emoji: "🫒"
        },
        {
            id: 7,
            category: "salads",
            name: "Go'sht salat",
            desc: "Qaynatilgan mol go'shti, kartoshka, tuxum, piyoz, mayonez",
            price: 40000,
            weight: "300g",
            time: "tayyor",
            calories: "380 kkal",
            emoji: "🥩",
            badge: "hit"
        },
        {
            id: 8,
            category: "salads",
            name: "Tili salat",
            desc: "Mol tili, tuxum, kartoshka, piyoz, mayonez bilan",
            price: 35000,
            weight: "280g",
            time: "tayyor",
            calories: "350 kkal",
            emoji: "🍖"
        },
        {
            id: 9,
            category: "salads",
            name: "Mimoza",
            desc: "Konservalangan baliq, tuxum, kartoshka, sabzi, mayonez qatlamli",
            price: 22000,
            weight: "260g",
            time: "tayyor",
            calories: "310 kkal",
            emoji: "🐟"
        },
        {
            id: 10,
            category: "salads",
            name: "Achichuk",
            desc: "Pomidor, piyoz, ko'katlar, qalampir — milliy salat",
            price: 6000,
            weight: "200g",
            time: "tayyor",
            calories: "60 kkal",
            emoji: "🍅"
        },
        {
            id: 11,
            category: "salads",
            name: "Vinegret",
            desc: "Lavlagi, kartoshka, sabzi, bodring, no'xat, o'simlik moyi",
            price: 8000,
            weight: "220g",
            time: "tayyor",
            calories: "170 kkal",
            emoji: "🥬"
        },
        {
            id: 12,
            category: "salads",
            name: "Markovcha",
            desc: "Koreyscha sabzi salati, ziravorlar va sarimsoq bilan",
            price: 15000,
            weight: "200g",
            time: "tayyor",
            calories: "130 kkal",
            emoji: "🥕"
        },
        {
            id: 13,
            category: "salads",
            name: "Svekla salati",
            desc: "Lavlagi salati, yong'oq va sarimsoq bilan",
            price: 15000,
            weight: "200g",
            time: "tayyor",
            calories: "150 kkal",
            emoji: "🟣"
        },

        // ===== SHO'RVALAR (Birinchi taom) =====
        {
            id: 14,
            category: "soups",
            name: "Tovuq sho'rva",
            desc: "Tovuq go'shti, kartoshka, sabzi, ko'katlar bilan tayyorlangan sho'rva",
            price: 32000,
            weight: "400ml",
            time: "20 min",
            calories: "250 kkal",
            emoji: "🍗",
            badge: "hit"
        },
        {
            id: 15,
            category: "soups",
            name: "No'xat sho'rva",
            desc: "No'xat, go'sht, kartoshka, sabzavotlar bilan sho'rva",
            price: 32000,
            weight: "400ml",
            time: "25 min",
            calories: "310 kkal",
            emoji: "🫘"
        },
        {
            id: 16,
            category: "soups",
            name: "Mastava",
            desc: "Guruch, go'sht, sabzavotlar, qatiq bilan tortiladi",
            price: 32000,
            weight: "400ml",
            time: "25 min",
            calories: "290 kkal",
            emoji: "🍲",
            badge: "hit"
        },
        {
            id: 17,
            category: "soups",
            name: "Shurpa",
            desc: "Qo'y go'shti, kartoshka, sabzi, piyoz, ko'katlar bilan",
            price: 32000,
            weight: "450ml",
            time: "30 min",
            calories: "380 kkal",
            emoji: "🥣",
            badge: "hit"
        },

        // ===== IKKINCHI TAOM (Asosiy taomlar) =====
        {
            id: 18,
            category: "main",
            name: "Osh (Palov)",
            desc: "An'anaviy o'zbek oshi: guruch, go'sht, sabzi, piyoz, ziravorlar",
            price: 32000,
            weight: "450g",
            time: "tayyor",
            calories: "580 kkal",
            emoji: "🍚",
            badge: "hit"
        },
        {
            id: 19,
            category: "main",
            name: "Qozon kabob",
            desc: "Qozonda tayyorlangan go'sht, kartoshka bilan (300g)",
            price: 35000,
            weight: "300g",
            time: "25 min",
            calories: "480 kkal",
            emoji: "🥘",
            badge: "hit"
        },
        {
            id: 20,
            category: "main",
            name: "Lag'mon (qovurilgan)",
            desc: "Qo'lda tayyorlangan qovurilgan lag'mon, go'sht va sabzavotlar",
            price: 32000,
            weight: "400g",
            time: "20 min",
            calories: "450 kkal",
            emoji: "🍝"
        },
        {
            id: 21,
            category: "main",
            name: "Lag'mon (suyuq)",
            desc: "Qo'lda tayyorlangan suyuq lag'mon, sho'rvali, go'sht bilan",
            price: 32000,
            weight: "450g",
            time: "20 min",
            calories: "420 kkal",
            emoji: "🍜"
        },
        {
            id: 22,
            category: "main",
            name: "Chuchvara",
            desc: "Qo'lda tayyorlangan chuchvara, sho'rvada, qatiq bilan",
            price: 32000,
            weight: "350g",
            time: "25 min",
            calories: "380 kkal",
            emoji: "🥟"
        },
        {
            id: 23,
            category: "main",
            name: "Tortilla",
            desc: "Lavashga o'ralgan go'sht va sabzavotlar, maxsus sous bilan",
            price: 35000,
            weight: "350g",
            time: "15 min",
            calories: "420 kkal",
            emoji: "🌯"
        },
        {
            id: 24,
            category: "main",
            name: "Dimlama",
            desc: "Go'sht, kartoshka, sabzi, piyoz, barchasi dimlab pishirilgan",
            price: 30000,
            weight: "400g",
            time: "25 min",
            calories: "460 kkal",
            emoji: "🫕"
        },
        {
            id: 25,
            category: "main",
            name: "Kuritov",
            desc: "Qo'lda yoyilgan xamir, go'sht va qatiq bilan tortiladi",
            price: 30000,
            weight: "380g",
            time: "20 min",
            calories: "400 kkal",
            emoji: "🍲"
        },
        {
            id: 26,
            category: "main",
            name: "Jo'jali taom",
            desc: "Tovuq go'shti bilan tayyorlangan maxsus taom, yon taom bilan",
            price: 32000,
            weight: "350g",
            time: "20 min",
            calories: "380 kkal",
            emoji: "🍗"
        },
        {
            id: 27,
            category: "main",
            name: "Chalpak",
            desc: "An'anaviy o'zbek chalpagi, go'sht va sabzavotlar bilan",
            price: 32000,
            weight: "350g",
            time: "20 min",
            calories: "410 kkal",
            emoji: "🫓"
        },
        {
            id: 28,
            category: "main",
            name: "Rulet (go'shtli)",
            desc: "Go'shtli rulet, tuxum va ziravorlar bilan",
            price: 18000,
            weight: "200g",
            time: "tayyor",
            calories: "280 kkal",
            emoji: "🥩"
        },
        {
            id: 29,
            category: "main",
            name: "Tovuq go'shtli taom",
            desc: "Qovurilgan tovuq go'shti, yon taom bilan tortiladi",
            price: 35000,
            weight: "350g",
            time: "20 min",
            calories: "400 kkal",
            emoji: "🍗"
        },
        {
            id: 30,
            category: "main",
            name: "Ugra oshi",
            desc: "Qo'lda qirqilgan ugra, go'sht sho'rvada, qatiq bilan",
            price: 32000,
            weight: "400g",
            time: "20 min",
            calories: "370 kkal",
            emoji: "🍜"
        },
        {
            id: 31,
            category: "main",
            name: "Tuxum barak",
            desc: "Tuxumli barak, qatiq va ko'katlar bilan tortiladi",
            price: 30000,
            weight: "350g",
            time: "20 min",
            calories: "320 kkal",
            emoji: "🥟"
        },

        // ===== SHASHLIKLAR =====
        {
            id: 32,
            category: "kebab",
            name: "Qo'y shashlik",
            desc: "Tuzlangan qo'y go'shti, ko'mirda pishirilgan, piyoz va lavash bilan",
            price: 210000,
            weight: "1 kg",
            time: "30 min",
            calories: "650 kkal",
            emoji: "🍢",
            badge: "hit"
        },
        {
            id: 33,
            category: "kebab",
            name: "Kabob (1 dona)",
            desc: "Ko'mirda pishirilgan go'sht kabobi, piyoz va lavash bilan",
            price: 25000,
            weight: "150g",
            time: "20 min",
            calories: "320 kkal",
            emoji: "🥙"
        },
        {
            id: 34,
            category: "kebab",
            name: "Jigar kabob",
            desc: "Yangi jigar, ko'mirda pishirilgan, piyoz va lavash bilan",
            price: 25000,
            weight: "150g",
            time: "18 min",
            calories: "280 kkal",
            emoji: "🔥"
        },
        {
            id: 35,
            category: "kebab",
            name: "Tovuq kabob",
            desc: "Marinadlangan tovuq filesi, ko'mirda pishirilgan",
            price: 25000,
            weight: "200g",
            time: "18 min",
            calories: "260 kkal",
            emoji: "🍗"
        },
        {
            id: 36,
            category: "kebab",
            name: "Lyulya kabob",
            desc: "Qiyma kabob, ko'mirda pishirilgan, lavash va piyoz bilan",
            price: 25000,
            weight: "150g",
            time: "18 min",
            calories: "340 kkal",
            emoji: "🥙"
        },

        // ===== QO'SHIMCHA =====
        {
            id: 37,
            category: "extras",
            name: "Somsa (1 dona)",
            desc: "Tandir somsasi, go'sht va piyozli, issiq holda",
            price: 8000,
            weight: "180g",
            time: "tayyor",
            calories: "320 kkal",
            emoji: "🫓",
            badge: "hit"
        },
        {
            id: 38,
            category: "extras",
            name: "Non",
            desc: "Tandirda pishirilgan issiq non",
            price: 5000,
            weight: "250g",
            time: "tayyor",
            calories: "280 kkal",
            emoji: "🍞"
        },
        {
            id: 39,
            category: "extras",
            name: "Qazi",
            desc: "An'anaviy ot go'shtidan tayyorlangan qazi, tilib tortiladi",
            price: 40000,
            weight: "200g",
            time: "tayyor",
            calories: "420 kkal",
            emoji: "🥩",
            badge: "hit"
        },
        {
            id: 40,
            category: "extras",
            name: "Tuxum",
            desc: "Qovurilgan tuxum, ko'katlar bilan",
            price: 5000,
            weight: "120g",
            time: "5 min",
            calories: "180 kkal",
            emoji: "🍳"
        },
        {
            id: 41,
            category: "extras",
            name: "Limon",
            desc: "Yangi limon, tilimlab tortiladi",
            price: 7000,
            weight: "100g",
            time: "tayyor",
            calories: "20 kkal",
            emoji: "🍋"
        },
        {
            id: 42,
            category: "extras",
            name: "Qatiq",
            desc: "Uy qatiqi, taomlar uchun",
            price: 6000,
            weight: "200ml",
            time: "tayyor",
            calories: "80 kkal",
            emoji: "🥛"
        },

        // ===== ICHIMLIKLAR =====
        {
            id: 43,
            category: "drinks",
            name: "Choy (choynek)",
            desc: "Ko'k yoki qora choy, 1 litrli choynek",
            price: 10000,
            weight: "1000ml",
            time: "10 min",
            calories: "5 kkal",
            emoji: "🍵",
            badge: "hit"
        },
        {
            id: 44,
            category: "drinks",
            name: "Limonli choy",
            desc: "Issiq choy, limon bo'laklari bilan",
            price: 10000,
            weight: "250ml",
            time: "5 min",
            calories: "30 kkal",
            emoji: "🍋"
        },
        {
            id: 45,
            category: "drinks",
            name: "Kompot",
            desc: "Uy kompoti, mevalardan tayyorlangan",
            price: 8000,
            weight: "300ml",
            time: "tayyor",
            calories: "60 kkal",
            emoji: "🥤"
        },
        {
            id: 46,
            category: "drinks",
            name: "Mineral suv",
            desc: "Gazli yoki gazsiz suv, 0.5 litr",
            price: 5000,
            weight: "500ml",
            time: "tayyor",
            calories: "0 kkal",
            emoji: "💧"
        },
        {
            id: 47,
            category: "drinks",
            name: "Coca-Cola / Fanta / Sprite",
            desc: "Gazlangan ichimlik, 0.5 litr",
            price: 10000,
            weight: "500ml",
            time: "tayyor",
            calories: "210 kkal",
            emoji: "🥤"
        },
        {
            id: 48,
            category: "drinks",
            name: "Qahva",
            desc: "Issiq qora qahva",
            price: 10000,
            weight: "200ml",
            time: "5 min",
            calories: "10 kkal",
            emoji: "☕"
        }
    ]
};
