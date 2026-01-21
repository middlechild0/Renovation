# Renovation Client Portal - Setup Guide

## Quick Start (5 minutes)

### Step 1: Install Frontend Dependencies
```bash
cd Techhive-frontend
npm install
```

### Step 2: Install Backend Dependencies
```bash
cd ../Renovation/api
pip install -r requirements.txt
```

### Step 3: Get Stripe Keys
1. Go to [https://dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys)
2. Copy your **Publishable key** (starts with `pk_test_`)
3. Copy your **Secret key** (starts with `sk_test_`)

### Step 4: Configure Frontend
```bash
cd ../../Techhive-frontend
cp .env.example .env
```

Edit `.env`:
```
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Step 5: Configure Backend
```bash
cd ../Renovation/api
cp .env.example .env
```

Edit `.env`:
```
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
```

### Step 6: Run Both Servers

**Terminal 1 - Backend:**
```bash
cd Renovation/api
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd Techhive-frontend
npm run dev
```

### Step 7: Test It Out
1. Open [http://localhost:3000](http://localhost:3000)
2. Search for "Java House" or "Dental"
3. Click "Get Access" on any demo
4. Use Stripe test card: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits
   - ZIP: Any 5 digits

## Testing Checklist

- [ ] Frontend loads at localhost:3000
- [ ] Backend API responds at localhost:5000/api/health
- [ ] Search returns demo results
- [ ] Payment modal opens
- [ ] Stripe payment processes
- [ ] Demo URL is displayed after payment
- [ ] Order saved in database

## Troubleshooting

### "Module not found" errors
```bash
cd Techhive-frontend
rm -rf node_modules package-lock.json
npm install
```

### "Connection refused" to API
- Make sure Flask server is running on port 5000
- Check `next.config.js` proxy configuration

### Stripe errors
- Verify `.env` files have correct keys
- Use test mode keys (pk_test_ and sk_test_)
- Check Stripe dashboard for errors

### Database errors
- Delete `client_orders.db` and restart Flask server
- Database will be recreated automatically

## File Locations

- Frontend: `Techhive-frontend/`
- Backend API: `Renovation/api/`
- Demo Data: `Renovation/demo_results.json`
- Database: `Renovation/api/client_orders.db` (auto-created)

## Next Steps

1. Customize the design in `app/globals.css`
2. Adjust pricing in `api/app.py` (line 87)
3. Add your business logo to components
4. Test with real Stripe keys in production
5. Deploy to Vercel (frontend) and your server (backend)

## Production Deployment

### Frontend (Vercel)
```bash
cd Techhive-frontend
vercel --prod
```

### Backend (Any Server)
```bash
cd Renovation/api
# Use production WSGI server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Remember to:
- Switch to production Stripe keys
- Update NEXT_PUBLIC_API_URL to production API URL
- Enable HTTPS for both frontend and backend
- Set up proper database (PostgreSQL recommended)

## Support

Check these files for more details:
- `Techhive-frontend/README.md` - Frontend documentation
- `Renovation/api/README.md` - Backend API documentation
