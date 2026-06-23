const MENU_DATA = {
    categories: [
        { id: "salads", name: "Salatlar", icon: "🥗" },
        { id: "soups", name: "Sho'rvalar", icon: "🍜" },
        { id: "hot", name: "Issiq taomlar", icon: "🥘" },
        { id: "kebab", name: "Kaboblar", icon: "🍢" },
        { id: "national", name: "Milliy taomlar", icon: "🫕" },
        { id: "pizza", name: "Pizza", icon: "🍕" },
        { id: "desserts", name: "Desertlar", icon: "🍰" },
        { id: "drinks", name: "Ichimliklar", icon: "🥤" },
        { id: "tea", name: "Choy & Qahva", icon: "🍵" }
    ],

    items: [
        // === SALATLAR ===
        {
            id: 1,
            category: "salads",
            name: "Sezar salat",
            desc: "Tovuq filesi, romaine salat bargi, parmessan, krutonlar, sezar sousi",
            price: 38000,
            weight: "280g",
            time: "15 min",
            calories: "320 kkal",
            emoji: "🥗",
            badge: "hit"
        },
        {
            id: 2,
            category: "salads",
            name: "Grek salati",
            desc: "Pomidor, bodring, bolgar qalampiri, zaytun, feta pishloq, zaytun moyi",
            price: 32000,
            weight: "250g",
            time: "10 min",
            calories: "240 kkal",
            emoji: "🥒"
        },
        {
            id: 3,
            category: "salads",
            name: "Toshkent salati",
            desc: "Mol go'shti, tuxum, kartoshka, sabzi, no'xat, mayonez",
            price: 35000,
            weight: "300g",
            time: "12 min",
            calories: "380 kkal",
            emoji: "🥬",
            badge: "new"
        },
        {
            id: 4,
            category: "salads",
            name: "Vitaminli salat",
            desc: "Karam, sabzi, bodring, ko'katlar, limon sousi",
            price: 22000,
            weight: "220g",
            time: "8 min",
            calories: "120 kkal",
            emoji: "🥕"
        },
        {
            id: 5,
            category: "salads",
            name: "Oasis maxsus salat",
            desc: "Krevetka, avokado, mango, mix salat, limon-zanjabil sousi",
            price: 52000,
            weight: "300g",
            time: "15 min",
            calories: "290 kkal",
            emoji: "🦐",
            badge: "new"
        },

        // === SHO'RVALAR ===
        {
            id: 6,
            category: "soups",
            name: "Mastava",
            desc: "Guruch, sabzavotlar, go'sht, qatiq bilan tortiladi",
            price: 28000,
            weight: "400ml",
            time: "20 min",
            calories: "280 kkal",
            emoji: "🍲",
            badge: "hit"
        },
        {
            id: 7,
            category: "soups",
            name: "Lag'mon sho'rva",
            desc: "Qo'lda tayyorlangan lag'mon, mol go'shti, sabzavotlar",
            price: 32000,
            weight: "450ml",
            time: "25 min",
            calories: "420 kkal",
            emoji: "🍜"
        },
        {
            id: 8,
            category: "soups",
            name: "Shurpa",
            desc: "Qo'y go'shti, kartoshka, sabzi, piyoz, ko'katlar",
            price: 35000,
            weight: "450ml",
            time: "30 min",
            calories: "380 kkal",
            emoji: "🥣",
            badge: "hit"
        },
        {
            id: 9,
            category: "soups",
            name: "Qaynatma sho'rva",
            desc: "Mol go'shti, kartoshka, pomidor, ko'katlar",
            price: 30000,
            weight: "400ml",
            time: "25 min",
            calories: "350 kkal",
            emoji: "🍵"
        },
        {
            id: 10,
            category: "soups",
            name: "Krem-sup (zamburug'li)",
            desc: "Shampinon, qaymoq, piyoz, sariyog', krutonlar",
            price: 34000,
            weight: "350ml",
            time: "20 min",
            calories: "310 kkal",
            emoji: "🍄"
        },

        // === ISSIQ TAOMLAR ===
        {
            id: 11,
            category: "hot",
            name: "Tovuq steyк",
            desc: "Grilda pishirilgan tovuq filesi, yon taom: jasmin guruch",
            price: 48000,
            weight: "350g",
            time: "25 min",
            calories: "450 kkal",
            emoji: "🍗"
        },
        {
            id: 12,
            category: "hot",
            name: "Mol go'sht steyk",
            desc: "Marmurlangan mol go'sht, grilda tayyorlangan, yon taom bilan",
            price: 89000,
            weight: "300g",
            time: "30 min",
            calories: "550 kkal",
            emoji: "🥩",
            badge: "hit"
        },
        {
            id: 13,
            category: "hot",
            name: "Baliq file",
            desc: "Olovda pishirilgan baliq filesi, limon sousi, sabzavotlar",
            price: 56000,
            weight: "280g",
            time: "25 min",
            calories: "320 kkal",
            emoji: "🐟"
        },
        {
            id: 14,
            category: "hot",
            name: "Jiz-biz",
            desc: "Qo'y go'shti, jigar, kartoshka, piyoz, ko'katlar",
            price: 52000,
            weight: "400g",
            time: "25 min",
            calories: "520 kkal",
            emoji: "🍖",
            badge: "hit"
        },
        {
            id: 15,
            category: "hot",
            name: "Do'lma",
            desc: "Uzum bargiga o'ralgan qiyma, guruch, ziravorlar, qatiq bilan",
            price: 38000,
            weight: "350g",
            time: "20 min",
            calories: "380 kkal",
            emoji: "🫔"
        },

        // === KABOBLAR ===
        {
            id: 16,
            category: "kebab",
            name: "Qo'y kabob",
            desc: "Tuzlangan qo'y go'shti, ko'mirda pishirilgan, piyoz, lavash",
            price: 42000,
            weight: "250g",
            time: "20 min",
            calories: "480 kkal",
            emoji: "🍢",
            badge: "hit"
        },
        {
            id: 17,
            category: "kebab",
            name: "Tovuq kabob",
            desc: "Marinadlangan tovuq filesi, ko'mirda pishirilgan",
            price: 32000,
            weight: "250g",
            time: "18 min",
            calories: "350 kkal",
            emoji: "🍗"
        },
        {
            id: 18,
            category: "kebab",
            name: "Lyulya kabob",
            desc: "Qiyma kabob, ko'mirda pishirilgan, lavash, piyoz",
            price: 35000,
            weight: "250g",
            time: "18 min",
            calories: "420 kkal",
            emoji: "🥙"
        },
        {
            id: 19,
            category: "kebab",
            name: "Mix grill",
            desc: "Qo'y, tovuq, lyulya kabob, grilda sabzavotlar, lavash",
            price: 78000,
            weight: "500g",
            time: "30 min",
            calories: "680 kkal",
            emoji: "🔥",
            badge: "hit"
        },
        {
            id: 20,
            category: "kebab",
            name: "Baliq kabob",
            desc: "Oq baliq filesi, ko'mirda pishirilgan, limon, ko'katlar",
            price: 48000,
            weight: "250g",
            time: "20 min",
            calories: "280 kkal",
            emoji: "🐠",
            badge: "new"
        },

        // === MILLIY TAOMLAR ===
        {
            id: 21,
            category: "national",
            name: "Osh (Palov)",
            desc: "An'anaviy o'zbek oshi: guruch, go'sht, sabzi, piyoz, ziravorlar",
            price: 35000,
            weight: "450g",
            time: "na tayyor",
            calories: "580 kkal",
            emoji: "🍚",
            badge: "hit"
        },
        {
            id: 22,
            category: "national",
            name: "Lag'mon",
            desc: "Qo'lda cho'zilgan lag'mon, go'sht, sabzavotlar, maxsus sous",
            price: 34000,
            weight: "400g",
            time: "25 min",
            calories: "450 kkal",
            emoji: "🍝"
        },
        {
            id: 23,
            category: "national",
            name: "Manti",
            desc: "Qo'lda tayyorlangan manti, go'sht va piyoz bilan, qatiq",
            price: 32000,
            weight: "350g",
            time: "30 min",
            calories: "420 kkal",
            emoji: "🥟",
            badge: "hit"
        },
        {
            id: 24,
            category: "national",
            name: "Chuchvara",
            desc: "Kichik pelmeni, sho'rvada yoki qovurilgan, qatiq bilan",
            price: 30000,
            weight: "350g",
            time: "25 min",
            calories: "380 kkal",
            emoji: "🥟"
        },
        {
            id: 25,
            category: "national",
            name: "Somsa",
            desc: "Tandir somsasi, go'sht va piyozli, issiq holda",
            price: 12000,
            weight: "180g",
            time: "na tayyor",
            calories: "320 kkal",
            emoji: "🫓"
        },
        {
            id: 26,
            category: "national",
            name: "No'rin",
            desc: "Qo'lda cho'zilgan xamir, qaynatilgan go'sht, piyoz",
            price: 36000,
            weight: "380g",
            time: "20 min",
            calories: "440 kkal",
            emoji: "🍜",
            badge: "new"
        },

        // === PIZZA ===
        {
            id: 27,
            category: "pizza",
            name: "Margarita",
            desc: "Mozzarella, pomidor sousi, bazilika, zaytun moyi",
            price: 42000,
            weight: "450g",
            time: "20 min",
            calories: "680 kkal",
            emoji: "🍕"
        },
        {
            id: 28,
            category: "pizza",
            name: "Pepperoni",
            desc: "Pepperoni kolbasa, mozzarella, pomidor sousi",
            price: 48000,
            weight: "480g",
            time: "20 min",
            calories: "750 kkal",
            emoji: "🍕",
            badge: "hit"
        },
        {
            id: 29,
            category: "pizza",
            name: "4 Pishloq",
            desc: "Mozzarella, parmessan, dor-blyu, cheddar",
            price: 52000,
            weight: "470g",
            time: "20 min",
            calories: "720 kkal",
            emoji: "🧀"
        },
        {
            id: 30,
            category: "pizza",
            name: "Oasis Special",
            desc: "Tovuq, zamburug', bolgar qalampiri, piyoz, mozzarella, maxsus sous",
            price: 56000,
            weight: "520g",
            time: "22 min",
            calories: "780 kkal",
            emoji: "⭐",
            badge: "new"
        },
        {
            id: 31,
            category: "pizza",
            name: "Go'shtli pizza",
            desc: "Mol go'shti, pepperoni, bekon, mozzarella, BBQ sous",
            price: 58000,
            weight: "530g",
            time: "22 min",
            calories: "820 kkal",
            emoji: "🥩"
        },

        // === DESERTLAR ===
        {
            id: 32,
            category: "desserts",
            name: "Tiramisu",
            desc: "Italyan deserti: maskarpone, qahva, kakao, savoyyardi",
            price: 32000,
            weight: "180g",
            time: "tayyor",
            calories: "380 kkal",
            emoji: "🍰",
            badge: "hit"
        },
        {
            id: 33,
            category: "desserts",
            name: "Chiz-keyk",
            desc: "Nyu-York uslubidagi chiz-keyk, yong'oqli taglik, mevali sous",
            price: 34000,
            weight: "170g",
            time: "tayyor",
            calories: "350 kkal",
            emoji: "🍮"
        },
        {
            id: 34,
            category: "desserts",
            name: "Shokoladli fondant",
            desc: "Issiq shokoladli keks, ichida suyuq shokolad, muzqaymoq bilan",
            price: 36000,
            weight: "200g",
            time: "15 min",
            calories: "450 kkal",
            emoji: "🍫",
            badge: "new"
        },
        {
            id: 35,
            category: "desserts",
            name: "Panna kotta",
            desc: "Qaymoqli Italyan deserti, mevali sous bilan",
            price: 28000,
            weight: "160g",
            time: "tayyor",
            calories: "280 kkal",
            emoji: "🍨"
        },
        {
            id: 36,
            category: "desserts",
            name: "Baqlava",
            desc: "An'anaviy baqlava, yong'oq, asal, yupqa qatlam",
            price: 24000,
            weight: "150g",
            time: "tayyor",
            calories: "420 kkal",
            emoji: "🍯"
        },
        {
            id: 37,
            category: "desserts",
            name: "Muzqaymoq assortisi",
            desc: "3 ta turli xildagi muzqaymoq: vanil, shokolad, pistashka",
            price: 22000,
            weight: "180g",
            time: "tayyor",
            calories: "280 kkal",
            emoji: "🍦"
        },

        // === ICHIMLIKLAR ===
        {
            id: 38,
            category: "drinks",
            name: "Mojito (alkolsiz)",
            desc: "Yalpiz, laim, shakar, gazlangan suv, muz",
            price: 22000,
            weight: "400ml",
            time: "5 min",
            calories: "120 kkal",
            emoji: "🍹",
            badge: "hit"
        },
        {
            id: 39,
            category: "drinks",
            name: "Limonad",
            desc: "Yangi siqilgan limon, shakar siropi, yalpiz, muz",
            price: 18000,
            weight: "400ml",
            time: "5 min",
            calories: "90 kkal",
            emoji: "🍋"
        },
        {
            id: 40,
            category: "drinks",
            name: "Yangi siqilgan sharbat",
            desc: "Apelsin / olma / sabzi / anor (tanlash mumkin)",
            price: 24000,
            weight: "300ml",
            time: "5 min",
            calories: "110 kkal",
            emoji: "🧃"
        },
        {
            id: 41,
            category: "drinks",
            name: "Milkshake",
            desc: "Qulupnay / shokolad / vanil / banan (tanlash mumkin)",
            price: 28000,
            weight: "400ml",
            time: "5 min",
            calories: "320 kkal",
            emoji: "🥛"
        },
        {
            id: 42,
            category: "drinks",
            name: "Smoothie",
            desc: "Mango, banan, yogurt, asal",
            price: 26000,
            weight: "350ml",
            time: "5 min",
            calories: "180 kkal",
            emoji: "🫐",
            badge: "new"
        },
        {
            id: 43,
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
            id: 44,
            category: "drinks",
            name: "Mineral suv",
            desc: "Gazli yoki gazsiz suv, 0.5 litr",
            price: 6000,
            weight: "500ml",
            time: "tayyor",
            calories: "0 kkal",
            emoji: "💧"
        },

        // === CHOY & QAHVA ===
        {
            id: 45,
            category: "tea",
            name: "Ko'k choy (choynek)",
            desc: "Yuqori navli o'zbek ko'k choyi, 1 litrli choynek",
            price: 12000,
            weight: "1000ml",
            time: "10 min",
            calories: "5 kkal",
            emoji: "🍵",
            badge: "hit"
        },
        {
            id: 46,
            category: "tea",
            name: "Qora choy (choynek)",
            desc: "An'anaviy qora choy, 1 litrli choynek",
            price: 12000,
            weight: "1000ml",
            time: "10 min",
            calories: "5 kkal",
            emoji: "☕"
        },
        {
            id: 47,
            category: "tea",
            name: "Amerikano",
            desc: "Klassik qora qahva, 100% arabika donalari",
            price: 16000,
            weight: "200ml",
            time: "5 min",
            calories: "10 kkal",
            emoji: "☕"
        },
        {
            id: 48,
            category: "tea",
            name: "Cappuccino",
            desc: "Espresso, ko'pikli sut, kakao kukunlari",
            price: 22000,
            weight: "250ml",
            time: "5 min",
            calories: "120 kkal",
            emoji: "☕",
            badge: "hit"
        },
        {
            id: 49,
            category: "tea",
            name: "Latte",
            desc: "Espresso, issiq sut, nozik ko'pik",
            price: 24000,
            weight: "300ml",
            time: "5 min",
            calories: "150 kkal",
            emoji: "🥛"
        },
        {
            id: 50,
            category: "tea",
            name: "Raf qahva",
            desc: "Espresso, qaymoq, vanil siropi",
            price: 26000,
            weight: "300ml",
            time: "5 min",
            calories: "200 kkal",
            emoji: "🍦",
            badge: "new"
        }
    ]
};
