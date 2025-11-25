# SSL Certificate Management

## Current Setup

- **Domain**: iut-aiagent.ir, www.iut-aiagent.ir
- **Certificate Provider**: Let's Encrypt
- **Certificate Location**: `/etc/letsencrypt/live/iut-aiagent.ir/`
- **Expiration**: Certificates expire every 90 days
- **Auto-Renewal**: Configured via cron job (daily at 3 AM)

## Certificate Files

- **Full Chain**: `/etc/letsencrypt/live/iut-aiagent.ir/fullchain.pem`
- **Private Key**: `/etc/letsencrypt/live/iut-aiagent.ir/privkey.pem`

## Manual Renewal

If you need to manually renew the certificate:

```bash
# Stop nginx container
cd /root/aiagent-website/Ai-Agent
docker compose stop nginx

# Renew certificate
sudo certbot renew

# Start nginx container
docker compose up -d nginx
```

## Automatic Renewal

A cron job runs daily at 3 AM to check and renew certificates:
```
0 3 * * * /root/aiagent-website/Ai-Agent/renew-cert.sh >> /var/log/ssl-renewal.log 2>&1
```

Check renewal logs:
```bash
tail -f /var/log/ssl-renewal.log
```

## Troubleshooting

### Check certificate expiration
```bash
sudo certbot certificates
```

### Test nginx configuration
```bash
docker exec nginx-proxy nginx -t
```

### Verify certificate is mounted in container
```bash
docker exec nginx-proxy ls -la /etc/letsencrypt/live/iut-aiagent.ir/
```

### Check HTTPS status
```bash
curl -I https://iut-aiagent.ir
```

## Adding New Domains

To add additional domains to the certificate:
```bash
# Stop nginx
docker compose stop nginx

# Add domain
sudo certbot certonly --standalone --cert-name iut-aiagent.ir \
  -d iut-aiagent.ir -d www.iut-aiagent.ir -d newdomain.com

# Update nginx config to include new domain
# Then restart nginx
docker compose up -d nginx
```
