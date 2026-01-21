# Design What You Want (DWYW) 🎨

An AI-powered web design platform that lets you create stunning, professional websites with visual customization, natural language AI assistance, and one-click deployment.

## ✨ Features

### 🎨 Visual Customization
- **Color Schemes**: Customize primary, secondary, accent, background, and text colors with visual color picker
- **Typography**: Choose from 10+ professional fonts for headings, body text, and accents
- **Spacing & Layout**: Adjust spacing scale and border radius for unique designs
- **Animations**: Enable fade, slide, or bounce animations with parallax and hover effects

### ✨ AI Design Assistant
- **Natural Language Interface**: Describe changes in plain English ("Make the design more modern")
- **Intelligent Parsing**: AI understands intent and applies appropriate design changes
- **Real-time Analysis**: Get instant feedback on usability, accessibility, SEO, and performance
- **Design Suggestions**: AI recommends improvements based on best practices

### 👁️ Live Preview
- **Real-time Updates**: See changes instantly as you customize
- **Multi-Device Preview**: Test on desktop (1920px), tablet (768px), and mobile (375px)
- **Section-by-Section Rendering**: Preview all template sections with your customizations

### 💰 Transparent Pricing
- **Feature-Based**: Pay only for the features you need
- **Dependency Tracking**: Automatic inclusion of required dependencies
- **Clear Explanations**: Understand what you're paying for with detailed breakdowns
- **No Subscriptions**: One-time payment for full ownership

### 🚀 One-Click Deployment
- **Production-Ready Code**: Get optimized Next.js, TypeScript, and Tailwind CSS
- **Auto-Configuration**: Deployment settings generated automatically
- **Multiple Platforms**: Deploy to Vercel, Netlify, or custom hosting
- **Full Source Code**: Complete ownership with documentation

### 🛡️ Guardrails System
- **SEO Enforcement**: Ensures meta tags, semantic HTML, and performance optimization
- **Mobile-First**: Guarantees responsive design across all devices
- **Accessibility Warnings**: Alerts on contrast, font size, and ARIA issues
- **Performance Monitoring**: Tracks image optimization and animation impact

## 🏗️ Architecture

### Frontend (Next.js 14)
```
DWYW/
├── app/
│   ├── page.tsx              # Landing page
│   ├── editor/page.tsx       # Main design editor
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── components/
│   ├── TemplateSelector.tsx  # Template selection UI
│   ├── CustomizationPanel.tsx # Design controls
│   ├── LivePreview.tsx       # Real-time preview
│   ├── AIAssistant.tsx       # Chat interface
│   └── PricingDisplay.tsx    # Pricing breakdown
├── store/
│   └── project.ts            # Zustand state management
├── lib/
│   ├── templates.ts          # Template registry
│   ├── sections.ts           # Section definitions
│   ├── pricing.ts            # Feature pricing
│   ├── ai-assistant.ts       # AI analysis engine
│   └── build-pipeline.ts     # Code generation
└── types/
    └── index.ts              # TypeScript definitions
```

### Core Libraries

#### Templates System
- **4 Professional Templates**: Restaurant, E-Commerce, SaaS, Portfolio
- **13+ Section Types**: Hero, Features, Pricing, Gallery, Dashboard, etc.
- **40+ Section Variants**: Multiple design variations per section
- **Modular Composition**: Mix and match sections freely

#### Pricing Engine
- **30+ Features**: Authentication, payments, database, analytics, etc.
- **Dependency Resolution**: Auto-includes required dependencies
- **Transparent Breakdown**: Detailed explanation for each cost
- **Dynamic Calculation**: Updates in real-time as you customize

#### AI Analysis Engine
- **Usability Analysis**: Button sizes, clickable areas, form complexity
- **Accessibility Checks**: Color contrast, font sizes, ARIA attributes
- **SEO Evaluation**: Meta tags, semantic HTML, heading structure
- **Performance Scoring**: Image optimization, animation impact
- **Mobile Optimization**: Touch targets, viewport settings

#### Build Pipeline
- **Code Generation**: Creates Next.js components and pages
- **Configuration**: Generates package.json, tsconfig, tailwind config
- **Backend Setup**: Optional API routes for auth, payments, database
- **Deployment Config**: Platform-specific deployment settings

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Git

