export function getBackendUrl() {
    const mode = process.env.NODE_ENV;    
    if (mode === 'development') {
      console.log('Running in development mode');
      return 'https://tunnel.cardmath.ai';
    } else if (mode === 'production') { 
      return 'https://backend-dot-cardmath-llc.uc.r.appspot.com';
    } else {
      throw new Error('Unknown mode');
    }
  }
  