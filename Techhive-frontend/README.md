# Renovation Automations - Client Portal

A modern Next.js client-facing portal for the Renovation Automations demo generation system. This portal allows clients to search, purchase, and access production-ready business demos.

## 🌟 Features

- **Demo Search**: Search through available demos by business name or industry
- **Stripe Integration**: Secure payment processing for demo access
- **Access Management**: Track purchased demos and grant access after payment
- **Responsive Design**: Built with Tailwind CSS for mobile-friendly experience
- **TypeScript**: Fully typed for better development experience

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for backend API)
- Stripe account (for payments)

### Frontend Setup

1. Install dependencies:
```bash
cd Techhive-frontend
npm install
```

2. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add:
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:5000)

3. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Backend Setup

1. Navigate to the API directory:
```bash
cd ../Renovation/api
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your Stripe secret key.

4. Run the Flask server:
```bash
python app.py
```

The API will run on [http://localhost:5000](http://localhost:5000).

## 📁 Project Structure

```
Techhive-frontend/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Home page (demo search)
│   └── my-demos/
│       └── page.tsx          # Client's purchased demos
├── components/
│   ├── DemoCard.tsx          # Individual demo card component
│   ├── DemoSearch.tsx        # Search interface
│   ├── Header.tsx            # Navigation header
│   └── PaymentModal.tsx      # Stripe payment modal
├── package.json              # Dependencies
├── next.config.js            # Next.js configuration
├── tailwind.config.ts        # Tailwind CSS config
└── tsconfig.json             # TypeScript config

Renovation/api/
├── app.py                    # Flask API server
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # API documentation
```

## 🔗 Integration with Existing System

This portal integrates with the existing Renovation Automations infrastructure:

- **Demo Data**: Reads from `Renovation/demo_results.json`
- **Live Demos**: Uses existing Vercel-deployed demos
- **Payment System**: New Stripe integration for monetization
- **Database**: SQLite database for order tracking

## 🎨 Pages

### 1. Home Page (/)
- Search interface for finding demos
- Grid display of search results
- Quick example searches

### 2. My Demos (/my-demos)
- View all purchased demos by email
- Access demo URLs
- Purchase history

## 💳 Payment Flow

1. User searches for demos
2. Clicks "Get Access" on desired demo
3. Enters email and payment details
4. Stripe processes payment
5. Access granted to demo URL
6. Order recorded in database

## 🛠️ Technologies

**Frontend:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Stripe React Elements
- Axios

**Backend:**
- Flask
- SQLite
- Stripe Python SDK
- Flask-CORS

## 📊 API Endpoints

See [Renovation/api/README.md](../Renovation/api/README.md) for complete API documentation.

## 🔐 Security

- Stripe payment processing (PCI compliant)
- Environment variables for sensitive keys
- CORS configuration for API access
- Payment verification before access

## 📝 Development

### Build for Production

```bash
npm run build
npm start
```

### Type Checking

```bash
npx tsc --noEmit
```

### Linting

```bash
npm run lint
```

## 🚢 Deployment

### Frontend (Vercel)

```bash
vercel --prod
```

### Backend (Any server)

```bash
cd ../Renovation/api
python app.py
```

## 📖 Key Integration Points

1. **Demo Results**: Backend reads from `../demo_results.json`
2. **Vercel URLs**: Frontend displays existing Vercel-hosted demos
3. **Payment System**: New Stripe integration wraps existing demo access
4. **Order Tracking**: SQLite database tracks client purchases

## 🎯 Future Enhancements

- [ ] User authentication system
- [ ] Admin dashboard for managing demos
- [ ] Email notifications for purchases
- [ ] Demo preview without payment
- [ ] Subscription plans for multiple demos
- [ ] Analytics dashboard

## 📄 License

Private - Renovation Automations

## 🤝 Support

For issues or questions, contact support at your business email.

---

Built with ❤️ using Next.js and Flask