### Installation

1. **Clone the repository**
   ```bash
   cd /home/wainaina/Desktop/Jimmy/Techhive/DWYW
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

4. **Open in browser**
   ```
   http://localhost:3000
   ```

### Usage

1. **Select a Template**: Choose from Restaurant, E-Commerce, SaaS, or Portfolio
2. **Customize Design**: Use the customization panel to adjust colors, fonts, spacing, animations
3. **Use AI Assistant**: Chat with AI to make changes in natural language
4. **Preview Changes**: See updates in real-time across different devices
5. **Check Pricing**: View transparent breakdown of features and costs
6. **Deploy**: One-click deployment to production

## 🎯 Template Options

### 🍽️ Restaurant Template
Perfect for restaurants, cafes, and food businesses
- Hero with menu showcase
- Gallery for food photos
- Online ordering integration
- Reservation system
- Contact and location

### 🛍️ E-Commerce Template
Full-featured online store
- Product catalog with search
- Shopping cart and checkout
- Payment processing (Stripe)
- User accounts
- Order management

### 💼 SaaS Template
Software and service businesses
- Feature showcase
- Pricing tiers
- User dashboard
- Analytics integration
- Admin panel

### 🎨 Portfolio Template
Personal branding and creative work
- Project showcase
- About section
- Skills and experience
- Contact form
- Blog integration

## 🛠️ Technology Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **Zustand**: Lightweight state management
- **React Colorful**: Color picker

### AI & Analysis
- **OpenAI**: Natural language processing (planned)
- **Custom Analysis Engine**: Usability, accessibility, SEO, performance scoring
- **Guardrails System**: Automated checks and enforcement

### Payments & Deployment
- **Stripe**: Payment processing
- **Vercel/Netlify**: Hosting platforms
- **GitHub**: Version control

## 📦 Feature Registry

| Feature | Base Price | Dependencies |
|---------|-----------|--------------|
| Online Ordering | $200 | Shopping Cart, Checkout, Payments |
| Shopping Cart | $150 | - |
| Checkout | $150 | Payments |
| User Authentication | $250 | - |
| Payments (Stripe) | $200 | - |
| Database (MongoDB) | $300 | - |
| Admin Dashboard | $400 | User Auth, Database |
| Analytics | $200 | Database |
| Blog/CMS | $300 | Database |
| Image Gallery | $100 | - |
| Contact Forms | $50 | - |
| Live Chat | $300 | User Auth, Database |
| Multi-language | $400 | - |
| Dark Mode | $100 | - |

*See [lib/pricing.ts](lib/pricing.ts) for complete feature list*

## 🔐 Guardrails

### Enforced (Deployment Blocked)
- ✅ SEO: Meta tags, Open Graph, structured data
- ✅ Mobile-First: Responsive design, touch targets

### Warnings (Alerts Only)
- ⚠️ Accessibility: Color contrast, font sizes, ARIA
- ⚠️ Performance: Image optimization, animation impact

## 📊 Analysis Scoring

Each design receives scores (0-100) in:
- **Usability**: Button sizes, form complexity, navigation
- **Accessibility**: Contrast, font sizes, semantic HTML
- **SEO**: Meta tags, headings, content structure
- **Performance**: Image optimization, animations
- **Mobile**: Touch targets, viewport, layout

## 🤝 Contributing

This is a proprietary project for TechHive. Internal contributions welcome.

## 📄 License

Proprietary - All rights reserved by TechHive

## 📧 Support

For questions or issues:
- Email: jimmymathu28@gmail.com
- GitHub Issues: [Create an issue](https://github.com/middlechild0/Renovation/issues)

## 🗺️ Roadmap

- [x] Template system with 4 templates
- [x] Visual customization panel
- [x] Live preview system
- [x] AI assistant infrastructure
- [x] Pricing calculator
- [x] Build pipeline
- [ ] OpenAI integration for AI assistant
- [ ] Backend API endpoints
- [ ] User authentication
- [ ] Payment processing
- [ ] Deployment automation
- [ ] Project saving and loading
- [ ] More templates (Landing pages, Blogs, etc.)
- [ ] Advanced animations and interactions
- [ ] A/B testing capabilities
- [ ] SEO tools and analytics

---

Built with ❤️ by TechHive
