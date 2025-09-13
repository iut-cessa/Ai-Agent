# Nginx Multi-Domain Configuration

This setup provides three separate domains for different purposes:

## 🌐 **Domain Configuration**

### **1. Main Website: `iut-aiagent.ir`**
- **Purpose**: Main Django application
- **Access**: `http://iut-aiagent.ir`
- **Features**: 
  - Full Django application
  - Static files serving
  - Media files serving
  - Health checks

### **2. API Documentation: `api.iut-aiagent.ir`**
- **Purpose**: Swagger/OpenAPI documentation
- **Access**: `http://api.iut-aiagent.ir`
- **Features**:
  - Swagger UI at `/swagger/`
  - ReDoc documentation at `/redoc/`
  - API endpoints at `/api/`
  - CORS headers enabled
  - Auto-redirect to Swagger

### **3. Database Admin: `admin.iut-aiagent.ir`**
- **Purpose**: phpMyAdmin interface (Password Protected)
- **Access**: `http://admin.iut-aiagent.ir`
- **Authentication**: 
  - **Username**: `admin`
  - **Password**: `admin123`
- **Features**:
  - HTTP Basic Authentication
  - Rate limiting protection
  - Enhanced security headers
  - Large file upload support

## 🔧 **Setup Instructions**

### **1. Domain Configuration**
Add these entries to your DNS or `/etc/hosts` file:
```
YOUR_SERVER_IP    iut-aiagent.ir
YOUR_SERVER_IP    api.iut-aiagent.ir  
YOUR_SERVER_IP    admin.iut-aiagent.ir
```

### **2. Local Testing**
For local testing, add to your hosts file:
```
127.0.0.1    iut-aiagent.ir
127.0.0.1    api.iut-aiagent.ir
127.0.0.1    admin.iut-aiagent.ir
```

**Windows**: `C:\Windows\System32\drivers\etc\hosts`
**Linux/Mac**: `/etc/hosts`

### **3. Deploy**
```bash
docker-compose down
docker-compose up --build -d
```

## 🔐 **Security Features**

### **phpMyAdmin Protection**
- ✅ HTTP Basic Authentication (admin/admin123)
- ✅ Rate limiting (1 request/second)
- ✅ Internal container access only
- ✅ Enhanced security headers
- ✅ File upload size: 200MB

### **API Security**
- ✅ CORS headers configured
- ✅ Security headers applied
- ✅ File upload size: 50MB

### **Main Site Security**
- ✅ Security headers
- ✅ Static file caching
- ✅ File upload size: 100MB

## 📁 **File Structure**
```
nginx/
├── nginx.conf          # Main nginx configuration
├── main-site.conf      # iut-aiagent.ir configuration
├── api-site.conf       # api.iut-aiagent.ir configuration
├── admin-site.conf     # admin.iut-aiagent.ir configuration
├── htpasswd            # Authentication file for phpMyAdmin
└── create-htpasswd.sh  # Script to create new users
```

## 🛠 **Adding New Users to phpMyAdmin**

### **Method 1: Using htpasswd command**
```bash
# Enter the nginx container
docker exec -it nginx-proxy sh

# Add new user (will prompt for password)
htpasswd /etc/nginx/.htpasswd newusername
```

### **Method 2: Using the script**
```bash
# Make script executable
chmod +x nginx/create-htpasswd.sh

# Run the script
./nginx/create-htpasswd.sh
```

## 🌍 **Access URLs**

- **Main Site**: http://iut-aiagent.ir
- **API Docs**: http://api.iut-aiagent.ir
- **Database Admin**: http://admin.iut-aiagent.ir (requires: admin/admin123)

## 🔄 **SSL/HTTPS Configuration**

To add SSL certificates, update the server blocks in the conf files:
```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    # ... rest of configuration
}
```
