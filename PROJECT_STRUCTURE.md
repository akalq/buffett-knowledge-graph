# Buffett Letters Knowledge Base - Project Structure

## 📁 Directory Structure

```
巴菲特知识库-LearnBuffett版/
├── index.html                      # Homepage
├── assets/                         # Static assets
│   ├── css/
│   │   └── main.css               # Main stylesheet (extracted from index.html)
│   ├── js/
│   │   └── main.js                # Main JavaScript (extracted from index.html)
│   └── images/                    # Image assets
├── pages/                         # Page templates
│   ├── index-pages/               # Index pages
│   │   ├── letters-index.html     # Letters overview
│   │   ├── concepts-index.html    # Concepts index
│   │   ├── companies-index.html   # Companies index
│   │   ├── people-index.html      # People index
│   │   ├── timeline.html          # Timeline
│   │   └── knowledge-tree.html    # Knowledge tree
│   ├── concepts/                  # Concept detail pages
│   ├── companies/                 # Company detail pages
│   ├── people/                    # People detail pages
│   └── letters/                   # Letter pages
│       ├── berkshire/            # Berkshire letters
│       ├── partnership/           # Partnership letters
│       └── special/               # Special letters
├── scripts/                       # Build & utility scripts
│   ├── add_cross_links.py        # Cross-link generation
│   ├── add_cross_links_v2.py
│   ├── add_cross_links_v3.py
│   ├── bilingual-generator.py    # Bilingual letter generation
│   ├── generate_companies.py      # Company page generation
│   └── ...
├── data/                          # Data files
│   ├── backlinks.json            # Backlink data
│   ├── entities.json             # Entity data
│   └── reference_counts.json     # Reference counts
├── bilingual-letters/            # Bilingual letters
├── english-letters/              # English original letters
├── knowledge-data/               # Knowledge base data
├── links.json                    # Link mapping data
├── METHODOLOGY.md                # Project methodology
└── README.md                     # This file
```

## 📊 Statistics

- **Total HTML files**: 283+
- **Concepts**: 50+
- **Companies**: 60+
- **People**: 17
- **Letters**: 98+

## 🛠️ Build Scripts

All Python scripts for building and maintaining the knowledge base are located in the `scripts/` directory:

| Script | Purpose |
|--------|---------|
| `add_cross_links.py` | Generate cross-links between pages |
| `bilingual-generator.py` | Generate bilingual letter pages |
| `generate_companies.py` | Generate company detail pages |
| `apply_sidebar.py` | Apply consistent sidebar to all pages |

## 🎨 Stylesheet Structure

The main stylesheet (`assets/css/main.css`) contains:

- CSS Variables (colors, spacing)
- Sidebar styles
- Header/Navigation styles
- Hero section styles
- Card and grid layouts
- Responsive breakpoints
- Mobile menu styles

## 📝 Notes

- All HTML pages share common CSS via `assets/css/main.css`
- JavaScript functionality is centralized in `assets/js/main.js`
- Build scripts are separated from content for easier maintenance
- Data files are in JSON format for easy processing
