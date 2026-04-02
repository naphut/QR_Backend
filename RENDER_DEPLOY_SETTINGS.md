# 🚀 Render Backend Deployment - EXACT Settings

## ⚙️ **Render Web Service Configuration**

Copy these settings EXACTLY as shown:

---

### **📋 Basic Settings**
```
Name: QR_Backend
Language: Python 3
Branch: main
Region: Oregon (US West) (or your preferred region)
```

### **🔧 Advanced Settings**
```
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### **💰 Instance Type**
- **Free**: $0/month (spins down when inactive)
- **Starter**: $7/month (recommended for production)

---

## 🔑 **Environment Variables (Add After First Deploy)**

After the first deployment, go to your service dashboard → Environment Variables:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://your-admin-app.vercel.app,https://your-user-app.vercel.app
```

---

## 📊 **What Happens During Deploy**

1. **Render clones** your GitHub repository
2. **Changes to backend directory**
3. **Installs dependencies** from requirements.txt
4. **Starts FastAPI** with uvicorn
5. **Creates PostgreSQL database** automatically

---

## ✅ **Verification Steps**

After deployment, check:

1. **Health Check**: `https://your-app.onrender.com/health`
2. **API Docs**: `https://your-app.onrender.com/docs`
3. **Products API**: `https://your-app.onrender.com/api/products`

---

## 🚨 **Common Issues & Fixes**

### **Issue: Build fails**
- ✅ Check Root Directory is set to `backend`
- ✅ Verify requirements.txt has all dependencies

### **Issue: Start command fails**
- ✅ Use exact start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### **Issue: Database connection**
- ✅ Add DATABASE_URL environment variable after first deploy
- ✅ Run database initialization if needed

---

## 🎯 **Next Steps After Backend Deploy**

1. **Copy the backend URL** (e.g., `https://qr-backend.onrender.com`)
2. **Deploy Admin Frontend** to Vercel with this API URL
3. **Deploy User Frontend** to Vercel with this API URL
4. **Add environment variables** to both frontends

---

## 🔗 **Quick Copy-Paste Settings**

```
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Use these EXACT settings for successful deployment!** 🚀
