// Used to add jwt Authorization to request headers for API calls
export default function authHeader() {
    let user = JSON.parse(localStorage.getItem('user'));
  
    if (user && user.access_token) {
      return { Authorization: 'Bearer ' + user.access_token };
    } else {
      return {};
    }
}