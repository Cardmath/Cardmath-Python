export function getBackendUrl() {
    const mode = process.env.REACT_APP_MODE;    
    console.log("mode", mode)
    if (mode === 'development') {
      return 'https://tunnel.cardmath.ai';
    } else {
      return 'https://your-backend-dot-cardmath-llc.uc.r.appspot.com';
    }
  }
  