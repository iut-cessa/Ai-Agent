import logging
import time
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

# Set up logger
logger = logging.getLogger('request_logger')

class RequestResponseLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all incoming requests and outgoing responses
    Format: YYYY/MM/DD - HH:MM:SS | STATUS | TIME | CLIENT_IP | METHOD "PATH"
    Example: 2025/09/13 - 09:30:29 | 200 | 1.189559ms | 37.255.216.73 | GET "/api/groups/?page=1&limit=10"
    """
    
    def process_request(self, request):
        """Store the start time of the request"""
        request.start_time = time.time()
        
    def process_response(self, request, response):
        """Log the request and response details"""
        try:
            # Calculate response time
            if hasattr(request, 'start_time'):
                duration = (time.time() - request.start_time) * 1000  # Convert to milliseconds
                duration_str = f"{duration:.3f}ms"
            else:
                duration_str = "unknown"
            
            # Get client IP address
            client_ip = self.get_client_ip(request)
            
            # Get current timestamp
            timestamp = timezone.now().strftime('%Y/%m/%d - %H:%M:%S')
            
            # Get request method and full path with query string
            method = request.method
            path = request.get_full_path()
            
            # Get status code
            status_code = response.status_code
            
            # Format log message
            log_message = f'{timestamp} | {status_code} | {duration_str:>10} | {client_ip:>15} | {method:<8} "{path}"'
            
            # Log based on status code
            if status_code >= 500:
                logger.error(log_message)
            elif status_code >= 400:
                logger.warning(log_message)
            else:
                logger.info(log_message)
                
        except Exception as e:
            # If logging fails, don't break the request
            logger.error(f"Error in logging middleware: {e}")
        
        return response
    
    def get_client_ip(self, request):
        """Get the real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip
