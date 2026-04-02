# 🔧 Complete Backend Setup Guide

## ✅ **Backend Successfully Deployed!**

Your backend is live at: `https://qr-backend.onrender.com`

---

## 🔑 **Step 1: Add Environment Variables**

Go to your Render service dashboard → **Environment Variables** → **Add Environment Variables**:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-super-secret-key-change-this-in-production-123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://your-admin-app.vercel.app,https://your-user-app.vercel.app,http://localhost:3000,http://localhost:3001
```

**Note**: 
- `DATABASE_URL` will be provided by Render automatically
- Copy it from Render dashboard and paste it above
- Change the `SECRET_KEY` to something unique

---

## 🗄️ **Step 2: Initialize Database**

After adding environment variables, create the database tables:

1. Go to Render dashboard → **Jobs** → **New Job**
2. **Command**: `python init_db.py`
3. **Click**: **Create Job** → **Run Job**

This will create:
- ✅ Admin user: `admin123@gmail.com` / `admin123`
- ✅ Demo user: `demo@routine.com` / `demo123`
- ✅ Sample products (10 items)

---

## 🧪 **Step 3: Test Backend APIs**

Test these endpoints to ensure everything works:

### **Health Check**
```bash
curl https://qr-backend.onrender.com/health
```
Expected: `{"status":"healthy","timestamp":1234567890.123}`

### **Get Products**
```bash
curl https://qr-backend.onrender.com/api/products/
```
Expected: JSON array with products

### **API Documentation**
Visit: `https://qr-backend.onrender.com/docs`
- Interactive API documentation
- Test all endpoints

---

## 🚀 **Step 4: Deploy Frontends**

### **Admin Frontend**
1. Go to Vercel → New Project
2. Connect: `QR_Admin_frontend`
3. Environment Variable: 
   ```
   REACT_APP_API_URL=https://qr-backend.onrender.com/api
   ```
4. Deploy

### **User Frontend**
1. Go to Vercel → New Project
2. Connect: `QR_user-frontend`
3. Environment Variable:
   ```
   REACT_APP_API_URL=https://qr-backend.onrender.com/api
   ```
4. Deploy

---

## 🔗 **Step 5: Update CORS Origins**

After deploying frontends, update `ALLOWED_ORIGINS` in Render:

```env
ALLOWED_ORIGINS=https://your-admin-app.vercel.app,https://your-user-app.vercel.app,http://localhost:3000,http://localhost:3001
```

Replace with your actual Vercel URLs.

---

## 🎯 **Complete Platform URLs**

After setup, you'll have:

- **Backend API**: `https://qr-backend.onrender.com`
- **Admin Dashboard**: `https://your-admin-app.vercel.app`
- **User Storefront**: `https://your-user-app.vercel.app`
- **API Docs**: `https://qr-backend.onrender.com/docs`

---

## 🔧 **Troubleshooting**

### **CORS Issues**
- Update `ALLOWED_ORIGINS` with correct frontend URLs
- Redeploy backend after updating

### **Database Issues**
- Run `python init_db.py` job again
- Check `DATABASE_URL` is correct

### **Auth Issues**
- Verify `SECRET_KEY` is set
- Check JWT tokens are working

---

## 🎉 **Success Checklist**

- ✅ Backend deployed and healthy
- ✅ Environment variables configured
- ✅ Database initialized with sample data
- ✅ Frontends deployed with correct API URL
- ✅ CORS configured for all domains
- ✅ All APIs tested and working

---

## 📞 **Support**

If anything doesn't work:
1. Check Render logs for errors
2. Verify environment variables
3. Test APIs individually
4. Ensure CORS origins are correct

**Your QR E-commerce platform will be fully functional!** 🚀
