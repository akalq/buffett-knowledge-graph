/* Buffett Knowledge Base - Main JavaScript */
/* Extracted from index.html */

// ==================== Wisdom Data ====================
const wisdoms = [
    { quote: "护城河的本质是'我与别人不同'，而非'我比别人更好'。", source: "护城河", link: "concepts/护城河.html" },
    { quote: "安全边际不是用来'猜对'的，而是用来应对'猜错'的。", source: "安全边际", link: "concepts/安全边际.html" },
    { quote: "能力圈的核心是知道边界在哪里，而非范围有多大。", source: "能力圈", link: "concepts/能力圈.html" },
    { quote: "价格是你付出的，价值是你得到的。", source: "内在价值", link: "concepts/内在价值.html" },
    { quote: "别人恐惧时我贪婪，别人贪婪时我恐惧。", source: "市场先生", link: "concepts/市场先生.html" },
    { quote: "如果你不愿意持有一只股票十年，那就不要考虑持有它十分钟。", source: "长期持有", link: "concepts/长期持有.html" },
    { quote: "时间是优秀企业的朋友，是平庸企业的敌人。", source: "复利", link: "concepts/复利.html" },
    { quote: "风险来自于你不知道自己在做什么。", source: "风险", link: "concepts/风险.html" },
    { quote: "投资不需要极高的智商，需要的是稳定的情绪和独立思考的能力。", source: "投资者心理", link: "concepts/投资者心理.html" },
    { quote: "买入一家公司的股票，就是买入它的一部分生意。", source: "股东心态", link: "concepts/股东心态.html" }
];

let currentWisdomIndex = 0;

function showRandomWisdom() {
    currentWisdomIndex = Math.floor(Math.random() * wisdoms.length);
    const wisdom = wisdoms[currentWisdomIndex];
    document.getElementById('wisdomQuote').textContent = '"' + wisdom.quote + '"';
    document.getElementById('wisdomSource').textContent = '— ' + wisdom.source;
    document.getElementById('wisdomSource').href = wisdom.link;
}

// Initialize wisdom
showRandomWisdom();

// Refresh wisdom button
document.getElementById('wisdomRefresh').addEventListener('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    showRandomWisdom();
});

// ==================== Recommendations Data ====================
const recommendations = {
    letters: [
        { year: "1987", title: "黑色星期一后的投资思考", desc: "黑色星期一后的投资思考，展现逆向投资智慧", file: "letters/berkshire/1987.html" },
        { year: "2008", title: "金融危机中的贪婪", desc: "2008年金融危机中的贪婪与恐惧，值得反复研读", file: "letters/berkshire/2008.html" },
        { year: "1988", title: "买入可口可乐的决策", desc: "详细阐述买入可口可乐的思路与逻辑", file: "letters/berkshire/1988.html" },
        { year: "2016", title: "首次投资苹果", desc: "科技股投资的突破性决策", file: "letters/berkshire/2016.html" }
    ],
    concepts: [
        { name: "护城河", quote: "护城河的本质是我与别人不同，而非我比别人更好", file: "concepts/护城河.html" },
        { name: "安全边际", quote: "安全边际是应对猜错的保护，而非用来猜对", file: "concepts/安全边际.html" },
        { name: "能力圈", quote: "知道边界在哪里比范围大更重要", file: "concepts/能力圈.html" },
        { name: "复利", quote: "时间是好企业的朋友，是平庸企业的敌人", file: "concepts/复利.html" }
    ],
    companies: [
        { name: "喜诗糖果", desc: "经典价值投资案例，完美诠释护城河理念", file: "companies/喜诗糖果.html" },
        { name: "可口可乐", desc: "消费品牌护城河典范，长期持有的典范", file: "companies/可口可乐.html" },
        { name: "苹果", desc: "科技投资的标杆，展现能力圈扩展", file: "companies/苹果.html" },
        { name: "盖可保险", desc: "保险业务的核心，浮存金的来源", file: "companies/盖可保险.html" }
    ],
    people: [
        { name: "查理·芒格", desc: "巴菲特的终身伙伴，51次在信件中被提及", file: "people/芒格.html" },
        { name: "阿吉特·贾恩", desc: "保险业务掌门人，再保险之父", file: "people/阿吉特·贾恩.html" },
        { name: "格雷厄姆", desc: "价值投资之父，巴菲特的导师", file: "people/格雷厄姆.html" },
        { name: "B夫人", desc: "传奇女企业家，内布拉斯加家具城创始人", file: "people/B夫人.html" }
    ]
};

function getRandomItem(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function initRecommendations() {
    // Recommended Letter
    const recLetter = getRandomItem(recommendations.letters);
    document.getElementById('recLetterYear').textContent = recLetter.year + '年信件';
    document.getElementById('recLetterDesc').textContent = recLetter.desc;
    document.querySelectorAll('.recommend-card')[0].href = recLetter.file;
    
    // Recommended Concept
    const recConcept = getRandomItem(recommendations.concepts);
    document.getElementById('recConceptName').textContent = recConcept.name;
    document.getElementById('recConceptQuote').textContent = '"' + recConcept.quote + '"';
    document.getElementById('recConcept').href = recConcept.file;
    
    // Recommended Company
    const recCompany = getRandomItem(recommendations.companies);
    document.getElementById('recCompanyName').textContent = recCompany.name;
    document.getElementById('recCompanyDesc').textContent = recCompany.desc;
    document.getElementById('recCompany').href = recCompany.file;
    
    // Recommended People
    const recPeople = getRandomItem(recommendations.people);
    document.getElementById('recPeopleName').textContent = recPeople.name;
    document.getElementById('recPeopleDesc').textContent = recPeople.desc;
    document.getElementById('recPeople').href = recPeople.file;
}

// Initialize recommendations
initRecommendations();

// ==================== Sidebar Toggle ====================
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const toggleIcon = document.getElementById('toggleIcon');
const mainWrapper = document.getElementById('mainWrapper');

if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('expanded');
        if (mainWrapper) {
            mainWrapper.classList.toggle('sidebar-expanded');
        }
        toggleIcon.textContent = sidebar.classList.contains('expanded') ? '✕' : '☰';
    });
}

// ==================== Mobile Menu ====================
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const sidebarOverlay = document.getElementById('sidebarOverlay');

function openMobileMenu() {
    sidebar.classList.add('mobile-open');
    if (sidebarOverlay) {
        sidebarOverlay.classList.add('active');
    }
}

function closeMobileMenu() {
    sidebar.classList.remove('mobile-open');
    if (sidebarOverlay) {
        sidebarOverlay.classList.remove('active');
    }
}

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', function() {
        if (sidebar.classList.contains('mobile-open')) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    });
}

if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeMobileMenu);
}

// Close mobile menu when clicking nav items
document.querySelectorAll('.nav-item').forEach(function(item) {
    item.addEventListener('click', function() {
        if (window.innerWidth <= 900) {
            closeMobileMenu();
        }
    });
});

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 900) {
        closeMobileMenu();
    }
});
